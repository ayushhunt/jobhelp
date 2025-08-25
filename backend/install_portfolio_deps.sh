#!/bin/bash

# Portfolio Research Service Dependencies Installation Script

echo "Installing Portfolio Research Service Dependencies..."
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install core dependencies
echo "Installing core dependencies..."
pip install beautifulsoup4==4.12.2
pip install trafilatura
pip install lxml==4.9.3

# Install NLP dependencies
echo "Installing NLP dependencies..."
pip install keybert==0.7.0
pip install spacy==3.7.2
pip install sumy==0.11.0
pip install sentence-transformers==2.2.2

# Download spaCy model
echo "Downloading spaCy English model..."
python -m spacy download en_core_web_sm

# Install additional dependencies that might be needed
echo "Installing additional dependencies..."
pip install nltk
pip install textblob

# Update requirements.txt
echo "Updating requirements.txt..."
pip freeze > requirements.txt

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "To test the service, run:"
echo "  python test_portfolio.py"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
echo "Note: You may need to restart your IDE/editor to pick up the new dependencies."

