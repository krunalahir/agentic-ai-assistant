#!/bin/bash

# Agentic AI Assistant - Startup Script
# This script starts both FastAPI backend and Streamlit frontend

echo "🤖 Starting Agentic AI Assistant..."
echo ""

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activate virtual environment
echo "📦 Activating virtual environment..."
source .venv/bin/activate

# Check if FastAPI is already running
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ FastAPI backend already running on port 8000"
else
    echo "🚀 Starting FastAPI backend on http://localhost:8000"
    python src/backend/api.py &
    sleep 3
fi

# Check if Streamlit is already running
if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null ; then
    echo "✅ Streamlit frontend already running on port 8501"
else
    echo "🎨 Starting Streamlit frontend on http://localhost:8501"
    streamlit run src/frontend/streamlit_fastapi.py --server.address localhost --server.port 8501 &
    sleep 3
fi

echo ""
echo "✅ Application started successfully!"
echo ""
echo "📡 FastAPI Backend:  http://localhost:8000"
echo "🖥️  Streamlit Frontend: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for user interrupt
wait
