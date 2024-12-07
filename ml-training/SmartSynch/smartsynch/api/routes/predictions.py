"""
Prediction Routes

API endpoints for task categorization predictions.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from ...models.predictor import LocalPredictor

logger = logging.getLogger(__name__)
router = APIRouter()

# Initialize the predictor
predictor = LocalPredictor()

class TaskRequest(BaseModel):
    title: str
    description: str

class PredictionResponse(BaseModel):
    category: str
    confidence: float

@router.post("/predict", response_model=PredictionResponse)
async def predict_task(task: TaskRequest):
    """Predict category for a single task"""
    try:
        result = predictor.predict(task.title, task.description)
        return PredictionResponse(**result)
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 