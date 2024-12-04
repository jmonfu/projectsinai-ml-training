"""
API Dependencies

Dependency injection for FastAPI routes.
"""

from functools import lru_cache
from redis import Redis
import os
from ..models.predictor import Predictor

@lru_cache(maxsize=1)
def get_predictor():
    """Get or create TaskPredictor instance."""
    return Predictor()

@lru_cache()
def get_redis_client():
    """Get Redis client instance."""
    return Redis(
        host=os.getenv("REDISHOST", "redis"),
        port=int(os.getenv("REDISPORT", 6379)),
        password=os.getenv("REDISPASSWORD", None),
        db=0,
        decode_responses=True
    ) 