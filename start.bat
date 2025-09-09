@echo off
chcp 65001 >nul
title Inventory Management System

echo.
echo ========================================
echo 🏪 Inventory Management System
echo 👨‍💻 Developed by: محمد فاروق
echo 📅 Last Updated: 9/9/2025
echo © All Rights Reserved 2025
echo ========================================
echo.

:: Check if EXE exists
if not exist "dist\inventory_system.exe" (
    echo ❌ EXE file not found!
    echo.
    echo 🔧 Building EXE file...
    call build_exe.bat
    if errorlevel 1 (
        echo ❌ Failed to build EXE
        pause
        exit /b 1
    )
)

:: Check if database exists
if not exist "inventory.db" (
    echo ❌ Database not found!
    echo.
    echo 🔧 Creating database...
    python -c "from app import create_app; from app.models.database import init_db; app = create_app(); app.app_context().push(); init_db()"
    if errorlevel 1 (
        echo ❌ Failed to create database
        pause
        exit /b 1
    )
)

echo ✅ All required files are available
echo.

echo 🚀 Starting Inventory Management System...
echo 📱 Browser will open automatically at: http://127.0.0.1:8080
echo 🔑 Login: admin / admin123
echo.

cd /d "%~dp0"
"dist\inventory_system.exe"

pause
