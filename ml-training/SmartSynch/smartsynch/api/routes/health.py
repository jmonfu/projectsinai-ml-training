"""
Health Check Routes

API endpoints for service health monitoring.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os
import logging
from huggingface_hub import HfApi

logger = logging.getLogger(__name__)
router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    huggingface: bool
    token_present: bool
    api_version: str = "1.0.0"
    error: str = None

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Check the health of the API and its dependencies"""
    try:
        # Check if token exists
        token = os.getenv("HUGGINGFACE_TOKEN")
        token_present = bool(token)
        
        if not token:
            return HealthResponse(
                status="unhealthy",
                huggingface=False,
                token_present=False,
                error="HUGGINGFACE_TOKEN not found"
            )

        try:
            # Test Hugging Face API
            api = HfApi()
            # Simple test - just verify token works
            api.whoami(token=token)
            
            return HealthResponse(
                status="healthy",
                huggingface=True,
                token_present=True
            )
        except Exception as e:
            logger.error(f"Hugging Face API test failed: {str(e)}")
            return HealthResponse(
                status="unhealthy",
                huggingface=False,
                token_present=True,
                error=f"API test failed: {str(e)}"
            )

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return HealthResponse(
            status="unhealthy",
            huggingface=False,
            token_present=False,
            error=str(e)
        ) 