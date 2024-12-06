"""
Text Processing Utilities

Helper functions for text preprocessing and cleaning.
"""

import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

def combine_title_description(title: str, description: str) -> str:
    """Combine title and description into a single text."""
    return f"{title}. {description}"

def clean_text(text: str) -> str:
    """Clean and normalize text for processing."""
    return text.lower().strip()

def contains_keywords(text: str, keywords: List[str]) -> bool:
    """Check if text contains any of the given keywords."""
    text = clean_text(text)
    return any(keyword in text for keyword in keywords)

def is_review_task(text: str) -> Tuple[bool, bool]:
    """
    Check if task is a review task and what type.
    Returns: (is_review, is_multi_review)
    """
    text = clean_text(text)
    is_review = "review" in text
    review_keywords = ["design", "implementation", "research", "findings", "analysis"]
    is_multi_review = is_review and sum(1 for k in review_keywords if k in text) >= 2
    
    return is_review, is_multi_review

def get_task_aspects(text: str) -> Dict[str, bool]:
    """
    Analyze different aspects of a task.
    """
    text = clean_text(text)
    
    return {
        "has_status": any(word in text for word in ["status", "progress", "general"]),
        "has_technical": any(word in text for word in [
            "code", "pr", "implementation", "api", "jwt", "auth"
        ]),
        "has_architecture": "architecture" in text,
        "has_project": any(word in text for word in ["project", "progress", "general"])
    }

def is_sprint_related(text: str) -> bool:
    """Check if task is sprint-related."""
    text = clean_text(text)
    sprint_terms = ["sprint review", "sprint planning", "sprint retro"]
    return any(term in text for term in sprint_terms) 