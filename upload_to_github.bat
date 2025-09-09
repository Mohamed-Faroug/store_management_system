@echo off
chcp 65001 >nul
title رفع المشروع على GitHub

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                                                            ██
echo ██  🚀 رفع نظام إدارة المخزون على GitHub                     ██
echo ██  👨‍💻 تم تطوير هذا النظام بواسطة: محمد فاروق              ██
echo ██  📅 تاريخ آخر تحديث: 9/9/2025                            ██
echo ██  © جميع الحقوق محفوظة 2025                                ██
echo ██                                                            ██
echo ████████████████████████████████████████████████████████████████
echo.

echo 🔍 فحص Git...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git غير مثبت!
    echo.
    echo 📥 يرجى تثبيت Git من: https://git-scm.com
    pause
    exit /b 1
) else (
    echo ✅ Git مثبت
)

echo.
echo 🔧 تهيئة Git...
git init
if errorlevel 1 (
    echo ❌ فشل في تهيئة Git
    pause
    exit /b 1
) else (
    echo ✅ تم تهيئة Git بنجاح
)

echo.
echo 📁 إضافة الملفات...
git add .
if errorlevel 1 (
    echo ❌ فشل في إضافة الملفات
    pause
    exit /b 1
) else (
    echo ✅ تم إضافة الملفات بنجاح
)

echo.
echo 💾 إنشاء commit...
git commit -m "Initial commit: نظام إدارة المخزون - مخزن الزينة"
if errorlevel 1 (
    echo ❌ فشل في إنشاء commit
    pause
    exit /b 1
) else (
    echo ✅ تم إنشاء commit بنجاح
)

echo.
echo 🔗 ربط المشروع بـ GitHub...
git remote add origin https://github.com/Mohamed-Faroug/inventory_system.git
if errorlevel 1 (
    echo ⚠️  المستودع البعيد موجود بالفعل
    git remote set-url origin https://github.com/Mohamed-Faroug/inventory_system.git
    echo ✅ تم تحديث رابط المستودع
) else (
    echo ✅ تم ربط المشروع بـ GitHub بنجاح
)

echo.
echo 🌿 تعيين الفرع الرئيسي...
git branch -M main
if errorlevel 1 (
    echo ❌ فشل في تعيين الفرع الرئيسي
    pause
    exit /b 1
) else (
    echo ✅ تم تعيين الفرع الرئيسي بنجاح
)

echo.
echo 🚀 رفع المشروع على GitHub...
git push -u origin main
if errorlevel 1 (
    echo ❌ فشل في رفع المشروع
    echo.
    echo 🔧 الحلول المقترحة:
    echo    1. تحقق من بيانات الدخول لـ GitHub
    echo    2. استخدم Personal Access Token
    echo    3. تحقق من اتصال الإنترنت
    echo.
    pause
    exit /b 1
) else (
    echo ✅ تم رفع المشروع بنجاح!
)

echo.
echo ████████████████████████████████████████████████████████████████
echo ██                    تم الرفع بنجاح!                        ██
echo ████████████████████████████████████████████████████████████████
echo.
echo 🌐 يمكنك الآن الوصول للمشروع من:
echo    📱 https://github.com/Mohamed-Faroug/inventory_system
echo.
echo 📋 الخطوات التالية:
echo    1. أضف وصف للمستودع
echo    2. أضف Topics (inventory-management, pos-system, flask)
echo    3. فعّل GitHub Actions
echo    4. أضف README.md
echo.
echo 🔄 للتحديثات المستقبلية:
echo    git add .
echo    git commit -m "وصف التغييرات"
echo    git push origin main
echo.

pause
