"""
Complete model training pipeline for MediMind.
Trains on real chest X-ray datasets with validation.
"""

import os
import sys
import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
import numpy as np
from pathlib import Path
from tqdm import tqdm
import logging

# Add directories to path
model_dir = os.path.join(os.path.dirname(__file__), 'model')
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
if model_dir not in sys.path:
    sys.path.insert(0, model_dir)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from model import MediMindModel
from dataset import ChestXrayDataset
from metrics import calculate_metrics

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_torchxrayvision_dataset():
    """Load dataset using torchxrayvision library."""
    try:
        import torchxrayvision as xrv
        logger.info("Loading CheXpert dataset via torchxrayvision...")
        
        # Download and load CheXpert
        download_dir = os.path.expanduser("~/.medimind_datasets")
        os.makedirs(download_dir, exist_ok=True)
        
        dataset = xrv.datasets.CheX_Dataset(
            imgpath=download_dir,
            csvpath=os.path.join(download_dir, "train.csv"),
            views=["PA"]
        )
        
        logger.info(f"Loaded {len(dataset)} images from CheXpert")
        return dataset
    except ImportError:
        logger.error("torchxrayvision not installed. Run: pip install torchxrayvision")
        return None
    except Exception as e:
        logger.error(f"Failed to load torchxrayvision dataset: {e}")
        logger.info("This is expected if CheXpert data is not downloaded yet.")
        return None

def train():
    """Main training function."""
    parser = argparse.ArgumentParser(description='Train MediMind model on real datasets')
    parser.add_argument('--dataset', type=str, default='torchxrayvision',
                        choices=['torchxrayvision', 'local_csv', 'chexpert'],
                        help='Dataset source')
    parser.add_argument('--csv-path', type=str, default='datasets/labels.csv',
                        help='Path to CSV for local datasets')
    parser.add_argument('--image-dir', type=str, default='datasets/images',
                        help='Path to image directory')
    parser.add_argument('--batch-size', type=int, default=32,
                        help='Batch size for training')
    parser.add_argument('--epochs', type=int, default=50,
                        help='Number of epochs')
    parser.add_argument('--lr', type=float, default=1e-4,
                        help='Learning rate')
    parser.add_argument('--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu',
                        help='Device to use (cuda/cpu)')
    parser.add_argument('--patience', type=int, default=5,
                        help='Early stopping patience')
    parser.add_argument('--output', type=str, default='backend/medimind_best_model.pth',
                        help='Output model path')
    
    args = parser.parse_args()
    
    device = torch.device(args.device)
    logger.info(f"Using device: {device}")
    
    # Load dataset
    if args.dataset == 'torchxrayvision':
        dataset = load_torchxrayvision_dataset()
        if dataset is None:
            logger.warning("Falling back to local CSV dataset...")
            args.dataset = 'local_csv'
        else:
            # For torchxrayvision, we need to convert to our format
            train_loader, val_loader = prepare_torchxrayvision_loaders(
                dataset, args.batch_size, device
            )
            _train_model(train_loader, val_loader, args, device)
            return
    
    if args.dataset == 'local_csv':
        if not os.path.exists(args.csv_path):
            logger.error(f"CSV file not found: {args.csv_path}")
            logger.info("Run 'python prepare_dataset.py' first to set up datasets")
            return
        
        logger.info(f"Loading dataset from CSV: {args.csv_path}")
        train_loader, val_loader = prepare_csv_loaders(
            args.csv_path, args.image_dir, args.batch_size, device
        )
    else:
        logger.error(f"Unknown dataset: {args.dataset}")
        return
    
    _train_model(train_loader, val_loader, args, device)

def prepare_csv_loaders(csv_path, image_dir, batch_size, device):
    """Prepare data loaders from CSV file."""
    import pandas as pd
    
    df = pd.read_csv(csv_path)
    
    # Filter valid images
    valid_df = df[df['image_path'].apply(lambda x: os.path.exists(os.path.join(image_dir, x)))].copy()
    
    if len(valid_df) == 0:
        raise ValueError(f"No valid images found in {image_dir}")
    
    logger.info(f"Found {len(valid_df)} valid images")
    
    # Label columns
    label_cols = ['Pneumonia', 'Tuberculosis', 'Lung Opacity', 'Cardiomegaly', 'Pleural Effusion', 'Normal']
    
    # Create dataset
    dataset = ChestXrayDataset(valid_df, image_dir, label_cols, is_train=True)
    
    # Split into train/val
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=4)
    
    return train_loader, val_loader

def prepare_torchxrayvision_loaders(dataset, batch_size, device):
    """Prepare loaders from torchxrayvision dataset."""
    from torch.utils.data import Dataset as TorchDataset
    from dataset import get_transforms
    
    # Create wrapper dataset with transforms
    class TransformDataset(TorchDataset):
        def __init__(self, indices, base_dataset, transform):
            self.indices = indices
            self.base_dataset = base_dataset
            self.transform = transform
        
        def __len__(self):
            return len(self.indices)
        
        def __getitem__(self, idx):
            actual_idx = self.indices[idx]
            data = self.base_dataset[actual_idx]
            
            if isinstance(data, tuple) and len(data) == 2:
                img, label = data
            else:
                img = data
                label = torch.zeros(6)
            
            if self.transform:
                if hasattr(img, 'convert'):
                    img = self.transform(img)
                else:
                    try:
                        img = torch.tensor(np.array(img), dtype=torch.float32)
                    except:
                        img = img
            
            if not isinstance(label, torch.Tensor):
                label = torch.tensor(label, dtype=torch.float32)
            else:
                label = label.float()
            
            return img, label
    
    # Split dataset
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    train_indices = list(range(train_size))
    val_indices = list(range(train_size, train_size + val_size))
    
    train_dataset = TransformDataset(
        train_indices,
        dataset,
        transform=get_transforms(is_train=True)
    )
    val_dataset = TransformDataset(
        val_indices,
        dataset,
        transform=get_transforms(is_train=False)
    )
    
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=0)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=0)
    
    return train_loader, val_loader

def _train_model(train_loader, val_loader, args, device):
    """Internal training function."""
    logger.info("Initializing model...")
    
    # Model
    model = MediMindModel(num_classes=6, freeze_early_layers=False)  # Unfreeze for full training
    model = model.to(device)
    
    # Loss and optimizer
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=args.lr, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
        optimizer, mode='min', factor=0.5, patience=2
    )
    
    best_val_loss = float('inf')
    patience_counter = 0
    
    logger.info("Starting training...")
    logger.info(f"Epochs: {args.epochs}, Batch size: {args.batch_size}, LR: {args.lr}")
    
    for epoch in range(args.epochs):
        # Training phase
        model.train()
        train_loss = 0.0
        
        with tqdm(train_loader, desc=f"Epoch {epoch+1}/{args.epochs} [Train]") as pbar:
            for images, labels in pbar:
                images = images.to(device)
                labels = labels.to(device).float()
                
                optimizer.zero_grad()
                logits = model(images)
                loss = criterion(logits, labels)
                
                loss.backward()
                torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
                optimizer.step()
                
                train_loss += loss.item()
                pbar.set_postfix({'loss': loss.item()})
        
        train_loss = train_loss / len(train_loader)
        
        # Validation phase
        model.eval()
        val_loss = 0.0
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            with tqdm(val_loader, desc=f"Epoch {epoch+1}/{args.epochs} [Val]") as pbar:
                for images, labels in pbar:
                    images = images.to(device)
                    labels = labels.to(device).float()
                    
                    logits = model(images)
                    loss = criterion(logits, labels)
                    val_loss += loss.item()
                    
                    probs = torch.sigmoid(logits)
                    all_preds.append(probs.cpu().numpy())
                    all_labels.append(labels.cpu().numpy())
        
        val_loss = val_loss / len(val_loader)
        scheduler.step(val_loss)
        
        # Metrics
        all_preds = np.vstack(all_preds)
        all_labels = np.vstack(all_labels)
        metrics = calculate_metrics(all_labels, all_preds)
        
        logger.info(f"Epoch {epoch+1}/{args.epochs}")
        logger.info(f"  Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
        logger.info(f"  AUC: {metrics['auc_score']:.4f} | Sensitivity: {metrics['sensitivity']:.4f} | Specificity: {metrics['specificity']:.4f}")
        
        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            
            # Save best model
            os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
            torch.save(model.state_dict(), args.output)
            logger.info(f"✓ Saved best model to {args.output}")
        else:
            patience_counter += 1
            if patience_counter >= args.patience:
                logger.info(f"Early stopping triggered after {epoch+1} epochs")
                break
    
    logger.info("✓ Training completed!")
    logger.info(f"Best model saved to: {args.output}")

if __name__ == '__main__':
    try:
        train()
    except KeyboardInterrupt:
        logger.info("\nTraining interrupted by user")
    except Exception as e:
        logger.error(f"Training failed: {e}", exc_info=True)
