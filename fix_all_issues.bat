@echo off
chcp 65001 >nul
echo ========================================
echo   إصلاح جميع المشاكل
echo   Fix All Issues
echo ========================================
echo.

echo 🔧 إصلاح أدوار المستخدمين...
echo Fixing user roles...

python -c "
import sqlite3
from werkzeug.security import generate_password_hash

# Connect to database
conn = sqlite3.connect('inventory.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print('🔍 Current users in database:')
cursor.execute('SELECT username, role FROM users')
users = cursor.fetchall()
for user in users:
    print(f'  - {user[\"username\"]}: {user[\"role\"]}')

print('\n🔧 Fixing dev user...')
cursor.execute('SELECT * FROM users WHERE username = ?', ('dev',))
dev_user = cursor.fetchone()

if dev_user:
    cursor.execute('UPDATE users SET role = ? WHERE username = ?', ('dev', 'dev'))
    print('✅ Updated dev user role to dev')
else:
    cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                 ('dev', generate_password_hash('dev'), 'dev'))
    print('✅ Created dev user with dev role')

print('\n🔧 Fixing owner user...')
cursor.execute('SELECT * FROM users WHERE username = ?', ('owner',))
owner_user = cursor.fetchone()

if owner_user:
    cursor.execute('UPDATE users SET role = ? WHERE username = ?', ('owner', 'owner'))
    print('✅ Updated owner user role to owner')
else:
    cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
                 ('owner', generate_password_hash('owner'), 'owner'))
    print('✅ Created owner user with owner role')

# Commit changes
conn.commit()

print('\n🔍 Final users:')
cursor.execute('SELECT username, role FROM users ORDER BY created_at')
users = cursor.fetchall()
for user in users:
    print(f'  - {user[\"username\"]}: {user[\"role\"]}')

print('\n✅ User roles fixed successfully!')
conn.close()
"

echo.
echo 🔄 نسخ الملفات المحدثة إلى GitHub...
echo Copying updated files to GitHub...

copy "app\utils\auth.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\utils\auth.py" /Y
copy "app\models\database.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\models\database.py" /Y
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
echo 📁 الانتقال إلى مجلد GitHub...
echo Changing to GitHub directory...
cd /d "C:\Users\mfh\Pictures\New folder\store_management_system"

echo.
echo 🔄 رفع التحديثات على GitHub...
echo Uploading updates to GitHub...

git add .
git commit -m "Fix user roles and permissions - Add proper dev and owner access"
git push origin main

echo.
echo 🎉 تم إصلاح جميع المشاكل ورفعها بنجاح!
echo All issues fixed and uploaded successfully!
echo.
echo 🔗 الرابط: https://github.com/Mohamed-Faroug/store_management_system
echo Link: https://github.com/Mohamed-Faroug/store_management_system
echo.
echo 📋 المستخدمون الجدد:
echo New users:
echo   - owner / owner (جميع الصلاحيات)
echo   - dev / dev (جميع الصلاحيات)
echo.
pause
