"""
FastAPI Application

Main FastAPI application for model serving.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Dict, Optional
import logging
import os
from dotenv import load_dotenv

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SmartSynch Task Categorization API",
    description="API for automatic task categorization",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Determine which .env file to load based on the ENV variable
env_file = ".env.development" if os.getenv("ENV") == "development" else ".env.production"
load_dotenv(env_file)

# Add this after load_dotenv to debug
logger.info(f"Loading env file: {env_file}")
logger.info(f"HUGGINGFACE_TOKEN present: {bool(os.getenv('HUGGINGFACE_TOKEN'))}")

# Verify HUGGINGFACE_TOKEN is loaded
token = os.getenv("HUGGINGFACE_TOKEN")
if not token:
    logger.warning("HUGGINGFACE_TOKEN not found in environment!")

# Import routes
from .routes import predictions, health

# Include routers
app.include_router(predictions.router, prefix="/api/smartsynch/v1")
app.include_router(health.router, prefix="/api/smartsynch/v1")

# Add a health check endpoint (Render will use this)
@app.get("/api/smartsynch/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "huggingface_token": "configured" if token else "missing"
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    ) 