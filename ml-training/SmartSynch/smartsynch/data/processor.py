"""
Data Processor for SmartSynch Task Categorization

This module handles all data preprocessing steps for the task categorization model:
1. Text cleaning and normalization
2. Tokenization
3. Embedding generation
4. Training/validation split
"""

import json
import nltk
import spacy
from typing import List, Dict, Tuple, Union
import numpy as np
from sklearn.model_selection import train_test_split
from sentence_transformers import SentenceTransformer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import torch

class DataProcessor:
    def __init__(self, max_length: int = 512):
        """Initialize the data processor with required models and tools."""
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('wordnet')
        
        # Initialize NLP tools
        self.nlp = spacy.load('en_core_web_sm')
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize sentence transformer
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.max_length = max_length

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text data.
        
        Args:
            text: Input text string
            
        Returns:
            Cleaned and normalized text
        """
        # Tokenize text
        tokens = word_tokenize(text.lower())
        
        # Remove stopwords and lemmatize
        tokens = [
            self.lemmatizer.lemmatize(token) 
            for token in tokens 
            if token not in self.stop_words and token.isalnum()
        ]
        
        return ' '.join(tokens)

    def combine_title_description(self, title: str, description: str) -> str:
        """
        Combine title and description with appropriate weighting.
        Title is repeated to give it more importance in the embedding.
        
        Args:
            title: Task title
            description: Task description
            
        Returns:
            Combined text string
        """
        return f"{title} {title} {description}"

    def prepare_data(self, data_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load and prepare data for training.
        
        Args:
            data_path: Path to training data JSON file
            
        Returns:
            Tuple of (features, labels)
        """
        # Load data
        with open(data_path, 'r') as f:
            data = json.load(f)
        
        # Process text and create features
        texts = []
        labels = []
        categories = set()
        
        for sample in data['samples']:
            # Combine and clean text
            combined_text = self.combine_title_description(
                sample['title'], 
                sample['description']
            )
            cleaned_text = self.clean_text(combined_text)
            
            texts.append(cleaned_text)
            labels.append(sample['category'])
            categories.add(sample['category'])
        
        # Convert categories to indices
        self.category_map = {cat: idx for idx, cat in enumerate(sorted(categories))}
        
        # Generate embeddings
        embeddings = self.encoder.encode(texts)
        
        # Convert labels to numeric
        numeric_labels = np.array([self.category_map[label] for label in labels])
        
        return embeddings, numeric_labels

    def split_data(self, X: np.ndarray, y: np.ndarray, 
                  test_size: float = 0.2, random_state: int = 42) -> Tuple:
        """
        Split data into training and validation sets.
        
        Args:
            X: Feature matrix (embeddings)
            y: Labels
            test_size: Proportion of data to use for validation
            random_state: Random seed for reproducibility
            
        Returns:
            (X_train, X_val, y_train, y_val)
        """
        return train_test_split(X, y, test_size=test_size, 
                              random_state=random_state, stratify=y)

    def text_to_tensor(self, text: Union[str, List[str]]) -> torch.Tensor:
        """Convert text to tensor format."""
        if isinstance(text, str):
            # Tokenize the text
            tokens = word_tokenize(text.lower())
            
            # Create a fixed-size tensor filled with zeros
            tensor = torch.zeros(self.max_length, dtype=torch.long)
            
            # Fill tensor with token lengths (or whatever encoding you're using)
            for i, token in enumerate(tokens[:self.max_length]):
                tensor[i] = len(token)
            
            # Add batch dimension
            return tensor.unsqueeze(0)  # Shape becomes [1, max_length]
        else:
            # Handle list of texts
            tensors = [self.text_to_tensor(t) for t in text]
            return torch.cat(tensors, dim=0)  # Stack along batch dimension
