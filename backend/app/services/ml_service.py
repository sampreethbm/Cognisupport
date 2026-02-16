import joblib
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from app.core.config import settings

class MLService:
    def __init__(self):
        self.model = None
        self.load_or_train_model()

    def load_or_train_model(self):
        try:
            if os.path.exists(settings.MODEL_PATH):
                self.model = joblib.load(settings.MODEL_PATH)
                print(f"Model loaded from {settings.MODEL_PATH}")
            else:
                print(f"Model not found at {settings.MODEL_PATH}. Training new model...")
                self.train_model()
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = None

    def train_model(self):
        try:
            # Generate synthetic data
            df = self._generate_data()
            
            X_train, X_test, y_train, y_test = train_test_split(df['text'], df['category'], test_size=0.2, random_state=42)
            
            pipeline = Pipeline([
                ('tfidf', TfidfVectorizer(ngram_range=(1,2), stop_words='english')),
                ('clf', LinearSVC(random_state=42, dual='auto'))
            ])
            
            pipeline.fit(X_train, y_train)
            
            # Save the model
            joblib.dump(pipeline, settings.MODEL_PATH)
            self.model = pipeline
            print(f"Model trained and saved to {settings.MODEL_PATH}")
        except Exception as e:
            print(f"Failed to train model: {e}")

    def _generate_data(self):
        data = {
            'text': [
                # Hardware
                "Laptop screen is flickering", "Mouse not working", "Keyboard keys stuck", "Printer jamming", "Monitor won't turn on",
                "Laptop battery drains fast", "External hard drive not detected", "Webcam shows black screen", "Touchpad unresponsive", "Headset microphone broken",
                "Docking station not charging", "Projector bulb burnt out", "Scanner not connecting", "USB port loose", "Fan making loud noise",
                "Laptop overheating", "Screen has dead pixels", "Power adapter frayed", "Bluetooth mouse lagging", "Second monitor no signal",
                
                # Network
                "Cannot connect to WiFi", "Internet is very slow", "VPN connection failed", "DNS resolution error", "Packet loss high",
                "Network drive inaccessible", "Zoom call dropping", "Ethernet cable broken", "Firewall blocking site", "IP address conflict",
                "WiFi password incorrect", "Router needs restart", "Download speed slow", "Upload failed", "Cannot access intranet",
                "VPN keeps disconnecting", "Ping is too high", "Default gateway unreachable", "Network printer offline", "SSL certificate error",

                # Software
                "Outlook crashing on startup", "Excel visualization error", "Adobe Reader not opening", "Chrome keeps freezing", "Windows update failed",
                "Slack messages not syncing", "Teams audio issues", "Jira ticket not saving", "VS Code extensions missing", "Python environment broken",
                "Java update required", "Browser cache issue", "Software license expired", "Application access denied", "CRM login loop",
                "SharePoint file locked", "OneDrive not syncing", "Zoom update stuck", "Antivirus blocking install", "OS activated warning",

                # Security
                "Suspicious email attachment", "Password reset required", "2FA code not received", "Phishing attempt detected", "Account locked out",
                "Virus alert popup", "Malware scan requested", "Unauthorized login attempt", "Security token expired", "Badge access denied",
                "Encrypted file unreadable", "USB drive blocked", "Admin rights needed", "Compromised credentials", "Spam filter too aggressive",
                "Unusual activity detected", "Screen lock policy", "Password change forced", "VPN certificate invalid", "Data breach suspected",

                # Account Access
                "Forgot my password", "Cannot login to email", "User account disabled", "Need access to shared folder", "Create new user account",
                "Profile picture update", "Change display name", "Unlock AD account", "Permission denied for folder", "Role update request",
                "SSO login failure", "MFA device lost", "Account expiration warning", "Guest wifi access", "Offboarding user request",
                "Onboarding setup needed", "Email alias request", "Distribution list add", "Slack channel access", "VPN access request"
            ] * 5, 
            'category': (
                ['Hardware'] * 20 +
                ['Network'] * 20 +
                ['Software'] * 20 +
                ['Security'] * 20 +
                ['Account Access'] * 20
            ) * 5
        }
        return pd.DataFrame(data)

    def predict(self, title: str, description: str):
        if not self.model:
            return None 
        
        full_text = f"{title} {description}"
        
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
