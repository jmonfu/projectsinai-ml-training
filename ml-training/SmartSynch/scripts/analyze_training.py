import json
import matplotlib.pyplot as plt
from pathlib import Path

def analyze_training_results(model_dir: str):
    """Analyze training results and generate visualizations"""
    history_file = Path(model_dir) / "training_history.json"
    
    with open(history_file, 'r') as f:
        history = json.load(f)
    
    # Plot loss curves
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(history['train_loss'], label='Training Loss')
    plt.plot(history['val_loss'], label='Validation Loss')
    plt.title('Model Loss')
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.legend()
    
    # Plot accuracy curves if available
    if 'train_acc' in history:
        plt.subplot(1, 2, 2)
        plt.plot(history['train_acc'], label='Training Accuracy')
        plt.plot(history['val_acc'], label='Validation Accuracy')
        plt.title('Model Accuracy')
        plt.xlabel('Epoch')
        plt.ylabel('Accuracy')
        plt.legend()
    
    plt.tight_layout()
    plt.savefig(Path(model_dir) / 'training_analysis.png')
    plt.close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, required=True)
    args = parser.parse_args()
    
    analyze_training_results(args.model_dir) 