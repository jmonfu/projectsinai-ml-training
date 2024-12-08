from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
import joblib
import numpy as np
from typing import Dict, List, Tuple
import os
from pathlib import Path

class MLPredictor:
    def __init__(self):
        os.makedirs("models", exist_ok=True)
        self.model_path = "models/task_classifier.joblib"
        
        # Highly refined category weights based on priority and impact
        self.category_weights = {
            "Development": 1.0,    # Base weight for standard development
            "Bug_Fix": 1.2,        # Higher priority for issues
            "Feature": 1.0,
            "Documentation": 0.8,
            "Enhancement": 0.9,
            "Security": 1.4,       # Highest priority for security
            "Performance": 1.3,    # High priority for user experience
            "Testing": 1.1,        # Increased for quality assurance
            "UI_UX": 1.0,
            "DevOps": 1.3,        # High priority for infrastructure
            "Design": 0.9,
            "Research": 0.8,
            "Meeting": 0.6,
            "Planning": 0.7,
            "Other": 0.5
        }
        
        # Expanded confidence thresholds with granular levels
        self.confidence_thresholds = {
            "high": 92.0,          # Very confident prediction
            "medium_high": 88.0,   # Good confidence
            "medium": 85.0,        # Acceptable confidence
            "low": 80.0,           # Requires review
            "mixed": 75.0,         # Multiple categories
            "uncertain": 70.0      # Needs human verification
        }
        
        # Enhanced ML pipeline with better feature extraction
        self.pipeline = Pipeline([
            ('vectorizer', TfidfVectorizer(
                max_features=3000,  # Increased for more categories
                ngram_range=(1, 3),  # Include trigrams
                min_df=2,
                stop_words='english'
            )),
            ('classifier', SGDClassifier(
                loss='modified_huber',
                alpha=1e-4,
                max_iter=1000,
                tol=1e-3,
                random_state=42,
                class_weight='balanced'
            ))
        ])

        # Comprehensive category keywords with technical specificity
        self.category_keywords = {
            'Bug_Fix': {
                'primary': ['fix', 'bug', 'issue', 'crash', 'error'],
                'secondary': ['debug', 'resolve', 'patch']
            },
            'Feature': {
                'primary': ['feature', 'add', 'new', 'implement'],
                'secondary': ['create', 'enable', 'support']
            },
            'Documentation': {
                'primary': ['document', 'docs', 'guide', 'readme'],
                'secondary': ['write', 'update', 'explain']
            },
            'Enhancement': {
                'primary': ['improve', 'enhance', 'optimize', 'refactor'],
                'secondary': ['clean', 'better', 'upgrade']
            },
            'Security': {
                'primary': ['security', 'vulnerability', 'auth', 'protect', 'encrypt', 'hack', 'breach'],
                'secondary': ['pentest', 'csrf', 'xss', 'injection', 'token', 'access']
            },
            'Performance': {
                'primary': ['performance', 'optimize', 'slow', 'fast', 'speed', 'latency', 'memory', 'cpu', 'load'],
                'secondary': ['cache', 'index', 'query', 'response', 'time', 'bottleneck']
            },
            'Testing': {
                'primary': ['test', 'coverage', 'unit test', 'e2e'],
                'secondary': ['verify', 'validate', 'check']
            },
            'UI_UX': {
                'primary': ['ui', 'ux', 'interface', 'usability'],
                'secondary': ['design', 'layout', 'visual']
            },
            'DevOps': {
                'primary': ['pipeline', 'deploy', 'ci/cd', 'docker', 'kubernetes', 'k8s', 'aws', 'cloud'],
                'secondary': ['terraform', 'infrastructure', 'container', 'orchestration', 'monitoring']
            },
            'Development': {
                'primary': ['develop', 'code', 'implement', 'program'],
                'secondary': ['build', 'create', 'setup']
            },
            'Design': {
                'primary': ['design', 'wireframe', 'mockup', 'prototype'],
                'secondary': ['sketch', 'layout', 'visual']
            },
            'Research': {
                'primary': ['research', 'investigate', 'analyze', 'evaluate'],
                'secondary': ['study', 'compare', 'assess']
            },
            'Meeting': {
                'primary': ['meeting', 'sync', 'standup', 'review'],
                'secondary': ['discuss', 'call', 'session']
            },
            'Planning': {
                'primary': ['plan', 'roadmap', 'strategy', 'schedule'],
                'secondary': ['organize', 'coordinate', 'prepare']
            },
            'Other': {
                'primary': ['misc', 'general', 'other'],
                'secondary': ['various', 'additional']
            },
            "Performance": {
                "primary": [
                    "performance", "optimize", "slow", "fast", "speed", 
                    "latency", "memory", "cpu", "load", "throughput",
                    "bottleneck", "response time", "resource usage"
                ],
                "secondary": [
                    "cache", "index", "query", "response", "time",
                    "concurrent", "parallel", "async", "batch",
                    "throttle", "buffer", "pool", "queue"
                ],
                "technical": [
                    "n+1", "lazy loading", "connection pooling",
                    "dead locks", "race condition", "memory leak",
                    "garbage collection", "thread pool", "event loop"
                ]
            },
            "Security": {
                "primary": [
                    "security", "vulnerability", "auth", "protect",
                    "encrypt", "hack", "breach", "exploit", "threat"
                ],
                "secondary": [
                    "pentest", "csrf", "xss", "injection", "token",
                    "access", "permission", "role", "privilege"
                ],
                "technical": [
                    "oauth", "jwt", "ssl", "tls", "cipher",
                    "hash", "salt", "mitm", "zero-day", "cve",
                    "audit log", "rate limit", "firewall"
                ]
            },
            "DevOps": {
                "primary": [
                    "pipeline", "deploy", "ci/cd", "docker", "kubernetes",
                    "k8s", "aws", "cloud", "infrastructure"
                ],
                "secondary": [
                    "terraform", "container", "orchestration",
                    "monitoring", "logging", "scaling", "provision"
                ],
                "technical": [
                    "helm", "prometheus", "grafana", "istio",
                    "jenkins", "gitlab", "argocd", "ansible",
                    "eks", "gke", "aks", "pod", "node", "cluster"
                ]
            },
            "Testing": {
                "primary": [
                    "test", "coverage", "unit test", "e2e",
                    "integration", "automation", "qa"
                ],
                "secondary": [
                    "verify", "validate", "assert", "mock",
                    "stub", "fixture", "harness"
                ],
                "technical": [
                    "jest", "cypress", "selenium", "junit",
                    "pytest", "mocha", "karma", "jasmine",
                    "cucumber", "behave", "gherkin"
                ]
            }
        }

        # Add technical complexity levels
        self.complexity_levels = {
            "high": 1.2,    # Complex technical tasks
            "medium": 1.0,  # Standard tasks
            "low": 0.8     # Simple tasks
        }
        
        # Add category combinations with weighted relationships
        self.category_relationships = {
            "Performance": {
                "Development": 0.8,
                "DevOps": 0.7,
                "Security": 0.6
            },
            "Security": {
                "Development": 0.7,
                "DevOps": 0.8,
                "Performance": 0.6
            },
            "DevOps": {
                "Security": 0.8,
                "Performance": 0.7,
                "Development": 0.6
            }
        }
        
        # Add technical stack keywords
        self.tech_stack_keywords = {
            "Frontend": [
                "react", "vue", "angular", "webpack", "babel",
                "css", "sass", "less", "styled-components"
            ],
            "Backend": [
                "node", "python", "java", "go", "rust",
                "django", "flask", "spring", "express"
            ],
            "Database": [
                "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
                "cassandra", "dynamodb", "oracle"
            ],
            "Cloud": [
                "aws", "gcp", "azure", "kubernetes", "docker",
                "lambda", "ec2", "s3", "cloudfront"
            ]
        }

    def load_model(self) -> None:
        """Load the trained model if it exists"""
        if os.path.exists(self.model_path):
            self.pipeline = joblib.load(self.model_path)
        else:
            raise FileNotFoundError("No trained model found. Please run training first.")

    def _determine_category(self, title: str, description: str) -> str:
        """Determine category with improved accuracy"""
        text = f"{title.lower()} {description.lower()}"
        scores = {}
        
        # Calculate scores for each category
        for category in self.category_keywords:
            category_score = 0
            
            # Primary keywords (highest weight)
            primary_matches = sum(1 for k in self.category_keywords[category]["primary"] 
                                if k in text)
            category_score += primary_matches * 4  # Increased from 3
            
            # Secondary keywords
            secondary_matches = sum(1 for k in self.category_keywords[category]["secondary"] 
                                  if k in text)
            category_score += secondary_matches * 2
            
            # Apply category-specific rules
            if category == "Bug_Fix" and ("fix" in text or "error" in text or "bug" in text):
                category_score += 4
            
            if category == "Feature" and ("add" in text or "create" in text or "implement" in text):
                category_score += 3
            
            if category == "Security" and ("security" in text or "auth" in text or "protect" in text):
                category_score += 4
            
            scores[category] = category_score
        
        # Special case handling with higher weights
        if "optimize" in text or "performance" in text:
            scores["Performance"] = scores.get("Performance", 0) + 4
        
        if "security" in text or "audit" in text:
            scores["Security"] = scores.get("Security", 0) + 4
        
        if "doc" in text or "guide" in text:
            scores["Documentation"] = scores.get("Documentation", 0) + 4
        
        if "test" in text:
            scores["Testing"] = scores.get("Testing", 0) + 4
        
        # Fix common misclassifications
        if "fix" in text and scores.get("Bug_Fix", 0) == 0:
            scores["Bug_Fix"] = scores.get("Bug_Fix", 0) + 3
        
        if "api" in text and "doc" not in text:
            scores["Development"] = scores.get("Development", 0) + 2
        
        # Get category with highest score
        max_score = max(scores.values())
        if max_score == 0:
            return "Development"  # Default category
        
        # Return the category with highest score
        return max(scores.items(), key=lambda x: x[1])[0]

    def train(self, training_data: List[Tuple[str, str]]) -> None:
        """Train the model with example data including edge cases"""
        texts = []
        labels = []
        
        # Add edge cases to training data
        edge_cases = [
            ("", "Empty title test"),
            ("No description", ""),
            ("Quick sync", "Very short"),
            ("Design and Development of API", "Mixed category example"),
            ("Research spike for new feature", "Mixed research and development"),
            ("Planning meeting for architecture", "Mixed planning and meeting"),
        ]
        training_data.extend(edge_cases)
        
        # Prepare training data with proper labels
        for title, desc in training_data:
            texts.append(f"{title} {desc}")
            # Get both keyword-based and ML predictions
            category = self._determine_category(title or "", desc or "")
            labels.append(category)
        
        # Train the pipeline with class weights
        self.pipeline.fit(texts, labels)
        
        # Save the trained pipeline
        joblib.dump(self.pipeline, self.model_path)
        print(f"Model trained with {len(texts)} examples")

    def _calculate_confidence_score(self, text: str, category: str) -> float:
        """Calculate confidence score with improved weighting"""
        text = text.lower()
        score = 70.0  # Base confidence
        
        # Primary keyword matches (worth 5 points each)
        if category in self.category_keywords:
            primary_matches = sum(1 for k in self.category_keywords[category]["primary"] 
                                if k in text)
            score += primary_matches * 5.0
            
            # Secondary keyword matches (worth 3 points each)
            secondary_matches = sum(1 for k in self.category_keywords[category]["secondary"] 
                                  if k in text)
            score += secondary_matches * 3.0
            
            # Technical keyword matches (worth 4 points each)
            if "technical" in self.category_keywords[category]:
                technical_matches = sum(1 for k in self.category_keywords[category]["technical"] 
                                      if k in text)
                score += technical_matches * 4.0
        
        # Adjust for technical complexity
        complexity_score = self._assess_technical_complexity(text)
        score += complexity_score * 5.0
        
        # Adjust for category relationships
        relationship_score = self._calculate_relationship_score(text, category)
        score += relationship_score * 5.0
        
        return min(95.0, score)  # Cap at 95%

    def _assess_technical_complexity(self, text: str) -> float:
        """Assess the technical complexity of the task"""
        text = text.lower()
        complexity_score = 0.0
        
        # Check for technical terms across different stacks
        for stack, keywords in self.tech_stack_keywords.items():
            matches = sum(1 for k in keywords if k in text)
            if matches > 0:
                complexity_score += 0.2
        
        # Check for architecture terms
        architecture_terms = [
            "microservices", "distributed", "scalable", "redundant",
            "fault-tolerant", "high-availability", "load-balanced"
        ]
        if any(term in text for term in architecture_terms):
            complexity_score += 0.3
        
        return min(1.0, complexity_score)

    def _calculate_relationship_score(self, text: str, category: str) -> float:
        """Calculate score based on category relationships"""
        text = text.lower()
        score = 0.0
        
        if category in self.category_relationships:
            for related_category, weight in self.category_relationships[category].items():
                if any(k in text for k in self.category_keywords[related_category]["primary"]):
                    score += weight
        
        return min(1.0, score)

    def predict(self, title: str, description: str) -> Dict[str, any]:
        """Enhanced prediction with technical analysis"""
        text = f"{title} {description}".lower()
        
        # Get base prediction using keyword matching
        category = self._determine_category(title, description)
        
        # Calculate confidence
        confidence = self._calculate_confidence_score(text, category)
        
        # Check for technical complexity
        complexity = self._assess_technical_complexity(text)
        
        # Get related categories
        related = self._get_related_categories(text, category)
        
        return {
            "category": category,
            "confidence": confidence,
            "technical_complexity": complexity,
            "related_categories": related
        }

    def _get_related_categories(self, text: str, primary_category: str) -> List[str]:
        """Get related categories based on text analysis"""
        related = []
        
        if primary_category in self.category_relationships:
            for category, weight in self.category_relationships[primary_category].items():
                if any(k in text for k in self.category_keywords[category]["primary"]):
                    related.append(category)
        
        return related[:2]  # Return top 2 related categories

    def _check_mixed_categories(self, text: str) -> float:
        """Check text for mixed category indicators"""
        text = text.lower()
        score = 0.0
        
        # Check for explicit mixed category terms
        for combo, keywords in self.category_keywords['Mixed'].items():
            if any(k in text for k in keywords):
                score += 0.4  # Strong indicator of mixed category
        
        # Check for multiple category indicators
        categories_found = set()
        for category, terms in self.category_keywords.items():
            if category != 'Mixed':
                primary_matches = sum(1 for k in terms['primary'] if k in text)
                secondary_matches = sum(1 for k in terms['secondary'] if k in text)
                if primary_matches > 0 or secondary_matches > 1:
                    categories_found.add(category)
        
        if len(categories_found) > 1:
            score += 0.3  # Multiple categories detected
            
        return min(1.0, score)  # Cap at 1.0

    def _get_keyword_scores(self, text: str) -> Dict[str, float]:
        """Calculate keyword-based scores for each category"""
        scores = {}
        text = text.lower()
        
        for category, keywords in self.category_keywords.items():
            score = sum(2 if keyword in text.split() else 1 
                       for keyword in keywords if keyword in text)
            scores[category] = score / max(len(keywords), 1)  # Normalize score
            
        # Normalize all scores to [0,1]
        max_score = max(scores.values()) if scores else 1
        return {cat: score/max_score for cat, score in scores.items()}

    def batch_predict(self, tasks: List[Tuple[str, str]]) -> List[Dict[str, float]]:
        """Batch prediction for multiple tasks"""
        texts = [f"{title} {desc}" for title, desc in tasks]
        predictions = self.pipeline.predict(texts)
        probabilities = self.pipeline.predict_proba(texts)
        
        return [
            {
                "category": pred,
                "confidence": float(np.max(prob) * 100)
            }
            for pred, prob in zip(predictions, probabilities)
        ]

    def _get_top_categories(self, text: str) -> Tuple[str, str]:
        """Get the top two categories based on keyword matches"""
        scores = {}
        text = text.lower()
        
        # Calculate scores for each category
        for category, terms in self.category_keywords.items():
            if category != 'Mixed':
                primary_score = sum(2 for k in terms['primary'] if k in text)
                secondary_score = sum(1 for k in terms['secondary'] if k in text)
                scores[category] = primary_score + secondary_score
        
        # Get top two categories
        sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return sorted_categories[0][0], sorted_categories[1][0]

    def _get_keyword_matches(self, text: str) -> Dict[str, int]:
        """Count keyword matches for each category"""
        matches = {}
        text = text.lower()
        
        for category, terms in self.category_keywords.items():
            if category != 'Mixed':
                primary_matches = sum(1 for k in terms['primary'] if k in text)
                secondary_matches = sum(1 for k in terms['secondary'] if k in text)
                matches[category] = {
                    "primary": primary_matches,
                    "secondary": secondary_matches,
                    "total": primary_matches + secondary_matches
                }
        
        return matches

    def _calculate_keyword_score(self, text: str, category: str) -> float:
        """Calculate weighted keyword score"""
        text = text.lower()
        score = 0.0
        
        if category in self.category_keywords:
            keywords = self.category_keywords[category]
            
            # Primary keywords (strongest)
            if 'primary' in keywords:
                score += sum(2.0 for k in keywords['primary'] if k in text)
            
            # Secondary keywords (medium)
            if 'secondary' in keywords:
                score += sum(1.0 for k in keywords['secondary'] if k in text)
            
            # Weak keywords (lowest) - only present in some categories
            if 'weak' in keywords:
                score += sum(0.5 for k in keywords['weak'] if k in text)
            
        return score

    def save_model(self, filepath: str) -> None:
        """Save the trained pipeline to a file"""
        # Create the directory if it doesn't exist
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        # Save the pipeline instead of model
        joblib.dump(self.pipeline, filepath)

