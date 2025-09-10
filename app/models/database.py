# -*- coding: utf-8 -*-
"""
نماذج قاعدة البيانات

المطور: محمد فاروق
التاريخ: 10/9/2025
"""

import sqlite3
import os
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask import g

def get_db():
    """الحصول على اتصال قاعدة البيانات"""
    from flask import current_app
    
    if 'db' not in g:
        database_path = current_app.config['DATABASE']
        os.makedirs(os.path.dirname(database_path), exist_ok=True)
        g.db = sqlite3.connect(database_path)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(exception=None):
    """إغلاق اتصال قاعدة البيانات"""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """تهيئة قاعدة البيانات"""
    from flask import current_app
    try:
        db = get_db()
        db.executescript(SCHEMA_SQL)
    except Exception as e:
        print(f"Database schema creation warning: {e}")
        # Continue with other initialization
    
    # Database migration - add new columns if they don't exist
    try:
        # Check if total_price column exists in sales table
        db.execute('SELECT total_price FROM sales LIMIT 1')
    except sqlite3.OperationalError:
        # Add missing columns to existing tables
        db.execute('ALTER TABLE sales ADD COLUMN total_price REAL NOT NULL DEFAULT 0')
        db.execute('ALTER TABLE sales ADD COLUMN invoice_id INTEGER')
        db.execute('ALTER TABLE items ADD COLUMN category_id INTEGER')
        db.execute('ALTER TABLE items ADD COLUMN description TEXT')
        db.execute('ALTER TABLE items ADD COLUMN cost_price REAL DEFAULT 0')
        db.execute('ALTER TABLE items ADD COLUMN selling_price REAL DEFAULT 0')
        db.execute('ALTER TABLE items ADD COLUMN image_url TEXT')
        db.commit()
    
    # Create categories table if it doesn't exist
    try:
        db.execute('SELECT * FROM categories LIMIT 1')
    except sqlite3.OperationalError:
        db.execute('''
            CREATE TABLE categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()
    
    # Create invoices table if it doesn't exist
    try:
        db.execute('SELECT * FROM invoices LIMIT 1')
    except sqlite3.OperationalError:
        db.execute('''
            CREATE TABLE invoices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                invoice_number TEXT UNIQUE NOT NULL,
                customer_name TEXT,
                customer_phone TEXT,
                total_amount REAL NOT NULL DEFAULT 0,
                discount_amount REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                final_amount REAL NOT NULL DEFAULT 0,
                payment_method TEXT DEFAULT 'cash',
                status TEXT DEFAULT 'completed',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER,
                FOREIGN KEY(created_by) REFERENCES users(id)
            )
        ''')
        db.commit()
    
    # Create purchases table if it doesn't exist
    try:
        db.execute('SELECT * FROM purchases LIMIT 1')
    except sqlite3.OperationalError:
        db.execute('''
            CREATE TABLE purchases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT,
                supplier_phone TEXT,
                total_amount REAL NOT NULL DEFAULT 0,
                discount_amount REAL DEFAULT 0,
                tax_amount REAL DEFAULT 0,
                final_amount REAL NOT NULL DEFAULT 0,
                payment_method TEXT DEFAULT 'cash',
                status TEXT DEFAULT 'completed',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                created_by INTEGER,
                FOREIGN KEY(created_by) REFERENCES users(id)
            )
        ''')
        db.commit()
    
    # Create purchase_items table if it doesn't exist
    try:
        db.execute('SELECT * FROM purchase_items LIMIT 1')
    except sqlite3.OperationalError:
        db.execute('''
            CREATE TABLE purchase_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                purchase_id INTEGER,
                item_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_cost REAL NOT NULL DEFAULT 0,
                total_cost REAL NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(purchase_id) REFERENCES purchases(id) ON DELETE CASCADE,
                FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
            )
        ''')
        db.commit()
        
        # Update existing sales records to have total_price
        existing_sales = db.execute('SELECT id, quantity, unit_price FROM sales WHERE total_price = 0').fetchall()
        for sale in existing_sales:
            total_price = sale['quantity'] * sale['unit_price']
            db.execute('UPDATE sales SET total_price = ? WHERE id = ?', (total_price, sale['id']))
        db.commit()
    
    # Add new columns to sales table if they don't exist
    try:
        db.execute('SELECT discount_amount FROM sales LIMIT 1')
    except sqlite3.OperationalError:
        db.execute('ALTER TABLE sales ADD COLUMN discount_amount REAL DEFAULT 0')
        db.execute('ALTER TABLE sales ADD COLUMN tax_amount REAL DEFAULT 0')
        db.execute('ALTER TABLE sales ADD COLUMN final_price REAL NOT NULL DEFAULT 0')
        
        # Update existing sales records
        existing_sales = db.execute('SELECT id, total_price FROM sales').fetchall()
        for sale in existing_sales:
            db.execute('UPDATE sales SET final_price = ? WHERE id = ?', (sale['total_price'], sale['id']))
        db.commit()
    
    # مستخدمين افتراضيين إذا لا يوجدون
    cur = db.execute('SELECT COUNT(*) as c FROM users')
    if cur.fetchone()['c'] == 0:
        db.execute('INSERT INTO users (username, password_hash, role) VALUES (?,?,?)',
                   ('admin', generate_password_hash('admin123'), 'manager'))
        db.execute('INSERT INTO users (username, password_hash, role) VALUES (?,?,?)',
                   ('clerk', generate_password_hash('clerk123'), 'clerk'))
        db.execute('INSERT INTO users (username, password_hash, role) VALUES (?,?,?)',
                   ('dev', generate_password_hash('dev'), 'dev'))
        db.commit()
    
    # التأكد من وجود مستخدم dev
    dev_user = db.execute('SELECT * FROM users WHERE username = ?', ('dev',)).fetchone()
    if not dev_user:
        db.execute('INSERT INTO users (username, password_hash, role) VALUES (?,?,?)',
                   ('dev', generate_password_hash('dev'), 'dev'))
        db.commit()
    else:
        # تحديث دور المستخدم dev إذا كان موجود
        db.execute('UPDATE users SET role = ? WHERE username = ?', ('dev', 'dev'))
        db.commit()
    
    # فئات افتراضية إذا لا توجد
    cur = db.execute('SELECT COUNT(*) as c FROM categories')
    if cur.fetchone()['c'] == 0:
        default_categories = [
            ('إطارات', 'إطارات السيارات بأنواعها وأحجام مختلفة'),
            ('زينة خارجية', 'زينة خارجية للسيارات - مرايا، مصدات، شعارات'),
            ('زينة داخلية', 'زينة داخلية للسيارات - مقاعد، ستائر، أغطية'),
            ('إضاءة', 'أنظمة الإضاءة للسيارات - لمبات، مصابيح LED'),
            ('صوتيات', 'أنظمة الصوت والسماعات للسيارات'),
            ('أدوات', 'أدوات وقطع غيار للسيارات'),
            ('زيوت ومواد تشحيم', 'زيوت المحرك والفرامل والمواد المساعدة'),
            ('بطاريات', 'بطاريات السيارات بأنواعها المختلفة'),
            ('إطارات احتياطية', 'إطارات احتياطية وقطع غيار الإطارات'),
            ('أجهزة إنذار', 'أنظمة الأمان والإنذار للسيارات'),
            ('أكسسوارات هواتف', 'حاملات الهواتف وشواحن السيارات'),
            ('منظفات ومواد العناية', 'منظفات السيارات ومواد العناية بها'),
            ('قطع غيار محرك', 'قطع غيار المحرك والأنظمة الميكانيكية'),
            ('قطع غيار فرامل', 'أنظمة الفرامل وقطع الغيار الخاصة بها'),
            ('قطع غيار تعليق', 'أنظمة التعليق والمقاعد الهوائية')
        ]
        for name, desc in default_categories:
            db.execute('INSERT INTO categories (name, description) VALUES (?,?)', (name, desc))
        db.commit()

SCHEMA_SQL = r'''
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('manager','clerk','dev')) NOT NULL DEFAULT 'clerk',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category_id INTEGER,
    sku TEXT UNIQUE,
    description TEXT,
    quantity INTEGER NOT NULL DEFAULT 0,
    reorder_level INTEGER NOT NULL DEFAULT 5,
    cost_price REAL DEFAULT 0,
    selling_price REAL DEFAULT 0,
    image_url TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(category_id) REFERENCES categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_number TEXT UNIQUE NOT NULL,
    customer_name TEXT,
    customer_phone TEXT,
    total_amount REAL NOT NULL DEFAULT 0,
    discount_amount REAL DEFAULT 0,
    tax_amount REAL DEFAULT 0,
    final_amount REAL NOT NULL DEFAULT 0,
    payment_method TEXT DEFAULT 'cash',
    status TEXT DEFAULT 'completed',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY(created_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    invoice_id INTEGER,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL DEFAULT 0,
    total_price REAL NOT NULL DEFAULT 0,
    discount_amount REAL DEFAULT 0,
    tax_amount REAL DEFAULT 0,
    final_price REAL NOT NULL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(invoice_id) REFERENCES invoices(id) ON DELETE CASCADE,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS purchases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT,
    supplier_phone TEXT,
    total_amount REAL NOT NULL DEFAULT 0,
    discount_amount REAL DEFAULT 0,
    tax_amount REAL DEFAULT 0,
    final_amount REAL NOT NULL DEFAULT 0,
    payment_method TEXT DEFAULT 'cash',
    status TEXT DEFAULT 'completed',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    FOREIGN KEY(created_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS purchase_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    purchase_id INTEGER,
    item_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_cost REAL NOT NULL DEFAULT 0,
    total_cost REAL NOT NULL DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(purchase_id) REFERENCES purchases(id) ON DELETE CASCADE,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
);
'''

def now_str():
    """الحصول على التاريخ والوقت الحالي كسلسلة نصية"""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
