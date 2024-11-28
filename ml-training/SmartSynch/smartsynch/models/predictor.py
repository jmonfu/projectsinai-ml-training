"""
Task Predictor

Provides a high-level interface for making task category predictions.
"""

from typing import List, Dict, Tuple
from .manager import ModelManager
from ..data.processor import DataProcessor
import torch
import torch.nn.functional as F
import logging

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

    def predict(self, title: str, description: str) -> dict:
        try:
            # Combine title and description
            input_text = self.processor.combine_title_description(title, description)
            print(f"Combined text: {input_text}")  # Debugging statement
            
            input_tensor = self.processor.text_to_tensor(input_text)
            print(f"Input tensor shape: {input_tensor.shape}")  # Debugging statement
            
            # Get model predictions
            with torch.no_grad():
                # Get raw logits
                logits = self.model.forward(input_tensor)
                print(f"Logits: {logits}")  # Debugging statement
                
                # Convert to probabilities
                probabilities = F.softmax(logits, dim=1)
                print(f"Probabilities: {probabilities}")  # Debugging statement
                
                # Get predicted class and confidence
                confidence, predicted_class = torch.max(probabilities, dim=1)
                
                # Convert to Python types
                predicted_class = int(predicted_class.item())
                confidence = float(confidence.item())
                
                # Get category name
                category = self.model_manager.category_map.get(str(predicted_class), "Unknown")
                print(f"Predicted class: {predicted_class}, Category: {category}, Confidence: {confidence}")  # Debugging statement
            
            return {
                "category": category,
                "category_id": predicted_class,
                "confidence": confidence,
                "probabilities": {
                    self.model_manager.category_map.get(str(i)): float(prob)
                    for i, prob in enumerate(probabilities[0])
                }
            }
            
        except Exception as e:
            print(f"Error in prediction: {str(e)}")  # Debugging statement
            raise ValueError(f"Prediction error: {str(e)}")

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
