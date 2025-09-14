@echo off
chcp 65001 >nul
echo ========================================
echo   رفع المشروع على GitHub
echo   Upload Project to GitHub
echo ========================================
echo.

echo 📁 نسخ الملفات المحدثة...
echo Copying updated files...

:: Copy updated files to GitHub project
copy "app\models\database.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\models\database.py" /Y
copy "app\utils\auth.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\utils\auth.py" /Y
copy "app\views\users.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\views\users.py" /Y
copy "app\views\invoices.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\views\invoices.py" /Y
copy "app\views\advanced_settings.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\views\advanced_settings.py" /Y
copy "app\views\data_management.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\views\data_management.py" /Y
copy "app\views\api.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\views\api.py" /Y
copy "app\views\settings.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\views\settings.py" /Y
copy "app\templates\users\new.html" "C:\Users\mfh\Pictures\New folder\store_management_system\app\templates\users\new.html" /Y
copy "app\templates\users\edit.html" "C:\Users\mfh\Pictures\New folder\store_management_system\app\templates\users\edit.html" /Y
copy "README.md" "C:\Users\mfh\Pictures\New folder\store_management_system\README.md" /Y
copy "USER_ROLES_GUIDE.md" "C:\Users\mfh\Pictures\New folder\store_management_system\USER_ROLES_GUIDE.md" /Y

echo.
echo ✅ تم نسخ الملفات بنجاح
echo Files copied successfully
echo.

echo 📁 الانتقال إلى مجلد GitHub...
echo Changing to GitHub directory...
cd /d "C:\Users\mfh\Pictures\New folder\store_management_system"

echo.
echo 🔄 رفع التحديثات على GitHub...
echo Uploading updates to GitHub...

git add .
git commit -m "Add owner role and fix database initialization issues"
git push origin main

echo.
echo 🎉 تم رفع المشروع بنجاح!
echo Project uploaded successfully!
echo.
echo 🔗 الرابط: https://github.com/Mohamed-Faroug/store_management_system
echo Link: https://github.com/Mohamed-Faroug/store_management_system
echo.
pause
