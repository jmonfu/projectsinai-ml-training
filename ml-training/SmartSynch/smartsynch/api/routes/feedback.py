"""
Feedback Routes

API endpoints for collecting user feedback on predictions.
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
import json
from datetime import datetime
from ..dependencies import get_redis_client

router = APIRouter()

class FeedbackInput(BaseModel):
    task_id: str
    predicted_category: str
    actual_category: str
    confidence: float
    accepted: bool
    notes: Optional[str] = None

@router.post("/feedback")
async def submit_feedback(
    feedback: FeedbackInput,
    redis_client = Depends(get_redis_client)
):
    """
    Submit feedback for a prediction.
    """
    try:
        feedback_data = {
            **feedback.dict(),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Store feedback in Redis
        redis_client.lpush(
            "prediction_feedback",
            json.dumps(feedback_data)
        )
        
        # Update feedback stats
        if feedback.accepted:
            redis_client.hincrby("feedback_stats", "accepted", 1)
        else:
            redis_client.hincrby("feedback_stats", "rejected", 1)
        
        return {"status": "success", "message": "Feedback recorded"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error recording feedback: {str(e)}"
        )

@router.get("/feedback/stats")
async def get_feedback_stats(
    redis_client = Depends(get_redis_client)
):
    """
    Get feedback statistics.
    """
    try:
        stats = redis_client.hgetall("feedback_stats")
        return {
            "accepted": int(stats.get("accepted", 0)),
            "rejected": int(stats.get("rejected", 0))
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error fetching stats: {str(e)}"
        ) 