#!/usr/bin/env python
"""
Model Training Script for SmartSynch Task Categorization

This script handles model training with:
- Initial training using PyTorch
- Fine-tuning capabilities
- Early stopping
- Model checkpointing
- Experiment tracking
"""

import argparse
import logging
import yaml
from pathlib import Path
import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from datetime import datetime
from smartsynch.models.classifier import TaskClassifier
from smartsynch.models.manager import ModelManager
from smartsynch.utils.metrics import compute_metrics

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_training_data(data_dir: Path):
    """Load preprocessed training data."""
    X_train = np.load(data_dir / "X_train.npy")
    X_val = np.load(data_dir / "X_val.npy")
    y_train = np.load(data_dir / "y_train.npy")
    y_val = np.load(data_dir / "y_val.npy")
    category_map = np.load(data_dir / "category_map.npy", allow_pickle=True).item()
    
    return X_train, X_val, y_train, y_val, category_map

def create_data_loaders(X_train, X_val, y_train, y_val, batch_size):
    """Create PyTorch data loaders."""
    train_dataset = TensorDataset(
        torch.FloatTensor(X_train),
        torch.LongTensor(y_train)
    )
    val_dataset = TensorDataset(
        torch.FloatTensor(X_val),
        torch.LongTensor(y_val)
    )
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=batch_size)
    
    return train_loader, val_loader

def train_epoch(model, train_loader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    total_loss = 0
    
    for batch_X, batch_y in train_loader:
        batch_X, batch_y = batch_X.to(device), batch_y.to(device)
        
        optimizer.zero_grad()
        outputs = model(batch_X)
        loss = criterion(outputs, batch_y)
        
        loss.backward()
        optimizer.step()
        
        total_loss += loss.item()
    
    return total_loss / len(train_loader)

def evaluate(model, val_loader, criterion, device):
    """Evaluate the model."""
    model.eval()
    total_loss = 0
    all_preds = []
    all_labels = []
    
    with torch.no_grad():
        for batch_X, batch_y in val_loader:
            batch_X, batch_y = batch_X.to(device), batch_y.to(device)
            
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            
            total_loss += loss.item()
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(batch_y.cpu().numpy())
    
    metrics = compute_metrics(all_labels, all_preds)
    metrics['loss'] = total_loss / len(val_loader)
    
    return metrics

def main():
    """Main training pipeline."""
    parser = argparse.ArgumentParser(description='Train task categorization model')
    parser.add_argument('--config', type=str, default='configs/training_config.yaml')
    parser.add_argument('--data-dir', type=str, default='data/processed')
    args = parser.parse_args()
    
    # Load config
    with open(args.config) as f:
        config = yaml.safe_load(f)
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")
    
    # Load data
    data_dir = Path(args.data_dir)
    X_train, X_val, y_train, y_val, category_map = load_training_data(data_dir)
    
    # Create data loaders
    train_loader, val_loader = create_data_loaders(
        X_train, X_val, y_train, y_val, 
        config['training']['batch_size']
    )
    
    # Initialize model
    model = TaskClassifier(
        num_classes=len(category_map),
        dropout_rate=config['model']['dropout_rate']
    ).to(device)
    
    # Training setup
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=config['training']['learning_rate']
    )
    
    # Training loop
    best_val_loss = float('inf')
    patience = config['training']['patience']
    patience_counter = 0
    
    for epoch in range(config['training']['epochs']):
        # Train
        train_loss = train_epoch(model, train_loader, criterion, optimizer, device)
        
        # Evaluate
        val_metrics = evaluate(model, val_loader, criterion, device)
        
        # Log metrics
        logger.info(
            f"Epoch {epoch+1}/{config['training']['epochs']} - "
            f"Train Loss: {train_loss:.4f} - "
            f"Val Loss: {val_metrics['loss']:.4f} - "
            f"Val Accuracy: {val_metrics['accuracy']:.4f}"
        )
        
        # Early stopping
        if val_metrics['loss'] < best_val_loss:
            best_val_loss = val_metrics['loss']
            patience_counter = 0
            
            # Save best model
            model_manager = ModelManager()
            version = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_manager.save_model(
                model=model,
                version=version,
                category_map=category_map,
                metrics=val_metrics
            )
            logger.info(f"Saved best model version: {version}")
        else:
            patience_counter += 1
            if patience_counter >= patience:
                logger.info("Early stopping triggered")
                break

if __name__ == "__main__":
    main()
