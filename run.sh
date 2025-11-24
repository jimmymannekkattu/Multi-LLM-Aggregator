#!/bin/bash

# AI Nexus - One-Click Startup Script
echo "🤖 Starting AI Nexus..."

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Start backend API in background
echo "🚀 Starting API server..."
uvicorn api:app --host 0.0.0.0 --port 8000 --reload > /dev/null 2>&1 &
API_PID=$!

# Start Streamlit in background
echo "🎨 Starting Desktop App..."
streamlit run app.py --server.headless=true > /dev/null 2>&1 &
STREAMLIT_PID=$!

# Give services time to start
sleep 3

echo ""
echo "✅ AI Nexus is running!"
echo ""
echo "📍 Choose your interface:"
echo "   Landing Page: file://$(pwd)/index.html"
echo "   Desktop App:  http://localhost:8501"
echo "   Web Chat:     file://$(pwd)/examples/chat-full.html"
echo "   API Docs:     http://localhost:8000/docs"
echo ""

# Open landing page
if command -v xdg-open > /dev/null; then
    xdg-open "$(pwd)/index.html" 2>/dev/null
elif command -v open > /dev/null; then
    open "$(pwd)/index.html" 2>/dev/null
fi

echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $API_PID $STREAMLIT_PID 2>/dev/null; echo ''; echo '👋 AI Nexus stopped'; exit" INT
wait
