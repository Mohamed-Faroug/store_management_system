@echo off
chcp 65001 >nul
title نظام إدارة المخزون - مخزن الزينة

echo ========================================
echo 🏪 نظام إدارة المخزون - مخزن الزينة
echo 👨‍💻 تم تطوير هذا النظام بواسطة: محمد فاروق
echo 📅 تاريخ آخر تحديث: 9/9/2025
echo © جميع الحقوق محفوظة 2025
echo ========================================
echo.

echo 🔍 فحص المتطلبات...
python -c "import flask, werkzeug, sqlite3; print('✅ جميع المتطلبات متوفرة')" 2>nul
if errorlevel 1 (
    echo ❌ مكتبة مفقودة. يرجى تثبيت المتطلبات:
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

echo 🚀 بدء تشغيل النظام...
echo 📱 سيتم فتح المتصفح تلقائياً على: http://127.0.0.1:8080
echo.

python main.py

pause
