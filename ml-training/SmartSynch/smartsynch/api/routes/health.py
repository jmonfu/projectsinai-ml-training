"""
Health Check Routes

API endpoints for service health monitoring.
"""

from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict:
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model": "scikit-learn",
        "api_version": "1.0.0",
        "error": None
    } 