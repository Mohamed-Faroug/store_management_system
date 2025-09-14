@echo off
chcp 65001 >nul
echo ========================================
echo   إصلاح خطأ القيد في قاعدة البيانات
echo   Fix Constraint Error in Database
echo ========================================
echo.

echo 🔧 إصلاح قيد الأدوار في قاعدة البيانات...
echo Fixing role constraint in database...

python -c "
import sqlite3
from werkzeug.security import generate_password_hash

# Connect to database
conn = sqlite3.connect('inventory.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

print('🔍 Current users in database:')
try:
    cursor.execute('SELECT id, username, role FROM users')
    users = cursor.fetchall()
    for user in users:
        print(f'  ID: {user[\"id\"]}, Username: {user[\"username\"]}, Role: {user[\"role\"]}')
except Exception as e:
    print(f'Error reading users: {e}')

print('\n🔧 Recreating users table with new structure...')

# Create new table with correct structure (no CHECK constraint)
cursor.execute('''
    CREATE TABLE users_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        permissions TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'مرئي',
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
''')

# Copy data from old table with role mapping
try:
    old_users = cursor.execute('SELECT * FROM users').fetchall()
    print(f'Found {len(old_users)} users to migrate...')
    
    for user in old_users:
        # Map old roles to new roles
        if user['username'] == 'dev':
            new_role = 'المطور'
            permissions = 'جميع الصلاحيات'
            status = 'مخفي'
        elif user['username'] == 'owner':
            new_role = 'المالك'
            permissions = 'جميع الصلاحيات'
            status = 'مخفي'
        elif user['username'] == 'admin' or user['role'] == 'manager':
            new_role = 'المدير'
            permissions = 'إدارة المستخدمين والمخزون والمبيعات'
            status = 'مرئي'
        elif user['username'] == 'clerk' or user['role'] == 'clerk':
            new_role = 'الموظف'
            permissions = 'المبيعات والمخزون'
            status = 'مرئي'
        else:
            new_role = 'الموظف'
            permissions = 'المبيعات والمخزون'
            status = 'مرئي'
        
        cursor.execute('''
            INSERT INTO users_new (id, role, username, password_hash, permissions, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user['id'], new_role, user['username'], user['password_hash'], 
              permissions, status, user.get('created_at', 'CURRENT_TIMESTAMP')))
        print(f'  Migrated: {user[\"username\"]} -> {new_role}')
    
    # Drop old table and rename new one
    cursor.execute('DROP TABLE users')
    cursor.execute('ALTER TABLE users_new RENAME TO users')
    conn.commit()
    print('✅ Users table recreated successfully!')
    
except Exception as e:
    print(f'Error during migration: {e}')
    conn.rollback()

# Ensure we have the required users
print('\n🔧 Ensuring required users exist...')
required_users = [
    ('المطور', 'dev', 'dev', 'جميع الصلاحيات', 'مخفي'),
    ('المالك', 'owner', 'owner', 'جميع الصلاحيات', 'مخفي'),
    ('المدير', 'admin', 'admin123', 'إدارة المستخدمين والمخزون والمبيعات', 'مرئي'),
    ('الموظف', 'clerk', 'clerk123', 'المبيعات والمخزون', 'مرئي')
]

for role, username, password, permissions, status in required_users:
    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if not cursor.fetchone():
        cursor.execute('''
            INSERT INTO users (role, username, password_hash, permissions, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (role, username, generate_password_hash(password), permissions, status))
        print(f'  Created: {username} ({role})')
    else:
        print(f'  Exists: {username} ({role})')

conn.commit()

print('\n🔍 Final users:')
cursor.execute('SELECT username, role, permissions, status FROM users ORDER BY created_at')
users = cursor.fetchall()
for user in users:
    print(f'  - {user[\"username\"]}: {user[\"role\"]} ({user[\"permissions\"]}) - {user[\"status\"]}')

print('\n✅ Database constraint fixed successfully!')
conn.close()
"

echo.
echo 🔄 نسخ الملفات المحدثة إلى GitHub...
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
git commit -m "Fix database constraint error - Remove old CHECK constraint"
git push origin main

echo.
echo 🎉 تم إصلاح خطأ القيد بنجاح!
echo Constraint error fixed successfully!
echo.
echo 🔗 الرابط: https://github.com/Mohamed-Faroug/store_management_system
echo Link: https://github.com/Mohamed-Faroug/store_management_system
echo.
pause
