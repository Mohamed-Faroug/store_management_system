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
    """Initialize the database with schema and default data"""
    db = get_db()
    db.executescript(SCHEMA_SQL)

    # ---- Default Users ----
    cur = db.execute('SELECT COUNT(*) as c FROM users')
    if cur.fetchone()['c'] == 0:
        default_users = [
            ('owner', 'owner', generate_password_hash('owner'), 'all_permissions', 'hidden'),
            ('dev', 'dev', generate_password_hash('dev'), 'all_permissions', 'hidden'),
            ('admin', 'admin', generate_password_hash('admin123'), 'manage_users_inventory_sales', 'visible'),
            ('clerk', 'clerk', generate_password_hash('clerk123'), 'sales_inventory', 'visible')
        ]
        for role, username, pwd, perms, status in default_users:
            db.execute(
                'INSERT INTO users (role, username, password_hash, permissions, status) VALUES (?,?,?,?,?)',
                (role, username, pwd, perms, status)
            )
        db.commit()

    # ---- Default Categories ----
    cur = db.execute('SELECT COUNT(*) as c FROM categories')
    if cur.fetchone()['c'] == 0:
        default_categories = [
            ('Tires', 'Car tires of different types and sizes'),
            ('Exterior Accessories', 'Car exterior accessories - mirrors, bumpers, logos'),
            ('Interior Accessories', 'Car interior accessories - seats, curtains, covers'),
            ('Lighting', 'Car lighting systems - bulbs, LED lamps'),
            ('Audio Systems', 'Car audio and speaker systems'),
            ('Tools', 'Car tools and spare parts'),
            ('Oils and Lubricants', 'Engine oils, brake fluids, and lubricants'),
            ('Batteries', 'Car batteries of all types'),
            ('Spare Tires', 'Spare tires and related parts'),
            ('Alarms', 'Car security and alarm systems'),
            ('Phone Accessories', 'Phone holders and car chargers'),
            ('Cleaners and Care', 'Car cleaning and care materials'),
            ('Engine Parts', 'Engine spare parts and mechanical systems'),
            ('Brake Parts', 'Brake systems and spare parts'),
            ('Suspension Parts', 'Suspension systems and air seats')
        ]
        for name, desc in default_categories:
            db.execute('INSERT INTO categories (name, description) VALUES (?,?)', (name, desc))
        db.commit()

SCHEMA_SQL = r'''
PRAGMA foreign_keys = ON;
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT NOT NULL,                    -- role (owner, dev, admin, clerk)
        username TEXT UNIQUE NOT NULL,         -- username
        password_hash TEXT NOT NULL,           -- encrypted password
        permissions TEXT NOT NULL,             -- permissions
        status TEXT NOT NULL DEFAULT 'visible',-- status (visible / hidden)
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
    created_by_name TEXT,
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
