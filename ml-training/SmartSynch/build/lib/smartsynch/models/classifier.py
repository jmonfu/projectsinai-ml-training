"""
Task Classification Model

This module implements the core model architecture combining:
1. Sentence-Transformer for text embedding
2. Custom classification head for task categorization
"""

import torch
import torch.nn as nn
from sentence_transformers import SentenceTransformer
from typing import Dict, List, Tuple

class TaskClassifier(nn.Module):
    def __init__(self, num_classes: int, dropout_rate: float = 0.2):
        """
        Initialize the task classifier model.
        
        Args:
            num_classes: Number of task categories
            dropout_rate: Dropout rate for regularization
        """
        super(TaskClassifier, self).__init__()
        
        # Load pre-trained sentence transformer
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = self.encoder.get_sentence_embedding_dimension()
        
        # Classification head
        self.classifier = nn.Sequential(
            nn.Linear(self.embedding_dim, 128),
            nn.ReLU(),
            nn.Dropout(dropout_rate),
            nn.Linear(128, num_classes),
            nn.Softmax(dim=1)
        )

    def forward(self, text: List[str]) -> torch.Tensor:
        """
        Forward pass through the model.
        
        Args:
            text: List of input texts (title + description)
            
        Returns:
            Tensor of class probabilities
        """
        # Generate embeddings
        with torch.no_grad():
            embeddings = self.encoder.encode(text, convert_to_tensor=True)
        
        # Pass through classifier
        logits = self.classifier(embeddings)
        return logits

    def predict(self, text: List[str]) -> Tuple[List[str], List[float]]:
        """
        Make predictions for input texts.
        
        Args:
            text: List of input texts
            
        Returns:
            Tuple of (predicted_categories, confidence_scores)
        """
        self.eval()
        with torch.no_grad():
            logits = self.forward(text)
            probs, preds = torch.max(logits, dim=1)
            return preds.tolist(), probs.tolist()

    def save(self, path: str):
        """Save model state."""
        torch.save(self.state_dict(), path)

    def load(self, path: str):
        """Load model state."""
        self.load_state_dict(torch.load(path)) 