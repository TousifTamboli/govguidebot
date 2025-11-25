@echo off
echo ========================================
echo GovGuideBot - Automated Setup Script
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [OK] Python is installed
echo.

REM Check if virtual environment exists
if exist "venv\" (
    echo [INFO] Virtual environment already exists
) else (
    echo [STEP 1/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [OK] Virtual environment created
)
echo.

REM Activate virtual environment and install dependencies
echo [STEP 2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment activated
echo.

echo [STEP 3/5] Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip upgraded
echo.

echo [STEP 4/5] Installing dependencies (this may take 2-5 minutes)...
echo [INFO] Installing core packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    echo [INFO] Trying to install packages individually...
    pip install gradio google-generativeai python-dotenv certifi
    pip install langchain langchain-google-genai langchain-core
    pip install chromadb pandas numpy
    pip install requests beautifulsoup4 lxml schedule
    pip install pytesseract opencv-python PyMuPDF pdf2image Pillow
    if errorlevel 1 (
        echo [ERROR] Some packages failed to install
        echo [INFO] You can still run the basic version without document checker
        echo [INFO] Run: python app.py
    )
)
echo [OK] Dependencies installation completed
echo.

REM Check if .env file exists
echo [STEP 5/5] Checking environment configuration...
if exist ".env" (
    echo [OK] .env file exists
) else (
    echo [WARNING] .env file not found
    echo.
    echo Please create a .env file with your Google API key:
    echo.
    echo 1. Get your API key from: https://aistudio.google.com/app/apikey
    echo 2. Create a file named .env in this directory
    echo 3. Add this line: GOOGLE_API_KEY=your_api_key_here
    echo.
    set /p api_key="Enter your Google API Key (or press Enter to skip): "
    if not "!api_key!"=="" (
        echo GOOGLE_API_KEY=!api_key!> .env
        echo [OK] .env file created
    ) else (
        echo [WARNING] Skipped .env creation. You'll need to create it manually.
    )
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To run the application:
echo   1. Make sure virtual environment is activated: venv\Scripts\activate
echo   2. Run: python app.py
echo   3. Open browser to: http://localhost:7862
echo.
echo Available versions:
echo   - python app.py              (Basic version)
echo   - python app_modern.py       (Modern UI)
echo   - python app_ultra_modern.py (Full-featured with document checker)
echo.
pause
