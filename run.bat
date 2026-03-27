@echo off
echo Starting GovGuideBot...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo [INFO] Virtual environment not found. Running setup...
    call setup.bat --no-pause
)

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found! Let's set it up...
    call setup.bat --no-pause
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
echo [INFO] Running app.py...
echo.
echo The app will open in your browser at: http://localhost:7862
echo Press Ctrl+C to stop the application
echo.

REM Open browser after a slight delay
start "" http://localhost:7862

python app.py

pause
