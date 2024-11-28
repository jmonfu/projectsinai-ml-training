"""
Unit tests for the DataProcessor class
"""

import unittest
import numpy as np
from pathlib import Path
import json
from smartsynch.data.processor import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test case."""
        self.processor = DataProcessor()
        self.test_data_path = Path(__file__).parent / "test_data.json"
        
        # Create test data
        self.test_data = {
            "samples": [
                {
                    "title": "Implement user authentication",
                    "description": "Create JWT-based auth system",
                    "category": "Development",
                    "confidence": 1.0
                },
                {
                    "title": "Design new logo",
                    "description": "Create minimalist logo",
                    "category": "Design",
                    "confidence": 1.0
                }
            ]
        }
        
        # Save test data
        with open(self.test_data_path, 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        """Clean up after each test case."""
        if self.test_data_path.exists():
            self.test_data_path.unlink()

    def test_clean_text(self):
        """Test text cleaning functionality."""
        text = "Testing the API endpoint! @123"
        cleaned = self.processor.clean_text(text)
        self.assertNotIn("!", cleaned)
        self.assertNotIn("@", cleaned)
        self.assertTrue(cleaned.islower())

    def test_combine_title_description(self):
        """Test title and description combination."""
        title = "Test Title"
        desc = "Test Description"
        combined = self.processor.combine_title_description(title, desc)
        self.assertEqual(combined.count(title), 2)
        self.assertEqual(combined.count(desc), 1)

    def test_prepare_data(self):
        """Test data preparation pipeline."""
        embeddings, labels = self.processor.prepare_data(str(self.test_data_path))
        self.assertIsInstance(embeddings, np.ndarray)
        self.assertIsInstance(labels, np.ndarray)
        self.assertEqual(len(embeddings), 2)
        self.assertEqual(len(labels), 2)

    def test_split_data(self):
        """Test data splitting functionality."""
        X = np.random.rand(100, 10)
        y = np.random.randint(0, 2, 100)
        splits = self.processor.split_data(X, y)
        self.assertEqual(len(splits), 4)
        X_train, X_val, y_train, y_val = splits
        self.assertEqual(len(X_train), 80)
        self.assertEqual(len(X_val), 20)
