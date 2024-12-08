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
from smartsynch.api.routes import predictions
from pydantic import BaseModel
from smartsynch.models.predictor import MLPredictor

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="SmartSynch Task Categorizer",
    description="API for automatic task categorization using ML",
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

# Import routes
from .routes import health

# Include routers
app.include_router(
    predictions.router,
    prefix="/api/smartsynch/v1",
    tags=["predictions"]
)
app.include_router(health.router, prefix="/api/smartsynch/v1")

# Add a health check endpoint (Render will use this)
@app.get("/api/smartsynch/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "model": "ML classifier loaded"
    }

# Add prediction models
class TaskInput(BaseModel):
    title: str
    description: str = ""

class PredictionResponse(BaseModel):
    category: str
    confidence: float

# Add prediction endpoint
@app.post("/api/smartsynch/v1/predict", response_model=PredictionResponse)
async def predict_task(task: TaskInput):
    try:
        predictor = MLPredictor()
        result = predictor.predict(task.title, task.description)
        return PredictionResponse(
            category=result["category"],
            confidence=result["confidence"]
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Prediction failed"}
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    ) 