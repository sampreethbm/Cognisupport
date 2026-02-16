# CogniSupport 🧠
> **AI-Driven IT Helpdesk & Ticketing System**

CogniSupport is a modern, intelligent helpdesk that automates ticket classification using Machine Learning. It provides **real-time AI insights** to users before they submit a ticket, ensuring requests are routed to the right team instantly.

---

## ✨ Features
- **🔮 Live AI Diagnostics**: Predicts issue category and priority *while typing*.
- **⚡ Auto-Triage**: Automatically routes tickets (Hardware, Network, Software, etc.).
- **🛡️ Secure & Scalable**: Decoupled architecture with FastAPI & React.
- **📊 Admin Dashboard**: Real-time tracking of ticket flow and team performance.

## 🚀 Quick Start
### Option 1: Docker (Recommended)
Run the entire stack with a single command:
```bash
docker-compose up --build
```
- **App**: `http://localhost:5173`
- **API**: `http://localhost:8000/docs`

### Option 2: Manual Setup
**Backend** (Python 3.10+)
```bash
cd backend
pip install -r requirements.txt
python ml_engine.py  # Train the ML model
uvicorn main:app --reload
```

**Frontend** (Node.js 18+)
```bash
cd frontend
npm install
npm run dev
```

## 🛠️ Tech Stack
- **Frontend**: React 18, Vite, Tailwind CSS (IBM Design Language)
- **Backend**: FastAPI (Python), Scikit-learn (Machine Learning)
- **Database**: SQLite (Dev) / PostgreSQL (Prod)

---
*Built with ❤️ by [Your Name]*
