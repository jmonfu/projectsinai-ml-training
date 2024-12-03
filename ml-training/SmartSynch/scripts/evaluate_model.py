#!/usr/bin/env python
"""
Model Evaluation Script

Evaluates model performance using various metrics:
- Accuracy, Precision, Recall, F1
- Confusion Matrix
- Confidence Analysis
"""

import argparse
import logging
import json
from pathlib import Path
import numpy as np
from smartsynch.models.predictor import Predictor
from smartsynch.utils.evaluation import ModelEvaluator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_test_data(test_file: str, labels_file: str = None):
    """Load test data from file."""
    if test_file.endswith('.npy'):
        if labels_file is None:
            raise ValueError("Labels file required when using .npy format")
        X = np.load(test_file, allow_pickle=True)
        y = np.load(labels_file, allow_pickle=True)
        return {'features': X, 'labels': y}
    elif test_file.endswith('.json'):
        with open(test_file) as f:
            return json.load(f)
    else:
        raise ValueError(f"Unsupported file format: {test_file}")

def evaluate_model(model_path: str, test_data: dict, output_dir: Path):
    """Evaluate model performance on test data."""
    logger.info("Loading model...")
    predictor = Predictor(model_path)
    
    # Extract features and labels from test data
    features = test_data['features']
    true_categories = test_data['labels']
    
    # Get predictions
    logger.info("Making predictions...")
    predictions = []
    confidences = []
    
    # Debug the feature format
    logger.info(f"Feature shape/type: {features.shape if hasattr(features, 'shape') else type(features)}")
    
    # Convert numpy array to tensor and pass directly to model
    try:
        import torch
        features_tensor = torch.from_numpy(features).float()  # Ensure float tensor
        logits = predictor.model.forward(features_tensor)
        predictions_tensor = torch.argmax(logits, dim=1)
        confidences_tensor = torch.max(torch.softmax(logits, dim=1), dim=1)[0]
        
        predictions = predictions_tensor.tolist()
        confidences = confidences_tensor.tolist()
    except Exception as e:
        logger.error(f"Error during prediction: {str(e)}")
        raise
    
    # Load category mapping from metadata
    metadata_path = Path(model_path).parent / 'metadata.json'
    if metadata_path.exists():
        with open(metadata_path) as f:
            metadata = json.load(f)
            category_map = metadata['category_map']
    else:
        # Fallback to default category map from test data
        category_map = {
            "Design": 0,
            "Development": 1,
            "Meeting": 2,
            "Planning": 3,
            "Research": 4
        }
    
    evaluator = ModelEvaluator(category_map)

def main():
    # Define parser
    parser = argparse.ArgumentParser(description='Evaluate model performance on test data')
    parser.add_argument('--model-path', required=True, help='Path to trained model')
    parser.add_argument('--test-data', required=True, help='Path to test data file')
    parser.add_argument('--labels', help='Path to labels file (required for .npy format)')
    parser.add_argument('--output-dir', required=True, help='Directory to save evaluation results')
    
    args = parser.parse_args()
    
    # Convert paths to absolute paths from project root
    project_root = Path(__file__).parent.parent  # This is the SmartSynch directory
    model_path = project_root / args.model_path
    test_data_path = project_root / args.test_data
    labels_path = project_root / args.labels if args.labels else None
    output_dir = project_root / args.output_dir
    
    # Ensure directories exist
    if not test_data_path.exists():
        logger.error(f"Test data not found at: {test_data_path}")
        logger.info(f"Current directory structure:")
        logger.info("\n".join(str(p) for p in project_root.glob("**/*") if p.is_file()))
        raise FileNotFoundError(f"Test data not found at: {test_data_path}")
        
    output_dir.mkdir(exist_ok=True, parents=True)
    
    # Load test data before passing to evaluate_model
    test_data = load_test_data(str(test_data_path), str(labels_path) if labels_path else None)
    evaluate_model(str(model_path), test_data, output_dir)

if __name__ == '__main__':
    main()
