import json
from collections import Counter
from pathlib import Path

def verify_training_data():
    # Load training data using correct path
    data_path = Path(__file__).parent.parent / 'data' / 'training_data.json'
    
    with open(data_path, 'r') as f:
        data = json.load(f)
    
    # Count categories
    categories = Counter(sample['category'] for sample in data['samples'])
    
    print("\nCategory Distribution:")
    print("-" * 50)
    for category, count in categories.items():
        print(f"{category}: {count} samples")
    
    # Check for minimum samples
    MIN_SAMPLES = 5
    insufficient = [cat for cat, count in categories.items() if count < MIN_SAMPLES]
    if insufficient:
        print(f"\nWarning: Categories with insufficient samples (<{MIN_SAMPLES}):")
        for cat in insufficient:
            print(f"- {cat}")
    else:
        print("\nAll categories have sufficient training samples.")

if __name__ == "__main__":
    verify_training_data() 