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
from smartsynch.models.predictor import TaskPredictor
from smartsynch.utils.evaluation import ModelEvaluator

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_test_data(test_file: str):
    """Load test data from JSON file."""
    with open(test_file, 'r') as f:
        data = json.load(f)
    return data['samples']

def evaluate_model(model_version: str, test_data: list, output_dir: Path):
    """
    Evaluate model performance on test data.
    
    Args:
        model_version: Model version to evaluate
        test_data: List of test samples
        output_dir: Directory to save evaluation results
    """
    # Initialize predictor and evaluator
    predictor = TaskPredictor(model_version)
    evaluator = ModelEvaluator(predictor.model_manager.category_map)
    
    # Prepare test data
    titles = [sample['title'] for sample in test_data]
    descriptions = [sample['description'] for sample in test_data]
    true_categories = [sample['category'] for sample in test_data]
    
    # Get predictions
    predictions = []
    confidences = []
    
    logger.info("Making predictions on test data...")
    for title, desc in zip(titles, descriptions):
        result = predictor.predict(title, desc)
        predictions.append(result['category'])
        confidences.append(result['confidence'])
    
    # Convert categories to indices
    category_map = predictor.model_manager.category_map
    y_true = [category_map[cat] for cat in true_categories]
    y_pred = [category_map[cat] for cat in predictions]
    
    # Compute all metrics
    logger.info("Computing evaluation metrics...")
    eval_results = evaluator.evaluate_model(y_true, y_pred, confidences)
    
    # Save confusion matrix plot
    logger.info("Generating confusion matrix plot...")
    evaluator.plot_confusion_matrix(
        y_true, y_pred,
        output_path=output_dir / 'confusion_matrix.png'
    )
    
    # Save detailed results
    logger.info("Saving evaluation results...")
    with open(output_dir / 'evaluation_results.json', 'w') as f:
        json.dump(eval_results, f, indent=2)
    
    # Log summary metrics
    logger.info("\nEvaluation Summary:")
    logger.info(f"Accuracy: {eval_results['basic_metrics']['accuracy']:.4f}")
    logger.info(f"F1 Score: {eval_results['basic_metrics']['f1']:.4f}")
    logger.info(f"Mean Confidence: {eval_results['confidence_metrics']['mean_confidence']:.4f}")

def main():
    """Main evaluation pipeline."""
    parser = argparse.ArgumentParser(description='Evaluate model performance')
    parser.add_argument(
        '--model-version',
        type=str,
        default='latest',
        help='Model version to evaluate'
    )
    parser.add_argument(
        '--test-data',
        type=str,
        default='data/test_data.json',
        help='Path to test data file'
    )
    parser.add_argument(
        '--output-dir',
        type=str,
        default='evaluation_results',
        help='Directory to save evaluation results'
    )
    args = parser.parse_args()
    
    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Load test data
        logger.info(f"Loading test data from {args.test_data}")
        test_data = load_test_data(args.test_data)
        
        # Run evaluation
        evaluate_model(args.model_version, test_data, output_dir)
        logger.info(f"Evaluation results saved to {output_dir}")
        
    except Exception as e:
        logger.error(f"Error during evaluation: {str(e)}")
        raise

if __name__ == "__main__":
    main()
