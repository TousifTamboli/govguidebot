@echo off
echo ========================================
echo GovGuideBot - Quick Fix Installer
echo ========================================
echo.

echo [INFO] This will install only essential packages
echo [INFO] Compatible with Python 3.8-3.12
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment not found
    echo [INFO] Please run setup.bat first
    pause
    exit /b 1
)

echo [STEP 1/3] Installing core packages...
pip install gradio google-generativeai python-dotenv certifi

echo.
echo [STEP 2/3] Installing LangChain and database...
pip install langchain langchain-google-genai langchain-core chromadb pandas numpy

echo.
echo [STEP 3/3] Installing web scraping tools...
pip install requests beautifulsoup4 lxml schedule

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo You can now run the basic version:
echo   python app.py
echo.
echo For document validation (optional):
echo   pip install pytesseract opencv-python PyMuPDF pdf2image Pillow
echo.
pause
