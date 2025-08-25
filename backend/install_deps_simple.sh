#!/bin/bash

# Simple Portfolio Research Dependencies Installation Script

echo "Installing Portfolio Research Dependencies..."
echo "============================================"

# Detect Python executable
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo "❌ Error: Python not found. Please install Python 3.7+ first."
    exit 1
fi

echo "Using Python: $PYTHON_CMD"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    $PYTHON_CMD -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install core dependencies
echo "Installing core dependencies..."
pip install beautifulsoup4
pip install trafilatura
pip install lxml

# Install NLP dependencies
echo "Installing NLP dependencies..."
pip install keybert
pip install spacy
pip install sumy
pip install sentence-transformers

# Download spaCy model
echo "Downloading spaCy English model..."
python -m spacy download en_core_web_sm

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "To test the service, run:"
echo "  python test_portfolio.py"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
