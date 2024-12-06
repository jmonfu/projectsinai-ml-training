"""
Prediction Routes
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Dict, Optional
from ..dependencies import get_classifier

router = APIRouter()

class TaskInput(BaseModel):
    title: str
    description: Optional[str] = None

class PredictionResponse(BaseModel):
    category: str
    confidence: float
    probabilities: Dict[str, float]

@router.post("/predict", response_model=PredictionResponse)
async def predict_category(
    task: TaskInput,
    classifier = Depends(get_classifier)
):
    """Predict category for a given task."""
    result = classifier.predict(task.title, task.description)
    return result 