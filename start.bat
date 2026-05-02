@echo off
title SentimentAI Dashboard

echo.
echo   ==========================================
echo      SentimentAI Dashboard - Starting
echo   ==========================================
echo.

echo [1/3] Installing backend dependencies...
cd backend
pip install -r requirements.txt -q
cd ..

echo [2/3] Starting FastAPI backend on port 8000...
start "SentimentAI Backend" cmd /k "cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

timeout /t 3 /nobreak > nul

echo [3/3] Starting frontend on port 3000...
start "SentimentAI Frontend" cmd /k "cd frontend && python -m http.server 3000"

timeout /t 2 /nobreak > nul

echo.
echo   ==========================================
echo     SentimentAI is running!
echo   ==========================================
echo.
echo   Dashboard  -  http://localhost:3000
echo   API Docs   -  http://localhost:8000/docs
echo.

start "" "http://localhost:3000"

pause
