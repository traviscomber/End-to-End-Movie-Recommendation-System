@echo off
REM Movie Recommendation System startup script for Windows

echo Starting Movie Recommendation System...
echo =======================================

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt > nul 2>&1

REM Run the app
echo.
echo Starting Flask application...
echo =======================================
echo The application will be available at:
echo http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo =======================================
echo.

python app.py

pause
