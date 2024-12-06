import requests
import json

def test_api():
    """Test the API endpoints manually."""
    BASE_URL = "http://localhost:8000/api/v1"
    
    # Test cases
    test_tasks = [
        {
            "title": "Implement login system",
            "description": "Create user authentication with JWT tokens"
        },
        {
            "title": "Design new logo",
            "description": "Create modern minimalist logo for brand"
        },
        {
            "title": "Research cloud providers",
            "description": "Compare AWS, GCP, and Azure services"
        },
        {
            "title": "Weekly team sync",
            "description": "Regular team meeting to discuss progress"
        },
        {
            "title": "Sprint planning",
            "description": "Plan next sprint tasks and priorities"
        }
    ]
    
    print("\nTesting Predictions:")
    print("-" * 50)
    
    for task in test_tasks:
        print(f"\nTesting task: {task['title']}")
        response = requests.post(f"{BASE_URL}/predict", json=task)
        
        if response.status_code == 200:
            result = response.json()
            print(f"Category: {result['category']}")
            print(f"Confidence: {result['confidence']:.2f}")
            print("\nProbabilities:")
            for category, prob in result['probabilities'].items():
                print(f"  {category}: {prob:.2f}")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)

if __name__ == "__main__":
    test_api() 