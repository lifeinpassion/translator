#!/bin/bash

# Universal Translator Web App Setup Script

echo "=========================================="
echo "Universal Translator - Setup Script"
echo "=========================================="
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ Created .env file - please edit it with your API keys"
else
    echo ""
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p static/uploads
mkdir -p data
echo "✓ Directories created"

# Done
echo ""
echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your API keys"
echo "2. Activate the virtual environment: source venv/bin/activate"
echo "3. Run the application: python app.py"
echo "4. Open your browser to: http://localhost:5000"
echo ""
echo "For DeepL API key: https://www.deepl.com/pro-api"
echo "For OpenAI API key: https://platform.openai.com/"
echo "For Anthropic API key: https://console.anthropic.com/"
echo "For Google API key: https://makersuite.google.com/app/apikey"
echo ""
