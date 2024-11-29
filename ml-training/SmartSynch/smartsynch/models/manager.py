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
import torch

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
        
        # Initialize default category map
        self.category_map = {
            "Design": 0,
            "Development": 1,
            "Meeting": 2,
            "Planning": 3,
            "Research": 4
        }
        
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)  # Changed to INFO for better debugging

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

    def load_model(self, model_version):
        """Load model from disk. Falls back to base model if no fine-tuned model exists."""
        try:
            # Try loading weights if they exist
            model_path = self._get_model_path(model_version)
            
            # Load metadata if available
            version_dir = self.model_dir / model_version
            if os.path.exists(version_dir / "metadata.json"):
                with open(version_dir / "metadata.json", "r") as f:
                    metadata = json.load(f)
                    self.category_map = metadata["category_map"]
                    self.logger.info(f"Loaded category map from metadata: {self.category_map}")
            
            # Create new model instance with correct number of classes
            model = TaskClassifier(num_classes=len(self.category_map))
            
            if os.path.exists(model_path):
                model.load_state_dict(torch.load(model_path, map_location='cpu'))
                self.logger.info(f"Loaded model weights from {model_path}")
            else:
                self.logger.info("No model weights found, using initialized model")
            
            model.eval()
            return model
                
        except Exception as e:
            self.logger.error(f"Error loading model: {str(e)}")
            return self.load_base_model()

    def _get_model_path(self, version: str) -> str:
        """Get the path to the model file for the given version."""
        # Check for version-specific model
        version_dir = self.model_dir / version
        model_path = version_dir / "model.pt"
        
        if os.path.exists(model_path):
            # Load metadata to get category map
            with open(version_dir / "metadata.json", "r") as f:
                metadata = json.load(f)
                self.category_map = metadata["category_map"]
            return str(model_path)
        
        # If no fine-tuned model exists, return base model path
        self.logger.info("No fine-tuned model found. Using base model.")
        return str(self.model_dir / "base_model.pt")

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
        # Use the same category map as fine-tuned models
        self.category_map = {
            "Design": 0,
            "Development": 1,
            "Meeting": 2,
            "Planning": 3,
            "Research": 4
        }
        
        # Create model with correct number of classes
        model = TaskClassifier(num_classes=len(self.category_map))
        model.eval()  # Set to evaluation mode
        return model
