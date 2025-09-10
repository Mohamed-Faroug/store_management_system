# التوثيق الفني - نظام إدارة المخزون

## نظرة عامة

هذا الملف يحتوي على التوثيق الفني الشامل لنظام إدارة المخزون، بما في ذلك هيكل قاعدة البيانات، نقاط نهاية API، ودليل إضافة الوحدات الجديدة.

## جدول المحتويات

1. [هيكل قاعدة البيانات](#هيكل-قاعدة-البيانات)
2. [نقاط نهاية API](#نقاط-نهاية-api)
3. [إضافة وحدات جديدة](#إضافة-وحدات-جديدة)
4. [معمارية التطبيق](#معمارية-التطبيق)
5. [إعدادات التطبيق](#إعدادات-التطبيق)

---

## هيكل قاعدة البيانات

### جداول قاعدة البيانات

#### 1. جدول المستخدمين (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'clerk',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

**الأدوار المتاحة:**
- `admin`: مدير النظام (جميع الصلاحيات)
- `manager`: مدير (إدارة المخزون والمبيعات)
- `clerk`: كاشير (المبيعات فقط)

#### 2. جدول الفئات (categories)
```sql
CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 3. جدول الأصناف (items)
```sql
CREATE TABLE items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    min_quantity INTEGER NOT NULL DEFAULT 0,
    category_id INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories (id)
);
```

#### 4. جدول المبيعات (sales)
```sql
CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

#### 5. جدول المشتريات (purchases)
```sql
CREATE TABLE purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    supplier TEXT,
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (item_id) REFERENCES items (id),
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

#### 6. جدول الفواتير (invoices)
```sql
CREATE TABLE invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE NOT NULL,
    customer_name TEXT,
    customer_phone TEXT,
    total_amount DECIMAL(10,2) NOT NULL,
    discount_amount DECIMAL(10,2) DEFAULT 0,
    tax_amount DECIMAL(10,2) DEFAULT 0,
    final_amount DECIMAL(10,2) NOT NULL,
    payment_method TEXT DEFAULT 'cash',
    user_id INTEGER NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

#### 7. جدول عناصر الفاتورة (invoice_items)
```sql
CREATE TABLE invoice_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (invoice_id) REFERENCES invoices (id),
    FOREIGN KEY (item_id) REFERENCES items (id)
);
```

---

## نقاط نهاية API

### 1. API المصادقة

#### تسجيل الدخول
```http
POST /login
Content-Type: application/x-www-form-urlencoded

username=admin&password=admin
```

**الاستجابة:**
```json
{
    "success": true,
    "message": "تم تسجيل الدخول بنجاح",
    "user": {
        "id": 1,
        "username": "admin",
        "role": "manager"
    }
}
```

#### تسجيل الخروج
```http
POST /logout
```

**الاستجابة:**
```json
{
    "success": true,
    "message": "تم تسجيل الخروج بنجاح"
}
```

### 2. API الأصناف

#### الحصول على جميع الأصناف
```http
GET /api/items
```

**الاستجابة:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "منتج 1",
            "description": "وصف المنتج",
            "price": 100.00,
            "quantity": 50,
            "min_quantity": 10,
            "category_id": 1,
            "category_name": "فئة 1"
        }
    ]
}
```

#### إضافة صنف جديد
```http
POST /api/items
Content-Type: application/json

{
    "name": "منتج جديد",
    "description": "وصف المنتج",
    "price": 150.00,
    "quantity": 25,
    "min_quantity": 5,
    "category_id": 1
}
```

#### تحديث صنف
```http
PUT /api/items/1
Content-Type: application/json

{
    "name": "منتج محدث",
    "price": 200.00
}
```

#### حذف صنف
```http
DELETE /api/items/1
```

### 3. API المبيعات

#### إضافة مبيعة جديدة
```http
POST /api/sales
Content-Type: application/json

{
    "item_id": 1,
    "quantity": 2,
    "unit_price": 100.00
}
```

#### الحصول على مبيعات اليوم
```http
GET /api/sales/today
```

### 4. API التقارير

#### إحصائيات عامة
```http
GET /api/stats
```

**الاستجابة:**
```json
{
    "success": true,
    "data": {
        "total_items": 150,
        "total_quantity": 2500,
        "low_stock_items": 5,
        "today_sales": 1500.00,
        "today_invoices": 25
    }
}
```

---

## إضافة وحدات جديدة

### 1. إنشاء وحدة جديدة

#### الخطوة 1: إنشاء ملف الوحدة
```python
# app/views/new_module.py
# -*- coding: utf-8 -*-
"""
وحدة جديدة - نظام إدارة المخزون
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..models.database import get_db
from ..utils.auth import login_required, manager_required

# إنشاء Blueprint للوحدة الجديدة
bp = Blueprint('new_module', __name__)

@bp.route('/new-module')
@login_required()
def index():
    """
    الصفحة الرئيسية للوحدة الجديدة
    """
    try:
        db = get_db()
        # منطق الوحدة
        data = db.execute('SELECT * FROM your_table').fetchall()
        return render_template('new_module/index.html', data=data)
    except Exception as e:
        print(f"❌ خطأ في الوحدة الجديدة: {e}")
        flash('حدث خطأ في تحميل البيانات', 'error')
        return redirect(url_for('main.index'))

@bp.route('/new-module/api', methods=['POST'])
@manager_required
def api_endpoint():
    """
    نقطة نهاية API للوحدة الجديدة
    """
    try:
        data = request.get_json()
        # معالجة البيانات
        return jsonify({'success': True, 'message': 'تم بنجاح'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
```

#### الخطوة 2: إنشاء القوالب
```html
<!-- app/templates/new_module/index.html -->
{% extends "base.html" %}

{% block title %}الوحدة الجديدة{% endblock %}

{% block content %}
<div class="container-fluid">
    <h1>الوحدة الجديدة</h1>
    <!-- محتوى الوحدة -->
</div>
{% endblock %}
```

#### الخطوة 3: تسجيل الوحدة
```python
# app/__init__.py
def create_app():
    # ... الكود الموجود ...
    
    # تسجيل الوحدة الجديدة
    from .views import new_module
    app.register_blueprint(new_module.bp, url_prefix='/new-module')
```

### 2. إضافة جدول جديد

#### الخطوة 1: إنشاء الجدول
```python
# app/models/database.py
def init_db():
    # ... الكود الموجود ...
    
    # إضافة الجدول الجديد
    db.executescript('''
        CREATE TABLE IF NOT EXISTS new_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    ''')
```

#### الخطوة 2: إضافة دوال قاعدة البيانات
```python
# app/models/new_module_model.py
def get_all_items():
    """الحصول على جميع العناصر"""
    db = get_db()
    return db.execute('SELECT * FROM new_table ORDER BY created_at DESC').fetchall()

def add_item(name, description):
    """إضافة عنصر جديد"""
    db = get_db()
    db.execute(
        'INSERT INTO new_table (name, description) VALUES (?, ?)',
        (name, description)
    )
    db.commit()
```

### 3. إضافة API جديد

#### إنشاء ملف API
```python
# app/views/api_new_module.py
from flask import Blueprint, request, jsonify
from ..utils.auth import login_required

api_bp = Blueprint('api_new_module', __name__)

@api_bp.route('/api/new-module', methods=['GET'])
@login_required()
def get_items():
    """الحصول على جميع العناصر"""
    try:
        # منطق API
        return jsonify({'success': True, 'data': []})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500
```

---

## معمارية التطبيق

### 1. هيكل المجلدات
```
app/
├── __init__.py              # تهيئة التطبيق
├── models/                  # نماذج البيانات
│   ├── database.py          # قاعدة البيانات
│   └── settings_models.py   # نماذج الإعدادات
├── views/                   # وحدات التحكم
│   ├── main.py             # الصفحة الرئيسية
│   ├── auth.py             # المصادقة
│   ├── items.py            # إدارة الأصناف
│   └── ...                 # باقي الوحدات
├── templates/              # قوالب HTML
│   ├── base.html           # القالب الأساسي
│   ├── dashboard.html      # لوحة التحكم
│   └── ...                 # باقي القوالب
├── static/                 # الملفات الثابتة
│   ├── css/                # ملفات CSS
│   └── js/                 # ملفات JavaScript
└── utils/                  # الأدوات المساعدة
    ├── auth.py             # أدوات المصادقة
    └── context_processors.py  # معالجات السياق
```

### 2. تدفق البيانات
```
المستخدم → القالب → الوحدة → قاعدة البيانات
    ↓         ↓        ↓         ↓
  HTML ← Jinja2 ← Python ← SQLite
```

### 3. نظام الصلاحيات
```
المستخدم → المصادقة → فحص الصلاحيات → الوصول للصفحة
    ↓         ↓           ↓              ↓
  Login ← Session ← Role Check ← Page Access
```

---

## إعدادات التطبيق

### 1. متغيرات البيئة
```bash
# إعدادات الإنتاج
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///inventory.db
DEBUG=False
FLASK_ENV=production

# إعدادات التطوير
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite:///inventory.db
DEBUG=True
FLASK_ENV=development
```

### 2. إعدادات قاعدة البيانات
```python
# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    DATABASE = os.environ.get('DATABASE_URL') or 'inventory.db'
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
```

### 3. إعدادات الأمان
```python
# إعدادات الأمان
app.config.update(
    SESSION_COOKIE_SECURE=True,      # HTTPS فقط
    SESSION_COOKIE_HTTPONLY=True,    # منع JavaScript
    SESSION_COOKIE_SAMESITE='Lax',   # حماية CSRF
    PERMANENT_SESSION_LIFETIME=timedelta(hours=24)  # انتهاء الجلسة
)
```

---

## الخلاصة

هذا التوثيق يغطي:
- **هيكل قاعدة البيانات**: جداول مفصلة مع العلاقات
- **نقاط نهاية API**: جميع APIs المتاحة
- **إضافة وحدات جديدة**: دليل شامل للتطوير
- **معمارية التطبيق**: هيكل وتدفق البيانات
- **إعدادات التطبيق**: تكوينات الإنتاج والتطوير

**استخدم هذا الدليل لتطوير وصيانة النظام!** 🚀
