@echo off
chcp 65001 >nul
title بناء نظام إدارة المخزون

echo.
echo ████████████████████████████████████████████████████████████████
echo ██  🏭 بناء نظام إدارة المخزون                              ██
echo ████████████████████████████████████████████████████████████████
echo.

echo 🧹 تنظيف الملفات القديمة...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"
echo ✅ تم التنظيف

echo.
echo 🔧 بناء ملف EXE...
pyinstaller --onefile --windowed --name "inventory_system" --add-data "app;app" --add-data "inventory.db;." main.py

if errorlevel 1 (
    echo ❌ فشل في بناء EXE
    pause
    exit /b 1
)

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                    تم البناء بنجاح!                       ██
echo ████████████████████████████████████████████████████████████████
echo.
echo 📁 الملف في: dist\inventory_system.exe
echo.
echo 🚀 يمكنك الآن تشغيل التطبيق من:
echo    📄 dist\inventory_system.exe
echo.

pause
