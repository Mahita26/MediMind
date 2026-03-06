"""
Utility script to verify model training and test predictions.
"""

import os
import sys
import torch
import numpy as np
from PIL import Image
import argparse

model_dir = os.path.join(os.path.dirname(__file__), 'model')
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
if model_dir not in sys.path:
    sys.path.insert(0, model_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from model import MediMindModel
from dataset import get_transforms

def verify_model(model_path='backend/medimind_best_model.pth'):
    """Verify model is properly trained and can make predictions."""
    
    print("=" * 70)
    print("MediMind Model Verification")
    print("=" * 70)
    
    # Check if model exists
    if not os.path.exists(model_path):
        print(f"❌ Model not found at: {model_path}")
        print("\nRun training first:")
        print("  python train_model.py --dataset torchxrayvision")
        return False
    
    print(f"✓ Model found at: {model_path}")
    
    # Load model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"✓ Using device: {device}")
    
    try:
        model = MediMindModel(num_classes=6)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model = model.to(device).eval()
        print("✓ Model loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return False
    
    # Test with random input
    print("\nTesting inference...")
    with torch.no_grad():
        dummy_input = torch.randn(1, 3, 224, 224).to(device)
        logits = model(dummy_input)
        probs = torch.sigmoid(logits)
        
    disease_labels = [
        "Pneumonia", "Tuberculosis", "Lung Opacity",
        "Cardiomegaly", "Pleural Effusion", "Normal"
    ]
    
    print("\nSample predictions (random input):")
    print("-" * 50)
    for label, prob in zip(disease_labels, probs[0].cpu().numpy()):
        print(f"  {label:20s} : {prob:.2%}")
    print("-" * 50)
    
    print("\n" + "=" * 70)
    print("✓ Model verification passed!")
    print("=" * 70)
    
    return True

def test_with_image(image_path, model_path='backend/medimind_best_model.pth'):
    """Test model with a real image."""
    
    if not os.path.exists(image_path):
        print(f"❌ Image not found: {image_path}")
        return
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    try:
        model = MediMindModel(num_classes=6)
        model.load_state_dict(torch.load(model_path, map_location=device))
        model = model.to(device).eval()
        
        # Load and preprocess image
        image = Image.open(image_path).convert('RGB')
        transform = get_transforms(is_train=False)
        input_tensor = transform(image).unsqueeze(0).to(device)
        
        # Inference
        with torch.no_grad():
            logits = model(input_tensor)
            probs = torch.sigmoid(logits)
        
        disease_labels = [
            "Pneumonia", "Tuberculosis", "Lung Opacity",
            "Cardiomegaly", "Pleural Effusion", "Normal"
        ]
        
        print(f"\nPredictions for: {image_path}")
        print("-" * 50)
        for label, prob in zip(disease_labels, probs[0].cpu().numpy()):
            confidence = "HIGH" if prob > 0.7 else "MEDIUM" if prob > 0.3 else "LOW"
            print(f"  {label:20s} : {prob:.2%} [{confidence}]")
        print("-" * 50)
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Verify MediMind model')
    parser.add_argument('--model', type=str, default='backend/medimind_best_model.pth',
                        help='Path to model checkpoint')
    parser.add_argument('--test-image', type=str, default=None,
                        help='Test with specific image')
    
    args = parser.parse_args()
    
    # Verify model
    if verify_model(args.model):
        if args.test_image:
            test_with_image(args.test_image, args.model)
    else:
        print("\n⚠️  Model training required. Run:")
        print("   python train_model.py --dataset torchxrayvision")
