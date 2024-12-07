"""
Predictor

Provides a high-level interface for making task category predictions.
"""

import logging
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
            token=token,
            task="zero-shot-classification"
        )
        self.categories = ["Development", "Design", "Research", "Meeting", "Planning"]

    def predict(self, title: str, description: str) -> dict:
        text = f"{title}. {description}"
        try:
            result = self.api(
                inputs=text,
                parameters={
                    "candidate_labels": self.categories,
                    "multi_label": False
                }
            )
            
            return {
                "category": result["labels"][0],
                "confidence": round(float(result["scores"][0]) * 100, 2)
            }
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            # Fallback to Development with lower confidence
            return {
                "category": "Development",
                "confidence": 70.0
            }

