#!/bin/bash

# Quick Start Script for Streamlit Visualization Dashboard
# This script sets up the project and runs the application

echo "🚀 Starting Streamlit Visualization Dashboard Setup..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q
echo "✅ Pip upgraded"
echo ""

# Install requirements
echo "📥 Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt -q
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created"
    echo "⚠️  Please edit .env file with your configuration"
else
    echo "✅ .env file already exists"
fi
echo ""

# Create data and assets directories
echo "📁 Creating data directories..."
mkdir -p data assets
echo "✅ Directories created"
echo ""

# Check if streamlit secrets exist
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "ℹ️  Streamlit secrets file not found"
    echo "   You can create it later if needed using .streamlit/secrets.toml.example"
fi
echo ""

echo "🎉 Setup complete!"
echo ""
echo "To run the application:"
echo "  1. Activate the virtual environment: source venv/bin/activate"
echo "  2. Run the app: streamlit run app.py"
echo ""
echo "Or simply run: ./run.sh"
echo ""

# Ask if user wants to start the app
read -p "Do you want to start the application now? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🚀 Starting Streamlit application..."
    echo "📱 Opening browser at http://localhost:8501"
    echo ""
    echo "Press Ctrl+C to stop the application"
    echo ""
    streamlit run app.py
fi
