from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import os
import random
from typing import Dict

# Initialize FastAPI app
app = FastAPI(title="CogniSupport API")

# CORS Middleware for localhost development
# System Engineering: Allowing all origins for ease of development in WSL2/Localhost environment.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model
MODEL_PATH = "model.joblib"
try:
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        # Fallback or strict error depending on requirements. 
        # For this setup, we assume model is trained via ml_engine.py first.
        print("Model not found. Please run ml_engine.py first.")
        model = None
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# Pydantic Models
class TicketRequest(BaseModel):
    title: str
    description: str

class TicketResponse(BaseModel):
    category: str
    priority: str
    confidence: str

# Utility for priority based on keywords
def determine_priority(text: str) -> str:
    text_lower = text.lower()
    if any(k in text_lower for k in ["urgent", "critical", "blocking", "down", "fail"]):
        return "High"
    if any(k in text_lower for k in ["slow", "warn", "error", "bug"]):
        return "Medium"
    return "Low"

@app.post("/analyze", response_model=TicketResponse)
async def analyze_ticket(ticket: TicketRequest):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Combine title and description for better context
        full_text = f"{ticket.title} {ticket.description}"
        
        # Predict Category
        prediction = model.predict([full_text])[0]
        
        # Calculate Confidence 
        # LinearSVC uses decision_function (signed distance to hyperplane). 
        # We convert this to a pseudo-probability/confidence score.
        decision_scores = model.decision_function([full_text])
        max_score =  max(decision_scores[0]) if hasattr(decision_scores[0], '__iter__') else decision_scores[0]
        
        # Simple heuristic for confidence string
        if max_score > 1.0:
            confidence = "High"
        elif max_score > 0.5:
            confidence = "Medium"
        else:
            confidence = "Low"

        priority = determine_priority(full_text)
        
        return TicketResponse(
            category=prediction,
            priority=priority,
            confidence=confidence
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats")
async def get_stats():
    # Mock data for dashboard
    return {
        "tickets_resolved_today": random.randint(10, 50),
        "active_tickets": random.randint(5, 20),
        "avg_response_time": f"{random.randint(5, 15)} mins"
    }

@app.get("/")
async def root():
    return {"message": "CogniSupport API is running"}

# Serve React App in Production (Docker)
from fastapi.staticfiles import StaticFiles
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
