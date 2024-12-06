"""
Prediction Routes

API endpoints for task categorization predictions.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
import time
from ...models.predictor import Predictor
from ..dependencies import get_predictor, get_redis_client
import logging

router = APIRouter()

class TaskInput(BaseModel):
    title: str
    description: str

class PredictionResponse(BaseModel):
    category: str | int
    category_id: int
    confidence: float
    probabilities: Dict[str, float] = {}  # Changed from Optional to default empty dict

class BatchTaskInput(BaseModel):
    tasks: List[TaskInput]

@router.post("/predict", response_model=PredictionResponse)
async def predict_category(
    task: TaskInput,
    predictor: Predictor = Depends(get_predictor),
    redis_client = Depends(get_redis_client)
):
    """
    Predict category for a single task.
    """
    # Check cache
    #TODO remove the time  after testing
    cache_key = f"pred:{task.title}:{task.description}:{time.time()}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    try:
        # Get prediction
        logger = logging.getLogger(__name__)
        logger.info(f"Making prediction for task: {task.title}")
        
        # Use original inputs directly
        result = predictor.predict(task.title, task.description)
        
        # Convert category to lowercase to match frontend
        result['category'] = result['category'].lower()
        
        # Ensure probabilities is included in the result
        if 'probabilities' not in result:
            result['probabilities'] = {}

        logger.info(f"Prediction result: {result}")
        
        # Cache result
        redis_client.setex(
            cache_key,
            3600,  # 1 hour expiry
            json.dumps(result)
        )
        
        if result['confidence'] < 0.4:  # Adjust threshold as needed
            logger.warning(f"Low confidence prediction: {result['confidence']}")
            # Maybe use a fallback strategy or return uncertainty flag
        
        return result
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

@router.post("/predict/batch", response_model=List[Dict])
async def predict_categories_batch(
    batch: BatchTaskInput,
    predictor: Predictor = Depends(get_predictor)
):
    """
    Predict categories for multiple tasks.
    """
    try:
        tasks = [
            {"title": task.title, "description": task.description}
            for task in batch.tasks
        ]
        return predictor.batch_predict(tasks)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction error: {str(e)}"
        ) 