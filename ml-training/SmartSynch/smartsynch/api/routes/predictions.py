"""
Prediction Routes

API endpoints for task categorization predictions.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Dict, Optional
import json
from ...models.predictor import TaskPredictor
from ..dependencies import get_predictor, get_redis_client

router = APIRouter()

class TaskInput(BaseModel):
    title: str
    description: str

class BatchTaskInput(BaseModel):
    tasks: List[TaskInput]

@router.post("/predict", response_model=Dict)
async def predict_category(
    task: TaskInput,
    predictor: TaskPredictor = Depends(get_predictor),
    redis_client = Depends(get_redis_client)
):
    """
    Predict category for a single task.
    """
    # Check cache
    cache_key = f"pred:{task.title}:{task.description}"
    cached_result = redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)

    try:
        # Get prediction
        result = predictor.predict(task.title, task.description)
        
        # Cache result
        redis_client.setex(
            cache_key,
            3600,  # 1 hour expiry
            json.dumps(result)
        )
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

@router.post("/predict/batch", response_model=List[Dict])
async def predict_categories_batch(
    batch: BatchTaskInput,
    predictor: TaskPredictor = Depends(get_predictor)
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