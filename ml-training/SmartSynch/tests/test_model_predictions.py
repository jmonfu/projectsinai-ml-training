import unittest
import torch
from sentence_transformers import SentenceTransformer
from pathlib import Path
import glob

class TestModelPredictions(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Find the latest model directory
        model_dirs = glob.glob('../models/fine_tuned/*/')
        latest_dir = max(model_dirs, key=lambda x: x.split('/')[-2])
        model_path = Path(latest_dir) / 'model.pt'
        
        # Load model data
        self.model_data = torch.load(model_path)
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Initialize classifier
        self.classifier = torch.nn.Sequential(
            torch.nn.Linear(384, 128),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.2),
            torch.nn.Linear(128, len(self.model_data['categories']))
        )
        self.classifier.load_state_dict(self.model_data['classifier_state'])
        self.classifier.eval()

    def predict_category(self, title, description):
        """Helper method to make predictions."""
        text = f"{title} {description}"
        embedding = self.embedding_model.encode([text], convert_to_tensor=True)
        
        with torch.no_grad():
            output = self.classifier(embedding)
            probabilities = torch.nn.functional.softmax(output, dim=1)
            
        category_idx = torch.argmax(probabilities).item()
        category = self.model_data['categories'][category_idx]
        confidence = probabilities[0][category_idx].item()
        
        return category, confidence

    def test_development_prediction(self):
        """Test development task prediction."""
        category, confidence = self.predict_category(
            "Implement login system",
            "Create user authentication with JWT tokens"
        )
        self.assertEqual(category, "Development")
        self.assertGreater(confidence, 0.5)

    def test_design_prediction(self):
        """Test design task prediction."""
        category, confidence = self.predict_category(
            "Design new logo",
            "Create modern minimalist logo for brand"
        )
        self.assertEqual(category, "Design")
        self.assertGreater(confidence, 0.5)

    def test_research_prediction(self):
        """Test research task prediction."""
        category, confidence = self.predict_category(
            "Research cloud providers",
            "Compare AWS, GCP, and Azure services"
        )
        self.assertEqual(category, "Research")
        self.assertGreater(confidence, 0.5)

if __name__ == '__main__':
    unittest.main() 