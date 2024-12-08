"""
Prediction Routes

API endpoints for task categorization predictions.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from smartsynch.models.predictor import MLPredictor
import os

router = APIRouter()

# Initialize predictor
predictor = MLPredictor()

# Load trained model if it exists
if os.path.exists("models/task_classifier.joblib"):
    predictor.load_model()

class TaskRequest(BaseModel):
    title: str
    description: str

class PredictionResponse(BaseModel):
    category: str
    confidence: float

@router.post("/predict", response_model=PredictionResponse)
async def predict_task(task: TaskRequest):
    try:
        result = predictor.predict(task.title, task.description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 