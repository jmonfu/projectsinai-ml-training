"""
Task Predictor

Provides a high-level interface for making task category predictions.
"""

from typing import List, Dict, Tuple
from .manager import ModelManager
from ..data.processor import DataProcessor

class TaskPredictor:
    def __init__(self, model_version: str = "latest"):
        """
        Initialize predictor with model and processor.
        
        Args:
            model_version: Version of model to load
        """
        self.model_manager = ModelManager()
        self.processor = DataProcessor()
        self.model = self.model_manager.load_model(model_version)
        self.category_map_reverse = {
            idx: cat for cat, idx in self.model_manager.category_map.items()
        }

    def predict(self, title: str, description: str) -> Dict[str, any]:
        """
        Predict category for a given task.
        
        Args:
            title: Task title
            description: Task description
            
        Returns:
            Dictionary containing prediction details:
            {
                "category": str,
                "confidence": float,
                "alternatives": List[Tuple[str, float]]
            }
        """
        # Combine and clean text
        combined_text = self.processor.combine_title_description(title, description)
        cleaned_text = self.processor.clean_text(combined_text)
        
        # Get model predictions
        logits = self.model([cleaned_text])
        pred_idx, confidence = self.model.predict([cleaned_text])
        
        # Get predicted category
        category = self.category_map_reverse[pred_idx[0]]
        
        # Get alternative predictions (if confidence is low)
        alternatives = []
        if confidence[0] < 0.8:  # Configurable threshold
            # Get top 3 predictions from logits
            top_k = min(3, len(self.category_map_reverse))
            top_indices = logits[0].topk(top_k)
            alternatives = [
                (self.category_map_reverse[idx], float(prob))
                for idx, prob in zip(top_indices.indices, top_indices.values)
                if idx != pred_idx[0]
            ]

        return {
            "category": category,
            "confidence": float(confidence[0]),
            "alternatives": alternatives
        }

    def batch_predict(self, tasks: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """
        Make predictions for multiple tasks.
        
        Args:
            tasks: List of dictionaries containing 'title' and 'description'
            
        Returns:
            List of prediction results
        """
        texts = [
            self.processor.combine_title_description(
                task['title'], task['description']
            )
            for task in tasks
        ]
        cleaned_texts = [self.processor.clean_text(text) for text in texts]
        
        # Get batch predictions
        pred_indices, confidences = self.model.predict(cleaned_texts)
        
        # Format results
        results = []
        for idx, conf in zip(pred_indices, confidences):
            results.append({
                "category": self.category_map_reverse[idx],
                "confidence": float(conf),
                "alternatives": []  # Could add alternatives if needed
            })
        
        return results
