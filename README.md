# MediMind - AI Radiology Assistant 🩺🧠

MediMind is a hackathon-winning, production-grade AI healthcare platform designed to detect lung abnormalities using deep learning and provide explainable heatmaps alongside structured radiology reports. 

## 🌐 Features
1. **AI Disease Detection:** Detects Pneumonia, Tuberculosis, Lung Opacity, Cardiomegaly, and Pleural Effusion.
2. **Explainable AI:** Uses Grad-CAM to generate visual heatmaps of the affected regions.
3. **Structured Reports:** Automatically generates full clinical radiology reports.
4. **Patient Explanations:** Translates complex medical jargon into simple, reassuring language for patients.
5. **Modern Dashboard:** A sleek, responsive, Next.js medical interface tailored for radiologists.

## 🏗️ Architecture Stack
- **AI Model Pipeline:** PyTorch, Torchvision (DenseNet121 Transfer Learning), scikit-learn.
- **Backend API:** FastAPI (Python), Uvicorn.
- **Frontend UI:** Next.js, React, Tailwind CSS, Lucide Icons.

## 🚀 Quickstart & Local Development

### 1. Backend (FastAPI + PyTorch)
```bash
cd backend
pip install -r ../requirements.txt
# To run the API server locally:
python main.py
```
*Note: If no pre-trained weights are present locally, the backend gracefully falls back to a realistic "Mock Mode" for instant demo capability without needing a GPU!*

### 2. Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
```
Open `http://localhost:3000` to view the application.

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
4. Set the Root Directory to `backend` (or ensure it runs `pip install -r requirements.txt` from the root).
5. Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Deploy!

*(For Hackathon Demos, if running out of model RAM on free tiers, ensure to keep the backend `model_path` pointing to a missing or mock file to activate Mock Mode).*

## 🔬 Dataset Preparation
To train the model from scratch, download subsets of the **NIH ChestXray14** or **CheXpert** dataset format and place them in `datasets/`. Use the provided `model/train.py` script.

## 👨‍💻 Contributing
This project was designed for rapid hackathon iteration.

Enjoy building the future of healthcare! 💙
