#!/bin/bash

# Script to check if virtual environment is active and properly configured

echo "=========================================="
echo "  Environment Check"
echo "=========================================="
echo ""

# Check if script is run from project directory
if [ ! -f "app/main.py" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "   Run: python3 -m venv venv"
    exit 1
else
    echo "✅ Virtual environment exists"
fi

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    echo "⚠️  Virtual environment is NOT activated"
    echo "   Run: source venv/bin/activate"
    echo ""
    echo "Activating now for this check..."
    source venv/bin/activate
else
    echo "✅ Virtual environment is ACTIVE"
    echo "   Path: $VIRTUAL_ENV"
fi

echo ""
echo "🐍 Python Information:"
echo "   Version: $(python --version)"
echo "   Location: $(which python)"
echo ""

# Check if dependencies are installed
echo "📦 Checking Dependencies:"

check_package() {
    python -c "import $1" 2>/dev/null
    if [ $? -eq 0 ]; then
        VERSION=$(python -c "import $1; print(getattr($1, '__version__', 'installed'))")
        echo "   ✅ $2: $VERSION"
        return 0
    else
        echo "   ❌ $2: NOT INSTALLED"
        return 1
    fi
}

MISSING=0

check_package "fastapi" "FastAPI" || MISSING=1
check_package "uvicorn" "Uvicorn" || MISSING=1
check_package "pydantic" "Pydantic" || MISSING=1
check_package "docx" "python-docx" || MISSING=1
check_package "reportlab" "ReportLab" || MISSING=1
check_package "structlog" "Structlog" || MISSING=1

echo ""

if [ $MISSING -eq 1 ]; then
    echo "⚠️  Some dependencies are missing!"
    echo "   Run: pip install -r requirements.txt"
    exit 1
else
    echo "✅ All core dependencies installed"
fi

echo ""
echo "🎯 Application Check:"

# Try to import the app
python -c "from app.main import app; print('   ✅ FastAPI app loads successfully')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "   ❌ Failed to load FastAPI app"
    echo "   There may be import errors. Check the logs above."
    exit 1
fi

echo ""
echo "=========================================="
echo "✅ Everything looks good!"
echo "=========================================="
echo ""
echo "To start the server, run:"
echo "   ./start_server.sh"
echo ""
echo "Or manually:"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload"
echo ""

