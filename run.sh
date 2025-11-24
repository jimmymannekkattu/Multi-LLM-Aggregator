#!/bin/bash

# AI Nexus - One-Click Startup Script
echo "🤖 Starting AI Nexus..."

# Determine VENV path
VENV_DIR="venv"
FALLBACK_VENV_DIR="$HOME/.ai-nexus/venv"

# Function to try creating venv
create_venv() {
    local target_dir=$1
    echo "📦 Attempting to create virtual environment in $target_dir..."
    
    # Try creating with standard command
    if python3 -m venv "$target_dir" 2>/dev/null; then
        return 0
    fi
    
    # Try with --copies (useful for some filesystems)
    if python3 -m venv "$target_dir" --copies 2>/dev/null; then
        return 0
    fi
    
    return 1
}

# Check/Create VENV
if [ -d "$VENV_DIR" ] && [ -f "$VENV_DIR/bin/activate" ]; then
    echo "✅ Found local virtual environment."
    source "$VENV_DIR/bin/activate"
elif [ -d "$FALLBACK_VENV_DIR" ] && [ -f "$FALLBACK_VENV_DIR/bin/activate" ]; then
    echo "✅ Found fallback virtual environment."
    source "$FALLBACK_VENV_DIR/bin/activate"
else
    # Try creating locally
    if create_venv "$VENV_DIR"; then
        echo "✅ Created local virtual environment."
        source "$VENV_DIR/bin/activate"
    else
        echo "⚠️  Could not create local venv (likely filesystem limitations)."
        echo "🔄 Trying fallback location: $FALLBACK_VENV_DIR"
        
        # Ensure parent dir exists
        mkdir -p "$(dirname "$FALLBACK_VENV_DIR")"
        
        if create_venv "$FALLBACK_VENV_DIR"; then
            echo "✅ Created fallback virtual environment."
            source "$FALLBACK_VENV_DIR/bin/activate"
        else
            echo "❌ Failed to create virtual environment anywhere."
            echo "Please install python3-venv and try again."
            exit 1
        fi
    fi
fi

# Install dependencies
echo "📥 Installing dependencies..."
$PIP_CMD install -r requirements.txt

# Create directory for g4f cookies (prevents errors)
mkdir -p har_and_cookies
chmod 777 har_and_cookies 2>/dev/null || true

# Start API Server
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
