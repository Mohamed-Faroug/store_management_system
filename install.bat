@echo off
chcp 65001 >nul
title نظام إدارة المخزون - التثبيت

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██  🏪 نظام إدارة المخزون - مخزن الزينة                      ██
echo ██  👨‍💻 تم تطوير هذا النظام بواسطة: محمد فاروق              ██
echo ██  📅 تاريخ آخر تحديث: 9/9/2025                            ██
echo ██  © جميع الحقوق محفوظة 2025                                ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

echo 🔧 بدء عملية التثبيت...
echo.

:: فحص وجود Python
echo 🔍 فحص Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت!
    echo.
    echo 📥 يرجى تثبيت Python من: https://python.org
    echo 📋 تأكد من تحديد "Add Python to PATH" أثناء التثبيت
    pause
    exit /b 1
) else (
    echo ✅ Python مثبت
)

:: إنشاء المجلدات المطلوبة
echo.
echo 📁 إنشاء المجلدات المطلوبة...
mkdir logs 2>nul
mkdir backups 2>nul
mkdir temp 2>nul
mkdir uploads 2>nul
mkdir data 2>nul
echo ✅ تم إنشاء المجلدات

:: تثبيت المتطلبات
echo.
echo 📦 تثبيت المتطلبات...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ فشل في تثبيت المتطلبات
    pause
    exit /b 1
) else (
    echo ✅ تم تثبيت المتطلبات بنجاح
)

:: إنشاء قاعدة البيانات
echo.
echo 🗄️ إنشاء قاعدة البيانات...
python -c "from app import create_app; from app.models.database import init_db; app = create_app(); app.app_context().push(); init_db()"
if errorlevel 1 (
    echo ❌ فشل في إنشاء قاعدة البيانات
    pause
    exit /b 1
) else (
    echo ✅ تم إنشاء قاعدة البيانات بنجاح
)

:: إنشاء ملف تشغيل
echo.
echo 📝 إنشاء ملف التشغيل...
echo @echo off > start.bat
echo chcp 65001 ^>nul >> start.bat
echo title نظام إدارة المخزون >> start.bat
echo echo 🚀 تشغيل نظام إدارة المخزون... >> start.bat
echo python main.py >> start.bat
echo pause >> start.bat
echo ✅ تم إنشاء ملف التشغيل

:: إنشاء اختصار سطح المكتب
echo.
echo 🖥️ إنشاء اختصار سطح المكتب...
set "desktop=%USERPROFILE%\Desktop"
set "current_dir=%CD%"
echo [InternetShortcut] > "%desktop%\نظام إدارة المخزون.url"
echo URL=file:///%current_dir%\start.bat >> "%desktop%\نظام إدارة المخزون.url"
echo IconFile=%current_dir%\start.bat >> "%desktop%\نظام إدارة المخزون.url"
echo IconIndex=0 >> "%desktop%\نظام إدارة المخزون.url"
echo ✅ تم إنشاء اختصار سطح المكتب

:: عرض معلومات التثبيت
echo.
echo ████████████████████████████████████████████████████████████████
echo ██                    تم التثبيت بنجاح!                      ██
echo ████████████████████████████████████████████████████████████████
echo.
echo 📱 للوصول للتطبيق:
echo    🌐 افتح المتصفح واذهب إلى: http://127.0.0.1:8080
echo.
echo 🔑 بيانات الدخول الافتراضية:
echo    👤 المدير: admin / admin123
echo    👤 الكاشير: cashier / cashier123
echo.
echo 🚀 طرق التشغيل:
echo    📄 انقر مرتين على: start.bat
echo    🖥️ أو من اختصار سطح المكتب
echo.
echo ⚠️  نصائح مهمة:
echo    🔒 غيّر كلمات المرور الافتراضية
echo    💾 احتفظ بنسخ احتياطية من قاعدة البيانات
echo    🔄 شغّل التحديثات بانتظام
echo.

:: سؤال المستخدم
set /p choice="هل تريد تشغيل التطبيق الآن؟ (y/n): "
if /i "%choice%"=="y" (
    echo.
    echo 🚀 تشغيل التطبيق...
    start.bat
) else (
    echo.
    echo 👋 شكراً لاستخدام نظام إدارة المخزون
    echo 📱 يمكنك تشغيل التطبيق لاحقاً من ملف start.bat
)

echo.
pause
