# دليل إنشاء نظام إدارة المخزون باستخدام Cursor AI

## نظرة عامة
هذا الدليل يوضح كيفية إنشاء نظام إدارة المخزون المتكامل من الصفر باستخدام Cursor AI و Python Flask.

## المتطلبات الأساسية
- Python 3.7 أو أحدث
- Cursor AI
- متصفح ويب حديث

## الخطوة 1: إعداد المشروع

### 1.1 إنشاء مجلد المشروع
```bash
mkdir store_management_system
cd store_management_system
```

### 1.2 إنشاء البيئة الافتراضية
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# أو
source venv/bin/activate  # Linux/Mac
```

### 1.3 إنشاء ملف requirements.txt
```txt
# Core Flask Framework
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3

# Database
SQLAlchemy==2.0.21
Flask-SQLAlchemy==3.0.5

# Authentication & Security
Flask-Login==0.6.3

# HTTP Requests
requests==2.31.0

# Date/Time Utilities
python-dateutil==2.8.2

# JSON Handling
simplejson==3.19.1

# Environment Variables
python-dotenv==1.0.0

# CORS Support
Flask-CORS==4.0.0

# Session Management
Flask-Session==0.5.0

# Form Handling
WTForms==3.0.1
Flask-WTF==1.1.1

# File Upload
Flask-Uploads==0.2.1

# Cache
Flask-Caching==2.0.2

# API Documentation
Flask-RESTful==0.3.10

# Database Migrations
Flask-Migrate==4.0.5

# Utilities
click==8.1.7
itsdangerous==2.1.2
blinker==1.6.2

# Production Server
gunicorn==21.2.0
```

### 1.4 تثبيت المكتبات
```bash
pip install -r requirements.txt
```

## الخطوة 2: هيكل المشروع

### 2.1 إنشاء هيكل المجلدات
```
store_management_system/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── settings_models.py
│   │   └── store_settings.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── auth.py
│   │   ├── items.py
│   │   ├── sales.py
│   │   ├── purchases.py
│   │   ├── invoices.py
│   │   ├── reports.py
│   │   ├── users.py
│   │   ├── categories.py
│   │   ├── stock.py
│   │   ├── settings.py
│   │   ├── advanced_settings.py
│   │   ├── data_management.py
│   │   └── api.py
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── dashboard.html
│   │   ├── items/
│   │   ├── sales/
│   │   ├── purchases/
│   │   ├── invoices/
│   │   ├── reports/
│   │   ├── users/
│   │   ├── categories/
│   │   ├── stock/
│   │   ├── settings/
│   │   ├── mobile/
│   │   └── tablet_pwa/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── icons/
│   └── utils/
│       ├── __init__.py
│       ├── auth.py
│       ├── context_processors.py
│       └── payment_utils.py
├── run.py
├── config.py
├── requirements.txt
├── START.bat
├── INSTALL_AND_RUN.bat
├── AUTO_START.bat
├── START_HIDDEN.vbs
└── README.md
```

## الخطوة 3: إنشاء الملفات الأساسية

### 3.1 ملف config.py
```python
# -*- coding: utf-8 -*-
"""
إعدادات التطبيق
"""

import os
from datetime import datetime

class Config:
    """إعدادات التطبيق الأساسية"""
    
    # إعدادات Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DEBUG = True
    
    # إعدادات قاعدة البيانات
    DATABASE = 'inventory.db'
    
    # إعدادات التحميل
    UPLOAD_FOLDER = 'uploads'
    
    # إعدادات التقارير
    REPORTS_PER_PAGE = 50
    
    # إعدادات النظام
    APP_NAME = 'نظام إدارة المخزون - مخزن الزينة'
    STORE_NAME = 'مخزن الزينة'
    VERSION = '1.0.0'
    
    # معلومات التواصل
    SUPPORT_EMAIL = 'mfh1134@gmail.com'
    DEVELOPER_NAME = 'inkplus اينك بلس'
    DEVELOPER_EMAIL = 'mfh1134@gmail.com'
    
    # إعدادات URL
    BASE_URL = 'http://localhost'
    LOCAL_URL = 'http://localhost'
    BASE_URL_WITH_PORT = 'http://localhost:5000'
    LOCAL_URL_WITH_PORT = 'http://localhost:5000'
    
    @staticmethod
    def init_app(app):
        """تهيئة التطبيق"""
        pass
```

### 3.2 ملف app/__init__.py
```python
# -*- coding: utf-8 -*-
"""
نظام إدارة المخزون - مخزن الزينة
تطبيق Flask لإدارة المخزون والمبيعات

المطور: inkplus اينك بلس
التاريخ: 10/9/2025
"""

from flask import Flask
import os
import sys

def create_app():
    """إنشاء تطبيق Flask"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # إعداد مسارات الملفات
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        app.config['DATABASE'] = os.path.join(base_path, 'inventory.db')
    else:
        app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), '..', 'inventory.db')
    
    # تهيئة قاعدة البيانات
    from .models.database import init_db, close_db
    with app.app_context():
        try:
            init_db()
        except Exception as e:
            print(f"Database warning: {e}")
    app.teardown_appcontext(close_db)
    
    # تسجيل المعالجات
    from .utils.context_processors import inject_store_settings
    app.context_processor(inject_store_settings)
    
    # تسجيل Blueprints
    from .views import (
        main, auth, items, sales, purchases, reports, 
        users, categories, invoices, stock, settings, 
        advanced_settings, data_management, api
    )
    
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(items.bp, url_prefix='/items')
    app.register_blueprint(sales.bp, url_prefix='/sales')
    app.register_blueprint(purchases.bp, url_prefix='/purchases')
    app.register_blueprint(reports.bp, url_prefix='/reports')
    app.register_blueprint(users.bp, url_prefix='/users')
    app.register_blueprint(categories.bp, url_prefix='/categories')
    app.register_blueprint(invoices.bp, url_prefix='/invoices')
    app.register_blueprint(stock.bp, url_prefix='/stock')
    app.register_blueprint(settings.settings_bp)
    app.register_blueprint(advanced_settings.advanced_settings_bp)
    app.register_blueprint(data_management.data_management_bp)
    app.register_blueprint(api.api_bp)
    
    return app
```

### 3.3 ملف run.py
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المخزون - مخزن الزينة
ملف التشغيل الرئيسي

المطور: inkplus اينك بلس
التاريخ: 10/9/2025
"""

import os
import sys
from datetime import datetime

def main():
    """الدالة الرئيسية لتشغيل التطبيق"""
    print("=" * 50)
    print("🏪 نظام إدارة المخزون - مخزن الزينة")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 جاري التشغيل...")
    print("📱 http://localhost")
    print("📱 http://localhost:5000")
    print("📱 http://127.0.0.1")
    print("📱 http://127.0.0.1:5000")
    print("⏹️  Ctrl+C للإيقاف")
    print("=" * 50)
    
    try:
        # إضافة مسار التطبيق
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # استيراد وإنشاء التطبيق
        from app import create_app
        app = create_app()
        
        # تشغيل التطبيق على المنفذ 5000
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n⏹️  تم الإيقاف")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    main()
```

## الخطوة 4: إنشاء نماذج قاعدة البيانات

### 4.1 ملف app/models/database.py
```python
# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات
"""

import sqlite3
import os
from flask import g, current_app
from werkzeug.security import generate_password_hash

def get_db():
    """الحصول على اتصال قاعدة البيانات"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """إغلاق اتصال قاعدة البيانات"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """تهيئة قاعدة البيانات"""
    db = get_db()
    
    # إنشاء جدول المستخدمين
    db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'clerk',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إنشاء جدول الفئات
    db.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # إنشاء جدول الأصناف
    db.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            min_stock_level INTEGER DEFAULT 5,
            barcode TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories (id)
        )
    ''')
    
    # إنشاء جدول المبيعات
    db.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            total_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # إنشاء جدول تفاصيل المبيعات
    db.execute('''
        CREATE TABLE IF NOT EXISTS sale_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (sale_id) REFERENCES sales (id),
            FOREIGN KEY (item_id) REFERENCES items (id)
        )
    ''')
    
    # إنشاء جدول المشتريات
    db.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            supplier_name TEXT NOT NULL,
            total_amount REAL NOT NULL,
            payment_method TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # إنشاء جدول تفاصيل المشتريات
    db.execute('''
        CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            purchase_id INTEGER NOT NULL,
            item_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            cost REAL NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases (id),
            FOREIGN KEY (item_id) REFERENCES items (id)
        )
    ''')
    
    # إنشاء جدول تعديلات المخزون
    db.execute('''
        CREATE TABLE IF NOT EXISTS stock_adjustments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            old_quantity INTEGER NOT NULL,
            new_quantity INTEGER NOT NULL,
            reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            user_id INTEGER,
            FOREIGN KEY (item_id) REFERENCES items (id),
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    ''')
    
    # إدراج المستخدم الافتراضي
    try:
        db.execute(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            ('admin', generate_password_hash('admin123'), 'manager')
        )
        db.execute(
            'INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)',
            ('clerk', generate_password_hash('clerk123'), 'clerk')
        )
    except sqlite3.IntegrityError:
        pass  # المستخدم موجود بالفعل
    
    db.commit()
```

## الخطوة 5: إنشاء وحدات التحكم

### 5.1 ملف app/views/auth.py
```python
# -*- coding: utf-8 -*-
"""
صفحات المصادقة
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from ..models.database import get_db
from ..models.store_settings import store_settings

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('تم تسجيل الدخول بنجاح.', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('بيانات الدخول غير صحيحة.', 'danger')
    
    # تحميل إعدادات المتجر
    store_settings_data = store_settings.get_all_settings()
    return render_template('login.html', store_settings=store_settings_data)

@bp.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج.', 'info')
    return redirect(url_for('auth.login'))
```

## الخطوة 6: إنشاء القوالب

### 6.1 ملف app/templates/base.html
```html
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{{ store_settings.app_name or 'نظام إدارة المخزون - مخزن الزينة' }}</title>
    
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link href="{{ url_for('static', filename='css/style.css') }}" rel="stylesheet">
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('main.index') }}">
          <i class="bi bi-shop me-2"></i>{{ store_settings.store_name or 'نظام إدارة المخزون' }}
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <div class="navbar-nav me-auto">
            <a class="nav-link" href="{{ url_for('main.index') }}">
              <i class="bi bi-house-door me-1"></i>الرئيسية
            </a>
            {% if session.get('role') == 'manager' %}
            <a class="nav-link" href="{{ url_for('items.list') }}">
              <i class="bi bi-box me-1"></i>الأصناف
            </a>
            <a class="nav-link" href="{{ url_for('categories.list') }}">
              <i class="bi bi-tags me-1"></i>الفئات
            </a>
            {% endif %}
            <a class="nav-link" href="{{ url_for('sales.new') }}">
              <i class="bi bi-cart-plus me-1"></i>بيع سريع
            </a>
            <a class="nav-link" href="{{ url_for('invoices.list') }}">
              <i class="bi bi-list-ul me-1"></i>قائمة الفواتير
            </a>
            {% if session.get('role') == 'manager' %}
            <a class="nav-link" href="{{ url_for('purchases.new') }}">
              <i class="bi bi-cart-dash me-1"></i>شراء جديد
            </a>
            <a class="nav-link" href="{{ url_for('reports.index') }}">
              <i class="bi bi-graph-up me-1"></i>التقارير
            </a>
            <a class="nav-link" href="{{ url_for('settings.store_settings') }}">
              <i class="bi bi-gear me-1"></i>الإعدادات
            </a>
            {% endif %}
          </div>
          <div class="navbar-nav">
            {% if session.get('user_id') %}
            <span class="navbar-text me-3">
              <i class="bi bi-person-circle me-1"></i>{{ session.get('username') }}
            </span>
            <a class="nav-link" href="{{ url_for('auth.logout') }}">
              <i class="bi bi-box-arrow-right me-1"></i>تسجيل الخروج
            </a>
            {% else %}
            <a class="nav-link" href="{{ url_for('auth.login') }}">
              <i class="bi bi-box-arrow-in-right me-1"></i>تسجيل الدخول
            </a>
            {% endif %}
          </div>
        </div>
      </div>
    </nav>

    <main class="container-fluid mt-4">
        {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
        <div class="row">
            <div class="col-12">
                {% for category, message in messages %}
                <div class="alert alert-{{ 'danger' if category == 'error' else category }} alert-dismissible fade show" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                </div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
        {% endwith %}

        {% block content %}{% endblock %}
    </main>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script src="{{ url_for('static', filename='js/main.js') }}"></script>
</body>
</html>
```

### 6.2 ملف app/templates/login.html
```html
{% extends "base.html" %}

{% block content %}
<div class="row justify-content-center align-items-center min-vh-100">
  <div class="col-md-5">
    <div class="card shadow-lg border-0">
      <div class="card-body p-5">
        <div class="text-center mb-4">
          <i class="bi bi-shop display-1 text-primary mb-3"></i>
          <h2 class="fw-bold text-primary">نظام إدارة المخزون</h2>
          <h4 class="text-success mb-2">{{ store_settings.store_name or 'مخزن الزينة' }}</h4>
          <p class="text-muted">مرحباً بك في {{ store_settings.store_name or 'نظام إدارة المخزون' }}</p>
        </div>
        
        <form method="post" class="needs-validation" novalidate>
          <div class="mb-4">
            <label class="form-label fw-semibold">
              <i class="bi bi-person me-2"></i>اسم المستخدم
            </label>
            <input name="username" class="form-control form-control-lg" required 
                   placeholder="أدخل اسم المستخدم">
            <div class="invalid-feedback">
              يرجى إدخال اسم المستخدم
            </div>
          </div>
          
          <div class="mb-4">
            <label class="form-label fw-semibold">
              <i class="bi bi-lock me-2"></i>كلمة المرور
            </label>
            <input name="password" type="password" class="form-control form-control-lg" required 
                   placeholder="أدخل كلمة المرور">
            <div class="invalid-feedback">
              يرجى إدخال كلمة المرور
            </div>
          </div>
          
          <button class="btn btn-primary btn-lg w-100 mb-3" type="submit">
            <i class="bi bi-box-arrow-in-right me-2"></i>تسجيل الدخول
          </button>
        </form>
        
        <div class="text-center">
          <small class="text-muted">
            <i class="bi bi-info-circle me-1"></i>
            بيانات الدخول الافتراضية: admin/admin123 أو clerk/clerk123
          </small>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}
```

## الخطوة 7: إنشاء ملفات التشغيل

### 7.1 ملف START.bat
```batch
@echo off
title Store Management System - متجر عمدة

echo.
echo ========================================
echo    Store Management System
echo    نظام إدارة المخزون - متجر عمدة
echo ========================================
echo.

echo Starting the application...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7+ from https://python.org
    pause
    exit /b 1
)

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

REM Check database
if not exist "inventory.db" (
    echo Creating database...
    python -c "from app.models.database import init_db; init_db()"
    if errorlevel 1 (
        echo Error: Failed to create database
        pause
        exit /b 1
    )
)

REM Start application
echo.
echo Application starting...
echo.
echo Access the application at:
echo    http://localhost:5000
echo    http://127.0.0.1:5000
echo.
echo Default login credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo Press Ctrl+C to stop
echo.

python run.py

echo.
echo Application stopped
pause
```

### 7.2 ملف INSTALL_AND_RUN.bat
```batch
@echo off
title Install and Run Store Management System

echo.
echo ========================================
echo    Install and Run Store Management
echo    تثبيت وتشغيل نظام إدارة المخزون
echo ========================================
echo.

echo Step 1: Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3.7+ from https://python.org
    echo.
    echo After installing Python, run this file again
    pause
    exit /b 1
)

echo Python is installed ✓
echo.

echo Step 2: Installing required packages...
echo This may take a few minutes...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo Packages installed successfully ✓
echo.

echo Step 3: Setting up database...
if not exist "inventory.db" (
    echo Creating database...
    python -c "from app.models.database import init_db; init_db()"
    if errorlevel 1 (
        echo Error: Failed to create database
        pause
        exit /b 1
    )
    echo Database created successfully ✓
) else (
    echo Database already exists ✓
)

echo.
echo ========================================
echo    Installation Complete!
echo    التثبيت مكتمل!
echo ========================================
echo.

echo Starting the application...
echo.
echo Access the application at:
echo    http://localhost:5000
echo    http://127.0.0.1:5000
echo.
echo Default login credentials:
echo    Username: admin
echo    Password: admin123
echo.
echo Press Ctrl+C to stop the application
echo.

python run.py

echo.
echo Application stopped
pause
```

## الخطوة 8: إنشاء ملف README.md
```markdown
# Store Management System - متجر عمدة

نظام إدارة المخزون المتكامل للمتاجر - مخصص لمتجر عمدة

## المميزات

- **إدارة المخزون**: تتبع المنتجات ومستويات المخزون والفئات
- **نظام المبيعات**: نظام نقاط البيع مع طباعة الفواتير
- **إدارة المشتريات**: تتبع مشتريات الموردين والفواتير
- **إدارة المستخدمين**: نظام متعدد المستخدمين مع صلاحيات مختلفة
- **التقارير**: تقارير يومية وشهرية وسنوية للمبيعات
- **الإعدادات**: إعدادات قابلة للتخصيص للمتجر وطرق الدفع والضرائب

## التثبيت والتشغيل

### الطريقة السهلة (موصى بها)

1. **انقر نقرتين على `INSTALL_AND_RUN.bat`**
   - سيقوم بتثبيت جميع المكتبات المطلوبة
   - سيقوم بإنشاء قاعدة البيانات
   - سيقوم بتشغيل التطبيق

### الطريقة السريعة

1. **انقر نقرتين على `START.bat`**
   - للتشغيل السريع (يجب أن تكون المكتبات مثبتة مسبقاً)

## الوصول للتطبيق

- **الرابط الرئيسي**: http://localhost:5000
- **الرابط البديل**: http://127.0.0.1:5000

## بيانات الدخول الافتراضية

- **اسم المستخدم**: admin
- **كلمة المرور**: admin123

## متطلبات النظام

- Windows 10/11
- Python 3.7 أو أحدث
- متصفح ويب حديث

## الدعم التقني

- **البريد الإلكتروني**: mfh1134@gmail.com
- **المطور**: inkplus اينك بلس

## الترخيص

هذا المشروع مرخص تحت رخصة MIT.

## الإصدار

الإصدار الحالي: 1.0.0
```

## الخطوة 9: إنشاء ملف .gitignore
```gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# Database
*.db
*.sqlite
*.sqlite3
inventory.db

# Configuration files
config_local.py
.env
.env.local
.env.production

# Logs
*.log
logs/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Uploads
uploads/
temp/

# Backup files
*.bak
*.backup
backup_*

# Settings files
*_settings.json
store_settings.json
payment_methods.json
tax_settings.json
currency_settings.json
pos_settings.json

# Test files
test_*.py
tests/
.pytest_cache/

# Coverage
htmlcov/
.coverage
.coverage.*
coverage.xml

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# pipenv
Pipfile.lock

# PEP 582
__pypackages__/

# Celery
celerybeat-schedule
celerybeat.pid

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# Pyre type checker
.pyre/
```

## الخطوة 10: تعليمات Cursor AI

### 10.1 أوامر Cursor AI الأساسية
```
1. إنشاء هيكل المشروع
2. إنشاء ملفات Python الأساسية
3. إنشاء قوالب HTML
4. إنشاء ملفات CSS و JavaScript
5. إنشاء ملفات التشغيل
6. إنشاء ملفات التوثيق
```

### 10.2 نصائح لاستخدام Cursor AI
```
1. استخدم أوامر واضحة ومحددة
2. اطلب إنشاء ملفات كاملة
3. اطلب شرح الكود المكتوب
4. اطلب تحسين الكود
5. اطلب إضافة مميزات جديدة
6. اطلب إصلاح الأخطاء
```

## الخطوة 11: اختبار التطبيق

### 11.1 تشغيل التطبيق
```bash
python run.py
```

### 11.2 الوصول للتطبيق
- افتح المتصفح
- اذهب إلى http://localhost:5000
- سجل دخول باستخدام admin/admin123

## الخطوة 12: نشر التطبيق

### 12.1 إنشاء ملف ZIP
```bash
# Windows
powershell Compress-Archive -Path * -DestinationPath store_management_system.zip

# Linux/Mac
zip -r store_management_system.zip .
```

### 12.2 رفع على GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/store_management_system.git
git push -u origin main
```

## ملاحظات مهمة

1. **تأكد من تثبيت Python 3.7+**
2. **تأكد من تثبيت جميع المكتبات**
3. **اختبر التطبيق قبل النشر**
4. **احفظ نسخة احتياطية من قاعدة البيانات**
5. **تأكد من صحة جميع المسارات**

## الدعم

- **البريد الإلكتروني**: mfh1134@gmail.com
- **المطور**: inkplus اينك بلس

---

**هذا الدليل شامل لإنشاء نظام إدارة المخزون من الصفر باستخدام Cursor AI!**
