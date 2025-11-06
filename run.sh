#!/bin/bash

# Run Script for Streamlit Visualization Dashboard
# Activates virtual environment and runs the application

echo "🚀 Starting Streamlit Visualization Dashboard..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found!"
    echo "Please run ./setup.sh to install dependencies"
    exit 1
fi

# Run the application
echo "📱 Opening browser at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the application"
echo ""

streamlit run app.py
