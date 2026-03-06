import torch
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix
import numpy as np

def calculate_metrics(y_true, y_pred_prob, threshold=0.5):
    """
    Calculate evaluation metrics for multi-label classification.
    
    Args:
        y_true (np.ndarray): Ground truth multi-hot labels.
        y_pred_prob (np.ndarray): Predicted probabilities (sigmoid output).
        threshold (float): Threshold to convert probability to binary prediction.
        
    Returns:
        dict: A dictionary containing Accuracy, F1 Score, AUC, Sensitivity, and Specificity.
    """
    y_pred = (y_pred_prob >= threshold).astype(int)
    
    # Macro metrics average across all labels
    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='macro', zero_division=0)
    
    # AUC might fail if a class only has one label type in a small batch
    try:
        auc = roc_auc_score(y_true, y_pred_prob, average='macro')
    except ValueError:
        auc = 0.5
        
    sensitivities = []
    specificities = []
    
    for i in range(y_true.shape[1]):
        tn, fp, fn, tp = confusion_matrix(y_true[:, i], y_pred[:, i], labels=[0, 1]).ravel()
        
        sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
        
        sensitivities.append(sensitivity)
        specificities.append(specificity)
        
    mean_sensitivity = np.mean(sensitivities)
    mean_specificity = np.mean(specificities)
    
    return {
        'accuracy': accuracy,
        'f1_score': f1,
        'auc_score': auc,
        'sensitivity': mean_sensitivity,
        'specificity': mean_specificity
    }
