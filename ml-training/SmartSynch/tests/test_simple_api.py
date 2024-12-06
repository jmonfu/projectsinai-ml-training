import unittest
from fastapi.testclient import TestClient
from smartsynch.api.main import app

class TestSimpleAPI(unittest.TestCase):
    def setUp(self):
        """Set up test client."""
        self.client = TestClient(app)
        
    def test_predict_development_task(self):
        """Test prediction for a development task."""
        response = self.client.post("/api/v1/predict", json={
            "title": "Implement login system",
            "description": "Create user authentication with JWT"
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["category"], "Development")
        self.assertGreater(data["confidence"], 0.5)
        self.assertIn("probabilities", data)
        
    def test_predict_design_task(self):
        """Test prediction for a design task."""
        response = self.client.post("/api/v1/predict", json={
            "title": "Design new homepage",
            "description": "Create mockup for website landing page"
        })
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["category"], "Design")
        self.assertGreater(data["confidence"], 0.5)
        
    def test_submit_feedback(self):
        """Test feedback submission."""
        response = self.client.post("/api/v1/feedback", json={
            "title": "Implement login",
            "description": "Create authentication system",
            "predicted_category": "Development",
            "actual_category": "Development",
            "confidence": 0.95,
            "accepted": True
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "success")

if __name__ == '__main__':
    unittest.main() 