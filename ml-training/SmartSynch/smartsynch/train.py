from smartsynch.models.predictor import MLPredictor
import json
from pathlib import Path
from collections import Counter
from smartsynch.data.test_cases import TEST_CASES, EDGE_CASES

def get_category_keywords():
    return {
        'bug_fix': [
            'fix', 'debug', 'resolve', 'crash', 'issue', 'problem',
            'error', 'bug', 'defect', 'failure', 'incorrect', 'invalid',
            'memory leak', 'race condition', 'deadlock', 'corruption'
        ],
        'feature': [
            'implement', 'add', 'create', 'new', 'build', 'integrate',
            'support for', 'enable', 'introduce', 'develop'
        ],
        'documentation': [
            'document', 'guide', 'readme', 'docs', 'wiki', 'manual',
            'tutorial', 'reference', 'changelog', 'api docs'
        ],
        'enhancement': [
            'improve', 'optimize', 'enhance', 'upgrade', 'modernize',
            'streamline', 'simplify', 'clean up', 'better', 'update'
        ],
        'security': [
            'security', 'vulnerability', 'auth', 'encryption', 'csrf',
            'xss', 'injection', 'authentication', 'authorization', 'exploit'
        ],
        'performance': [
            'performance', 'speed', 'optimize', 'fast', 'slow',
            'latency', 'memory', 'cpu', 'bottleneck', 'cache'
        ],
        'testing': [
            'test', 'coverage', 'unit test', 'integration test', 'e2e',
            'qa', 'quality', 'assertion', 'validation', 'verify'
        ],
        'ui_ux': [
            'accessibility', 'wcag', 'screen reader', 'keyboard navigation',
            'user interface', 'ux', 'ui', 'usability', 'user experience',
            'design system', 'component library', 'animation'
        ],
        'devops': [
            'deploy', 'ci/cd', 'pipeline', 'docker', 'kubernetes',
            'infrastructure', 'monitoring', 'logging', 'automation'
        ],
        'development': [
            'refactor', 'architecture', 'codebase', 'framework',
            'api', 'backend', 'frontend', 'database', 'service'
        ],
        'design': [
            'design', 'mockup', 'prototype', 'wireframe', 'layout',
            'visual', 'brand', 'style guide', 'theme', 'color scheme'
        ],
        'research': [
            'research', 'investigate', 'analyze', 'study', 'evaluate',
            'assess', 'explore', 'feasibility', 'proof of concept'
        ],
        'meeting': [
            'meeting', 'sync', 'discussion', 'review', 'planning',
            'workshop', 'session', 'standup', 'retrospective'
        ],
        'planning': [
            'plan', 'roadmap', 'strategy', 'timeline', 'milestone',
            'schedule', 'estimate', 'scope', 'requirements'
        ],
        'other': [
            'misc', 'general', 'various', 'other', 'maintenance',
            'cleanup', 'housekeeping', 'setup', 'configuration'
        ]
    }

def get_training_weights():
    return {
        'bug_fix': 1.3,      # Critical importance
        'feature': 1.1,      # Reduced to prevent overcategorization
        'documentation': 1.1,
        'enhancement': 1.1,   # Reduced to prevent overlap
        'security': 1.3,     # Critical importance
        'performance': 1.2,
        'testing': 1.1,
        'ui_ux': 1.4,        # Increased to improve UI/UX detection
        'devops': 1.2,
        'development': 1.2,
        'design': 1.3,       # Increased for better design task detection
        'research': 1.1,
        'meeting': 1.0,
        'planning': 1.1,
        'other': 1.0
    }

def preprocess_text(title, description):
    """Enhanced text preprocessing with keyword matching"""
    keywords = get_category_keywords()
    combined_text = f"{title.lower()} {description.lower()}"
    
    # Calculate keyword matches
    category_scores = {}
    for category, words in keywords.items():
        score = sum(1 for word in words if word in combined_text)
        category_scores[category] = score
    
    return combined_text, category_scores

def get_training_data():
    """Get example training data"""
    data_path = Path(__file__).parent / "data" / "training_data.json"
    with open(data_path) as f:
        categories = json.load(f)
    
    # Add weights for all categories from TASK_CATEGORIES
    category_weights = get_training_weights()
    
    # Flatten the data while applying weights
    training_data = []
    labels = []
    for category, examples in categories.items():
        weight = category_weights.get(category, 1.0)
        # Duplicate examples for weighted categories
        num_copies = int(len(examples) * weight)
        for _ in range(num_copies):
            for example in examples:
                title, desc = example
                training_data.append((title, desc))
                labels.append(category)
    
    # Debug print
    category_counts = Counter(labels)
    print(f"Number of examples per category (after weighting):")
    print(category_counts)
    
    return training_data, labels

def main():
    # Create and train predictor
    predictor = MLPredictor()
    training_data, labels = get_training_data()
    
    # Print dataset statistics
    print("\nTraining Data Statistics:")
    print("-" * 50)
    category_counts = Counter(labels)
    for category, count in sorted(category_counts.items()):
        print(f"{category}: {count} examples")
    print("-" * 50)
    
    # Train the model
    print("\nTraining model...")
    predictor.train(training_data)  # Pass only the training data tuples
    
    # Test both standard and edge cases
    test_cases = TEST_CASES + EDGE_CASES
    print("\nTesting all cases:")
    print("-" * 50)
    
    results = []
    for title, desc in test_cases:
        result = predictor.predict(title, desc)
        results.append(result)
        print(f"\nInput: {title} - {desc}")
        print(f"Prediction: {result['category']} ({result['confidence']:.1f}%)")
    
    # Analyze results
    print("\nPrediction Analysis:")
    print("-" * 50)
    confidence_by_category = {}
    for result in results:
        category = result['category']
        confidence = result['confidence']
        if category not in confidence_by_category:
            confidence_by_category[category] = []
        confidence_by_category[category].append(confidence)
    
    for category, confidences in confidence_by_category.items():
        avg_confidence = sum(confidences) / len(confidences)
        print(f"{category}: Average confidence {avg_confidence:.1f}%")
    
    # Save the model
    print("\nSaving model...")
    predictor.save_model("models/task_classifier.joblib")
    print("Done!")

if __name__ == "__main__":
    main() 