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
import torch.nn.functional as F

class TaskClassifier(nn.Module):
    def __init__(self, num_classes: int, dropout_rate: float = 0.2):
        super().__init__()
        
        # Load pre-trained sentence transformer
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = self.encoder.get_sentence_embedding_dimension()
        
        # Classification head with Xavier initialization
        self.classifier = nn.Sequential(
            nn.Linear(self.embedding_dim, 256),
            nn.ReLU(),
            nn.Dropout(p=dropout_rate),
            nn.Linear(256, num_classes)
        )
        
        # Initialize weights
        for m in self.classifier.modules():
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
                nn.init.zeros_(m.bias)

    def forward(self, batch_data):
        """Forward pass of the model."""
        # If input is already a tensor (during training), pass directly to classifier
        if isinstance(batch_data, torch.Tensor):
            return self.classifier(batch_data)
        
        # If input is text (during prediction), encode it first
        if isinstance(batch_data, str) or isinstance(batch_data, list):
            # Ensure we have a list of texts
            texts = [batch_data] if isinstance(batch_data, str) else batch_data
            # Get embeddings from sentence transformer
            embeddings = self.encoder.encode(texts, convert_to_tensor=True)
            # Pass through classifier
            return self.classifier(embeddings)
        
        raise ValueError(f"Unsupported input type: {type(batch_data)}")

    def predict(self, texts):
        """Predict categories for input texts."""
        # Get model outputs
        logits = self(texts)
        probabilities = F.softmax(logits, dim=1)
        
        # Get predicted class and confidence
        predicted_classes = torch.argmax(probabilities, dim=1)
        confidences = probabilities[torch.arange(probabilities.size(0)), predicted_classes]
        
        # Add bias towards Development category for development-related keywords
        dev_keywords = ['implement', 'develop', 'code', 'build', 'create', 'add', 'set up']
        if any(keyword in texts.lower() for keyword in dev_keywords):
            dev_class_idx = 1  # Development category index
            probabilities[:, dev_class_idx] *= 1.2  # Increase probability by 20%
            # Renormalize probabilities
            probabilities = probabilities / probabilities.sum(dim=1, keepdim=True)
        
        return predicted_classes.tolist(), confidences.tolist(), probabilities.tolist()

    def save(self, path: str):
        """Save model state."""
        torch.save(self.state_dict(), path)

    def load(self, path: str):
        """Load model state."""
        self.load_state_dict(torch.load(path)) 