import os
import torch
from torch.utils.data import Dataset
from PIL import Image, ImageFile
import pandas as pd
import numpy as np
from torchvision import transforms

ImageFile.LOAD_TRUNCATED_IMAGES = True

class GaussianNoise:
    def __init__(self, mean=0.0, std=0.05):
        self.mean = mean
        self.std = std
        
    def __call__(self, tensor):
        noise = torch.randn(tensor.size()) * self.std + self.mean
        return tensor + noise

def get_transforms(is_train: bool = True):
    if is_train:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.RandomHorizontalFlip(p=0.5),
            transforms.RandomRotation(degrees=10),
            transforms.ColorJitter(brightness=0.2),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            GaussianNoise(std=0.05)
        ])
    else:
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

class ChestXrayDataset(Dataset):
    def __init__(self, df: pd.DataFrame, image_dir: str, label_cols: list, is_train: bool = True):
        """
        Args:
            df (pd.DataFrame): DataFrame containing image filenames and labels.
            image_dir (str): Directory with all the images.
            label_cols (list): List of column names corresponding to labels.
            is_train (bool): Whether to apply training augmentations.
        """
        self.df = df
        self.image_dir = image_dir
        self.label_cols = label_cols
        self.transform = get_transforms(is_train)
        
        # Pre-filter dataset to remove completely corrupted / missing images if desired
        # For performance, we handle IOError during __getitem__ but ideally it's pre-filtered
        
    def __len__(self):
        return len(self.df)
    
    def __getitem__(self, idx):
        if torch.is_tensor(idx):
            idx = idx.tolist()
            
        img_name = os.path.join(self.image_dir, str(self.df.iloc[idx]['image_id']))
        try:
            image = Image.open(img_name).convert('RGB')
        except Exception as e:
            # Fallback to white noise image or another index if corrupted
            # In a real pipeline, we'd clean the dataset beforehand
            image = Image.new('RGB', (224, 224), (255, 255, 255))
            
        if self.transform:
            image = self.transform(image)
            
        labels = self.df.iloc[idx][self.label_cols].values
        labels = torch.from_numpy(labels.astype(np.float32))
        
        return image, labels
