"""
Unit tests for ModelEvaluator
"""

import unittest
import numpy as np
from smartsynch.utils.evaluation import ModelEvaluator

class TestModelEvaluator(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.category_map = {
            "Development": 0,
            "Design": 1,
            "Research": 2
        }
        self.evaluator = ModelEvaluator(self.category_map)
        
        # Sample test data
        self.y_true = [0, 1, 2, 0, 1, 2]
        self.y_pred = [0, 1, 2, 1, 1, 2]
        self.confidences = [0.9, 0.8, 0.95, 0.7, 0.85, 0.9]

    def test_basic_metrics(self):
        """Test basic metric calculations."""
        metrics = self.evaluator.compute_basic_metrics(
            self.y_true, self.y_pred
        )
        
        self.assertIn("accuracy", metrics)
        self.assertIn("precision", metrics)
        self.assertIn("recall", metrics)
        self.assertIn("f1", metrics)
        
        # Check accuracy calculation
        self.assertEqual(metrics["accuracy"], 5/6)

    def test_confusion_matrix(self):
        """Test confusion matrix computation."""
        cm = self.evaluator.compute_confusion_matrix(
            self.y_true, self.y_pred
        )
        
        self.assertIsInstance(cm, np.ndarray)
        self.assertEqual(cm.shape, (3, 3))
        
        # Check specific values
        self.assertEqual(cm[0, 0], 1)  # True Dev predicted as Dev
        self.assertEqual(cm[0, 1], 1)  # True Dev predicted as Design

    def test_classification_report(self):
        """Test detailed classification report."""
        report = self.evaluator.generate_classification_report(
            self.y_true, self.y_pred
        )
        
        self.assertIn("Development", report)
        self.assertIn("Design", report)
        self.assertIn("Research", report)
        
        for category in self.category_map:
            self.assertIn("precision", report[category])
            self.assertIn("recall", report[category])
            self.assertIn("f1-score", report[category])

    def test_full_evaluation(self):
        """Test comprehensive evaluation."""
        eval_results = self.evaluator.evaluate_model(
            self.y_true, self.y_pred, self.confidences
        )
        
        self.assertIn("basic_metrics", eval_results)
        self.assertIn("detailed_metrics", eval_results)
        self.assertIn("confidence_metrics", eval_results)
        
        # Check confidence metrics
        conf_metrics = eval_results["confidence_metrics"]
        self.assertEqual(conf_metrics["min_confidence"], 0.7)
        self.assertEqual(conf_metrics["max_confidence"], 0.95) 