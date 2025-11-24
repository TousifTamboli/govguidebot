#!/bin/bash

echo "========================================"
echo "GovGuideBot - Automated Setup Script"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[ERROR]${NC} Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}[OK]${NC} Python is installed: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo -e "${YELLOW}[INFO]${NC} Virtual environment already exists"
else
    echo "[STEP 1/5] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[ERROR]${NC} Failed to create virtual environment"
        exit 1
    fi
    echo -e "${GREEN}[OK]${NC} Virtual environment created"
fi
echo ""

# Activate virtual environment
echo "[STEP 2/5] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Failed to activate virtual environment"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} Virtual environment activated"
echo ""

# Upgrade pip
echo "[STEP 3/5] Upgrading pip..."
python -m pip install --upgrade pip --quiet
echo -e "${GREEN}[OK]${NC} Pip upgraded"
echo ""

# Install dependencies
echo "[STEP 4/5] Installing dependencies (this may take 2-5 minutes)..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo -e "${RED}[ERROR]${NC} Failed to install dependencies"
    exit 1
fi
echo -e "${GREEN}[OK]${NC} All dependencies installed"
echo ""

# Check if .env file exists
echo "[STEP 5/5] Checking environment configuration..."
if [ -f ".env" ]; then
    echo -e "${GREEN}[OK]${NC} .env file exists"
else
    echo -e "${YELLOW}[WARNING]${NC} .env file not found"
    echo ""
    echo "Please create a .env file with your Google API key:"
    echo ""
    echo "1. Get your API key from: https://aistudio.google.com/app/apikey"
    echo "2. Create a file named .env in this directory"
    echo "3. Add this line: GOOGLE_API_KEY=your_api_key_here"
    echo ""
    read -p "Enter your Google API Key (or press Enter to skip): " api_key
    if [ ! -z "$api_key" ]; then
        echo "GOOGLE_API_KEY=$api_key" > .env
        echo -e "${GREEN}[OK]${NC} .env file created"
    else
        echo -e "${YELLOW}[WARNING]${NC} Skipped .env creation. You'll need to create it manually."
    fi
fi
echo ""

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To run the application:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python app.py"
echo "  3. Open browser to: http://localhost:7862"
echo ""
echo "Available versions:"
echo "  - python app.py              (Basic version)"
echo "  - python app_modern.py       (Modern UI)"
echo "  - python app_ultra_modern.py (Full-featured with document checker)"
echo ""
