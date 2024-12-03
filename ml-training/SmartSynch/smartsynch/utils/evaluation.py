"""
Evaluation Metrics

Provides metrics for model evaluation including:
- Accuracy, Precision, Recall, F1
- Confusion Matrix
- Cross-validation scores
"""

from typing import List, Dict, Tuple
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    confusion_matrix, classification_report
)
import matplotlib.pyplot as plt
import seaborn as sns

class ModelEvaluator:
    def __init__(self, category_map: Dict[str, int]):
        """
        Initialize evaluator with category mapping.
        
        Args:
            category_map: Dictionary mapping category names to indices
        """
        self.category_map = category_map
        self.categories = list(category_map.keys())

    def compute_basic_metrics(
        self, y_true: List[int], y_pred: List[int]
    ) -> Dict[str, float]:
        """
        Compute basic classification metrics.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            
        Returns:
            Dictionary of metrics
        """
        accuracy = accuracy_score(y_true, y_pred)
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='weighted'
        )
        
        return {
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }

    def compute_confusion_matrix(
        self, y_true: List[int], y_pred: List[int]
    ) -> np.ndarray:
        """
        Compute confusion matrix.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            
        Returns:
            Confusion matrix array
        """
        return confusion_matrix(y_true, y_pred)

    def plot_confusion_matrix(
        self, y_true: List[int], y_pred: List[int], 
        output_path: str = None
    ):
        """
        Plot confusion matrix heatmap.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            output_path: Path to save plot (optional)
        """
        cm = self.compute_confusion_matrix(y_true, y_pred)
        
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            cm, 
            annot=True, 
            fmt='d',
            xticklabels=self.categories,
            yticklabels=self.categories
        )
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        
        if output_path:
            plt.savefig(output_path)
            plt.close()
        else:
            plt.show()

    def generate_classification_report(
        self, y_true: List[int], y_pred: List[int]
    ) -> Dict:
        """
        Generate detailed classification report.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            
        Returns:
            Dictionary containing detailed metrics
        """
        report = classification_report(
            y_true, y_pred,
            target_names=self.categories,
            output_dict=True
        )
        return report

    def evaluate_model(
        self, y_true: List[int], y_pred: List[int], 
        confidences: List[float]
    ) -> Dict:
        """
        Comprehensive model evaluation.
        
        Args:
            y_true: True labels
            y_pred: Predicted labels
            confidences: Prediction confidences
            
        Returns:
            Dictionary containing all evaluation metrics
        """
        basic_metrics = self.compute_basic_metrics(y_true, y_pred)
        detailed_report = self.generate_classification_report(y_true, y_pred)
        
        # Confidence analysis
        confidence_metrics = {
            "mean_confidence": np.mean(confidences),
            "min_confidence": np.min(confidences),
            "max_confidence": np.max(confidences)
        }
        
        return {
            "basic_metrics": basic_metrics,
            "detailed_metrics": detailed_report,
            "confidence_metrics": confidence_metrics
        } 