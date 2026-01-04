#!/bin/bash

# Lynx Resource Planning System - Run Script
# This script sets up and runs the enhanced application

echo "🦊 Lynx Resource Planning System - Enhanced Version"
echo "=================================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if dependencies are installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    echo "✅ Dependencies installed"
    echo ""
else
    echo "✅ Dependencies already installed"
    echo ""
fi

# Run the application
echo "🚀 Starting Lynx Resource Planning System..."
echo "   The app will open in your browser at http://localhost:8501"
echo ""
streamlit run app.py

