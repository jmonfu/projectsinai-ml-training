"""
Unit tests for TaskPredictor
"""

import unittest
from unittest.mock import Mock, patch
from smartsynch.models.predictor import TaskPredictor

class TestTaskPredictor(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.mock_model = Mock()
        self.mock_processor = Mock()
        
        # Mock category mapping
        self.category_map = {
            "Development": 0,
            "Design": 1,
            "Research": 2
        }
        
        with patch('smartsynch.models.predictor.ModelManager') as mock_manager:
            mock_manager.return_value.category_map = self.category_map
            mock_manager.return_value.load_model.return_value = self.mock_model
            self.predictor = TaskPredictor()

    def test_predict_high_confidence(self):
        """Test prediction with high confidence."""
        # Mock processor methods
        self.predictor.processor.combine_title_description.return_value = "test text"
        self.predictor.processor.clean_text.return_value = "cleaned text"
        
        # Mock model prediction
        self.mock_model.predict.return_value = ([0], [0.95])
        
        result = self.predictor.predict(
            "Test title", 
            "Test description"
        )
        
        self.assertEqual(result["category"], "Development")
        self.assertEqual(result["confidence"], 0.95)
        self.assertEqual(len(result["alternatives"]), 0)

    def test_predict_low_confidence(self):
        """Test prediction with low confidence."""
        self.predictor.processor.combine_title_description.return_value = "test text"
        self.predictor.processor.clean_text.return_value = "cleaned text"
        
        # Mock model prediction with low confidence
        self.mock_model.predict.return_value = ([0], [0.6])
        
        result = self.predictor.predict(
            "Test title", 
            "Test description"
        )
        
        self.assertEqual(result["category"], "Development")
        self.assertEqual(result["confidence"], 0.6)
        self.assertIn("alternatives", result)

    def test_batch_predict(self):
        """Test batch prediction functionality."""
        tasks = [
            {"title": "Task 1", "description": "Desc 1"},
            {"title": "Task 2", "description": "Desc 2"}
        ]
        
        self.predictor.processor.combine_title_description.side_effect = [
            "combined1", "combined2"
        ]
        self.predictor.processor.clean_text.side_effect = [
            "cleaned1", "cleaned2"
        ]
        
        self.mock_model.predict.return_value = ([0, 1], [0.9, 0.8])
        
        results = self.predictor.batch_predict(tasks)
        
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["category"], "Development")
        self.assertEqual(results[1]["category"], "Design")
