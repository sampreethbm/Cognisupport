import pandas as pd
import numpy as np
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# 1. Generate Synthetic Dataset (100+ Samples)
def generate_data():
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
        ] * 5, # Replicate to get > 100 samples
        'category': (
            ['Hardware'] * 20 +
            ['Network'] * 20 +
            ['Software'] * 20 +
            ['Security'] * 20 +
            ['Account Access'] * 20
        ) * 5
    }
    return pd.DataFrame(data)

def train_model():
    print("Generating synthetic data...")
    df = generate_data()
    
    X_train, X_test, y_train, y_test = train_test_split(df['text'], df['category'], test_size=0.2, random_state=42)
    
    # System Engineering: LinearSVC chosen for efficiency on short text classification tasks.
    # TfidfVectorizer converts text to numerical features based on term importance.
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), stop_words='english')),
        ('clf', LinearSVC(random_state=42, dual='auto'))
    ])
    
    print("Training model...")
    pipeline.fit(X_train, y_train)
    
    print("Model Performance:")
    print(classification_report(y_test, pipeline.predict(X_test)))
    
    # Save the model
    joblib.dump(pipeline, 'model.joblib')
    print("Model saved to model.joblib")

if __name__ == "__main__":
    train_model()
