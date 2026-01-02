"""
SignSpeak - Model Evaluation Utilities
Comprehensive model evaluation and metrics
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import sys
from sklearn.metrics import (
    accuracy_score, confusion_matrix, classification_report,
    precision_recall_fscore_support
)

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.config import ML_MODELS_PATH, ML_DATASET_PATH

def evaluate_model(model_path: Path = None, dataset_path: Path = None):
    """
    Comprehensive model evaluation
    
    Args:
        model_path: Path to model file
        dataset_path: Path to dataset directory
    """
    if model_path is None:
        model_path = ML_MODELS_PATH / "gesture_model.pkl"
    
    if dataset_path is None:
        dataset_path = ML_DATASET_PATH
    
    # Load model
    print("📦 Loading model...")
    model = joblib.load(model_path)
    label_encoder = joblib.load(ML_MODELS_PATH / "label_encoder.pkl")
    
    # Load dataset
    print("📂 Loading dataset...")
    dataframes = []
    for file in dataset_path.glob("*_dynamic.csv"):
        df = pd.read_csv(file)
        dataframes.append(df)
    
    if not dataframes:
        print("❌ No dataset files found!")
        return
    
    data = pd.concat(dataframes, ignore_index=True)
    
    # Prepare data
    X = data.drop("label", axis=1)
    y = data["label"]
    y_encoded = label_encoder.transform(y)
    
    # Predictions
    print("🔮 Making predictions...")
    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)
    
    # Metrics
    accuracy = accuracy_score(y_encoded, y_pred)
    precision, recall, f1, support = precision_recall_fscore_support(
        y_encoded, y_pred, average=None, zero_division=0
    )
    
    print("\n" + "=" * 60)
    print("MODEL EVALUATION RESULTS")
    print("=" * 60)
    print(f"\n📊 Overall Accuracy: {accuracy * 100:.2f}%")
    print(f"\n📈 Per-Class Metrics:")
    print(f"{'Gesture':<15} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Support':<10}")
    print("-" * 60)
    
    for i, gesture in enumerate(label_encoder.classes_):
        print(f"{gesture:<15} {precision[i]:<12.3f} {recall[i]:<12.3f} {f1[i]:<12.3f} {support[i]:<10}")
    
    # Confusion Matrix
    cm = confusion_matrix(y_encoded, y_pred)
    print(f"\n📋 Confusion Matrix:")
    print(cm)
    
    # Classification Report
    print(f"\n📄 Detailed Classification Report:")
    print(classification_report(y_encoded, y_pred, target_names=label_encoder.classes_))
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'confusion_matrix': cm
    }

if __name__ == "__main__":
    evaluate_model()

