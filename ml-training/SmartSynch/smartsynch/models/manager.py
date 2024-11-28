"""
Model Manager

Handles model loading, saving, and version management.
"""

import os
from pathlib import Path
import json
from typing import Dict, Optional
from .classifier import TaskClassifier
import logging

class ModelManager:
    def __init__(self, model_dir: str = "models/fine_tuned"):
        """
        Initialize model manager.
        
        Args:
            model_dir: Directory for storing model files
        """
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(parents=True, exist_ok=True)
        self.current_model: Optional[TaskClassifier] = None
        self.category_map: Dict[str, int] = {}
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.ERROR)

    def save_model(self, model: TaskClassifier, version: str, 
                  category_map: Dict[str, int], metrics: Dict):
        """
        Save model and associated metadata.
        
        Args:
            model: Trained model instance
            version: Model version string
            category_map: Category to index mapping
            metrics: Model performance metrics
        """
        # Create version directory
        version_dir = self.model_dir / version
        version_dir.mkdir(exist_ok=True)

        # Save model state
        model.save(str(version_dir / "model.pt"))

        # Save metadata
        metadata = {
            "version": version,
            "category_map": category_map,
            "metrics": metrics
        }
        with open(version_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)

    def load_model(self, version="latest"):
        """Load model from disk. Falls back to base model if no fine-tuned model exists."""
        try:
            # Try loading fine-tuned model first
            model_path = os.path.join(self.model_dir, "fine_tuned", version)
            if os.path.exists(model_path):
                return self.load_fine_tuned_model(model_path)
            
            # If no fine-tuned model exists, return base model
            self.logger.info("No fine-tuned model found. Using base model.")
            return self.load_base_model()
            
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            # Always fall back to base model on error
            self.logger.info("Falling back to base model.")
            return self.load_base_model()

    def load_fine_tuned_model(self, model_path: str):
        """Load a fine-tuned model from the given path."""
        if not os.path.exists(os.path.join(model_path, "model.pt")):
            raise FileNotFoundError(f"No model found at {model_path}")
            
        # Load metadata
        with open(os.path.join(model_path, "metadata.json"), "r") as f:
            metadata = json.load(f)
            
        # Create and load model
        self.current_model = TaskClassifier()
        self.current_model.load(os.path.join(model_path, "model.pt"))
        self.category_map = metadata["category_map"]
        return self.current_model

    def load_base_model(self):
        """Load the base model."""
        num_classes = 10  # Adjust based on your actual number of categories
        self.current_model = TaskClassifier(num_classes=num_classes)
        
        # Define meaningful category mappings
        self.category_map = {
            "0": "Bug Fix",
            "1": "Feature Request",
            "2": "Documentation",
            "3": "Enhancement",
            "4": "Security",
            "5": "Performance",
            "6": "Testing",
            "7": "UI/UX",
            "8": "DevOps",
            "9": "Other"
        }
        return self.current_model
