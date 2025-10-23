#!/bin/bash

# Check FastAPI Server Status Script

echo "=========================================="
echo "  FastAPI Server Status Check"
echo "=========================================="
echo ""

# Check if virtual environment is active
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment: NOT ACTIVE"
    echo "   Activate with: source venv/bin/activate"
else
    echo "✅ Virtual environment: ACTIVE"
    echo "   Path: $VIRTUAL_ENV"
fi

echo ""

# Check Python location
PYTHON_PATH=$(which python)
if [[ "$PYTHON_PATH" == *"venv"* ]]; then
    echo "✅ Python: Using venv"
    echo "   Location: $PYTHON_PATH"
else
    echo "⚠️  Python: Using system Python"
    echo "   Location: $PYTHON_PATH"
fi

echo ""
echo "🐍 Python version: $(python --version 2>&1)"
echo ""

# Check if server is running
PIDS=$(pgrep -f "uvicorn app.main:app")

if [ -z "$PIDS" ]; then
    echo "🔴 Server Status: NOT RUNNING"
    echo ""
    echo "To start the server:"
    echo "   ./start_server.sh"
else
    echo "🟢 Server Status: RUNNING"
    echo "   PID(s): $PIDS"
    echo ""
    
    # Try to reach the server
    if command -v curl &> /dev/null; then
        echo "📡 Testing connection..."
        HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null)
        if [ $? -eq 0 ]; then
            echo "✅ Server responding at http://localhost:8000"
            echo "   Response: $HEALTH"
        else
            echo "⚠️  Server process running but not responding"
        fi
    fi
    
    echo ""
    echo "📖 API Documentation: http://localhost:8000/docs"
    echo "💚 Health Check: http://localhost:8000/health"
    echo ""
    echo "To stop the server:"
    echo "   ./stop_server.sh"
fi

echo ""
echo "=========================================="
echo ""

