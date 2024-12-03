"""
Unit tests for health check endpoints
"""

import unittest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from smartsynch.api.app import app

class TestHealthCheck(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
        self.mock_predictor = Mock()
        self.mock_redis = Mock()

    @patch('smartsynch.api.routes.health.get_predictor')
    @patch('smartsynch.api.routes.health.get_redis_client')
    def test_health_check_all_healthy(self, mock_get_redis, mock_get_predictor):
        """Test health check when all services are healthy."""
        # Setup mocks
        mock_get_predictor.return_value = self.mock_predictor
        mock_get_redis.return_value = self.mock_redis
        
        # Configure mock behaviors
        self.mock_redis.ping.return_value = True
        self.mock_predictor.predict.return_value = {
            "category": "Development",
            "confidence": 0.95,
            "alternatives": []
        }
        
        # Make request
        response = self.client.get("/api/v1/health")
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["services"]["api"], "healthy")
        self.assertEqual(data["services"]["model"], "healthy")
        self.assertEqual(data["services"]["cache"], "healthy")

    @patch('smartsynch.api.routes.health.get_predictor')
    @patch('smartsynch.api.routes.health.get_redis_client')
    def test_health_check_redis_unhealthy(self, mock_get_redis, mock_get_predictor):
        """Test health check when Redis is down."""
        # Setup mocks
        mock_get_predictor.return_value = self.mock_predictor
        mock_get_redis.return_value = self.mock_redis
        
        # Configure mock behaviors
        self.mock_redis.ping.side_effect = Exception("Redis connection failed")
        self.mock_predictor.predict.return_value = {
            "category": "Development",
            "confidence": 0.95,
            "alternatives": []
        }
        
        # Make request
        response = self.client.get("/api/v1/health")
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "degraded")
        self.assertEqual(data["services"]["api"], "healthy")
        self.assertEqual(data["services"]["model"], "healthy")
        self.assertEqual(data["services"]["cache"], "unhealthy")

    @patch('smartsynch.api.routes.health.get_predictor')
    @patch('smartsynch.api.routes.health.get_redis_client')
    def test_health_check_model_unhealthy(self, mock_get_redis, mock_get_predictor):
        """Test health check when model prediction fails."""
        # Setup mocks
        mock_get_predictor.return_value = self.mock_predictor
        mock_get_redis.return_value = self.mock_redis
        
        # Configure mock behaviors
        self.mock_redis.ping.return_value = True
        self.mock_predictor.predict.side_effect = Exception("Model prediction failed")
        
        # Make request
        response = self.client.get("/api/v1/health")
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "degraded")
        self.assertEqual(data["services"]["api"], "healthy")
        self.assertEqual(data["services"]["model"], "unhealthy")
        self.assertEqual(data["services"]["cache"], "healthy") 