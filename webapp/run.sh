#!/bin/bash

# Universal Translator Web App Run Script

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Error: .env file not found!"
    echo "Please run ./setup.sh first or create .env from .env.example"
    exit 1
fi

# Run the Flask application
echo "Starting Universal Translator Web App..."
echo "Access the app at: http://localhost:5000"
echo ""
python app.py
