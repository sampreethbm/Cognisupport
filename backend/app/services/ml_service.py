import joblib
import os
from app.core.config import settings

class MLService:
    def __init__(self):
        self.model = None
        self.load_model()

    def load_model(self):
        try:
            if os.path.exists(settings.MODEL_PATH):
                self.model = joblib.load(settings.MODEL_PATH)
                print(f"Model loaded from {settings.MODEL_PATH}")
            else:
                print(f"Model not found at {settings.MODEL_PATH}. Prediction will be unavailable.")
                self.model = None
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def predict(self, title: str, description: str):
        if not self.model:
            return None # Will handle in router or return specific error state
        
        full_text = f"{title} {description}"
        
        # Predict Category
        prediction = self.model.predict([full_text])[0]
        
        # Calculate Confidence 
        decision_scores = self.model.decision_function([full_text])
        max_score = max(decision_scores[0]) if hasattr(decision_scores[0], '__iter__') else decision_scores[0]
        
        if max_score > 1.0:
            confidence = "High"
        elif max_score > 0.5:
            confidence = "Medium"
        else:
            confidence = "Low"

        priority = self._determine_priority(full_text)
        
        return {
            "category": prediction,
            "priority": priority,
            "confidence": confidence
        }

    def _determine_priority(self, text: str) -> str:
        text_lower = text.lower()
        if any(k in text_lower for k in ["urgent", "critical", "blocking", "down", "fail"]):
            return "High"
        if any(k in text_lower for k in ["slow", "warn", "error", "bug"]):
            return "Medium"
        return "Low"

ml_service = MLService()
