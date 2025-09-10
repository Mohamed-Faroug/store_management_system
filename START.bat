@echo off
title Store Management System - متجر عمدة

echo.
echo ========================================
echo    Store Management System
echo    نظام إدارة المخزون - متجر عمدة
echo ========================================
echo.

echo Starting the application...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Check database
if not exist "inventory.db" (
    echo Creating database...
    python -c "from app.models.database import init_db; init_db()"
    if errorlevel 1 (
        echo Error: Failed to create database
        pause
        exit /b 1
    )
)

REM Start application
echo.
echo Application starting...
echo.
echo Access the application at:
echo    http://localhost:5000
echo    http://127.0.0.1:5000
echo.
echo Default login credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo Press Ctrl+C to stop
echo.

python run.py

echo.
echo Application stopped
pause
