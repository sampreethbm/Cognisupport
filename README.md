# CogniSupport: AI-Driven IT Helpdesk

CogniSupport is a modern, intelligent IT helpdesk system that automates ticket classification and prioritization using Machine Learning. Built with a **React (Vite)** frontend and **FastAPI** backend, it provides real-time "Live AI Insights" to users before they even submit a ticket, streamlining support workflows.

## 🚀 Features

- **Live AI Insight**: Real-time category and priority prediction as users type (Debounced).
- **Auto-Triage**: Automatically routes tickets to Hardware, Network, Software, Security, or Account Access teams.
- **Urgency Detection**: NLP-based keyword analysis determines ticket priority (Low/Medium/High).
- **Dashboard**: Admin view to track incoming tickets and performance stats.
- **Production Ready**: Containerized with Docker and served via a high-performance ASGI server.

## 🛠️ Tech Stack

### Backend
- **FastAPI (Python)**: High-performance, asynchronous web framework.
- **Scikit-learn**: TF-IDF Vectorizer + LinearSVC pipeline for efficient text classification.
- **Joblib**: Model serialization.
- **Pydantic**: Robust data validation.

### Frontend
- **React 18 + Vite**: Lightning-fast frontend tooling.
- **Tailwind CSS**: Utility-first styling with a custom "IBM Blue" enterprise theme.
- **Axios**: Efficient HTTP client for API integration.

## 🔧 Installation & Setup

### Prerequisites
- Docker & Docker Compose (Recommended)
- OR Python 3.10+ and Node.js 18+

### Option 1: Docker (Single Command)
1. Build and run the container:
   ```bash
   docker build -t cognisupport .
   docker run -p 8000:8000 cognisupport
   ```
2. Open `http://localhost:8000` to view the app.

### Option 2: Local Development (WSL2/Linux/Mac)

**Backend:**
1. Navigate to `backend/`:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```
2. Train the model:
   ```bash
   python ml_engine.py
   ```
3. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

**Frontend:**
1. Navigate to `frontend/`:
   ```bash
   cd frontend
   npm install
   ```
2. Start the dev server:
   ```bash
   npm run dev
   ```
3. Open `http://localhost:5173`.

## 💼 Technical Impact (Resume Points)

*   **Full-Stack Architecture**: Designed and implemented a decoupled architecture using **FastAPI** and **React**, enabling independent scaling and development velocity.
*   **AI Integration**: Engineered a **Scikit-learn pipeline (TF-IDF + LinearSVC)** to classify IT support tickets with high accuracy, reducing manual triage time by an estimated 40%.
*   **Real-Time UX**: Implemented a **debounced AI feedback loop** in React, providing instant user guidance and reducing miscategorized tickets.
*   **Containerization**: Optimized deployment using a **multi-stage Docker build**, reducing image size and ensuring consistent environments across development and production.
*   **System Engineering**: Selected **FastAPI** for its asynchronous capabilities and **Pydantic** integration, ensuring type safety and high concurrency for API requests.
