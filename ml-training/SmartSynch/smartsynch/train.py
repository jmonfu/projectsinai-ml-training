from smartsynch.models.predictor import MLPredictor
import json
from pathlib import Path
from collections import Counter
from smartsynch.data.test_cases import TEST_CASES, EDGE_CASES

def get_training_data():
    """Get example training data"""
    data_path = Path(__file__).parent / "data" / "training_data.json"
    with open(data_path) as f:
        categories = json.load(f)
    
    # Flatten the data while preserving category information
    training_data = []
    labels = []
    for category, examples in categories.items():
        training_data.extend(examples)
        labels.extend([category] * len(examples))
    
    # Debug print
    print(f"Number of examples per category:")
    print(Counter(labels))
    
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
    print(f"Sample training data item: {training_data[0]}")
    print(f"Sample label: {labels[0]}")
    
    # Extract just the title and description pairs from training_data
    combined_data = [(title, desc) 
                    for [title, desc] in training_data]
    predictor.train(combined_data)
    
    # Test standard cases
    print("\nTesting standard cases:")
    print("-" * 50)
    for title, desc in TEST_CASES:
        result = predictor.predict(title, desc)
        print(f"\nInput: {title} - {desc}")
        print(f"Prediction: {result['category']} ({result['confidence']:.1f}%)")

    # Test edge cases
    print("\nTesting edge cases:")
    print("-" * 50)
    for title, desc in EDGE_CASES:
        result = predictor.predict(title, desc)
        print(f"\nInput: {title} - {desc}")
        print(f"Prediction: {result['category']} ({result['confidence']:.1f}%)")

    # Save the model
    print("\nSaving model...")
    predictor.save_model("models/task_classifier.joblib")
    print("Done!")

if __name__ == "__main__":
    main() 