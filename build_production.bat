@echo off
chcp 65001 >nul
title بناء نظام إدارة المخزون للإنتاج

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██  🏭 بناء نظام إدارة المخزون للإنتاج                        ██
echo ██  👨‍💻 تم تطوير هذا النظام بواسطة: محمد فاروق              ██
echo ██  📅 تاريخ آخر تحديث: 9/9/2025                            ██
echo ██  © جميع الحقوق محفوظة 2025                                ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

echo 🧹 تنظيف الملفات القديمة...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del "*.spec"
echo ✅ تم التنظيف

echo.
echo 🔧 بناء ملف EXE للإنتاج...
pyinstaller --onefile ^
    --windowed ^
    --name "inventory_system" ^
    --add-data "app;app" ^
    --add-data "inventory.db;." ^
    --add-data "config.py;." ^
    --hidden-import flask ^
    --hidden-import werkzeug ^
    --hidden-import jinja2 ^
    --hidden-import sqlite3 ^
    --hidden-import waitress ^
    --hidden-import schedule ^
    --hidden-import threading ^
    --optimize 2 ^
    --clean ^
    main.py

if errorlevel 1 (
    echo ❌ فشل في بناء EXE
    pause
    exit /b 1
)

echo.
echo 📦 إنشاء حزمة التثبيت...

:: إنشاء مجلد التوزيع
mkdir "inventory_system_release" 2>nul
mkdir "inventory_system_release\app" 2>nul

:: نسخ الملفات المطلوبة
copy "dist\inventory_system.exe" "inventory_system_release\"
copy "inventory.db" "inventory_system_release\"
copy "config.py" "inventory_system_release\"
copy "requirements.txt" "inventory_system_release\"
copy "README.md" "inventory_system_release\"

:: نسخ مجلد app
xcopy "app" "inventory_system_release\app" /E /I /Q

:: إنشاء ملف تشغيل
echo @echo off > "inventory_system_release\start.bat"
echo chcp 65001 ^>nul >> "inventory_system_release\start.bat"
echo title نظام إدارة المخزون >> "inventory_system_release\start.bat"
echo echo 🚀 تشغيل نظام إدارة المخزون... >> "inventory_system_release\start.bat"
echo echo 📱 سيتم فتح المتصفح تلقائياً على: http://127.0.0.1:8080 >> "inventory_system_release\start.bat"
echo echo 🔑 بيانات الدخول: admin / admin123 >> "inventory_system_release\start.bat"
echo echo. >> "inventory_system_release\start.bat"
echo inventory_system.exe >> "inventory_system_release\start.bat"
echo pause >> "inventory_system_release\start.bat"

:: إنشاء ملف تثبيت
echo @echo off > "inventory_system_release\install.bat"
echo chcp 65001 ^>nul >> "inventory_system_release\install.bat"
echo title تثبيت نظام إدارة المخزون >> "inventory_system_release\install.bat"
echo echo 🏪 نظام إدارة المخزون - مخزن الزينة >> "inventory_system_release\install.bat"
echo echo 👨‍💻 تم تطوير هذا النظام بواسطة: محمد فاروق >> "inventory_system_release\install.bat"
echo echo 📅 تاريخ آخر تحديث: 9/9/2025 >> "inventory_system_release\install.bat"
echo echo © جميع الحقوق محفوظة 2025 >> "inventory_system_release\install.bat"
echo echo. >> "inventory_system_release\install.bat"
echo echo 🚀 تشغيل نظام إدارة المخزون... >> "inventory_system_release\install.bat"
echo echo 📱 سيتم فتح المتصفح تلقائياً على: http://127.0.0.1:8080 >> "inventory_system_release\install.bat"
echo echo 🔑 بيانات الدخول: admin / admin123 >> "inventory_system_release\install.bat"
echo echo. >> "inventory_system_release\install.bat"
echo start.bat >> "inventory_system_release\install.bat"

:: إنشاء ملف README
echo # نظام إدارة المخزون - مخزن الزينة > "inventory_system_release\README.txt"
echo. >> "inventory_system_release\README.txt"
echo ## كيفية التشغيل: >> "inventory_system_release\README.txt"
echo 1. انقر مرتين على install.bat للتثبيت >> "inventory_system_release\README.txt"
echo 2. أو انقر مرتين على start.bat للتشغيل المباشر >> "inventory_system_release\README.txt"
echo. >> "inventory_system_release\README.txt"
echo ## الوصول للتطبيق: >> "inventory_system_release\README.txt"
echo http://127.0.0.1:8080 >> "inventory_system_release\README.txt"
echo. >> "inventory_system_release\README.txt"
echo ## بيانات الدخول: >> "inventory_system_release\README.txt"
echo المدير: admin / admin123 >> "inventory_system_release\README.txt"
echo الكاشير: cashier / cashier123 >> "inventory_system_release\README.txt"

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                    تم البناء بنجاح!                       ██
echo ████████████████████████████████████████████████████████████████
echo.
echo 📁 الملفات في: inventory_system_release\
echo.
echo 📋 محتويات الحزمة:
echo    📄 inventory_system.exe - التطبيق الرئيسي
echo    📄 start.bat - تشغيل سريع
echo    📄 install.bat - ملف التثبيت
echo    📄 README.txt - دليل الاستخدام
echo    📁 app\ - ملفات التطبيق
echo    📄 inventory.db - قاعدة البيانات
echo.
echo 🚀 يمكنك الآن:
echo    1. نسخ مجلد inventory_system_release\ إلى أي جهاز
echo    2. تشغيل install.bat للتثبيت
echo    3. أو تشغيل start.bat مباشرة
echo.

pause
