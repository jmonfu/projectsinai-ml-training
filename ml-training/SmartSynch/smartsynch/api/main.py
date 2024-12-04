"""
FastAPI Application

Main FastAPI application for model serving.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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

# Import routes
from .routes import predictions, feedback, health

# Include routers
app.include_router(predictions.router, prefix="/api/smartsynch/v1")
app.include_router(feedback.router, prefix="/api/smartsynch/v1")
app.include_router(health.router, prefix="/api/smartsynch/v1") 