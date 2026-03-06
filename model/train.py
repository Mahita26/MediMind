import torch
import torch.nn as nn
from torch.utils.data import DataLoader
import numpy as np
from tqdm import tqdm
from dataset import ChestXrayDataset
from model import MediMindModel
from metrics import calculate_metrics
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def train_model(
    model, 
    train_loader, 
    val_loader, 
    criterion, 
    optimizer, 
    scheduler, 
    num_epochs=10, 
    device='cpu', 
    patience=3
):
    """
    Trains the MediMindModel.
    """
    model.to(device)
    best_val_loss = float('inf')
    epochs_no_improve = 0
    
    for epoch in range(num_epochs):
        logging.info(f"Epoch {epoch+1}/{num_epochs}")
        
        # Training Phase
        model.train()
        train_loss = 0.0
        
        for images, labels in tqdm(train_loader, desc="Training"):
            images, labels = images.to(device), labels.to(device)
            
            optimizer.zero_grad()
            logits = model(images)
            loss = criterion(logits, labels)
            
            loss.backward()
            optimizer.step()
            
            train_loss += loss.item() * images.size(0)
            
        train_loss = train_loss / len(train_loader.dataset)
        
        # Validation Phase
        model.eval()
        val_loss = 0.0
        all_preds = []
        all_labels = []
        
        with torch.no_grad():
            for images, labels in tqdm(val_loader, desc="Validation"):
                images, labels = images.to(device), labels.to(device)
                
                logits = model(images)
                loss = criterion(logits, labels)
                val_loss += loss.item() * images.size(0)
                
                probs = torch.sigmoid(logits)
                all_preds.append(probs.cpu().numpy())
                all_labels.append(labels.cpu().numpy())
                
        val_loss = val_loss / len(val_loader.dataset)
        scheduler.step(val_loss)
        
        # Calculate Metrics
        all_preds = np.vstack(all_preds)
        all_labels = np.vstack(all_labels)
        metrics = calculate_metrics(all_labels, all_preds)
        
        logging.info(f"Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")
        logging.info(f"Metrics: AUC: {metrics['auc_score']:.4f}, Sensitivity: {metrics['sensitivity']:.4f}, Specificity: {metrics['specificity']:.4f}")
        
        # Early Stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            epochs_no_improve = 0
            torch.save(model.state_dict(), 'medimind_best_model.pth')
            logging.info("Saved best model!")
        else:
            epochs_no_improve += 1
            if epochs_no_improve >= patience:
                logging.info(f"Early stopping triggered after {epoch+1} epochs.")
                break

if __name__ == '__main__':
    # This acts as an entry point for training
    logging.info("Initializing MediMind training pipeline... To run this, prepare your dataframe and datasets!")
