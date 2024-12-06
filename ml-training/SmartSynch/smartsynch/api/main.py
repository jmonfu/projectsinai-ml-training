"""
FastAPI Application

Main FastAPI application for model serving.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import models  # import the new router
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ProjectsInAI API Gateway",
    description="API Gateway for AI Models",
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

# Include the models router
app.include_router(models.router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 