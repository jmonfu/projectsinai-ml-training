"""
Feedback Routes
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter()

class FeedbackInput(BaseModel):
    title: str
    description: Optional[str] = None
    predicted_category: str
    actual_category: str
    confidence: float
    accepted: bool

@router.post("/feedback")
async def submit_feedback(feedback: FeedbackInput):
    """Submit feedback for a prediction."""
    feedback_data = {
        **feedback.dict(),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Temporarily just return the feedback data
    return {"status": "success", "message": "Feedback recorded", "data": feedback_data}

@router.get("/feedback/stats")
async def get_feedback_stats():
    """Get feedback statistics."""
    # Temporarily return dummy stats
    return {
        "accepted": 0,
        "rejected": 0
    } 