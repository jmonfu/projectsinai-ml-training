"""
Predictor

Provides a high-level interface for making task category predictions.
"""

from typing import List, Dict, Tuple
import torch
import torch.nn.functional as F
import logging
from sentence_transformers import SentenceTransformer
from huggingface_hub import InferenceApi
import os

logger = logging.getLogger(__name__)

class Predictor:
    def __init__(self):
        token = os.getenv('HUGGINGFACE_TOKEN')
        if not token:
            logger.warning("HUGGINGFACE_TOKEN not set!")
            
        self.api = InferenceApi(
            repo_id="facebook/bart-large-mnli",
            token=token
        )
        self.categories = ["Development", "Design", "Research", "Meeting", "Planning"]

    def predict(self, title, description):
        text = f"{title}. {description}"
        try:
            result = self.api.zero_shot_classification(
                text, 
                labels=self.categories
            )
            return {
                "category": result["labels"][0],
                "confidence": round(result["scores"][0] * 100, 2)
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            raise

