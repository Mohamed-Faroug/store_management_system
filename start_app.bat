@echo off
chcp 65001 >nul
echo.
echo ========================================
echo    نظام إدارة المخزون - مخزن الزينة
echo ========================================
echo.
echo جميع الحقوق محفوظة © 2025
echo تم تطوير هذا النظام بواسطة: محمد فاروق
echo تاريخ آخر تحديث: 9/9/2025
echo.
echo ========================================
echo.

echo [1] تشغيل التطبيق
echo [2] إضافة بيانات تجريبية
echo [3] تشغيل النسخ الاحتياطي
echo [4] إنهاء
echo.

set /p choice="اختر رقم العملية: "

if "%choice%"=="1" (
    echo.
    echo تشغيل التطبيق...
    python main.py
    pause
) else if "%choice%"=="2" (
    echo.
    echo إضافة البيانات التجريبية...
    python demo_data.py
    pause
) else if "%choice%"=="3" (
    echo.
    echo تشغيل النسخ الاحتياطي...
    python backup.py
    pause
) else if "%choice%"=="4" (
    echo.
    echo شكراً لاستخدام النظام!
    exit
) else (
    echo.
    echo اختيار غير صحيح!
    pause
)

goto :eof