#!/bin/bash

# FastAPI Server Stop Script

echo "=========================================="
echo "  Stopping FastAPI Server"
echo "=========================================="
echo ""

# Find and kill uvicorn processes
PIDS=$(pgrep -f "uvicorn app.main:app")

if [ -z "$PIDS" ]; then
    echo "ℹ️  No FastAPI server is currently running"
else
    echo "🛑 Found running server(s) with PID(s): $PIDS"
    echo "   Stopping..."
    pkill -f "uvicorn app.main:app"
    sleep 1
    
    # Check if killed successfully
    STILL_RUNNING=$(pgrep -f "uvicorn app.main:app")
    if [ -z "$STILL_RUNNING" ]; then
        echo "✅ Server stopped successfully"
    else
        echo "⚠️  Server still running, forcing kill..."
        pkill -9 -f "uvicorn app.main:app"
        sleep 1
        echo "✅ Server force stopped"
    fi
fi

echo ""
echo "=========================================="
echo "Server status: STOPPED"
echo "=========================================="
echo ""
echo "To start the server again, run:"
echo "   ./start_server.sh"
echo ""

