#!/usr/bin/env python3
"""
MediMind Quick Start - Run this script to get started with training
"""

import os
import subprocess
import sys

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def print_step(step, description):
    print(f"📍 Step {step}: {description}")
    print("-" * 70)

def run_command(cmd, description):
    print(f"Running: {cmd}\n")
    try:
        result = subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Failed: {description}")
        return False

if __name__ == "__main__":
    print_header("🏥 MediMind Quick Start Setup")
    
    print("""
This script will help you get MediMind running with real model training.

REQUIREMENTS:
- Python 3.8+ 
- pip (Python package manager)
- ~10 GB disk space (for datasets)
- 4GB+ RAM (8GB+ recommended)
- GPU optional but recommended (30x faster training)

WHAT WILL HAPPEN:
1. Install Python dependencies ✓
2. Show training options (you choose)
3. Provide commands to run ✓

Let's get started! 🚀
    """)
    
    input("Press ENTER to continue...")
    
    # Step 1: Check Python
    print_step(1, "Checking Python Installation")
    if not run_command(f"{sys.executable} --version", "Check Python"):
        print("❌ Python not found!")
        sys.exit(1)
    print("✓ Python found\n")
    
    # Step 2: Install dependencies
    print_step(2, "Installing Dependencies")
    print("This may take 5-15 minutes...")
    
    os.chdir("backend")
    if not run_command(f"{sys.executable} -m pip install -r requirements.txt", 
                       "Install dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    os.chdir("..")
    print("✓ Dependencies installed\n")
    
    # Step 3: Explain training options
    print_step(3, "Choose Your Training Dataset")
    
    print("""
OPTION 1: TorchXRayVision (EASIEST - Recommended) ⭐
  • Automatically downloads CheXpert dataset
  • 19.2K real chest X-rays from Stanford
  • Takes 30-60 minutes
  • Works on GPU or CPU
  Command: python train_model.py --dataset torchxrayvision --epochs 30

OPTION 2: Manual CheXpert Dataset
  • Download from: https://stanfordmlgroup.github.io/competitions/chexpert/
  • Extract to: datasets/chexpert
  • Command: python train_model.py --dataset chexpert --epochs 30

OPTION 3: Your Own Dataset
  • Place images in: datasets/images/
  • Create CSV: datasets/labels.csv
  • Command: python train_model.py --dataset local_csv --epochs 30

OPTION 4: Quick Demo (No Data)
  • Just verify setup without training
  • Command: python verify_model.py
    """)
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    print_step(4, "Run Training")
    
    if choice == "1":
        print("✓ Running TorchXRayVision training...")
        print("\nCommand to run:")
        print("  python train_model.py --dataset torchxrayvision --epochs 30")
        print("\nThis will:")
        print("  1. Download CheXpert dataset (~20 GB)")
        print("  2. Train for 30 epochs")
        print("  3. Save model to: backend/medimind_best_model.pth")
        print("\nExpected time: 30-60 minutes on GPU")
        
        if input("\nRun now? (y/n): ").lower() == 'y':
            os.system("python train_model.py --dataset torchxrayvision --epochs 30")
    
    elif choice == "2":
        print("✓ CheXpert dataset selected")
        print("\nSteps:")
        print("  1. Download from: https://stanfordmlgroup.github.io/competitions/chexpert/")
        print("  2. Extract to: datasets/chexpert")
        print("  3. Run: python train_model.py --dataset chexpert --epochs 30")
        
    elif choice == "3":
        print("✓ Custom dataset selected")
        print("\nSteps:")
        print("  1. Place images in: datasets/images/")
        print("  2. Create CSV: datasets/labels.csv")
        print("     Columns: image_path, Pneumonia, Tuberculosis, Lung Opacity, Cardiomegaly, Pleural Effusion, Normal")
        print("  3. Run: python train_model.py --dataset local_csv --epochs 30")
        
    elif choice == "4":
        print("✓ Running verification...")
        os.system("python verify_model.py")
    
    # Final step
    print_step(5, "After Training")
    
    print("""
When training completes:

1. Verify the model:
   python verify_model.py

2. Restart the backend server:
   cd backend
   uvicorn main:app --reload --port 8000

3. Start the frontend:
   cd frontend
   npm run dev

4. Open browser:
   http://localhost:3000

5. Test with real chest X-ray images!
    """)
    
    print_header("✨ Setup Complete!")
    print("""
For more information, see:
  • README.md - Project overview
  • TRAINING_GUIDE.md - Detailed training guide
  • FIX_SUMMARY.md - Issues and solutions
  • ISSUES_FIXED.txt - Visual summary

Questions? Check the documentation files!
    """)

