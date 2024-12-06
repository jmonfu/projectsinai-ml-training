from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

class SimpleTaskClassifier:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        
        # Enhanced patterns with stronger design recognition
        self.patterns = {
            "Design": {
                "primary": [
                    r"\b(design)\b.*\b(screen|interface|layout|page)\b",
                    r"\b(create|update|improve)\b.*\b(ui|ux|design)\b",
                    r"\b(mockup|wireframe|prototype)\b",
                    r"\b(design)\b.*\b(new|brand|login)\b",  # Added pattern
                    r"\b(visual|interface)\b.*\b(design|creation)\b"  # Added pattern
                ],
                "context": [
                    r"\b(visual|creative|user|interface)\b",
                    r"\b(responsive|interactive|aesthetic)\b",
                    r"\b(brand|style|theme)\b",  # Added context
                    r"\b(material|component|element)\b"  # Added context
                ],
                "weight": 1.4  # Increased weight for design
            },
            "Development": {
                "primary": [
                    r"\b(implement|develop|code|build|program)\b",
                    r"\b(api|backend|database|logging|testing)\b",
                    r"\b(debug|deploy|fix|integrate)\b"
                ],
                "context": [
                    r"\b(feature|system|application|service)\b",
                    r"\b(technical|software|engineering)\b"
                ],
                "weight": 1.2
            },
            "Meeting": {
                "primary": [
                    r"\b(meet|meeting|discuss|sync)\b.*\b(with|team|client)\b",
                    r"\b(call|review|standup)\b",
                    r"\b(present|presentation)\b"
                ],
                "context": [
                    r"\b(schedule|discuss|review)\b",
                    r"\b(team|client|group)\b"
                ],
                "weight": 1.0
            },
            "Research": {
                "primary": [
                    r"\b(research|investigate|analyze|study)\b",
                    r"\b(evaluate|assess|compare)\b",
                    r"\b(explore|review)\b.*\b(options|alternatives)\b"
                ],
                "context": [
                    r"\b(analysis|evaluation|investigation)\b",
                    r"\b(performance|efficiency|effectiveness)\b"
                ],
                "weight": 1.0
            },
            "Planning": {
                "primary": [
                    r"\b(plan|schedule|organize)\b",
                    r"\b(create|define)\b.*\b(roadmap|timeline)\b",
                    r"\b(estimate|coordinate)\b"
                ],
                "context": [
                    r"\b(strategy|timeline|milestone)\b",
                    r"\b(project|sprint|release)\b"
                ],
                "weight": 1.0
            }
        }
        
        # Pre-compute embeddings for each category
        self.embeddings = {}
        for category, patterns in self.patterns.items():
            # Create representative text for category
            text = " ".join([
                p.replace(r"\b", "").replace(r"|", " ")
                for p in patterns["primary"] + patterns["context"]
            ])
            self.embeddings[category] = self.encoder.encode(text.lower())

    def _get_pattern_score(self, text: str, category: str) -> float:
        """Calculate pattern match score with context."""
        text = text.lower()
        
        # Check primary patterns (higher weight)
        primary_matches = sum(
            len(re.findall(pattern, text))
            for pattern in self.patterns[category]["primary"]
        ) * 0.6
        
        # Check context patterns (lower weight)
        context_matches = sum(
            len(re.findall(pattern, text))
            for pattern in self.patterns[category]["context"]
        ) * 0.3
        
        return min(primary_matches + context_matches, 1.0)

    def predict(self, title: str, description: str = None) -> dict:
        # Prepare input text with stronger title emphasis
        input_text = f"{title} {title} {title}"  # Triple weight on title
        if description:
            input_text = f"{input_text} {description}"
            
        # Get scores
        pattern_scores = {
            category: self._get_pattern_score(input_text, category) * self.patterns[category]["weight"]
            for category in self.patterns.keys()
        }
        
        embedding_scores = {
            category: float(cosine_similarity([self.encoder.encode(input_text.lower())], 
                                           [self.embeddings[category]])[0][0])
            for category in self.patterns.keys()
        }
        
        # Combine scores with higher pattern weight for design
        combined_scores = {}
        for category in self.patterns.keys():
            if category == "Design":
                # Higher pattern weight for design category
                combined_scores[category] = (0.9 * pattern_scores[category] + 
                                          0.1 * embedding_scores[category])
            else:
                # Normal weights for other categories
                combined_scores[category] = (0.8 * pattern_scores[category] + 
                                          0.2 * embedding_scores[category])
        
        # Sharper probability calculation
        max_score = max(combined_scores.values())
        exp_scores = {
            k: np.exp((v - max_score) * 4)  # Increased temperature scaling
            for k, v in combined_scores.items()
        }
        
        total = sum(exp_scores.values())
        probabilities = {
            k: float(v / total)
            for k, v in exp_scores.items()
        }
        
        best_category = max(probabilities.items(), key=lambda x: x[1])
        
        return {
            "category": best_category[0],
            "confidence": best_category[1],
            "probabilities": probabilities
        }
