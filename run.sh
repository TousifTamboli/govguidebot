#!/bin/bash

echo "Starting GovGuideBot..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[ERROR] Virtual environment not found!"
    echo "Please run ./setup.sh first"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "[WARNING] .env file not found!"
    echo "Please create .env file with your Google API key"
    echo ""
fi

# Activate virtual environment
source venv/bin/activate

# Run the application
echo "Running app.py..."
echo ""
echo "The app will open in your browser at: http://localhost:7862"
echo "Press Ctrl+C to stop the application"
echo ""
python app.py
