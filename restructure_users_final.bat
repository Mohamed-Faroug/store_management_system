@echo off
chcp 65001 >nul
echo ========================================
echo   إعادة هيكلة المستخدمين والأدوار
echo   Restructure Users and Roles
echo ========================================
echo.

echo 🔧 إعادة هيكلة قاعدة البيانات...
echo Restructuring database...

python -c "
import sqlite3
from werkzeug.security import generate_password_hash

# Connect to database
conn = sqlite3.connect('inventory.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print('🔍 Current users in database:')
cursor.execute('SELECT id, username, role FROM users')
users = cursor.fetchall()
for user in users:
    print(f'  ID: {user[\"id\"]}, Username: {user[\"username\"]}, Role: {user[\"role\"]}')

print('\n🔧 Adding new columns to users table...')
try:
    cursor.execute('SELECT permissions FROM users LIMIT 1')
    print('✅ Columns already exist')
except sqlite3.OperationalError:
    cursor.execute('ALTER TABLE users ADD COLUMN permissions TEXT')
    cursor.execute('ALTER TABLE users ADD COLUMN status TEXT DEFAULT \"مرئي\"')
    print('✅ New columns added')

print('\n🔧 Updating users with new structure...')
# Delete and recreate dev and owner users
cursor.execute('DELETE FROM users WHERE username IN (?, ?)', ('dev', 'owner'))
cursor.execute('INSERT INTO users (role, username, password_hash, permissions, status) VALUES (?, ?, ?, ?, ?)',
             ('المطور', 'dev', generate_password_hash('dev'), 'جميع الصلاحيات', 'مخفي'))
cursor.execute('INSERT INTO users (role, username, password_hash, permissions, status) VALUES (?, ?, ?, ?, ?)',
             ('المالك', 'owner', generate_password_hash('owner'), 'جميع الصلاحيات', 'مخفي'))

# Update existing users
users = cursor.execute('SELECT id, username, role FROM users WHERE username NOT IN (?, ?)', ('dev', 'owner')).fetchall()
for user in users:
    if user['username'] == 'admin':
        cursor.execute('UPDATE users SET role = ?, permissions = ?, status = ? WHERE id = ?',
                      ('المدير', 'إدارة المستخدمين والمخزون والمبيعات', 'مرئي', user['id']))
    elif user['username'] == 'clerk':
        cursor.execute('UPDATE users SET role = ?, permissions = ?, status = ? WHERE id = ?',
                      ('الموظف', 'المبيعات والمخزون', 'مرئي', user['id']))
    else:
        cursor.execute('UPDATE users SET role = ?, permissions = ?, status = ? WHERE id = ?',
                      ('الموظف', 'المبيعات والمخزون', 'مرئي', user['id']))

# Commit changes
conn.commit()

print('\n🔍 Final users:')
cursor.execute('SELECT username, role, permissions, status FROM users ORDER BY created_at')
users = cursor.fetchall()
for user in users:
    print(f'  - {user[\"username\"]}: {user[\"role\"]} ({user[\"permissions\"]}) - {user[\"status\"]}')

print('\n✅ Users restructured successfully!')
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
git commit -m "Restructure users and roles - Add permissions and status columns"
git push origin main

echo.
echo 🎉 تم إعادة هيكلة المستخدمين والأدوار بنجاح!
echo Users and roles restructured successfully!
echo.
echo 🔗 الرابط: https://github.com/Mohamed-Faroug/store_management_system
echo Link: https://github.com/Mohamed-Faroug/store_management_system
echo.
echo 📋 الهيكل الجديد:
echo New structure:
echo   ✅ المالك (owner) - جميع الصلاحيات - مخفي
echo   ✅ المطور (dev) - جميع الصلاحيات - مخفي
echo   ✅ المدير (admin) - إدارة المستخدمين والمخزون - مرئي
echo   ✅ الموظف (clerk) - المبيعات والمخزون - مرئي
echo.
pause
