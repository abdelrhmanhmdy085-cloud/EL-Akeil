# ================================
# El Akeil - Windows Setup Script
# ================================
# This script sets up the entire El Akeil application on Windows

param(
    [string]$Action = "full",
    [switch]$SkipVenv,
    [switch]$SkipDeps
)

# Color functions
function Write-Success {
    param([string]$Message)
    Write-Host "✅ $Message" -ForegroundColor Green
}

function Write-Info {
    param([string]$Message)
    Write-Host "ℹ️  $Message" -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$Message)
    Write-Host "⚠️  $Message" -ForegroundColor Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "❌ $Message" -ForegroundColor Red
}

# Check if running as admin
$isAdmin = [bool]([System.Security.Principal.WindowsIdentity]::GetCurrent().Groups -match "S-1-5-32-544")
if (-not $isAdmin) {
    Write-Warning "This script is running without administrator privileges. Some features may not work."
}

Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║   El Akeil - Windows Setup Script      ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════╝`n" -ForegroundColor Magenta

# Get current directory
$ProjectRoot = Get-Location
Write-Info "Project Root: $ProjectRoot"

# ============================================
# 1️⃣ Create Virtual Environment
# ============================================
if (-not $SkipVenv) {
    Write-Info "Creating Virtual Environment..."
    
    if (Test-Path ".\.venv") {
        Write-Warning "Virtual environment already exists. Skipping creation."
    } else {
        try {
            python -m venv .venv
            Write-Success "Virtual environment created successfully"
        } catch {
            Write-Error "Failed to create virtual environment: $_"
            exit 1
        }
    }
}

# Activate virtual environment
Write-Info "Activating Virtual Environment..."
& ".\.venv\Scripts\Activate.ps1"
Write-Success "Virtual environment activated"

# ============================================
# 2️⃣ Install Dependencies
# ============================================
if (-not $SkipDeps) {
    Write-Info "Installing dependencies..."
    
    try {
        # Upgrade pip
        Write-Info "Upgrading pip..."
        python -m pip install --upgrade pip
        Write-Success "pip upgraded"
        
        # Check if requirements.txt exists
        if (Test-Path "requirements.txt") {
            Write-Info "Installing packages from requirements.txt..."
            pip install -r requirements.txt
            Write-Success "All packages installed"
        } else {
            Write-Warning "requirements.txt not found. Skipping dependency installation."
        }
    } catch {
        Write-Error "Failed to install dependencies: $_"
        exit 1
    }
}

# ============================================
# 3️⃣ Set Environment Variables
# ============================================
Write-Info "Setting environment variables..."

$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
$env:SECRET_KEY = "change_this_secret_key_in_production"

Write-Success "Environment variables set"
Write-Info "FLASK_ENV: $env:FLASK_ENV"
Write-Info "FLASK_DEBUG: $env:FLASK_DEBUG"

# ============================================
# 4️⃣ Create Database (if needed)
# ============================================
Write-Info "Checking database..."

$dbPath = "src\backend\data.db"
if (Test-Path $dbPath) {
    Write-Success "Database exists at $dbPath"
} else {
    Write-Warning "Database not found. Creating new database..."
    try {
        python -c "from src.backend.app import create_app, db; app = create_app(); app.app_context().push(); db.create_all(); print('Database created successfully')"
        Write-Success "Database created"
    } catch {
        Write-Error "Failed to create database: $_"
    }
}

# ============================================
# 5️⃣ Run Server or Custom Action
# ============================================
Write-Host "`n╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║        Setup Complete! Starting...     ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝`n" -ForegroundColor Green

switch ($Action.ToLower()) {
    "full" {
        Write-Info "Starting Flask development server..."
        Write-Info "Access the application at: http://localhost:5000"
        Write-Info "Press Ctrl+C to stop the server`n"
        
        cd "src\backend"
        python app.py
    }
    
    "shell" {
        Write-Info "Starting Flask shell..."
        cd "src\backend"
        flask shell
    }
    
    "migrate" {
        Write-Info "Running database migrations..."
        cd "src\backend"
        flask db upgrade
    }
    
    "test" {
        Write-Info "Running tests..."
        pytest
    }
    
    "seed" {
        Write-Info "Seeding database..."
        python seed_db.py
    }
    
    default {
        Write-Warning "Unknown action: $Action"
        Write-Info "Available actions: full (default), shell, migrate, test, seed"
    }
}

# ============================================
# Cleanup on Exit
# ============================================
Write-Info "Setup script completed."
