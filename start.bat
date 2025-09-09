@echo off
chcp 65001 >nul
title نظام إدارة المخزون والمبيعات

echo.
echo ========================================
echo    نظام إدارة المخزون والمبيعات
echo ========================================
echo.

echo 🔍 فحص المتطلبات...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت أو غير موجود في PATH
    echo يرجى تثبيت Python 3.8 أو أحدث
    pause
    exit /b 1
)

echo ✅ Python متوفر
echo.

echo 📦 فحص المتطلبات...
if not exist "requirements.txt" (
    echo ❌ ملف requirements.txt غير موجود
    pause
    exit /b 1
)

echo ✅ ملف المتطلبات موجود
echo.

echo 🔧 تثبيت المتطلبات...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ فشل في تثبيت المتطلبات
    pause
    exit /b 1
)

echo ✅ تم تثبيت المتطلبات بنجاح
echo.

echo 🗄️ فحص قاعدة البيانات...
if not exist "inventory.db" (
    echo ⚠️  قاعدة البيانات غير موجودة، سيتم إنشاؤها تلقائياً
)

echo ✅ قاعدة البيانات جاهزة
echo.

echo 🚀 تشغيل التطبيق...
echo.
echo 📱 المتصفح: http://127.0.0.1:5000
echo ⏹️  لإيقاف التطبيق: Ctrl+C
echo ========================================
echo.

python run.py

echo.
echo 👋 تم إيقاف التطبيق
pause