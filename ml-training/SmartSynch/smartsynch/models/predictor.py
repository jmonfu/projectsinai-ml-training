"""
Predictor

Provides a high-level interface for making task category predictions.
"""

from typing import List, Dict, Tuple
from smartsynch.models.manager import ModelManager
from smartsynch.data.processor import DataProcessor
import torch
import torch.nn.functional as F
import logging

logger = logging.getLogger(__name__)

class Predictor:
    def __init__(self, model_version: str = "latest"):
        """
        Initialize predictor with model and processor.
        
        Args:
            model_version: Version of model to load
        """
        try:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model_manager = ModelManager()
            self.processor = DataProcessor()
            
            # Debug logging for model loading
            logger.info(f"Loading model version: {model_version}")
            self.model = self.model_manager.load_model(model_version)
            
            # Debug logging for category mappings
            logger.info(f"Original category map: {self.model_manager.category_map}")
            
            self.model.to(self.device)
            self.category_map_reverse = {
                idx: cat for cat, idx in self.model_manager.category_map.items()
            }
            
            # Debug the reverse mapping
            logger.info(f"Reverse category map: {self.category_map_reverse}")
            
        except Exception as e:
            logger.error(f"Failed to initialize predictor: {str(e)}")
            raise

    def predict(self, title: str, description: str) -> dict:
        """Make a prediction for a single task."""
        try:
            # Add more weight to the title (it's often more indicative of category)
            combined_text = f"{title} {title} {description}"  # Repeat title for emphasis
            
            # Add logging to see raw predictions
            logger.debug(f"Input - Title: {title}")
            logger.debug(f"Input - Description: {description}")
            logger.debug(f"Combined text: {combined_text}")
            
            with torch.no_grad():
                logits = self.model([combined_text])
                probabilities = F.softmax(logits, dim=1)
                
                # Log raw probabilities for each category
                for idx, prob in enumerate(probabilities[0]):
                    logger.debug(f"Category {self.category_map_reverse[idx]}: {prob:.4f}")
                
                confidence, predicted_class = torch.max(probabilities, dim=1)
                
                # Convert to Python types
                predicted_class = int(predicted_class.item())
                confidence = float(confidence.item())
                
                # Debug logging
                logger.debug(f"Predicted class index: {predicted_class}")
                logger.debug(f"Category map reverse: {self.category_map_reverse}")
                category = self.category_map_reverse.get(predicted_class, "Unknown")
                
                # Create probabilities dict
                prob_dict = {
                    self.category_map_reverse[i]: float(prob)
                    for i, prob in enumerate(probabilities[0])
                    if i in self.category_map_reverse
                }
                
                return {
                    "category": category,
                    "category_id": predicted_class,
                    "confidence": confidence,
                    "probabilities": prob_dict,
                    "alternatives": [] if confidence >= 0.8 else [
                        (cat, float(prob)) 
                        for cat, prob in prob_dict.items()
                        if cat != category
                    ][:2]
                }
                
        except Exception as e:
            logger.error(f"Prediction failed: {str(e)}")
            raise ValueError(f"Prediction error: {str(e)}")

    def batch_predict(self, tasks: List[Dict[str, str]]) -> List[Dict[str, any]]:
        """Make predictions for multiple tasks."""
        try:
            # Process all texts
            texts = [
                self.processor.combine_title_description(
                    task['title'], task['description']
                )
                for task in tasks
            ]
            
            # Get batch predictions
            with torch.no_grad():
                # Convert texts to tensors
                input_tensors = torch.stack([
                    self.processor.text_to_tensor(text) for text in texts
                ]).to(self.device)
                
                # Get predictions
                logits = self.model.forward(input_tensors)
                probabilities = F.softmax(logits, dim=1)
                
                # Get predicted classes and confidences
                confidences, predicted_classes = torch.max(probabilities, dim=1)
                
                # Format results
                results = []
                for idx, (pred_class, conf, probs) in enumerate(zip(
                    predicted_classes, confidences, probabilities)):
                    results.append({
                        "category": self.category_map_reverse.get(int(pred_class), "Unknown"),
                        "category_id": int(pred_class),
                        "confidence": float(conf),
                        "probabilities": {
                            self.category_map_reverse.get(i): float(prob)
                            for i, prob in enumerate(probs)
                        }
                    })
                
                return results
                
        except Exception as e:
            logger.error(f"Batch prediction failed: {str(e)}")
            raise ValueError(f"Batch prediction error: {str(e)}")

