from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from services import ai_service, generate_radiology_report, generate_patient_explanation
import uvicorn

app = FastAPI(title="MediMind API", description="AI Radiology Assistant Backend", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "MediMind API is running."}

@app.post("/upload_xray")
async def upload_xray(file: UploadFile = File(...)):
    """Uploads an image, runs inference, and returns all results at once (hackathon friendly workflow)."""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
        
    contents = await file.read()
    
    # 1. Predict
    predictions = ai_service.predict(contents)
    
    # 2. Get top class index if it's not normal
    # For a real pipeline we might extract index dynamically based on highest prob
    
    # 3. Generate Heatmap
    heatmap_base64 = ai_service.generate_heatmap(contents)
    
    # 4. Generate Report
    report = generate_radiology_report(predictions)
    
    # 5. Generate Patient Explanation
    explanation = generate_patient_explanation(report)
    
    return {
        "status": "success",
        "predictions": predictions,
        "heatmap": heatmap_base64,
        "report": report,
        "patient_explanation": explanation
    }

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
