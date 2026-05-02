#!/bin/bash

# ── SentimentAI — One-command startup ─────────────────────────────────────
set -e

GREEN='\033[0;32m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo ""
echo -e "${CYAN}  ╔══════════════════════════════════╗${NC}"
echo -e "${CYAN}  ║    🧠  SentimentAI Dashboard     ║${NC}"
echo -e "${CYAN}  ╚══════════════════════════════════╝${NC}"
echo ""

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "❌ Python 3 not found. Please install Python 3.9+"
  exit 1
fi

# Install backend deps
echo -e "${YELLOW}▸ Installing backend dependencies...${NC}"
cd backend
pip install -r requirements.txt -q
cd ..

# Launch FastAPI in background
echo -e "${YELLOW}▸ Starting FastAPI backend on port 8000...${NC}"
cd backend
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!
cd ..

# Wait for API to come up
sleep 2

# Health check
if curl -sf http://localhost:8000/health > /dev/null 2>&1; then
  echo -e "${GREEN}✅ Backend running at http://localhost:8000${NC}"
else
  echo -e "${YELLOW}⚠ Backend starting (may take a moment)...${NC}"
fi

# Serve frontend
echo -e "${YELLOW}▸ Starting frontend on port 3000...${NC}"
cd frontend
if command -v python3 &>/dev/null; then
  python3 -m http.server 3000 &
  FRONTEND_PID=$!
fi
cd ..

echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}  🚀 SentimentAI is running!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "  Dashboard  →  ${CYAN}http://localhost:3000${NC}"
echo -e "  API Docs   →  ${CYAN}http://localhost:8000/docs${NC}"
echo -e "  API Health →  ${CYAN}http://localhost:8000/health${NC}"
echo ""
echo -e "  Press ${YELLOW}Ctrl+C${NC} to stop all services"
echo ""

# Wait and clean up on exit
trap "echo ''; echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Done.'" EXIT
wait
