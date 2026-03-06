import os
import torch
import numpy as np
from PIL import Image
import base64
import io

# Optional mock logic for demo purposes when model isn't yet trained
class AIService:
    def __init__(self, model_path="medimind_best_model.pth"):
        try:
            import torch
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            has_torch = True
        except ImportError:
            self.device = 'cpu'
            has_torch = False
            
        self.mock_mode = not os.path.exists(model_path) or not has_torch
        self.disease_labels = [
            "Pneumonia", "Tuberculosis", "Lung Opacity", 
            "Cardiomegaly", "Pleural Effusion", "Normal"
        ]
        
        if not self.mock_mode:
            try:
                import sys
                sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
                from model import MediMindModel
                import torch
                
                self.model = MediMindModel(num_classes=6)
                self.model.load_state_dict(torch.load(model_path, map_location=self.device))
                self.model.to(self.device).eval()
                print("Model loaded successfully.")
            except Exception as e:
                print(f"Failed to load real model: {e}")
                self.mock_mode = True
        else:
            print("Running in MOCK mode. Model checkpoint not found or PyTorch missing.")
            
    def predict(self, image_bytes: bytes):
        """Runs inference on uploaded image bytes."""
        # For mock mode, return realistic looking random probabilities
        if self.mock_mode:
            # bias towards normal or one random disease for demo
            probs = np.random.rand(6) * 0.3
            probs[5] = 0.95  # Default to Normal being high
            return {label: float(prob) for label, prob in zip(self.disease_labels, probs)}
            
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
        from dataset import get_transforms
        
        # Real inference
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        transform = get_transforms(is_train=False)
        input_tensor = transform(image).unsqueeze(0).to(self.device)
        
        with torch.no_grad():
            preds = self.model.predict_proba(input_tensor).cpu().numpy()[0]
            
        return {label: float(prob) for label, prob in zip(self.disease_labels, preds)}
        
    def generate_heatmap(self, image_bytes: bytes, target_class=None):
        """Generates Grad-CAM base64 string."""
        if self.mock_mode:
            # Return same image back but pretend it's a heatmap
            encoded = base64.b64encode(image_bytes).decode('utf-8')
            return f"data:image/jpeg;base64,{encoded}"
            
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'model')))
        from dataset import get_transforms
        from cam import generate_gradcam_heatmap
        
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        transform = get_transforms(is_train=False)
        input_tensor = transform(image).unsqueeze(0).to(self.device)
        original_img_np = np.array(image).astype(np.float32) / 255.0
        
        visualization = generate_gradcam_heatmap(self.model, input_tensor, original_img_np, target_class)
        
        # Convert visualization (np array) to base64
        vis_image = Image.fromarray((visualization * 255).astype(np.uint8))
        buffered = io.BytesIO()
        vis_image.save(buffered, format="JPEG")
        encoded = base64.b64encode(buffered.getvalue()).decode('utf-8')
        
        return f"data:image/jpeg;base64,{encoded}"

def generate_radiology_report(predictions: dict, threshold=0.5):
    """Generates structured radiology report."""
    detected = [k for k, v in predictions.items() if v > threshold and k != "Normal"]
    
    findings = []
    if detected:
        findings.append(f"Significant indications of: {', '.join(detected)}.")
        findings.append("Other lung fields appear relatively clear.")
        impression = f"Positive for {', '.join(detected)}."
        recommendation = "Recommend further clinical correlation and potentially a follow-up CT scan."
    else:
        findings.append("No acute cardiopulmonary abnormalities detected.")
        findings.append("Lung volumes and vascularity appear within normal limits.")
        impression = "Normal chest radiograph."
        recommendation = "No specific follow-up required based on this automated screening."
        
    report = {
        "findings": " ".join(findings),
        "impression": impression,
        "recommendation": recommendation
    }
    return report

def generate_patient_explanation(report: dict):
    """Translates medical jargon to patient-friendly language."""
    base_text = "Your recent chest X-ray was analyzed by our AI system.\n\n"
    
    if "Normal" in report["impression"]:
        explanation = base_text + "Good news! The AI did not detect any obvious signs of infection or lung problems. Your lungs look healthy based on this scan."
    else:
        explanation = base_text + f"The system noticed some patterns that might relate to what the doctors call '{report['impression']}'. This could indicate a possible infection or other common lung conditions. Please don't worry—your doctor will review this and discuss the best next steps with you."
        
    disclaimer = "\n\nDisclaimer: This AI system assists doctors and does not replace professional medical diagnosis."
    return explanation + disclaimer

ai_service = AIService()
