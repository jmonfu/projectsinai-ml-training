"""
Health Check Routes

API endpoints for service health monitoring.
"""

from fastapi import APIRouter, Depends
from ..dependencies import get_predictor, get_redis_client

router = APIRouter()

@router.get("/health")
async def health_check(
    predictor = Depends(get_predictor),
    redis_client = Depends(get_redis_client)
):
    """
    Check health of all services.
    """
    health_status = {
        "status": "healthy",
        "services": {
            "api": "healthy",
            "model": "healthy",
            "cache": "healthy"
        }
    }
    
    # Check Redis connection
    try:
        redis_client.ping()
    except Exception:
        health_status["services"]["cache"] = "unhealthy"
        health_status["status"] = "degraded"
    
    # Check model
    try:
        predictor.predict(
            "Test task",
            "Test description"
        )
    except Exception:
        health_status["services"]["model"] = "unhealthy"
        health_status["status"] = "degraded"
    
    return health_status 