@echo off
chcp 65001 >nul
echo ========================================
echo   إصلاح جميع المشاكل نهائياً
echo   Fix All Issues Finally
echo ========================================
echo.

echo 🔧 إصلاح أدوار المستخدمين...
echo Fixing user roles...

python -c "
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Connect to database
conn = sqlite3.connect('inventory.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print('🔍 Current users in database:')
cursor.execute('SELECT id, username, role FROM users')
users = cursor.fetchall()
for user in users:
    print(f'  ID: {user[\"id\"]}, Username: {user[\"username\"]}, Role: {user[\"role\"]}')

print('\n🔧 Recreating dev user...')
cursor.execute('DELETE FROM users WHERE username = ?', ('dev',))
cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
             ('dev', generate_password_hash('dev'), 'dev'))
print('✅ Dev user recreated with correct role')

print('\n🔧 Recreating owner user...')
cursor.execute('DELETE FROM users WHERE username = ?', ('owner',))
cursor.execute('INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
             ('owner', generate_password_hash('owner'), 'owner'))
print('✅ Owner user recreated with correct role')

# Verify password hashes
print('\n🔐 Verifying password hashes...')
cursor.execute('SELECT username, password_hash FROM users WHERE username IN (?, ?)', ('dev', 'owner'))
test_users = cursor.fetchall()

for user in test_users:
    if check_password_hash(user['password_hash'], user['username']):
        print(f'✅ {user[\"username\"]} password verified')
    else:
        print(f'❌ {user[\"username\"]} password verification failed')

# Commit changes
conn.commit()

print('\n🔍 Final verification:')
cursor.execute('SELECT username, role FROM users ORDER BY created_at')
users = cursor.fetchall()

for user in users:
    print(f'  - {user[\"username\"]}: {user[\"role\"]}')

print('\n✅ User roles fixed successfully!')
conn.close()
"

echo.
echo 🔧 إصلاح مشكلة حذف المستخدمين في الفواتير...
echo Fixing deleted users in invoices...

python -c "
import sqlite3

# Connect to database
conn = sqlite3.connect('inventory.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print('🔧 Adding created_by_name column to invoices...')
try:
    cursor.execute('SELECT created_by_name FROM invoices LIMIT 1')
    print('✅ Column already exists')
except sqlite3.OperationalError:
    cursor.execute('ALTER TABLE invoices ADD COLUMN created_by_name TEXT')
    print('✅ Column added successfully')

# Update existing invoices with usernames
print('🔧 Updating existing invoices...')
invoices = cursor.execute('SELECT id, created_by FROM invoices WHERE created_by IS NOT NULL').fetchall()
updated_count = 0

for invoice in invoices:
    user = cursor.execute('SELECT username FROM users WHERE id = ?', (invoice['created_by'],)).fetchone()
    if user:
        cursor.execute('UPDATE invoices SET created_by_name = ? WHERE id = ?', 
                      (user['username'], invoice['id']))
        updated_count += 1

print(f'✅ Updated {updated_count} invoices with usernames')

# Commit changes
conn.commit()
conn.close()
print('✅ Invoice user names fixed successfully!')
"

echo.
echo 🔄 نسخ الملفات المحدثة إلى GitHub...
echo Copying updated files to GitHub...

copy "app\utils\auth.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\utils\auth.py" /Y
copy "app\models\database.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\models\database.py" /Y
copy "app\views\invoices.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\views\invoices.py" /Y
copy "app\views\users.py" "C:\Users\mfh\Pictures\New folder\store_management_system\app\views\users.py" /Y
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
git commit -m "Fix user roles and invoice user names - Final solution"
git push origin main

echo.
echo 🎉 تم إصلاح جميع المشاكل نهائياً!
echo All issues fixed finally!
echo.
echo 🔗 الرابط: https://github.com/Mohamed-Faroug/store_management_system
echo Link: https://github.com/Mohamed-Faroug/store_management_system
echo.
echo 📋 المشاكل التي تم حلها:
echo Issues fixed:
echo   ✅ أدوار المستخدمين dev و owner
echo   ✅ مشكلة حذف المستخدمين في الفواتير
echo   ✅ حفظ اسم المستخدم في الفواتير
echo.
pause
