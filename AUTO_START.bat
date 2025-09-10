@echo off
title Auto Start Store Management System

REM Change to the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python first.
    pause
    exit /b 1
)

REM Check if database exists
if not exist "inventory.db" (
    echo Creating database...
    python -c "from app.models.database import init_db; init_db()"
)

REM Start the application
echo Starting Store Management System...
python run.py
