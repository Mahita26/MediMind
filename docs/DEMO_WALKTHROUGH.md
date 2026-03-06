# 🚀 Hackathon Demo Walkthrough: MediMind

Use this script to deliver a flawless, high-impact hackathon presentation.

## Setup
1. Ensure both your frontend (`npm run dev`) and backend (`python main.py`) are running. 
2. Have two sample X-rays ready on your desktop:
   - `normal_chest_xray.jpg`
   - `pneumonia_chest_xray.jpg`

## The Pitch (1 Minute)
> "Hello everyone, we are team MediMind. Radiologists are currently overwhelmed, leading to delayed diagnoses and physician burnout. Our solution is MediMind: an AI Radiology Assistant that acts as a reliable second pair of eyes, increasing diagnostic speed and accuracy."

## The Demo (2 Minutes)
1. **Landing Page (`/`)**: 
   - Show the beautiful, responsive landing page.
   - Point out the clean "medical blue" aesthetic and animated "Analysis Progress" card.
   - Click **"Doctor Login"**.

2. **Login (`/login`)**: 
   - Enter mock credentials.
   - Click "Sign in" (Note the sleek loading spinner).

3. **Dashboard Interface (`/dashboard`)**:
   - Welcome the judges to the primary radiologist workspace.
   - Click the upload area and select your `pneumonia_chest_xray.jpg`.
   
4. **Analysis & Explainability**:
   - Click **"Analyze Imaging Scan"**.
   - Point out the beautiful loading animation: *"The image is instantly sent to our FastAPI backend where our deep learning model processes it."*
   - Once results load, highlight the **Confidence Scores**: *"MediMind detected high probability for Pneumonia and Lung Opacity."*
   - Point to the **Image**: *"Crucially, we implemented Grad-CAM explainable AI. The heatmap shows exactly which part of the lung the AI focused on. This builds trust with the doctors."*

5. **Reporting**:
   - Scroll to the **Structured Radiology Report**: *"We automate the tedious reporting process by generating clinical findings."*
   - Highlight the **Patient Explanation**: *"Finally, we added a translation module. It converts complex medical jargon into simple, empathetic language for the patient, saving the doctor translation time."*

## The Tech Stack & Architecture (1 Minute)
> "All of this runs on an incredibly robust stack. PyTorch DenseNet121 transfer learning for rapid inference, FastAPI for a decoupled backend, and a modern Next.js + Tailwind React frontend. It's fully production-ready and deployed right now using Vercel and Render."

## Q&A Preparation
- **"What about False Positives?"** We calibrate our probabilities using temperature scaling so that confidence scores are reliable. Furthermore, sensitivity is prioritized in medical AI so missing diseases occurs less often than false alarms. 
- **"Is the model overfitting?"** We froze early convolution layers during transfer learning and utilized robust augmentations (horizontal flip, brightness jitter, gaussian noise) to ensure high generalization.
