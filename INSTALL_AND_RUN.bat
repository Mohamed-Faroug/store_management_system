@echo off
title Install and Run Store Management System

echo.
echo ========================================
echo    Install and Run Store Management
echo    تثبيت وتشغيل نظام إدارة المخزون
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7+ from https://python.org
    echo.
    echo After installing Python, run this file again
    pause
    exit /b 1
)

echo Python is installed ✓
echo.

echo Step 2: Installing required packages...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo Packages installed successfully ✓
echo.

echo Step 3: Setting up database...
if not exist "inventory.db" (
    echo Creating database...
    python -c "from app.models.database import init_db; init_db()"
    if errorlevel 1 (
        echo Error: Failed to create database
        pause
        exit /b 1
    )
    echo Database created successfully ✓
) else (
    echo Database already exists ✓
)

echo.
echo ========================================
echo    Installation Complete!
echo    التثبيت مكتمل!
echo ========================================
echo.

echo Starting the application...
echo.
echo Access the application at:
echo    http://localhost:5000
echo    http://127.0.0.1:5000
echo.
echo Default login credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo Press Ctrl+C to stop the application
echo.

python run.py

echo.
echo Application stopped
pause
