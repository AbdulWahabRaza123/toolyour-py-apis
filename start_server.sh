#!/bin/bash

# FastAPI Server Startup Script
# This script ensures the virtual environment is activated before starting the server

echo "=========================================="
echo "  FastAPI Document Converter Backend"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python3 -m venv venv"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Verify we're in the virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Failed to activate virtual environment!"
    exit 1
fi

echo "✅ Virtual environment activated: $VIRTUAL_ENV"
echo ""

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import fastapi, uvicorn" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ Required packages not found!"
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Dependencies verified"
echo ""

# Display Python and package info
echo "🐍 Python version: $(python --version)"
echo "📍 Using Python from: $(which python)"
echo "📦 FastAPI version: $(python -c 'import fastapi; print(fastapi.__version__)')"
echo ""

# Start the server
echo "🚀 Starting FastAPI server..."
echo "📖 API Documentation: http://localhost:8000/docs"
echo "📖 ReDoc: http://localhost:8000/redoc"
echo "💚 Health Check: http://localhost:8000/health"
echo ""
echo "Press CTRL+C to stop the server"
echo "=========================================="
echo ""

# Run uvicorn with reload for development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

