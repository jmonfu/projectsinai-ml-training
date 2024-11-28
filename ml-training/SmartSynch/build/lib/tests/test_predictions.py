"""
Unit tests for prediction endpoints
"""

import unittest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from smartsynch.api.app import app

class TestPredictionRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
        self.mock_predictor = Mock()
        self.mock_redis = Mock()
        
        # Sample prediction result
        self.sample_prediction = {
            "category": "Development",
            "confidence": 0.95,
            "alternatives": []
        }

    @patch('smartsynch.api.routes.predictions.get_predictor')
    @patch('smartsynch.api.routes.predictions.get_redis_client')
    def test_predict_single_uncached(self, mock_get_redis, mock_get_predictor):
        """Test single prediction without cache."""
        # Setup mocks
        mock_get_predictor.return_value = self.mock_predictor
        mock_get_redis.return_value = self.mock_redis
        
        # Configure mock behaviors
        self.mock_redis.get.return_value = None
        self.mock_predictor.predict.return_value = self.sample_prediction
        
        # Make request
        response = self.client.post("/api/v1/predict", json={
            "title": "Test task",
            "description": "Test description"
        })
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["category"], "Development")
        self.assertEqual(data["confidence"], 0.95)
        self.assertEqual(len(data["alternatives"]), 0)

    @patch('smartsynch.api.routes.predictions.get_predictor')
    @patch('smartsynch.api.routes.predictions.get_redis_client')
    def test_predict_single_cached(self, mock_get_redis, mock_get_predictor):
        """Test single prediction with cache hit."""
        # Setup mocks
        mock_get_predictor.return_value = self.mock_predictor
        mock_get_redis.return_value = self.mock_redis
        
        # Configure mock behaviors
        self.mock_redis.get.return_value = '{"category": "Development", "confidence": 0.95, "alternatives": []}'
        
        # Make request
        response = self.client.post("/api/v1/predict", json={
            "title": "Test task",
            "description": "Test description"
        })
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["category"], "Development")
        
        # Verify predictor wasn't called
        self.mock_predictor.predict.assert_not_called()

    @patch('smartsynch.api.routes.predictions.get_predictor')
    def test_batch_predict(self, mock_get_predictor):
        """Test batch prediction endpoint."""
        # Setup mock
        mock_get_predictor.return_value = self.mock_predictor
        
        # Configure mock behavior
        self.mock_predictor.batch_predict.return_value = [
            {
                "category": "Development",
                "confidence": 0.9,
                "alternatives": []
            },
            {
                "category": "Design",
                "confidence": 0.8,
                "alternatives": []
            }
        ]
        
        # Make request
        response = self.client.post("/api/v1/predict/batch", json={
            "tasks": [
                {"title": "Task 1", "description": "Desc 1"},
                {"title": "Task 2", "description": "Desc 2"}
            ]
        })
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["category"], "Development")
        self.assertEqual(data[1]["category"], "Design")

    @patch('smartsynch.api.routes.predictions.get_predictor')
    def test_invalid_input(self, mock_get_predictor):
        """Test prediction with invalid input."""
        # Make request with missing description
        response = self.client.post("/api/v1/predict", json={
            "title": "Test task"
        })
        
        # Verify error response
        self.assertEqual(response.status_code, 422) 