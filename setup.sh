#!/bin/bash
# MediMind Quick Setup Script
# Run this to set up everything needed for training

set -e

echo "=========================================="
echo "MediMind Setup Script"
echo "=========================================="
echo ""

# Check Python version
echo "✓ Checking Python version..."
python3 --version

# Create datasets directory
echo "✓ Creating datasets directory..."
mkdir -p datasets

# Install backend dependencies
echo "✓ Installing Python dependencies..."
cd backend
pip install -r requirements.txt

cd ..

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo ""
echo "1. Run model training:"
echo "   python train_model.py --dataset torchxrayvision --epochs 30"
echo ""
echo "2. Restart backend (after training completes):"
echo "   cd backend && uvicorn main:app --reload --port 8000"
echo ""
echo "3. Verify training:"
echo "   python verify_model.py"
echo ""
echo "For more details, see: TRAINING_GUIDE.md or FIX_SUMMARY.md"
echo ""
