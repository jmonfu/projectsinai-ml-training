"""
Predictor

Provides a high-level interface for making task category predictions.
"""

import logging
from typing import Dict, List, Tuple, Optional
import re

logger = logging.getLogger(__name__)

class LocalPredictor:
    def __init__(self):
        # Adjusted confidence thresholds
        self.CONFIDENCE_THRESHOLDS = {
            "VERY_HIGH": 95.0,    # Pure single category, multiple strong matches
            "HIGH": 90.0,         # Single category, strong match
            "MEDIUM_HIGH": 87.0,  # Clear winner with some mixed signals
            "MEDIUM": 85.0,       # Mixed categories, clear winner
            "MEDIUM_LOW": 82.0,   # Mixed categories, moderate competition
            "LOW": 80.0           # Mixed categories, strong competition
        }

        # Weak terms that should significantly reduce confidence
        self.WEAK_TERMS = {
            "sync": -8.0,         # Increased penalty
            "update": -8.0,       # Increased penalty
            "check": -8.0,
            "status": -8.0,
            "general": -8.0,
            "project": -5.0,      # Added penalty for generic terms
            "team": -3.0,
            "quick": -5.0,
            "touch base": -8.0
        }

        # Strong terms that should maintain confidence
        self.STRONG_TERMS = {
            "implementation": 3.0,
            "architecture": 3.0,
            "research findings": 4.0,
            "sprint planning": 4.0,
            "technical design": 4.0,
            "performance analysis": 4.0
        }

        # Minimum word requirements for confidence
        self.MIN_WORDS = {
            "VERY_HIGH": 6,   # Need substantial description
            "HIGH": 4,        # Need decent description
            "MEDIUM": 3       # Minimum for medium confidence
        }

        # Add minimal context penalty
        self.MINIMAL_CONTEXT_TERMS = {
            "sync": -5.0,
            "update": -5.0,
            "status": -5.0,
            "check": -5.0,
            "touch base": -5.0
        }

        # Add strong category combinations that should reduce confidence
        self.STRONG_COMBINATIONS = [
            ("design", "planning", "meeting"),
            ("research", "development", "planning"),
            ("technical", "review", "meeting"),
            ("design", "review", "planning")
        ]

        # Refined category combinations with specific confidence impacts
        self.CATEGORY_COMBINATIONS = {
            ("design", "planning"): -3.0,
            ("design", "meeting"): -4.0,
            ("research", "development"): -3.0,
            ("planning", "meeting"): -2.0,
            ("research", "planning"): -3.0
        }

        # Context strength multipliers
        self.CONTEXT_STRENGTH = {
            "strong": {
                "implementation": 1.5,
                "architecture": 1.5,
                "research findings": 1.5,
                "sprint planning": 1.5
            },
            "weak": {
                "sync": 0.7,
                "update": 0.7,
                "review": 0.7,
                "check": 0.7
            }
        }

        # Refined priority system with sub-categories
        self.category_priority = {
            "Meeting": {
                "priority": 1,
                "context_rules": {
                    "sprint review": "Planning",     # Override to Planning
                    "roadmap review": "Planning",    # Override to Planning
                    "technical review": "Design",    # Override to Design
                    "code review": "Development",    # Override to Development
                    "research presentation": "Research"  # Override to Research
                }
            },
            "Research": {
                "priority": 2,
                "sub_categories": {
                    "performance analysis": 1,
                    "investigation": 2,
                    "evaluation": 3
                }
            },
            "Design": {
                "priority": 3,
                "sub_categories": {
                    "architecture": 1,
                    "system design": 2,
                    "ui/ux": 3
                }
            },
            "Planning": {
                "priority": 4,
                "sub_categories": {
                    "sprint planning": 1,
                    "roadmap": 2,
                    "backlog": 3
                }
            },
            "Development": {
                "priority": 5,
                "sub_categories": {
                    "implementation": 1,
                    "bug fix": 2,
                    "maintenance": 3
                }
            }
        }

        self.keywords = {
            "Development": [
                ("implement", 4.5),
                ("implementation", 4.5),
                ("code", 4.0),
                ("develop", 4.0),
                ("bug fix", 4.0),
                ("fix bug", 4.0),
                ("bug", 3.5),
                ("fix", 3.5),
                ("api", 3.0),
                ("database", 3.0),
                ("deploy", 3.0),
                ("test", 2.5),
                ("debug", 2.5),
                ("optimize", 2.5),
                ("refactor", 2.5),
                ("maintenance", 2.5),
                ("update", 2.0),
                ("configuration", 2.0),
                ("setup", 2.0),
                ("install", 2.0),
                ("build", 2.0),
                ("integration", 2.0),
                ("ci/cd", 2.5)
            ],
            "Design": [
                ("architecture", 4.5),
                ("system architecture", 5.0),
                ("technical design", 5.0),
                ("design system", 4.5),
                ("design", 4.0),
                ("system design", 4.5),
                ("api design", 4.5),
                ("infrastructure", 3.5),
                ("wireframe", 3.0),
                ("mockup", 3.0),
                ("prototype", 2.5),
                ("layout", 2.5),
                ("ui/ux", 4.0),
                ("ui", 2.5),
                ("ux", 2.5),
                ("interface", 2.0),
                ("diagram", 2.0)
            ],
            "Research": [
                ("investigate", 4.5),
                ("investigation", 4.5),
                ("research", 4.0),
                ("analyze", 4.0),
                ("analysis", 4.0),
                ("performance analysis", 4.5),
                ("debug", 3.0),
                ("bottleneck", 2.5),
                ("study", 2.5),
                ("evaluate", 2.5),
                ("evaluation", 2.5),
                ("explore", 2.0),
                ("review", 2.0),
                ("compare", 2.0),
                ("assess", 2.0),
                ("root cause", 3.0),
                ("proof of concept", 3.5),
                ("poc", 3.0)
            ],
            "Meeting": [
                ("team meeting", 4.5),
                ("meeting", 3.5),        # Reduced from 4.5
                ("standup", 3.5),
                ("sync", 3.0),
                ("discussion", 3.0),
                ("review", 1.5),         # Further reduced
                ("team", 1.5),
                ("together", 1.0),
                ("present", 2.0),
                ("demo", 2.0)
            ],
            "Planning": [
                ("sprint review", 4.5),  # Added
                ("roadmap review", 4.5), # Added
                ("sprint planning", 4.5),
                ("planning", 4.0),
                ("roadmap", 3.5),
                ("timeline", 3.0),
                ("backlog", 3.0),
                ("sprint", 2.5),         # Increased
                ("milestone", 2.5)
            ]
        }

        # Compile patterns with word boundaries
        self.patterns = {
            category: [
                (re.compile(rf'\b{re.escape(word)}\b', re.I), weight) 
                for word, weight in keywords
            ]
            for category, keywords in self.keywords.items()
        }
        
        logger.info("LocalPredictor initialized with refined categories and patterns")

        # Add ambiguous terms list
        self.AMBIGUOUS_TERMS = {
            "review": -3.0,
            "discuss": -2.0,
            "status": -2.0,
            "check": -2.0,
            "update": -2.0,
            "current": -1.0,
            "system": -2.0,
            "general": -2.0
        }

        # Add compound terms with higher weights
        self.COMPOUND_TERMS = {
            "Meeting": {
                "code review meeting": 5.0,
                "review meeting": 4.5,
                "team review": 4.0,
                "team discussion": 4.0,
                "team sync": 4.0,
                "standup meeting": 4.5
            },
            "Design": {
                "api design": 4.5,
                "system design": 4.5,
                "architecture design": 4.5,
                "technical design": 4.5
            },
            "Research": {
                "performance analysis": 4.5,
                "technical analysis": 4.0,
                "investigate performance": 4.0
            }
        }

        # Technical term boosters
        self.TECHNICAL_TERMS = {
            "architecture": 2.0,
            "technical": 2.0,
            "implementation": 2.0,
            "performance": 2.0,
            "system": 1.0,
            "infrastructure": 1.5,
            "database": 1.5,
            "api": 1.5
        }

        # Category mixing penalties
        self.CATEGORY_MIXING = {
            ("technical", "review"): -5.0,
            ("architecture", "planning"): -5.0,
            ("api", "planning"): -5.0,
            ("development", "roadmap"): -5.0,
            ("system", "design"): -3.0,
            ("performance", "analysis"): -2.0  # Less penalty for natural combinations
        }

        # Pure category indicators (strong single-category phrases)
        self.PURE_INDICATORS = {
            "Meeting": ["team standup", "weekly sync", "daily standup"],
            "Planning": ["sprint planning", "roadmap planning", "backlog grooming"],
            "Research": ["performance analysis", "technical investigation"],
            "Design": ["system architecture", "technical design"],
            "Development": ["code implementation", "bug fixing"]
        }

        # Natural combinations (less penalty)
        self.NATURAL_COMBINATIONS = {
            ("sprint", "planning"): -2.0,
            ("performance", "analysis"): -2.0,
            ("system", "architecture"): -2.0,
            ("technical", "design"): -2.0
        }

        # Conflicting combinations (higher penalty)
        self.CONFLICTING_COMBINATIONS = {
            ("research", "development"): -5.0,
            ("design", "planning"): -5.0,
            ("technical", "planning"): -5.0,
            ("architecture", "development"): -5.0
        }

    def predict(self, title: str, description: str) -> dict:
        text = f"{title.lower()} {description.lower()}"
        
        # Check for strong combinations first
        for combination in self.STRONG_COMBINATIONS:
            if all(term in text.lower() for term in combination):
                # Determine primary category based on first word in title
                title_words = title.lower().split()
                for word in title_words:
                    for category in self.keywords.keys():
                        if any(kw[0] in word for kw in self.keywords[category]):
                            return {
                                "category": category,
                                "confidence": self.CONFIDENCE_THRESHOLDS["LOW"]
                            }
        
        # Regular prediction logic
        scores, matches = self._calculate_scores(title, description)
        
        # Combine scores
        scores = {
            category: scores.get(category, 0)
            for category in self.keywords.keys()
        }
        
        if not any(scores.values()):
            return self._fallback_prediction(text)
            
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        top_score = sorted_scores[0][1]
        
        # Adjust competitor threshold
        close_competitors = [
            (cat, score) for cat, score in sorted_scores 
            if score >= top_score * 0.85  # More lenient threshol
        ]
        
        if len(close_competitors) > 1:
            logger.info(f"Close competition between: {close_competitors}")
            best_category = self._resolve_competition(close_competitors, text)
            confidence = self._calculate_confidence(
                len(close_competitors),
                matches[best_category],
                top_score,
                text
            )
        else:
            best_category = sorted_scores[0][0]
            confidence = self._calculate_confidence(
                1,
                matches[best_category],
                top_score,
                text
            )
        
        logger.info(f"Scores: {scores}")
        logger.info(f"Matches: {matches}")
        logger.info(f"Selected: {best_category} ({confidence}%)")
        
        return {
            "category": best_category,
            "confidence": round(confidence, 2)
        }

    def _calculate_scores(self, title: str, description: str) -> Tuple[Dict[str, float], Dict[str, List[str]]]:
        scores = {category: 0.0 for category in self.keywords.keys()}
        matches = {category: [] for category in self.keywords.keys()}
        
        title_boost = 2.5
        
        for category, patterns in self.patterns.items():
            for pattern, weight in patterns:
                title_matches = pattern.findall(title.lower())
                desc_matches = pattern.findall(description.lower())
                
                if title_matches:
                    score = weight * len(title_matches) * title_boost
                    scores[category] += score
                    matches[category].extend(title_matches)
                    
                if desc_matches:
                    score = weight * len(desc_matches)
                    scores[category] += score
                    matches[category].extend(desc_matches)
                    
        return scores, matches

    def _resolve_competition(self, competitors: List[Tuple[str, float]], text: str) -> str:
        # First try to resolve using primary category priority
        best_priority = min(
            competitors,
            key=lambda x: self.category_priority[x[0]]["priority"]
        )
        
        # If clear winner by priority, return it
        if len([c for c in competitors if self.category_priority[c[0]]["priority"] == 
                self.category_priority[best_priority[0]]["priority"]]) == 1:
            return best_priority[0]
            
        # If still tied, use sub-categories
        return self._resolve_by_subcategory(
            [c[0] for c in competitors if self.category_priority[c[0]]["priority"] == 
             self.category_priority[best_priority[0]]["priority"]],
            text
        )

    def _resolve_by_subcategory(self, categories: List[str], text: str) -> str:
        # Default to first category if no sub-category matches
        if not categories:
            return categories[0]
            
        best_score = float('inf')
        best_category = categories[0]
        
        for category in categories:
            for sub_cat, priority in self.category_priority[category]["sub_categories"].items():
                if sub_cat in text:
                    if priority < best_score:
                        best_score = priority
                        best_category = category
                        
        return best_category

    def _calculate_confidence(self, num_competitors: int, matches: List[str], score: float, text: str) -> float:
        # Start with base confidence
        base_confidence = self.CONFIDENCE_THRESHOLDS["MEDIUM"]
        
        # Check for pure category indicators
        pure_category = False
        for category, indicators in self.PURE_INDICATORS.items():
            if any(indicator in text.lower() for indicator in indicators):
                base_confidence = self.CONFIDENCE_THRESHOLDS["HIGH"]
                pure_category = True
                break
        
        # Apply natural combination adjustments
        natural_penalty = sum(
            penalty 
            for (term1, term2), penalty in self.NATURAL_COMBINATIONS.items() 
            if term1 in text.lower() and term2 in text.lower()
        )
        
        # Apply conflicting combination penalties
        conflict_penalty = sum(
            penalty 
            for (term1, term2), penalty in self.CONFLICTING_COMBINATIONS.items() 
            if term1 in text.lower() and term2 in text.lower()
        )
        
        # Multiple category penalty
        category_penalty = 0
        if num_competitors > 1:
            category_penalty = (num_competitors - 1) * 3.0
            if pure_category:
                category_penalty *= 0.5  # Reduce penalty for pure categories
        
        # Calculate final confidence
        adjusted_confidence = base_confidence + natural_penalty + conflict_penalty - category_penalty
        
        # Enforce maximum for mixed cases
        if num_competitors > 1:
            adjusted_confidence = min(adjusted_confidence, self.CONFIDENCE_THRESHOLDS["MEDIUM_HIGH"])
        
        # Enforce minimum for pure cases
        if pure_category and conflict_penalty == 0:
            adjusted_confidence = max(adjusted_confidence, self.CONFIDENCE_THRESHOLDS["MEDIUM_HIGH"])
        
        # Final bounds check
        adjusted_confidence = max(
            min(adjusted_confidence, self.CONFIDENCE_THRESHOLDS["VERY_HIGH"]),
            self.CONFIDENCE_THRESHOLDS["LOW"]
        )
        
        return round(adjusted_confidence, 2)

    def _fallback_prediction(self, text: str) -> dict:
        """Fallback logic for when no keywords match."""
        # Common technical words that suggest Development
        technical_words = ['system', 'config', 'setup', 'check', 'verify', 'update']
        if any(word in text for word in technical_words):
            return {
                "category": "Development",
                "confidence": 75.0
            }
            
        # Default fallback
        return {
            "category": "Development",
            "confidence": 70.0
        }

    def _check_compound_terms(self, text: str) -> Dict[str, float]:
        scores = {category: 0.0 for category in self.keywords.keys()}
        
        for category, terms in self.COMPOUND_TERMS.items():
            for term, weight in terms.items():
                if term in text.lower():
                    scores[category] += weight
                    logger.info(f"Found compound term: {term} for {category}")
                    
        return scores

