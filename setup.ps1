# Expense Tracker Setup Script
# This script sets up the complete expense tracker application

Write-Host "Setting up Expense Tracker Application..." -ForegroundColor Green

# Create project directories
$directories = @(
    "app",
    "app\models",
    "app\routes",
    "app\utils",
    "static\css",
    "static\js",
    "static\images",
    "templates",
    "tests",
    "migrations"
)

foreach ($dir in $directories) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force
        Write-Host "Created directory: $dir" -ForegroundColor Yellow
    }
}

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Yellow
python init_db.py

Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "To start the application, run: python run.py" -ForegroundColor Cyan
Write-Host "The application will be available at: http://127.0.0.1:5000" -ForegroundColor Cyan
