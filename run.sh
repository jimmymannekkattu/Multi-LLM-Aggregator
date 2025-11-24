#!/bin/bash

# AI Nexus - One-Click Startup Script

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Starting AI Nexus...${NC}"

# 1. Check/Create Virtual Environment
if [ ! -d "venv" ]; then
    echo -e "${BLUE}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    echo -e "${BLUE}⬇️ Installing dependencies...${NC}"
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# 2. Start Backend (FastAPI) in background
echo -e "${GREEN}🔌 Starting Backend API (Port 8000)...${NC}"
uvicorn api:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to initialize
sleep 2

# 3. Start Frontend (Streamlit)
echo -e "${GREEN}🖥️ Starting Frontend UI (Port 8501)...${NC}"
streamlit run app.py &
FRONTEND_PID=$!

echo -e "${BLUE}✅ AI Nexus is running!${NC}"
echo -e "   - Desktop App: http://localhost:8501"
echo -e "   - Mobile API:  http://localhost:8000"
echo -e "${BLUE}Press Ctrl+C to stop all services.${NC}"

# 4. Handle Shutdown
trap "kill $BACKEND_PID $FRONTEND_PID; exit" SIGINT SIGTERM

# Keep script running
wait
