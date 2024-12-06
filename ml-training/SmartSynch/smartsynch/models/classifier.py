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
import numpy as np
import matplotlib.pyplot as plt
import logging
from torch.utils.data import DataLoader
import os
import json
from datetime import datetime

class TaskClassifier(nn.Module):
    def __init__(self, config):
        super(TaskClassifier, self).__init__()
        self.config = config
        self.history = {'train_loss': [], 'val_loss': []}
        self.best_val_loss = float('inf')
        self.patience_counter = 0
        
        # Load pre-trained sentence transformer
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.embedding_dim = self.encoder.get_sentence_embedding_dimension()
        
        # Add attention mechanism
        self.attention = nn.Sequential(
            nn.Linear(config['embedding_dim'], 128),
            nn.Tanh(),
            nn.Linear(128, 1),
            nn.Softmax(dim=1)
        )
        
        # Improved classifier architecture
        self.classifier = nn.Sequential(
            nn.Linear(config['embedding_dim'], 512),
            nn.ReLU(),
            nn.LayerNorm(512),  # Add layer normalization
            nn.Dropout(config['dropout_rate']),
            
            nn.Linear(512, 256),
            nn.ReLU(),
            nn.LayerNorm(256),
            nn.Dropout(config['dropout_rate']),
            
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.LayerNorm(128),
            nn.Dropout(config['dropout_rate']/2),  # Lower dropout in final layers
            
            nn.Linear(128, config['num_classes'])
        )

    def forward(self, x):
        # Convert input to tensor if it's not already
        if not isinstance(x, torch.Tensor):
            x = torch.tensor(x, dtype=torch.float32)
        
        # Add batch dimension if needed
        if len(x.shape) == 1:
            x = x.unsqueeze(0)
        
        # Apply attention
        attention_weights = self.attention(x)
        x = x * attention_weights
        
        # Classification
        return self.classifier(x)

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

    def train_model(self, train_loader, val_loader, criterion, optimizer, device):
        """Train the model"""
        for epoch in range(self.config['num_epochs']):
            logging.info(f"Epoch {epoch+1}/{self.config['num_epochs']}")
            
            # Training phase
            train_loss = self._train_epoch(train_loader, criterion, optimizer, device)
            self.history['train_loss'].append(train_loss)
            logging.info(f"Train Loss: {train_loss:.4f}")
            
            # Validation phase
            val_loss = self._validate(val_loader, criterion, device)
            self.history['val_loss'].append(val_loss)
            logging.info(f"Val Loss: {val_loss:.4f}")
            
            # Early stopping check
            if val_loss < self.best_val_loss:
                self.best_val_loss = val_loss
                self.patience_counter = 0
                self._save_best_model()
            else:
                self.patience_counter += 1
                if self.patience_counter >= self.config['early_stopping_patience']:
                    logging.info("Early stopping triggered!")
                    break
        
        # Save the training history
        self._save_training_history()

    def _train_epoch(self, train_loader, criterion, optimizer, device):
        self.train()  # Set model to training mode
        total_loss = 0.0
        num_batches = len(train_loader)

        for batch_idx, (data, target) in enumerate(train_loader):
            # Move data to device
            data, target = data.to(device), target.to(device)
            
            # Zero the parameter gradients
            optimizer.zero_grad()
            
            # Forward pass
            output = self(data)
            loss = criterion(output, target)
            
            # Backward pass and optimize
            loss.backward()
            optimizer.step()
            
            # Accumulate loss
            total_loss += loss.item()
        
        # Return average loss for the epoch
        return total_loss / num_batches

    def _validate(self, val_loader, criterion, device):
        """Validate the model"""
        self.eval()  # Set model to evaluation mode
        total_loss = 0.0
        num_batches = len(val_loader)

        with torch.no_grad():  # No gradient computation needed for validation
            for data, target in val_loader:
                # Move data to device
                data, target = data.to(device), target.to(device)
                
                # Forward pass
                output = self(data)
                loss = criterion(output, target)
                
                # Accumulate loss
                total_loss += loss.item()
        
        # Return average validation loss
        return total_loss / num_batches

    def _save_best_model(self):
        """Save the best model based on validation loss"""
        import os
        from datetime import datetime

        # Create timestamp for the model directory if it doesn't exist
        if not hasattr(self, 'model_save_dir'):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.model_save_dir = os.path.join(self.config['model_dir'], timestamp)
            os.makedirs(self.model_save_dir, exist_ok=True)

        # Save the model
        model_file = os.path.join(self.model_save_dir, 'best_model.pt')
        torch.save(self.state_dict(), model_file)

    def _plot_training_history(self) -> None:
        """Plot training and validation loss curves"""
        plt.figure(figsize=(10, 6))
        plt.plot(self.history['train_loss'], label='Training Loss')
        plt.plot(self.history['val_loss'], label='Validation Loss')
        plt.title('Model Loss Over Time')
        plt.xlabel('Epoch')
        plt.ylabel('Loss')
        plt.legend()
        plt.savefig('training_history.png')
        plt.close()

    def detect_overfitting(self):
        # Implement overfitting detection logic here
        pass 

    def _save_training_history(self):
        """Save training history to JSON"""
        # Create timestamp for the model directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_dir = os.path.join(self.config['model_dir'], timestamp)
        os.makedirs(model_dir, exist_ok=True)

        # Save the training history
        history_file = os.path.join(model_dir, 'training_history.json')
        with open(history_file, 'w') as f:
            json.dump(self.history, f)

        # Also save the model
        model_file = os.path.join(model_dir, 'model.pt')
        torch.save(self.state_dict(), model_file)
        
        logging.info(f"Saved model and history to {model_dir}")