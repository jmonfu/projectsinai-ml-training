"""
API Dependencies

Dependency injection for FastAPI routes.
"""

from functools import lru_cache
from redis import Redis
from ..models.predictor import Predictor

@lru_cache()
def get_predictor():
    """Get or create TaskPredictor instance."""
    return Predictor()

def get_redis_client():
    """Get Redis client instance."""
    return Redis(
        host="localhost",
        port=6379,
        db=0,
        decode_responses=True
    ) 