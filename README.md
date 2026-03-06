# MediMind - AI Radiology Assistant 🩺🧠

MediMind is a hackathon-winning, production-grade AI healthcare platform designed to detect lung abnormalities using deep learning and provide explainable heatmaps alongside structured radiology reports. 

## 🌐 Features
1. **AI Disease Detection:** Detects Pneumonia, Tuberculosis, Lung Opacity, Cardiomegaly, and Pleural Effusion.
2. **Explainable AI:** Uses Grad-CAM to generate visual heatmaps of the affected regions.
3. **Structured Reports:** Automatically generates full clinical radiology reports.
4. **Patient Explanations:** Translates complex medical jargon into simple, reassuring language for patients.
5. **Modern Dashboard:** A sleek, responsive, Next.js medical interface tailored for radiologists.
6. **Real Authentication:** Gmail OAuth2 + email validation for secure, real user accounts.

## 🏗️ Architecture Stack
- **AI Model Pipeline:** PyTorch, Torchvision (DenseNet121 Transfer Learning), scikit-learn.
- **Backend API:** FastAPI (Python), Uvicorn.
- **Frontend UI:** Next.js, React, Tailwind CSS, Lucide Icons.
- **Authentication:** Gmail OAuth2, JWT tokens, bcrypt password hashing.

## ⚡ IMPORTANT: Model Training Required

**⚠️ Current Status:** The model needs training on real chest X-ray data for accurate predictions.

### Quick Fix (5 Minutes)
```bash
# Install dependencies
cd backend
pip install -r requirements.txt

# Go back and train
cd ..

# Train model (downloads data automatically)
python train_model.py --dataset torchxrayvision --epochs 30
```

After training, restart the backend and the model will use **real trained weights** instead of mock predictions!

**See `TRAINING_GUIDE.md` or `FIX_SUMMARY.md` for detailed instructions.**

## 🚀 Quickstart & Local Development

### 1. Backend (FastAPI + PyTorch)
```bash
cd backend
pip install -r requirements.txt

# Run the API server (after training the model)
uvicorn main:app --reload --port 8000
```

#### 🎯 About Mock Mode
- If `backend/medimind_best_model.pth` doesn't exist, the backend runs in **Mock Mode**
- This provides random predictions for demo purposes
- **To use real predictions:** Run `python train_model.py` first

### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to view the application.

### 3. Gmail OAuth2 Setup (Optional)
To enable Gmail login:
1. Get credentials from [Google Cloud Console](https://console.cloud.google.com/)
2. Set environment variables:
   ```bash
   export GOOGLE_CLIENT_ID="your-client-id.apps.googleusercontent.com"
   export GOOGLE_CLIENT_SECRET="your-secret"
   ```

## 📊 Model Training Guide

### Option 1: TorchXRayVision (Easiest - Recommended)
```bash
python train_model.py --dataset torchxrayvision --epochs 30
```
- Automatically downloads CheXpert dataset
- Takes ~30-60 minutes on GPU
- Recommended for most users

### Option 2: Manual CheXpert Download
```bash
# 1. Download from: https://stanfordmlgroup.github.io/competitions/chexpert/
# 2. Extract to: datasets/chexpert
# 3. Run:
python train_model.py --dataset chexpert --epochs 30
```

### Option 3: Custom Dataset
```bash
# Place images in: datasets/images/
# Create CSV: datasets/labels.csv
python train_model.py --dataset local_csv --epochs 30
```

### Available Datasets
- **CheXpert** (Stanford) - 19.2K images
- **NIH ChestX-ray14** - 112K images  
- **VinDr-CXR** - 18K high-quality images
- **PadChest** - 160K+ images
- **TorchXRayVision** - Auto-managed (recommended)

See `TRAINING_GUIDE.md` for detailed dataset information.

## 🔐 Authentication

### Email Validation
- ✅ Real email addresses (gmail.com, yourcompany.com, etc.)
- ✅ Strong passwords (8+ chars, uppercase, numbers)
- ❌ Fake emails (test.com, fake.com, tempmail.com)
- ❌ Weak passwords

### Gmail OAuth2
Users can now log in with their real Gmail accounts:
```python
POST /auth/gmail-login
{
  "token": "<google_id_token>"
}
```

## ☁️ Deployment Instructions (Free Tier)

### Frontend (Vercel)
1. Push this repository to GitHub.
2. Log in to [Vercel](https://vercel.com).
3. Click "Add New Project" and import your `MediMind` repository.
4. Set the Root Directory to `frontend`.
5. Framework preset: Next.js.
6. Click Deploy!

### Backend (Render / Railway)
1. Log in to [Render](https://render.com) or [Railway](https://railway.app).
2. Create a new "Web Service".
3. Connect your GitHub repository.
4. Set the Root Directory to `backend`.
5. Start Command: `pip install -r requirements.txt && uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy!

## 📁 Project Structure
```
MediMind/
├── backend/                 # FastAPI server
│   ├── main.py             # Entry point
│   ├── auth.py             # JWT auth
│   ├── gmail_oauth.py       # Gmail integration
│   ├── models.py           # Database models
│   ├── services.py         # AI service
│   ├── routers/            # API endpoints
│   └── requirements.txt
├── frontend/               # Next.js UI
│   ├── src/app/
│   ├── src/components/
│   └── package.json
├── model/                  # PyTorch model
│   ├── model.py           # DenseNet121 architecture
│   ├── train.py           # Training script
│   ├── dataset.py         # Data loading
│   └── metrics.py         # Evaluation metrics
├── train_model.py          # NEW: Full training pipeline
├── prepare_dataset.py      # NEW: Dataset setup
├── verify_model.py         # NEW: Model verification
├── TRAINING_GUIDE.md       # NEW: Detailed guide
├── FIX_SUMMARY.md          # NEW: Summary of fixes
└── ISSUES_FIXED.txt        # NEW: Visual summary
```

## 🔬 Dataset Preparation
To train the model from scratch:
1. Run `python prepare_dataset.py` to see available datasets
2. Download real chest X-ray data (CheXpert, NIH, etc.)
3. Run `python train_model.py` with your dataset
4. Model will be saved to `backend/medimind_best_model.pth`

## 📚 Documentation
- **TRAINING_GUIDE.md** - Complete training documentation (5000+ words)
- **FIX_SUMMARY.md** - Summary of all issues and fixes
- **ISSUES_FIXED.txt** - Visual summary report
- **ISSUES_FIXED.txt** - Complete before/after comparison

## 👨‍💻 Contributing
This project was designed for rapid hackathon iteration. Contributions are welcome!

## ✨ Recent Improvements
- ✅ Added real email validation (rejects fake domains)
- ✅ Gmail OAuth2 integration
- ✅ Complete model training pipeline
- ✅ Support for multiple medical datasets (CheXpert, NIH, etc.)
- ✅ Model verification tools
- ✅ Comprehensive documentation

Enjoy building the future of healthcare! 💙

---

**First Time Setup?** See `TRAINING_GUIDE.md` or run:
```bash
python train_model.py --dataset torchxrayvision
```

