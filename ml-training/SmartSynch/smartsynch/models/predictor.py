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
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class Predictor:
    _instance = None
    _initialized = False
    
    def __new__(cls, model_path=None):
        if cls._instance is None:
            cls._instance = super(Predictor, cls).__new__(cls)
        return cls._instance

    def __init__(self, model_path=None):
        if not self._initialized:
            self.model_manager = ModelManager()
            self.model = self.model_manager.load_model(model_path)
            self.categories = list(self.model_manager.category_map.keys())
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.confidence_threshold = 0.15
            self.model.to(self.device)
            self.model.eval()
            self.sentence_transformer = SentenceTransformer('all-MiniLM-L6-v2')
            self._initialized = True

    def get_embeddings(self, text):
        """Get embeddings for input text using SentenceTransformer"""
        return self.sentence_transformer.encode(text, convert_to_tensor=True)

    def predict(self, title, description=None):
        # Combine with more emphasis on title
        if description:
            text = f"{title} - {title} - {description}"
        else:
            text = title
        
        logging.info(f"Processing text: {text}")
        
        # Get embeddings
        embeddings = self.get_embeddings(text)
        logging.info(f"Embedding shape: {embeddings.shape}")
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(embeddings)
            logging.info(f"Raw outputs: {outputs}")
            
            probabilities = F.softmax(outputs, dim=-1)
            logging.info(f"Softmax probabilities: {probabilities}")
        
        # Convert to list and get prediction
        probabilities = probabilities.squeeze().tolist()
        max_prob = max(probabilities)
        max_index = probabilities.index(max_prob)
        
        # Get top 2 predictions for comparison
        sorted_probs = sorted(enumerate(probabilities), key=lambda x: x[1], reverse=True)
        top_2 = [(self.categories[idx], prob) for idx, prob in sorted_probs[:2]]
        logging.info(f"Top 2 predictions: {top_2}")
        
        probs_dict = {cat: float(prob) for cat, prob in zip(self.categories, probabilities)}
        
        result = {
            "category": self.categories[max_index],
            "category_id": max_index,
            "confidence": max_prob,
            "probabilities": probs_dict
        }
        
        return result

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

