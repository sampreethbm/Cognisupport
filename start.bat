@echo off
echo ==========================================
echo   CogniSupport - Setup & Startup Script
echo ==========================================

echo [1/4] Setting up Backend...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install backend requirements.
    pause
    exit /b %errorlevel%
)

echo [2/4] Starting Backend Server...
start "CogniSupport Backend" cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

echo [3/4] Setting up Frontend...
cd ../frontend
call npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies.
    pause
    exit /b %errorlevel%
)

echo [4/4] Starting Frontend Server...
start "CogniSupport Frontend" cmd /k "npm run dev"

echo ==========================================
echo   Application Started!
echo   Backend API: http://localhost:8000/docs
echo   Frontend UI: http://localhost:5173
echo ==========================================
cd ..
