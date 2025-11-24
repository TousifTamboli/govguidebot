@echo off
echo Starting GovGuideBot...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Check if .env file exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Please create .env file with your Google API key
    echo.
    pause
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the application
echo Running app.py...
echo.
echo The app will open in your browser at: http://localhost:7862
echo Press Ctrl+C to stop the application
echo.
python app.py

pause
