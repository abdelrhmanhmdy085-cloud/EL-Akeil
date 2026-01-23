@echo off
REM ================================
REM El Akeil - Windows Batch Setup
REM ================================

setlocal enabledelayedexpansion

cls
echo.
echo ╔════════════════════════════════════════╗
echo ║   El Akeil - Windows Setup Batch      ║
echo ╚════════════════════════════════════════╝
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.x and add it to your PATH
    pause
    exit /b 1
)

echo ✅ Python detected

REM Change to project directory
cd /d "D:\3abdo\El Akeil"
if errorlevel 1 (
    echo ❌ Failed to change directory to project
    pause
    exit /b 1
)

echo ℹ️  Project directory: %cd%

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo ℹ️  Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo ℹ️  Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✅ Virtual environment activated

REM Upgrade pip
echo ℹ️  Upgrading pip...
python -m pip install --upgrade pip >nul 2>&1

REM Install requirements
if exist "requirements.txt" (
    echo ℹ️  Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
    echo ✅ Dependencies installed
) else (
    echo ⚠️  requirements.txt not found
)

REM Set environment variables
set FLASK_ENV=development
set FLASK_DEBUG=1
set SECRET_KEY=change_this_secret_key_in_production

echo ℹ️  Environment variables set
echo.

REM Start server
echo ╔════════════════════════════════════════╗
echo ║      Setup Complete! Starting...       ║
echo ╚════════════════════════════════════════╝
echo.
echo 🚀 Starting Flask development server...
echo 📱 Access the application at: http://localhost:5000
echo 🛑 Press Ctrl+C to stop the server
echo.

cd /d "D:\3abdo\El Akeil\src\backend"
python app.py

pause
