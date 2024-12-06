"""
API Dependencies
"""
from functools import lru_cache
from ..models.simple_classifier import SimpleTaskClassifier

@lru_cache(maxsize=1)
def get_classifier():
    """Get or create SimpleTaskClassifier instance."""
    return SimpleTaskClassifier()