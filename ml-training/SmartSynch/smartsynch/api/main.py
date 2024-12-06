"""
FastAPI Application

Main FastAPI application for model serving.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import redis
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

# Initialize Redis client
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    password=os.getenv("REDIS_PASSWORD", None),
    db=0,
    decode_responses=True
)

# Import routes
from .routes import predictions, feedback, health

# Include routers
app.include_router(predictions.router, prefix="/api/smartsynch/v1")
app.include_router(feedback.router, prefix="/api/smartsynch/v1")
app.include_router(health.router, prefix="/api/smartsynch/v1")

# Add a health check endpoint (Render will use this)
@app.get("/api/smartsynch/v1/health")
async def health_check():
    return {"status": "healthy"}

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Global error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    ) 