"""
Unit tests for feedback endpoints
"""

import unittest
from unittest.mock import Mock, patch
from datetime import datetime
from fastapi.testclient import TestClient
from smartsynch.api.app import app

class TestFeedbackRoutes(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.client = TestClient(app)
        self.mock_redis = Mock()
        
        # Sample feedback data
        self.feedback_data = {
            "task_id": "123",
            "predicted_category": "Development",
            "actual_category": "Development",
            "confidence": 0.95,
            "accepted": True,
            "notes": "Good prediction"
        }

    @patch('smartsynch.api.routes.feedback.get_redis_client')
    def test_submit_feedback_accepted(self, mock_get_redis):
        """Test submitting accepted prediction feedback."""
        # Setup mock
        mock_get_redis.return_value = self.mock_redis
        
        # Make request
        response = self.client.post(
            "/api/v1/feedback",
            json=self.feedback_data
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        
        # Verify Redis calls
        self.mock_redis.lpush.assert_called_once()
        self.mock_redis.hincrby.assert_called_with(
            "feedback_stats", "accepted", 1
        )

    @patch('smartsynch.api.routes.feedback.get_redis_client')
    def test_submit_feedback_rejected(self, mock_get_redis):
        """Test submitting rejected prediction feedback."""
        # Modify feedback data
        self.feedback_data["accepted"] = False
        self.feedback_data["actual_category"] = "Design"
        
        # Setup mock
        mock_get_redis.return_value = self.mock_redis
        
        # Make request
        response = self.client.post(
            "/api/v1/feedback",
            json=self.feedback_data
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        
        # Verify Redis calls
        self.mock_redis.lpush.assert_called_once()
        self.mock_redis.hincrby.assert_called_with(
            "feedback_stats", "rejected", 1
        )

    @patch('smartsynch.api.routes.feedback.get_redis_client')
    def test_get_feedback_stats(self, mock_get_redis):
        """Test retrieving feedback statistics."""
        # Setup mock
        mock_get_redis.return_value = self.mock_redis
        self.mock_redis.hgetall.return_value = {
            "accepted": "150",
            "rejected": "50"
        }
        
        # Make request
        response = self.client.get("/api/v1/feedback/stats")
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["accepted"], 150)
        self.assertEqual(data["rejected"], 50)

    def test_invalid_feedback_data(self):
        """Test submitting invalid feedback data."""
        # Make request with missing required fields
        response = self.client.post(
            "/api/v1/feedback",
            json={"task_id": "123"}  # Missing required fields
        )
        
        # Verify error response
        self.assertEqual(response.status_code, 422) 