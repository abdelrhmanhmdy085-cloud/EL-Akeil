@echo off
REM ================================
REM El Akeil - Quick Start Batch
REM ================================

cd /d "D:\3abdo\El Akeil"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Set environment variables
set FLASK_ENV=development
set FLASK_DEBUG=1
set SECRET_KEY=change_this_secret_key_in_production

cls
echo.
echo 🚀 Starting El Akeil Server...
echo 📱 Access at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop
echo.

cd /d "D:\3abdo\El Akeil\src\backend"
python app.py

pause
