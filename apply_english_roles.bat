@echo off
chcp 65001 >nul
echo ========================================
echo   تطبيق الأدوار الإنجليزية الجديدة
echo   Apply New English Roles System
echo ========================================
echo.

echo 🔧 تطبيق التحديثات الجديدة...
echo Applying new updates...

echo.
echo 📁 نسخ الملفات المحدثة إلى GitHub...
echo Copying updated files to GitHub...

copy "app\models\database.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\models\database.py" /Y
copy "app\utils\auth.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\utils\auth.py" /Y
copy "app\views\users.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\views\users.py" /Y
copy "app\templates\users\new.html" "C:\Users\mfh\Pictures\New folder\store_management_system\app\templates\users\new.html" /Y
copy "app\templates\users\edit.html" "C:\Users\mfh\Pictures\New folder\store_management_system\app\templates\users\edit.html" /Y

echo.
echo 📁 الانتقال إلى مجلد GitHub...
echo Changing to GitHub directory...
cd /d "C:\Users\mfh\Pictures\New folder\store_management_system"

echo.
echo 🔄 رفع التحديثات على GitHub...
echo Uploading updates to GitHub...

git add .
git commit -m "Apply English roles system - Simplified init_db() and updated authentication"
git push origin main

echo.
echo 🎉 تم تطبيق النظام الجديد بنجاح!
echo New system applied successfully!
echo.
echo ✨ المميزات الجديدة:
echo New Features:
echo.
echo 🔐 المستخدمون الافتراضيون:
echo Default Users:
echo   - owner (all_permissions, hidden)
echo   - dev (all_permissions, hidden)  
echo   - admin (manage_users_inventory_sales, visible)
echo   - clerk (sales_inventory, visible)
echo.
echo 🚀 النظام مبسط ومستقر:
echo System is simplified and stable:
echo   - لا توجد قيود CHECK معقدة
echo   - No complex CHECK constraints
echo   - دالة init_db() مبسطة
echo   - Simplified init_db() function
echo   - أدوار إنجليزية واضحة
echo   - Clear English roles
echo.
echo 🔗 الرابط: https://github.com/Mohamed-Faroug/store_management_system
echo Link: https://github.com/Mohamed-Faroug/store_management_system
echo.
pause
