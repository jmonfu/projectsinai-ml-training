"""
Model Manager

Handles model loading, saving, and version management.
"""

import os
from pathlib import Path
import json
from typing import Dict, Optional
from .classifier import TaskClassifier

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

    def load_model(self, version: str = "latest") -> TaskClassifier:
        """
        Load model and metadata.
        
        Args:
            version: Model version to load
            
        Returns:
            Loaded model instance
        """
        if version == "latest":
            # Get latest version
            versions = [d for d in self.model_dir.iterdir() if d.is_dir()]
            if not versions:
                raise ValueError("No models found")
            version_dir = max(versions, key=lambda x: x.stat().st_mtime)
        else:
            version_dir = self.model_dir / version

        # Load metadata
        with open(version_dir / "metadata.json", "r") as f:
            metadata = json.load(f)
        
        # Initialize and load model
        self.category_map = metadata["category_map"]
        num_classes = len(self.category_map)
        model = TaskClassifier(num_classes)
        model.load(str(version_dir / "model.pt"))
        
        self.current_model = model
        return model
