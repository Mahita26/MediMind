import torch
import torch.nn as nn
from torchvision import models

class MediMindModel(nn.Module):
    def __init__(self, num_classes=6, freeze_early_layers=True):
        """
        Initializes the DenseNet121 based model for multi-label classification.
        
        Args:
            num_classes (int): Number of target diseases.
            freeze_early_layers (bool): Whether to freeze the pre-trained weights.
        """
        super(MediMindModel, self).__init__()
        
        # Load pre-trained DenseNet121
        # Using weights parameter for newer torchvision versions
        self.backbone = models.densenet121(weights=models.DenseNet121_Weights.DEFAULT)
        
        if freeze_early_layers:
            # Freeze the entire features section initially
            for param in self.backbone.features.parameters():
                param.requires_grad = False
                
            # Unfreeze the last dense block and transition layer for fine-tuning
            for param in self.backbone.features.denseblock4.parameters():
                param.requires_grad = True
            for param in self.backbone.features.norm5.parameters():
                param.requires_grad = True
                
        # Replace the classifier head
        in_features = self.backbone.classifier.in_features
        self.backbone.classifier = nn.Sequential(
            nn.Linear(in_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),  # Dropout to prevent overfitting
            nn.Linear(512, num_classes)
        )
        
        # Temperature parameter for calibrated probability outputs (Platt scaling / Temperature scaling)
        self.temperature = nn.Parameter(torch.ones(1) * 1.5)
        
    def forward(self, x):
        # We process it through the backbone which now includes our custom classifier
        logits = self.backbone(x)
        # Apply temperature scaling
        scaled_logits = logits / self.temperature
        return scaled_logits
        
    def predict_proba(self, x):
        """Returns calibrated probabilities."""
        logits = self(x)
        # Sigmoid is used because this is a multi-label classification task
        return torch.sigmoid(logits)
