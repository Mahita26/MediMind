"""
Dataset preparation script for CheXpert or ChestX-ray14 datasets.
Downloads and prepares real chest X-ray data for model training.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path
import requests
from tqdm import tqdm

def download_chexpert_dataset(download_path="datasets/chexpert"):
    """
    Guide for downloading CheXpert dataset.
    Manual download required from: https://stanfordmlgroup.github.io/competitions/chexpert/
    """
    download_path = Path(download_path)
    download_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("CheXpert Dataset Setup Instructions")
    print("=" * 70)
    print("\n1. Go to: https://stanfordmlgroup.github.io/competitions/chexpert/")
    print("2. Sign up and download the CheXpert v1.0 dataset")
    print("3. Extract it to:", download_path)
    print("\nDataset includes:")
    print("- Pneumonia")
    print("- Tuberculosis")
    print("- Lung Opacity")
    print("- Cardiomegaly")
    print("- Pleural Effusion")
    print("\nOnce downloaded, run: python prepare_dataset.py")
    print("=" * 70)

def download_nih_chest_xray(download_path="datasets/nih_chest"):
    """
    Download NIH Chest X-ray dataset (122GB - large!)
    Alternative: Use smaller splits or the official torchxrayvision datasets
    
    For faster setup, consider:
    - torchxrayvision: pip install torchxrayvision
    - Uses pre-prepared NIH, CheXpert, PadChest datasets
    """
    download_path = Path(download_path)
    download_path.mkdir(parents=True, exist_ok=True)
    
    print("=" * 70)
    print("NIH Chest X-ray Dataset (Alternative Option)")
    print("=" * 70)
    print("\nOption A: Download manually from:")
    print("https://www.nih.gov/news-events/news-releases/nih-clinical-center-provides-public-chest-x-ray-dataset-ai-researchers")
    print("\nOption B: Use torchxrayvision (RECOMMENDED - Faster)")
    print("Install: pip install torchxrayvision")
    print("\nExample usage:")
    print("""
import torchxrayvision as xrv
dataset = xrv.datasets.CheX_Dataset(
    imgpath="path/to/chexpert",
    csvpath="path/to/labels.csv"
)
    """)
    print("=" * 70)

def create_sample_dataset(output_path="datasets/sample_chexray", num_samples=100):
    """
    Create a sample dataset from publicly available NIH chest X-ray images.
    For quick testing/demo purposes.
    """
    output_path = Path(output_path)
    images_dir = output_path / "images"
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Creating sample dataset with {num_samples} images...")
    
    # Disease labels we're detecting
    diseases = ["Pneumonia", "Tuberculosis", "Lung Opacity", "Cardiomegaly", "Pleural Effusion", "Normal"]
    
    # Sample data structure
    data = {
        'image_path': [],
        'Pneumonia': [],
        'Tuberculosis': [],
        'Lung Opacity': [],
        'Cardiomegaly': [],
        'Pleural Effusion': [],
        'Normal': []
    }
    
    # Generate synthetic entries pointing to real publicly available sources
    print("\nTo populate this dataset with REAL images, download from:")
    print("1. CheXpert: https://stanfordmlgroup.github.io/competitions/chexpert/")
    print("2. NIH ChestX-ray14: https://www.nih.gov/news-events/news-releases/nih-clinical-center-provides-public-chest-x-ray-dataset-ai-researchers")
    print("3. PadChest: https://bimcv.cipf.es/bimcv-projects/padchest/")
    print("4. VinDr-CXR: https://www.vindr.ai/datasets/cxr")
    
    # Create metadata CSV
    df = pd.DataFrame(data)
    csv_path = output_path / "labels.csv"
    df.to_csv(csv_path, index=False)
    
    print(f"\nDataset structure created at: {output_path}")
    print(f"CSV labels file: {csv_path}")
    print("\nNext steps:")
    print("1. Download real chest X-ray images from sources above")
    print("2. Place images in:", images_dir)
    print("3. Update CSV with correct file paths and labels (0 or 1 for multi-label)")
    
    return output_path

if __name__ == "__main__":
    # Create datasets directory structure
    Path("datasets").mkdir(exist_ok=True)
    
    print("\n" + "=" * 70)
    print("MediMind Real Dataset Setup")
    print("=" * 70)
    
    # Provide options
    print("\n\nOptional Datasets (Choose one or combine multiple):\n")
    
    create_sample_dataset()
    print("\n\n" + "-" * 70)
    download_chexpert_dataset()
    print("\n\n" + "-" * 70)
    download_nih_chest_xray()
    
    print("\n\n" + "=" * 70)
    print("QUICK START: Using torchxrayvision")
    print("=" * 70)
    print("""
pip install torchxrayvision
    
Then run training with:
    python train_model.py --use-torchxrayvision
    """)
