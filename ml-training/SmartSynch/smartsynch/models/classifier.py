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
        super().__init__()
        
        # Load pre-trained sentence transformer
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = self.encoder.get_sentence_embedding_dimension()
        
        self.classifier = nn.Sequential(
            nn.Linear(self.embedding_dim, 256),
            nn.ReLU(),
            nn.Dropout(p=dropout_rate),
            nn.Linear(256, num_classes)
        )

    def forward(self, x):
        # Ensure input tensor has correct shape
        if x.dim() == 1:
            x = x.unsqueeze(0)
        
        # Return logits directly
        logits = self.classifier(x.float())
        return logits

    def predict(self, x):
        self.eval()
        with torch.no_grad():
            # Return the full logits tensor instead of just the predicted class
            return self.forward(x)

    def save(self, path: str):
        """Save model state."""
        torch.save(self.state_dict(), path)

    def load(self, path: str):
        """Load model state."""
        self.load_state_dict(torch.load(path)) 