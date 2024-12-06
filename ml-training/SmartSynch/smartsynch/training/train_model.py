import json
import torch
from sentence_transformers import SentenceTransformer
from datetime import datetime
import os
from pathlib import Path

def load_training_data():
    with open('data/training_data.json', 'r') as f:
        return json.load(f)

def train_model():
    print("Loading training data...")
    data = load_training_data()
    
    print("Initializing sentence transformer...")
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Prepare texts by combining title and description
    texts = []
    labels = []
    categories = sorted(list(set(sample['category'] for sample in data['samples'])))
    category_to_idx = {cat: idx for idx, cat in enumerate(categories)}
    
    print(f"Found categories: {categories}")
    
    for sample in data['samples']:
        text = f"{sample['title']} - {sample['description']}"
        texts.append(text)
        labels.append(category_to_idx[sample['category']])
    
    print("Generating embeddings...")
    embeddings = embedding_model.encode(texts, convert_to_tensor=True)
    
    # Create and train classifier
    classifier = torch.nn.Sequential(
        torch.nn.Linear(embeddings.shape[1], 128),
        torch.nn.ReLU(),
        torch.nn.Dropout(0.2),
        torch.nn.Linear(128, len(categories))
    )
    
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(classifier.parameters(), lr=0.001)
    
    print("Training classifier...")
    num_epochs = 100
    for epoch in range(num_epochs):
        optimizer.zero_grad()
        outputs = classifier(embeddings)
        loss = criterion(outputs, torch.tensor(labels))
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 20 == 0:
            print(f"Epoch {epoch+1}/{num_epochs}, Loss: {loss.item():.4f}")
    
    # Save model
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_dir = Path(f'models/fine_tuned/{timestamp}')
    save_dir.mkdir(parents=True, exist_ok=True)
    
    model_data = {
        'classifier_state': classifier.state_dict(),
        'categories': categories,
        'category_to_idx': category_to_idx,
        'embedding_model': 'all-MiniLM-L6-v2'
    }
    
    model_path = save_dir / 'model.pt'
    torch.save(model_data, model_path)
    print(f"\nModel saved to: {model_path}")
    
    # Update prediction service path
    prediction_file = Path('smartsynch/api/routes/prediction.py')
    if prediction_file.exists():
        content = prediction_file.read_text()
        updated_content = content.replace(
            "model_path = 'models/fine_tuned/20241128_134706/model.pt'",
            f"model_path = 'models/fine_tuned/{timestamp}/model.pt'"
        )
        prediction_file.write_text(updated_content)
        print(f"Updated model path in prediction.py")

if __name__ == "__main__":
    train_model() 