# app.py
# -*- coding: utf-8 -*-
"""
تطبيق ويب مخزون بسيط لمحل زينة سيارات (ملف واحد)
— تسجيل الأصناف والكميات
— البيع اليومي مع خصم الكمية تلقائياً
— تنبيهات انخفاض المخزون
— مستخدمان افتراضيان: المدير (admin) والمشرف/الكاشير (clerk)

طريقة التشغيل:
1) ثبت المتطلبات:  pip install flask werkzeug
2) شغل التطبيق:    python casher1.py
3) افتح المتصفح على:  http://127.0.0.1:8080

بيانات الدخول الافتراضية:
- المدير:  admin / admin123
- الكاشير: clerk / clerk123
(يُنصح بتغييرها من صفحة "المستخدمون" بعد الدخول كمدير)
"""

import os
import sqlite3
from datetime import datetime
from flask import Flask, g, request, redirect, url_for, render_template_string, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

# ----------------------------- إعداد التطبيق -----------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), 'inventory.db')

# ----------------------------- قاعدة البيانات -----------------------------

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

SCHEMA_SQL = r'''
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT CHECK(role IN ('manager','clerk')) NOT NULL DEFAULT 'clerk',
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


def init_db():
    db = get_db()
    db.executescript(SCHEMA_SQL)
    
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

# ----------------------------- أدوات مساعدة -----------------------------

def login_required(role=None):
    def decorator(f):
        from functools import wraps
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('الرجاء تسجيل الدخول', 'warning')
                return redirect(url_for('login', next=request.path))
            if role:
                if session.get('role') != role:
                    flash('لا تملك صلاحية الوصول.', 'danger')
                    return redirect(url_for('index'))
            return f(*args, **kwargs)
        return wrapper
    return decorator


def now_str():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ----------------------------- صفحات المصادقة -----------------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    init_db()  # تأكد من تهيئة القاعدة في أول دخول
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
            return redirect(request.args.get('next') or url_for('index'))
        flash('بيانات الدخول غير صحيحة.', 'danger')
    inner = render_template_string(TPL_LOGIN)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/logout')
@login_required()
def logout():
    session.clear()
    flash('تم تسجيل الخروج.', 'info')
    return redirect(url_for('login'))

# ----------------------------- لوحة التحكم -----------------------------

@app.route('/')
@login_required()
def index():
    db = get_db()
    total_items = db.execute('SELECT COUNT(*) as c FROM items').fetchone()['c']
    total_qty = db.execute('SELECT IFNULL(SUM(quantity),0) as s FROM items').fetchone()['s']
    low_stock = db.execute('SELECT COUNT(*) as c FROM items WHERE quantity <= reorder_level').fetchone()['c']
    recent_sales = db.execute('''
        SELECT s.id, i.name, s.quantity, s.unit_price, s.total_price, s.created_at
        FROM sales s JOIN items i ON i.id = s.item_id
        ORDER BY s.created_at DESC LIMIT 10
    ''').fetchall()
    inner = render_template_string(TPL_DASHBOARD, data={
        'total_items': total_items,
        'total_qty': total_qty,
        'low_stock': low_stock,
        'recent_sales': recent_sales
    })
    return render_template_string(TPL_BASE, content=inner)

# ----------------------------- إدارة الأصناف -----------------------------

@app.route('/items')
@login_required()
def items_list():
    q = (request.args.get('q') or '').strip()
    db = get_db()
    if q:
        rows = db.execute('''
            SELECT i.*, c.name as category_name 
            FROM items i 
            LEFT JOIN categories c ON c.id = i.category_id 
            WHERE i.name LIKE ? OR c.name LIKE ? OR i.sku LIKE ? 
            ORDER BY i.id DESC
        ''', (f'%{q}%', f'%{q}%', f'%{q}%')).fetchall()
    else:
        rows = db.execute('''
            SELECT i.*, c.name as category_name 
            FROM items i 
            LEFT JOIN categories c ON c.id = i.category_id 
            ORDER BY i.id DESC
        ''').fetchall()
    inner = render_template_string(TPL_ITEMS_LIST, rows=rows, q=q)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/items/new', methods=['GET','POST'])
@login_required()
def items_new():
    if request.method == 'POST':
        name = request.form['name'].strip()
        category_id = request.form.get('category_id') or None
        sku = request.form.get('sku','').strip() or None
        description = request.form.get('description','').strip()
        quantity = int(request.form.get('quantity') or 0)
        reorder_level = int(request.form.get('reorder_level') or 5)
        cost_price = float(request.form.get('cost_price') or 0)
        selling_price = float(request.form.get('selling_price') or 0)
        image_url = request.form.get('image_url','').strip() or None
        db = get_db()
        db.execute('INSERT INTO items (name, category_id, sku, description, quantity, reorder_level, cost_price, selling_price, image_url) VALUES (?,?,?,?,?,?,?,?,?)',
                   (name, category_id, sku, description, quantity, reorder_level, cost_price, selling_price, image_url))
        db.commit()
        flash('تمت إضافة الصنف.', 'success')
        return redirect(url_for('items_list'))
    db = get_db()
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    inner = render_template_string(TPL_ITEMS_FORM, item=None, categories=categories)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/items/<int:item_id>/edit', methods=['GET','POST'])
@login_required()
def items_edit(item_id):
    db = get_db()
    item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    if not item:
        flash('الصنف غير موجود.', 'warning')
        return redirect(url_for('items_list'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        category_id = request.form.get('category_id') or None
        sku = request.form.get('sku','').strip() or None
        description = request.form.get('description','').strip()
        quantity = int(request.form.get('quantity') or 0)
        reorder_level = int(request.form.get('reorder_level') or 5)
        cost_price = float(request.form.get('cost_price') or 0)
        selling_price = float(request.form.get('selling_price') or 0)
        image_url = request.form.get('image_url','').strip() or None
        db.execute('UPDATE items SET name=?, category_id=?, sku=?, description=?, quantity=?, reorder_level=?, cost_price=?, selling_price=?, image_url=? WHERE id=?',
                   (name, category_id, sku, description, quantity, reorder_level, cost_price, selling_price, image_url, item_id))
        db.commit()
        flash('تم تحديث الصنف.', 'success')
        return redirect(url_for('items_list'))
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    inner = render_template_string(TPL_ITEMS_FORM, item=item, categories=categories)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/items/<int:item_id>/delete', methods=['POST'])
@login_required('manager')
def items_delete(item_id):
    db = get_db()
    db.execute('DELETE FROM items WHERE id = ?', (item_id,))
    db.commit()
    flash('تم حذف الصنف.', 'info')
    return redirect(url_for('items_list'))

# ----------------------------- البيع (الخصم من المخزون) -----------------------------

@app.route('/sales/new', methods=['GET','POST'])
@login_required()
def sales_new():
    db = get_db()
    items = db.execute('''
        SELECT i.*, c.name as category_name 
        FROM items i 
        LEFT JOIN categories c ON c.id = i.category_id 
        WHERE i.quantity > 0 
        ORDER BY i.name
    ''').fetchall()
    
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    
    if request.method == 'POST':
        # Handle cart-based sales
        item_ids = request.form.getlist('item_ids')
        quantities = request.form.getlist('quantities')
        prices = request.form.getlist('prices')
        
        if not item_ids:
            flash('لم يتم اختيار أي أصناف للبيع.', 'warning')
            return redirect(url_for('sales_new'))
        
        try:
            total_sales = 0
            for i, item_id in enumerate(item_ids):
                item_id = int(item_id)
                qty = int(quantities[i])
                price = float(prices[i])
                
                # جلب المخزون الحالي
                item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
                if not item:
                    flash(f'الصنف رقم {item_id} غير موجود.', 'danger')
                    return redirect(url_for('sales_new'))
                
                if item['quantity'] < qty:
                    flash(f'الكمية المطلوبة للصنف {item["name"]} أكبر من المتوفر بالمخزن.', 'warning')
                    return redirect(url_for('sales_new'))
                
                # استخدام سعر البيع إذا لم يتم تحديد سعر
                if price == 0 and item['selling_price'] > 0:
                    price = item['selling_price']
                
                total_price = qty * price
                total_sales += total_price
                
                # خصم من المخزون وتسجيل عملية البيع
                db.execute('UPDATE items SET quantity = quantity - ? WHERE id = ?', (qty, item_id))
                db.execute('INSERT INTO sales (item_id, quantity, unit_price, total_price, created_at) VALUES (?,?,?,?,?)',
                           (item_id, qty, price, total_price, now_str()))
            
            db.commit()
            flash(f'تم تسجيل البيع بنجاح! إجمالي المبيعات: {total_sales:.2f} ج.س', 'success')
            return redirect(url_for('index'))
            
        except (ValueError, IndexError) as e:
            flash('خطأ في البيانات المرسلة.', 'danger')
            return redirect(url_for('sales_new'))
    
    inner = render_template_string(TPL_SALES_FORM, items=items, categories=categories)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/sales')
@login_required()
def sales_list():
    db = get_db()
    rows = db.execute('''
        SELECT s.id, i.name, s.quantity, s.unit_price, s.total_price, s.created_at
        FROM sales s JOIN items i ON i.id = s.item_id
        ORDER BY s.created_at DESC
    ''').fetchall()
    inner = render_template_string(TPL_SALES_LIST, rows=rows)
    return render_template_string(TPL_BASE, content=inner)

# ----------------------------- إدارة الفئات -----------------------------

@app.route('/categories')
@login_required()
def categories_list():
    db = get_db()
    rows = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    inner = render_template_string(TPL_CATEGORIES_LIST, rows=rows)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/categories/new', methods=['GET','POST'])
@login_required('manager')
def categories_new():
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form.get('description','').strip()
        db = get_db()
        try:
            db.execute('INSERT INTO categories (name, description) VALUES (?,?)',
                       (name, description))
            db.commit()
            flash('تمت إضافة الفئة.', 'success')
            return redirect(url_for('categories_list'))
        except sqlite3.IntegrityError:
            flash('اسم الفئة مُستخدم من قبل.', 'danger')
    inner = render_template_string(TPL_CATEGORIES_FORM, category=None)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/categories/<int:category_id>/edit', methods=['GET','POST'])
@login_required('manager')
def categories_edit(category_id):
    db = get_db()
    category = db.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
    if not category:
        flash('الفئة غير موجودة.', 'warning')
        return redirect(url_for('categories_list'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        description = request.form.get('description','').strip()
        try:
            db.execute('UPDATE categories SET name=?, description=? WHERE id=?',
                       (name, description, category_id))
            db.commit()
            flash('تم تحديث الفئة.', 'success')
            return redirect(url_for('categories_list'))
        except sqlite3.IntegrityError:
            flash('اسم الفئة مُستخدم من قبل.', 'danger')
    inner = render_template_string(TPL_CATEGORIES_FORM, category=category)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required('manager')
def categories_delete(category_id):
    db = get_db()
    # Check if category has items
    items_count = db.execute('SELECT COUNT(*) as c FROM items WHERE category_id = ?', (category_id,)).fetchone()['c']
    if items_count > 0:
        flash('لا يمكن حذف الفئة لوجود أصناف مرتبطة بها.', 'warning')
        return redirect(url_for('categories_list'))
    db.execute('DELETE FROM categories WHERE id = ?', (category_id,))
    db.commit()
    flash('تم حذف الفئة.', 'info')
    return redirect(url_for('categories_list'))

# ----------------------------- إدارة المستخدمين (للمدير) -----------------------------

@app.route('/users')
@login_required('manager')
def users_list():
    rows = get_db().execute('SELECT id, username, role, created_at FROM users ORDER BY id DESC').fetchall()
    inner = render_template_string(TPL_USERS_LIST, rows=rows)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/users/new', methods=['GET','POST'])
@login_required('manager')
def users_new():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password']
        role = request.form.get('role','clerk')
        db = get_db()
        try:
            db.execute('INSERT INTO users (username, password_hash, role) VALUES (?,?,?)',
                       (username, generate_password_hash(password), role))
            db.commit()
            flash('تمت إضافة المستخدم.', 'success')
            return redirect(url_for('users_list'))
        except sqlite3.IntegrityError:
            flash('اسم المستخدم مُستخدم من قبل.', 'danger')
    inner = render_template_string(TPL_USERS_FORM)
    return render_template_string(TPL_BASE, content=inner)

# ----------------------------- إدارة الفواتير -----------------------------

@app.route('/invoices')
@login_required()
def invoices_list():
    db = get_db()
    rows = db.execute('''
        SELECT i.*, u.username as created_by_name
        FROM invoices i
        LEFT JOIN users u ON u.id = i.created_by
        ORDER BY i.created_at DESC
    ''').fetchall()
    inner = render_template_string(TPL_INVOICES_LIST, rows=rows)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/invoices/new', methods=['GET','POST'])
@login_required()
def invoices_new():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name','').strip()
        customer_phone = request.form.get('customer_phone','').strip()
        payment_method = request.form.get('payment_method','cash')
        discount_amount = float(request.form.get('discount_amount') or 0)
        tax_amount = float(request.form.get('tax_amount') or 0)
        
        # Handle cart-based invoice items
        item_ids = request.form.getlist('item_ids')
        quantities = request.form.getlist('quantities')
        prices = request.form.getlist('prices')
        
        if not item_ids:
            flash('لم يتم اختيار أي أصناف للفاتورة.', 'warning')
            return redirect(url_for('invoices_new'))
        
        try:
            # Generate invoice number
            db = get_db()
            invoice_count = db.execute('SELECT COUNT(*) as c FROM invoices').fetchone()['c']
            invoice_number = f"INV-{invoice_count + 1:06d}"
            
            # Calculate totals
            total_amount = 0
            for i, item_id in enumerate(item_ids):
                item_id = int(item_id)
                qty = int(quantities[i])
                price = float(prices[i])
                total_amount += qty * price
            
            final_amount = total_amount - discount_amount + tax_amount
            
            # Create invoice
            cursor = db.execute('''
                INSERT INTO invoices (invoice_number, customer_name, customer_phone, total_amount, 
                                    discount_amount, tax_amount, final_amount, payment_method, created_by)
                VALUES (?,?,?,?,?,?,?,?,?)
            ''', (invoice_number, customer_name, customer_phone, total_amount, 
                  discount_amount, tax_amount, final_amount, payment_method, session['user_id']))
            
            invoice_id = cursor.lastrowid
            
            # Add items to invoice
            for i, item_id in enumerate(item_ids):
                item_id = int(item_id)
                qty = int(quantities[i])
                price = float(prices[i])
                total_price = qty * price
                
                # Check stock availability
                item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
                if not item:
                    flash(f'الصنف رقم {item_id} غير موجود.', 'danger')
                    return redirect(url_for('invoices_new'))
                
                if item['quantity'] < qty:
                    flash(f'الكمية المطلوبة للصنف {item["name"]} أكبر من المتوفر بالمخزن.', 'warning')
                    return redirect(url_for('invoices_new'))
                
                # Add to sales
                db.execute('''
                    INSERT INTO sales (invoice_id, item_id, quantity, unit_price, total_price, created_at)
                    VALUES (?,?,?,?,?,?)
                ''', (invoice_id, item_id, qty, price, total_price, now_str()))
                
                # Update stock
                db.execute('UPDATE items SET quantity = quantity - ? WHERE id = ?', (qty, item_id))
            
            db.commit()
            flash(f'تم إنشاء الفاتورة بنجاح! رقم الفاتورة: {invoice_number}', 'success')
            return redirect(url_for('invoices_view', invoice_id=invoice_id))
            
        except (ValueError, IndexError) as e:
            flash('خطأ في البيانات المرسلة.', 'danger')
            return redirect(url_for('invoices_new'))
    
    db = get_db()
    items = db.execute('''
        SELECT i.*, c.name as category_name 
        FROM items i 
        LEFT JOIN categories c ON c.id = i.category_id 
        WHERE i.quantity > 0 
        ORDER BY i.name
    ''').fetchall()
    
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    
    inner = render_template_string(TPL_INVOICES_FORM, items=items, categories=categories)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/invoices/<int:invoice_id>')
@login_required()
def invoices_view(invoice_id):
    db = get_db()
    invoice = db.execute('''
        SELECT i.*, u.username as created_by_name
        FROM invoices i
        LEFT JOIN users u ON u.id = i.created_by
        WHERE i.id = ?
    ''', (invoice_id,)).fetchone()
    
    if not invoice:
        flash('الفاتورة غير موجودة.', 'warning')
        return redirect(url_for('invoices_list'))
    
    items = db.execute('''
        SELECT s.*, i.name as item_name, i.sku
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE s.invoice_id = ?
        ORDER BY s.id
    ''', (invoice_id,)).fetchall()
    
    inner = render_template_string(TPL_INVOICE_VIEW, invoice=invoice, items=items)
    return render_template_string(TPL_BASE, content=inner)

# ----------------------------- إدارة المشتريات -----------------------------

@app.route('/purchases')
@login_required()
def purchases_list():
    db = get_db()
    rows = db.execute('''
        SELECT p.*, u.username as created_by_name
        FROM purchases p
        LEFT JOIN users u ON u.id = p.created_by
        ORDER BY p.created_at DESC
    ''').fetchall()
    inner = render_template_string(TPL_PURCHASES_LIST, rows=rows)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/purchases/new', methods=['GET','POST'])
@login_required()
def purchases_new():
    if request.method == 'POST':
        supplier_name = request.form.get('supplier_name','').strip()
        supplier_phone = request.form.get('supplier_phone','').strip()
        payment_method = request.form.get('payment_method','cash')
        discount_amount = float(request.form.get('discount_amount') or 0)
        tax_amount = float(request.form.get('tax_amount') or 0)
        
        # Handle cart-based purchase items
        item_ids = request.form.getlist('item_ids')
        quantities = request.form.getlist('quantities')
        costs = request.form.getlist('costs')
        
        if not item_ids:
            flash('لم يتم اختيار أي أصناف للشراء.', 'warning')
            return redirect(url_for('purchases_new'))
        
        try:
            # Generate purchase number
            db = get_db()
            purchase_count = db.execute('SELECT COUNT(*) as c FROM purchases').fetchone()['c']
            purchase_number = f"PUR-{purchase_count + 1:06d}"
            
            # Calculate totals
            total_amount = 0
            for i, item_id in enumerate(item_ids):
                item_id = int(item_id)
                qty = int(quantities[i])
                cost = float(costs[i])
                total_amount += qty * cost
            
            final_amount = total_amount - discount_amount + tax_amount
            
            # Create purchase
            cursor = db.execute('''
                INSERT INTO purchases (supplier_name, supplier_phone, total_amount, 
                                    discount_amount, tax_amount, final_amount, payment_method, created_by)
                VALUES (?,?,?,?,?,?,?,?)
            ''', (supplier_name, supplier_phone, total_amount, 
                  discount_amount, tax_amount, final_amount, payment_method, session['user_id']))
            
            purchase_id = cursor.lastrowid
            
            # Add items to purchase
            for i, item_id in enumerate(item_ids):
                item_id = int(item_id)
                qty = int(quantities[i])
                cost = float(costs[i])
                total_cost = qty * cost
                
                # Check item exists
                item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
                if not item:
                    flash(f'الصنف رقم {item_id} غير موجود.', 'danger')
                    return redirect(url_for('purchases_new'))
                
                # Add to purchase items
                db.execute('''
                    INSERT INTO purchase_items (purchase_id, item_id, quantity, unit_cost, total_cost, created_at)
                    VALUES (?,?,?,?,?,?)
                ''', (purchase_id, item_id, qty, cost, total_cost, now_str()))
                
                # Update stock (add to inventory)
                db.execute('UPDATE items SET quantity = quantity + ? WHERE id = ?', (qty, item_id))
            
            db.commit()
            flash(f'تم إنشاء أمر الشراء بنجاح! رقم الأمر: {purchase_number}', 'success')
            return redirect(url_for('purchases_view', purchase_id=purchase_id))
            
        except (ValueError, IndexError) as e:
            flash('خطأ في البيانات المرسلة.', 'danger')
            return redirect(url_for('purchases_new'))
    
    db = get_db()
    items = db.execute('''
        SELECT i.*, c.name as category_name 
        FROM items i 
        LEFT JOIN categories c ON c.id = i.category_id 
        ORDER BY i.name
    ''').fetchall()
    
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    
    inner = render_template_string(TPL_PURCHASES_FORM, items=items, categories=categories)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/purchases/<int:purchase_id>')
@login_required()
def purchases_view(purchase_id):
    db = get_db()
    purchase = db.execute('''
        SELECT p.*, u.username as created_by_name
        FROM purchases p
        LEFT JOIN users u ON u.id = p.created_by
        WHERE p.id = ?
    ''', (purchase_id,)).fetchone()
    
    if not purchase:
        flash('أمر الشراء غير موجود.', 'warning')
        return redirect(url_for('purchases_list'))
    
    items = db.execute('''
        SELECT pi.*, i.name as item_name, i.sku
        FROM purchase_items pi
        JOIN items i ON i.id = pi.item_id
        WHERE pi.purchase_id = ?
        ORDER BY pi.id
    ''', (purchase_id,)).fetchall()
    
    inner = render_template_string(TPL_PURCHASE_VIEW, purchase=purchase, items=items)
    return render_template_string(TPL_BASE, content=inner)

# ----------------------------- إدارة المخزون -----------------------------

@app.route('/stock/adjust')
@login_required()
def stock_adjust():
    db = get_db()
    items = db.execute('''
        SELECT i.*, c.name as category_name 
        FROM items i 
        LEFT JOIN categories c ON c.id = i.category_id 
        ORDER BY i.name
    ''').fetchall()
    inner = render_template_string(TPL_STOCK_ADJUST, items=items)
    return render_template_string(TPL_BASE, content=inner)

@app.route('/stock/adjust', methods=['POST'])
@login_required()
def stock_adjust_post():
    item_id = int(request.form['item_id'])
    adjustment_type = request.form['adjustment_type']
    quantity = int(request.form['quantity'])
    reason = request.form.get('reason', '').strip()
    
    db = get_db()
    item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    if not item:
        flash('الصنف غير موجود.', 'danger')
        return redirect(url_for('stock_adjust'))
    
    # Calculate new quantity
    if adjustment_type == 'add':
        new_quantity = item['quantity'] + quantity
    else:  # subtract
        new_quantity = max(0, item['quantity'] - quantity)
    
    # Update quantity
    db.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_quantity, item_id))
    
    # Log the adjustment
    db.execute('''
        INSERT INTO sales (item_id, quantity, unit_price, total_price, created_at)
        VALUES (?,?,?,?,?)
    ''', (item_id, quantity if adjustment_type == 'add' else -quantity, 0, 0, now_str()))
    
    db.commit()
    
    action = 'إضافة' if adjustment_type == 'add' else 'خصم'
    flash(f'تم {action} {quantity} من المخزون. الكمية الجديدة: {new_quantity}', 'success')
    return redirect(url_for('stock_adjust'))

@app.route('/stock/alerts')
@login_required()
def stock_alerts():
    db = get_db()
    low_stock_items = db.execute('''
        SELECT i.*, c.name as category_name
        FROM items i
        LEFT JOIN categories c ON c.id = i.category_id
        WHERE i.quantity <= i.reorder_level
        ORDER BY i.quantity ASC
    ''').fetchall()
    
    out_of_stock_items = db.execute('''
        SELECT i.*, c.name as category_name
        FROM items i
        LEFT JOIN categories c ON c.id = i.category_id
        WHERE i.quantity = 0
        ORDER BY i.name
    ''').fetchall()
    
    inner = render_template_string(TPL_STOCK_ALERTS, data={
        'low_stock': low_stock_items,
        'out_of_stock': out_of_stock_items
    })
    return render_template_string(TPL_BASE, content=inner)

# ----------------------------- التقارير -----------------------------

@app.route('/reports')
@login_required()
def reports():
    db = get_db()
    
    # Sales summary
    sales_summary = db.execute('''
        SELECT 
            COUNT(*) as total_sales,
            SUM(quantity) as total_quantity,
            SUM(total_price) as total_revenue
        FROM sales
    ''').fetchone()
    
    # Top selling items
    top_items = db.execute('''
        SELECT i.name, SUM(s.quantity) as total_sold, SUM(s.total_price) as total_revenue
        FROM sales s
        JOIN items i ON i.id = s.item_id
        GROUP BY i.id, i.name
        ORDER BY total_sold DESC
        LIMIT 10
    ''').fetchall()
    
    # Low stock items
    low_stock = db.execute('''
        SELECT name, quantity, reorder_level
        FROM items
        WHERE quantity <= reorder_level
        ORDER BY quantity ASC
    ''').fetchall()
    
    inner = render_template_string(TPL_REPORTS, data={
        'sales_summary': sales_summary,
        'top_items': top_items,
        'low_stock': low_stock
    })
    return render_template_string(TPL_BASE, content=inner)

@app.route('/reports/daily')
@login_required()
def reports_daily():
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Daily sales
    daily_sales = db.execute('''
        SELECT 
            COUNT(*) as total_sales,
            SUM(quantity) as total_quantity,
            SUM(total_price) as total_revenue
        FROM sales
        WHERE DATE(created_at) = ?
    ''', (today,)).fetchone()
    
    # Daily top items
    daily_top_items = db.execute('''
        SELECT i.name, SUM(s.quantity) as total_sold, SUM(s.total_price) as total_revenue
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE DATE(s.created_at) = ?
        GROUP BY i.id, i.name
        ORDER BY total_sold DESC
        LIMIT 10
    ''', (today,)).fetchall()
    
    # Daily invoices
    daily_invoices = db.execute('''
        SELECT invoice_number, customer_name, final_amount, created_at
        FROM invoices
        WHERE DATE(created_at) = ?
        ORDER BY created_at DESC
    ''', (today,)).fetchall()
    
    inner = render_template_string(TPL_DAILY_REPORTS, data={
        'date': today,
        'sales_summary': daily_sales,
        'top_items': daily_top_items,
        'invoices': daily_invoices
    })
    return render_template_string(TPL_BASE, content=inner)

@app.route('/reports/monthly')
@login_required()
def reports_monthly():
    db = get_db()
    current_month = datetime.now().strftime('%Y-%m')
    
    # Monthly sales
    monthly_sales = db.execute('''
        SELECT 
            COUNT(*) as total_sales,
            SUM(quantity) as total_quantity,
            SUM(total_price) as total_revenue
        FROM sales
        WHERE strftime('%Y-%m', created_at) = ?
    ''', (current_month,)).fetchone()
    
    # Monthly top items
    monthly_top_items = db.execute('''
        SELECT i.name, SUM(s.quantity) as total_sold, SUM(s.total_price) as total_revenue
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE strftime('%Y-%m', s.created_at) = ?
        GROUP BY i.id, i.name
        ORDER BY total_sold DESC
        LIMIT 10
    ''', (current_month,)).fetchall()
    
    # Monthly invoices
    monthly_invoices = db.execute('''
        SELECT invoice_number, customer_name, final_amount, created_at
        FROM invoices
        WHERE strftime('%Y-%m', created_at) = ?
        ORDER BY created_at DESC
    ''', (current_month,)).fetchall()
    
    # Daily breakdown
    daily_breakdown = db.execute('''
        SELECT 
            DATE(created_at) as date,
            COUNT(*) as sales_count,
            SUM(total_price) as daily_revenue
        FROM sales
        WHERE strftime('%Y-%m', created_at) = ?
        GROUP BY DATE(created_at)
        ORDER BY date
    ''', (current_month,)).fetchall()
    
    inner = render_template_string(TPL_MONTHLY_REPORTS, data={
        'month': current_month,
        'sales_summary': monthly_sales,
        'top_items': monthly_top_items,
        'invoices': monthly_invoices,
        'daily_breakdown': daily_breakdown
    })
    return render_template_string(TPL_BASE, content=inner)

@app.route('/reports/yearly')
@login_required()
def reports_yearly():
    db = get_db()
    current_year = datetime.now().strftime('%Y')
    
    # Yearly sales
    yearly_sales = db.execute('''
        SELECT 
            COUNT(*) as total_sales,
            SUM(quantity) as total_quantity,
            SUM(total_price) as total_revenue
        FROM sales
        WHERE strftime('%Y', created_at) = ?
    ''', (current_year,)).fetchone()
    
    # Yearly top items
    yearly_top_items = db.execute('''
        SELECT i.name, SUM(s.quantity) as total_sold, SUM(s.total_price) as total_revenue
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE strftime('%Y', s.created_at) = ?
        GROUP BY i.id, i.name
        ORDER BY total_sold DESC
        LIMIT 10
    ''', (current_year,)).fetchall()
    
    # Monthly breakdown
    monthly_breakdown = db.execute('''
        SELECT 
            strftime('%Y-%m', created_at) as month,
            COUNT(*) as sales_count,
            SUM(total_price) as monthly_revenue
        FROM sales
        WHERE strftime('%Y', created_at) = ?
        GROUP BY strftime('%Y-%m', created_at)
        ORDER BY month
    ''', (current_year,)).fetchall()
    
    # Category performance
    category_performance = db.execute('''
        SELECT 
            c.name as category_name,
            COUNT(s.id) as sales_count,
            SUM(s.quantity) as total_quantity,
            SUM(s.total_price) as total_revenue
        FROM sales s
        JOIN items i ON i.id = s.item_id
        LEFT JOIN categories c ON c.id = i.category_id
        WHERE strftime('%Y', s.created_at) = ?
        GROUP BY c.id, c.name
        ORDER BY total_revenue DESC
    ''', (current_year,)).fetchall()
    
    inner = render_template_string(TPL_YEARLY_REPORTS, data={
        'year': current_year,
        'sales_summary': yearly_sales,
        'top_items': yearly_top_items,
        'monthly_breakdown': monthly_breakdown,
        'category_performance': category_performance
    })
    return render_template_string(TPL_BASE, content=inner)

# ----------------------------- الإعدادات -----------------------------

@app.route('/settings')
@login_required('manager')
def settings():
    db = get_db()
    # Get current settings (you can add a settings table later)
    inner = render_template_string(TPL_SETTINGS)
    return render_template_string(TPL_BASE, content=inner)

# ----------------------------- القوالب -----------------------------

TPL_BASE = r"""
<!doctype html>
<html lang="ar" dir="rtl">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>نظام إدارة المخزون - مخزن الزينة</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.rtl.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
      :root {
        --primary-color: #2c3e50;
        --secondary-color: #3498db;
        --success-color: #27ae60;
        --warning-color: #f39c12;
        --danger-color: #e74c3c;
        --info-color: #17a2b8;
        --light-bg: #f8f9fa;
        --dark-bg: #2c3e50;
        --gradient-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.15);
      }
      
      * {
        font-family: 'Cairo', sans-serif;
      }
      
      body {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
      }
      
      .navbar {
        background: var(--gradient-bg) !important;
        box-shadow: var(--shadow);
        border-bottom: 3px solid var(--secondary-color);
      }
      
      .navbar-brand {
        font-weight: 700;
        font-size: 1.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
      }
      
      .main-container {
        background: rgba(255, 255, 255, 0.95);
        border-radius: 20px;
        box-shadow: var(--shadow-lg);
        margin: 20px auto;
        padding: 30px;
        backdrop-filter: blur(10px);
      }
      
      .card {
        border: none;
        border-radius: 15px;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        overflow: hidden;
      }
      
      .card:hover {
        box-shadow: var(--shadow-lg);
      }
      
      .card-header {
        background: var(--gradient-bg);
        color: white;
        border: none;
        font-weight: 600;
        padding: 15px 20px;
      }
      
      .btn {
        border-radius: 10px;
        font-weight: 600;
        padding: 10px 20px;
        transition: all 0.3s ease;
        border: none;
        position: relative;
        overflow: hidden;
      }
      
      .btn::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.5s;
      }
      
      .btn:hover::before {
        left: 100%;
      }
      
      .btn-primary {
        background: linear-gradient(45deg, #3498db, #2980b9);
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4);
      }
      
      .btn-success {
        background: linear-gradient(45deg, #27ae60, #229954);
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.4);
      }
      
      .btn-warning {
        background: linear-gradient(45deg, #f39c12, #e67e22);
        box-shadow: 0 4px 15px rgba(243, 156, 18, 0.4);
      }
      
      .btn-danger {
        background: linear-gradient(45deg, #e74c3c, #c0392b);
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.4);
      }
      
      .btn-info {
        background: linear-gradient(45deg, #17a2b8, #138496);
        box-shadow: 0 4px 15px rgba(23, 162, 184, 0.4);
      }
      
      .btn-outline-primary {
        border: 2px solid var(--secondary-color);
        color: var(--secondary-color);
        background: transparent;
      }
      
      .btn-outline-primary:hover {
        background: var(--secondary-color);
      }
      
      .table {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: var(--shadow);
      }
      
      .table thead th {
        background: var(--gradient-bg);
        color: white;
        border: none;
        font-weight: 600;
        padding: 15px;
      }
      
      .table tbody tr {
        transition: all 0.3s ease;
      }
      
      .table tbody tr:hover {
        background: rgba(52, 152, 219, 0.1);
      }
      
      .form-control, .form-select {
        border-radius: 10px;
        border: 2px solid #e9ecef;
        padding: 12px 15px;
        transition: all 0.3s ease;
      }
      
      .form-control:focus, .form-select:focus {
        border-color: var(--secondary-color);
        box-shadow: 0 0 0 0.2rem rgba(52, 152, 219, 0.25);
      }
      
      .alert {
        border: none;
        border-radius: 15px;
        padding: 15px 20px;
        margin-bottom: 20px;
        box-shadow: var(--shadow);
        animation: slideInDown 0.5s ease;
      }
      
      @keyframes slideInDown {
        from {
          opacity: 0;
          transform: translateY(-30px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
      
      .stats-card {
        background: var(--gradient-bg);
        color: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        position: relative;
        overflow: hidden;
      }
      
      .stats-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        transition: all 0.3s ease;
      }
      
      .stats-card:hover::before {
        top: -25%;
        right: -25%;
      }
      
      .stats-card h3 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
      }
      
      .stats-card p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
      }
      
      .feature-card {
        background: white;
        border-radius: 20px;
        padding: 30px;
        text-align: center;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
        border: 3px solid transparent;
        position: relative;
        overflow: hidden;
      }
      
      .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 5px;
        background: var(--gradient-bg);
        transform: scaleX(0);
        transition: transform 0.3s ease;
      }
      
      .feature-card:hover {
        box-shadow: var(--shadow-lg);
        border-color: var(--secondary-color);
      }
      
      .feature-card:hover::before {
        transform: scaleX(1);
      }
      
      .feature-icon {
        font-size: 3rem;
        margin-bottom: 20px;
        background: var(--gradient-bg);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
      }
      
      .nav-pills .nav-link {
        border-radius: 10px;
        margin: 5px;
        font-weight: 600;
        transition: all 0.3s ease;
      }
      
      .nav-pills .nav-link.active {
        background: var(--gradient-bg);
        box-shadow: var(--shadow);
      }
      
      .badge {
        border-radius: 20px;
        padding: 8px 15px;
        font-weight: 600;
      }
      
      .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
      }
      
      @keyframes spin {
        to { transform: rotate(360deg); }
      }
      
      .fade-in {
        animation: fadeIn 0.5s ease-in;
      }
      
      @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
      }
      
      .pulse {
        animation: pulse 2s infinite;
      }
      
      @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
      }
      
      .sidebar {
        background: white;
        border-radius: 20px;
        box-shadow: var(--shadow);
        padding: 20px;
        margin-bottom: 20px;
      }
      
      .sidebar .nav-link {
        color: var(--primary-color);
        padding: 12px 20px;
        margin: 5px 0;
        border-radius: 10px;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
      }
      
      .sidebar .nav-link:hover {
        background: rgba(52, 152, 219, 0.1);
        color: var(--secondary-color);
      }
      
      .sidebar .nav-link i {
        margin-left: 10px;
        font-size: 1.2rem;
      }
      
      /* Print Styles */
      @media print {
        body * {
          visibility: hidden;
        }
        .printable, .printable * {
          visibility: visible;
        }
        .printable {
          position: absolute;
          left: 0;
          top: 0;
          width: 100%;
        }
        .no-print {
          display: none !important;
        }
        .card {
          border: 1px solid #000 !important;
          box-shadow: none !important;
        }
        .table {
          border-collapse: collapse !important;
        }
        .table th, .table td {
          border: 1px solid #000 !important;
        }
      }
    </style>
  </head>
  <body>
    <nav class="navbar navbar-expand-lg navbar-dark">
      <div class="container-fluid">
        <a class="navbar-brand" href="{{ url_for('index') }}">
          <i class="bi bi-shop me-2"></i>نظام إدارة المخزون
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <div class="navbar-nav me-auto">
            <a class="nav-link" href="{{ url_for('index') }}">
              <i class="bi bi-house-door me-1"></i>الرئيسية
            </a>
            <a class="nav-link" href="{{ url_for('items_list') }}">
              <i class="bi bi-box me-1"></i>الأصناف
            </a>
            <a class="nav-link" href="{{ url_for('categories_list') }}">
              <i class="bi bi-tags me-1"></i>الفئات
            </a>
            <a class="nav-link" href="{{ url_for('sales_new') }}">
              <i class="bi bi-cart-plus me-1"></i>بيع سريع
            </a>
            <a class="nav-link" href="{{ url_for('invoices_new') }}">
              <i class="bi bi-receipt me-1"></i>فاتورة جديدة
            </a>
            <a class="nav-link" href="{{ url_for('purchases_new') }}">
              <i class="bi bi-cart-dash me-1"></i>شراء جديد
            </a>
            <a class="nav-link" href="{{ url_for('reports') }}">
              <i class="bi bi-graph-up me-1"></i>التقارير
            </a>
          </div>
          <div class="navbar-nav">
            {% if session.get('username') %}
              <div class="nav-item dropdown">
                <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
                  <i class="bi bi-person-circle me-1"></i>{{ session['username'] }}
                  <span class="badge bg-light text-dark ms-1">{{ 'مدير' if session['role']=='manager' else 'كاشير' }}</span>
                </a>
                <ul class="dropdown-menu">
                  <li><a class="dropdown-item" href="{{ url_for('settings') if session.get('role')=='manager' else '#' }}">
                    <i class="bi bi-gear me-2"></i>الإعدادات
                  </a></li>
                  <li><hr class="dropdown-divider"></li>
                  <li><a class="dropdown-item" href="{{ url_for('logout') }}">
                    <i class="bi bi-box-arrow-right me-2"></i>تسجيل الخروج
                  </a></li>
                </ul>
              </div>
            {% endif %}
          </div>
        </div>
      </div>
    </nav>

    <main class="container-fluid">
      <div class="main-container fade-in">
        {% with messages = get_flashed_messages(with_categories=true) %}
          {% if messages %}
            {% for cat, msg in messages %}
              <div class="alert alert-{{cat}} alert-dismissible fade show" role="alert">
                <i class="bi bi-{{ 'check-circle' if cat=='success' else 'exclamation-triangle' if cat=='warning' else 'info-circle' if cat=='info' else 'x-circle' }} me-2"></i>
                {{ msg }}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
              </div>
            {% endfor %}
          {% endif %}
        {% endwith %}
        {{ content|safe }}
      </div>
    </main>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
      // Add loading states to buttons
      document.addEventListener('DOMContentLoaded', function() {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
          form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
              const originalText = submitBtn.innerHTML;
              submitBtn.innerHTML = '<span class="loading"></span> جاري المعالجة...';
              submitBtn.disabled = true;
            }
          });
        });
        
        // Add smooth scrolling
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
          anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
              behavior: 'smooth'
            });
          });
        });
        
        // Add tooltips
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
          return new bootstrap.Tooltip(tooltipTriggerEl);
        });
      });
    </script>
  </body>
</html>
"""

TPL_LOGIN = r"""
<div class="row justify-content-center align-items-center min-vh-100">
  <div class="col-md-5">
    <div class="card shadow-lg border-0">
      <div class="card-body p-5">
        <div class="text-center mb-4">
          <i class="bi bi-shop display-1 text-primary mb-3"></i>
          <h2 class="fw-bold text-primary">نظام إدارة المخزون</h2>
          <p class="text-muted">مرحباً بك في نظام إدارة مخزن الزينة</p>
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

<script>
// Bootstrap form validation
(function() {
  'use strict';
  window.addEventListener('load', function() {
    var forms = document.getElementsByClassName('needs-validation');
    var validation = Array.prototype.filter.call(forms, function(form) {
      form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
        form.classList.add('was-validated');
      }, false);
    });
  }, false);
})();
</script>
"""

TPL_DASHBOARD = r"""
<div class="row g-4 mb-5">
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-box feature-icon"></i>
      <h3>{{ data['total_items'] }}</h3>
      <p>إجمالي الأصناف</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-stack feature-icon"></i>
      <h3>{{ data['total_qty'] }}</h3>
      <p>إجمالي الكمية</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-exclamation-triangle feature-icon"></i>
      <h3 class="pulse">{{ data['low_stock'] }}</h3>
      <p>أصناف منخفضة</p>
    </div>
  </div>
</div>

<div class="row g-4 mb-5">
  <div class="col-md-3">
    <div class="feature-card">
      <i class="bi bi-box feature-icon"></i>
      <h5>إدارة الأصناف</h5>
      <p class="text-muted">إضافة وتعديل الأصناف</p>
      <a href="{{ url_for('items_list') }}" class="btn btn-primary">إدارة</a>
    </div>
  </div>
  <div class="col-md-3">
    <div class="feature-card">
      <i class="bi bi-tags feature-icon"></i>
      <h5>الفئات</h5>
      <p class="text-muted">تنظيم الأصناف بالفئات</p>
      <a href="{{ url_for('categories_list') }}" class="btn btn-outline-primary">إدارة</a>
    </div>
  </div>
  <div class="col-md-3">
    <div class="feature-card">
      <i class="bi bi-cart-plus feature-icon"></i>
      <h5>بيع سريع</h5>
      <p class="text-muted">تسجيل عملية بيع</p>
      <a href="{{ url_for('sales_new') }}" class="btn btn-success">بيع</a>
    </div>
  </div>
  <div class="col-md-3">
    <div class="feature-card">
      <i class="bi bi-receipt feature-icon"></i>
      <h5>فاتورة جديدة</h5>
      <p class="text-muted">إنشاء فاتورة متعددة الأصناف</p>
      <a href="{{ url_for('invoices_new') }}" class="btn btn-info">فاتورة</a>
    </div>
  </div>
  <div class="col-md-3">
    <div class="feature-card">
      <i class="bi bi-cart-dash feature-icon"></i>
      <h5>شراء جديد</h5>
      <p class="text-muted">إضافة أصناف للمخزون</p>
      <a href="{{ url_for('purchases_new') }}" class="btn btn-warning">شراء</a>
    </div>
  </div>
</div>

<div class="row g-4 mb-4">
  <div class="col-md-3">
    <div class="feature-card">
      <i class="bi bi-graph-up feature-icon"></i>
      <h5>التقارير</h5>
      <p class="text-muted">تقارير المبيعات والمخزون</p>
      <a href="{{ url_for('reports') }}" class="btn btn-outline-info">عرض</a>
    </div>
  </div>
  <div class="col-md-3">
    <div class="feature-card">
      <i class="bi bi-exclamation-triangle feature-icon"></i>
      <h5>تنبيهات المخزون</h5>
      <p class="text-muted">مراقبة الأصناف المنخفضة</p>
      <a href="{{ url_for('stock_alerts') }}" class="btn btn-warning">عرض</a>
    </div>
  </div>
  <div class="col-md-3">
    <div class="feature-card">
      <i class="bi bi-gear feature-icon"></i>
      <h5>تعديل المخزون</h5>
      <p class="text-muted">إضافة أو خصم من المخزون</p>
      <a href="{{ url_for('stock_adjust') }}" class="btn btn-outline-warning">تعديل</a>
    </div>
  </div>
  <div class="col-md-3">
    <div class="feature-card">
      <i class="bi bi-people feature-icon"></i>
      <h5>المستخدمون</h5>
      <p class="text-muted">إدارة المستخدمين والصلاحيات</p>
      {% if session.get('role')=='manager' %}
        <a href="{{ url_for('users_list') }}" class="btn btn-outline-secondary">إدارة</a>
      {% else %}
        <button class="btn btn-outline-secondary" disabled>غير متاح</button>
      {% endif %}
    </div>
  </div>
</div>

<div class="card">
  <div class="card-header">
    <h5 class="mb-0"><i class="bi bi-clock-history me-2"></i>آخر 10 مبيعات</h5>
  </div>
  <div class="card-body">
    <div class="table-responsive">
      <table class="table table-hover">
        <thead>
          <tr>
            <th><i class="bi bi-hash me-1"></i>#</th>
            <th><i class="bi bi-box me-1"></i>الصنف</th>
            <th><i class="bi bi-stack me-1"></i>الكمية</th>
            <th><i class="bi bi-currency-dollar me-1"></i>السعر</th>
            <th><i class="bi bi-calculator me-1"></i>المجموع</th>
            <th><i class="bi bi-calendar me-1"></i>التاريخ</th>
          </tr>
        </thead>
        <tbody>
          {% for r in data['recent_sales'] %}
          <tr>
            <td><span class="badge bg-primary">{{ r['id'] }}</span></td>
            <td><strong>{{ r['name'] }}</strong></td>
            <td><span class="badge bg-info">{{ r['quantity'] }}</span></td>
                <td>{{ '%.2f'|format(r['unit_price']) }} ج.س</td>
                <td><strong class="text-success">{{ '%.2f'|format(r['total_price']) }} ج.س</strong></td>
            <td><small class="text-muted">{{ r['created_at'] }}</small></td>
          </tr>
          {% else %}
          <tr>
            <td colspan="6" class="text-center text-muted py-4">
              <i class="bi bi-inbox display-4 d-block mb-3"></i>
              لا توجد بيانات بعد
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</div>
"""

TPL_ITEMS_LIST = r"""
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold text-primary mb-1">
      <i class="bi bi-box me-2"></i>إدارة الأصناف
    </h2>
    <p class="text-muted">إضافة وتعديل وإدارة أصناف المخزون</p>
  </div>
  <a href="{{ url_for('items_new') }}" class="btn btn-primary btn-lg">
    <i class="bi bi-plus-circle me-2"></i>إضافة صنف جديد
  </a>
</div>

<div class="card mb-4">
  <div class="card-body">
    <form method="get" class="row g-3">
      <div class="col-md-10">
        <div class="input-group input-group-lg">
          <span class="input-group-text">
            <i class="bi bi-search"></i>
          </span>
          <input type="search" name="q" value="{{ q }}" class="form-control" 
                 placeholder="البحث بالاسم، الفئة، أو الرمز...">
        </div>
      </div>
      <div class="col-md-2">
        <button class="btn btn-outline-primary btn-lg w-100" type="submit">
          <i class="bi bi-search me-1"></i>بحث
        </button>
      </div>
    </form>
  </div>
</div>

<div class="card">
  <div class="card-body p-0">
    <div class="table-responsive">
      <table class="table table-hover mb-0">
        <thead>
          <tr>
            <th><i class="bi bi-hash me-1"></i>#</th>
            <th><i class="bi bi-box me-1"></i>الاسم</th>
            <th><i class="bi bi-tags me-1"></i>الفئة</th>
            <th><i class="bi bi-upc me-1"></i>SKU</th>
            <th><i class="bi bi-stack me-1"></i>الكمية</th>
            <th><i class="bi bi-currency-dollar me-1"></i>سعر البيع</th>
            <th><i class="bi bi-exclamation-triangle me-1"></i>حد إعادة الطلب</th>
            <th><i class="bi bi-gear me-1"></i>إجراءات</th>
          </tr>
        </thead>
        <tbody>
          {% for r in rows %}
          <tr class="{% if r['quantity'] <= r['reorder_level'] %}table-warning{% endif %}">
            <td>
              <span class="badge bg-primary">{{ r['id'] }}</span>
            </td>
            <td>
              <div>
                <strong class="d-block">{{ r['name'] }}</strong>
                {% if r['description'] %}
                <small class="text-muted">{{ r['description'][:50] }}{% if r['description']|length > 50 %}...{% endif %}</small>
                {% endif %}
              </div>
            </td>
            <td>
              {% if r['category_name'] %}
                <span class="badge bg-info">{{ r['category_name'] }}</span>
              {% else %}
                <span class="text-muted">-</span>
              {% endif %}
            </td>
            <td>
              {% if r['sku'] %}
                <code>{{ r['sku'] }}</code>
              {% else %}
                <span class="text-muted">-</span>
              {% endif %}
            </td>
            <td>
              <span class="badge {% if r['quantity'] <= r['reorder_level'] %}bg-warning{% else %}bg-success{% endif %} fs-6">
                {{ r['quantity'] }}
              </span>
            </td>
            <td>
              {% if r['selling_price'] %}
                <strong class="text-success">{{ '%.2f'|format(r['selling_price']) }} ج.س</strong>
              {% else %}
                <span class="text-muted">-</span>
              {% endif %}
            </td>
            <td>
              <span class="badge bg-secondary">{{ r['reorder_level'] }}</span>
            </td>
            <td>
              <div class="btn-group" role="group">
                <a class="btn btn-outline-primary btn-sm" href="{{ url_for('items_edit', item_id=r['id']) }}" 
                   data-bs-toggle="tooltip" title="تعديل الصنف">
                  <i class="bi bi-pencil"></i>
                </a>
                {% if session.get('role')=='manager' %}
                <form action="{{ url_for('items_delete', item_id=r['id']) }}" method="post" style="display:inline" 
                      onsubmit="return confirm('هل أنت متأكد من حذف هذا الصنف؟');">
                  <button class="btn btn-outline-danger btn-sm" type="submit" 
                          data-bs-toggle="tooltip" title="حذف الصنف">
                    <i class="bi bi-trash"></i>
                  </button>
                </form>
                {% endif %}
              </div>
            </td>
          </tr>
          {% else %}
          <tr>
            <td colspan="8" class="text-center text-muted py-5">
              <i class="bi bi-inbox display-1 d-block mb-3"></i>
              <h5>لا توجد أصناف</h5>
              <p>ابدأ بإضافة أصناف جديدة إلى المخزون</p>
              <a href="{{ url_for('items_new') }}" class="btn btn-primary">
                <i class="bi bi-plus-circle me-2"></i>إضافة صنف جديد
              </a>
            </td>
          </tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
  </div>
</div>
"""

TPL_ITEMS_FORM = r"""
<div class="row justify-content-center">
  <div class="col-md-8">
    <div class="card shadow-sm">
      <div class="card-body">
        <h5 class="mb-3">{{ 'تعديل الصنف' if item else 'إضافة صنف جديد' }}</h5>
        <form method="post">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label">الاسم *</label>
              <input name="name" class="form-control" required value="{{ item['name'] if item else '' }}">
            </div>
            <div class="col-md-6">
              <label class="form-label">الفئة</label>
              <select name="category_id" class="form-select">
                <option value="">اختر الفئة</option>
                {% for cat in categories %}
                <option value="{{ cat['id'] }}" {% if item and item['category_id'] == cat['id'] %}selected{% endif %}>{{ cat['name'] }}</option>
                {% endfor %}
              </select>
            </div>
            <div class="col-md-6">
              <label class="form-label">SKU (اختياري)</label>
              <input name="sku" class="form-control" value="{{ item['sku'] if item else '' }}">
            </div>
            <div class="col-md-6">
              <label class="form-label">رابط الصورة (اختياري)</label>
              <input name="image_url" type="url" class="form-control" value="{{ item['image_url'] if item else '' }}">
            </div>
            <div class="col-12">
              <label class="form-label">الوصف</label>
              <textarea name="description" class="form-control" rows="3">{{ item['description'] if item else '' }}</textarea>
            </div>
            <div class="col-md-3">
              <label class="form-label">الكمية *</label>
              <input name="quantity" type="number" min="0" step="1" class="form-control" value="{{ item['quantity'] if item else 0 }}" required>
            </div>
            <div class="col-md-3">
              <label class="form-label">حد إعادة الطلب</label>
              <input name="reorder_level" type="number" min="0" step="1" class="form-control" value="{{ item['reorder_level'] if item else 5 }}">
            </div>
            <div class="col-md-3">
              <label class="form-label">سعر التكلفة</label>
              <input name="cost_price" type="number" step="0.01" min="0" class="form-control" value="{{ item['cost_price'] if item else 0 }}">
            </div>
            <div class="col-md-3">
              <label class="form-label">سعر البيع</label>
              <input name="selling_price" type="number" step="0.01" min="0" class="form-control" value="{{ item['selling_price'] if item else 0 }}">
            </div>
          </div>
          <div class="mt-3 d-flex gap-2">
            <button class="btn btn-primary">حفظ</button>
            <a href="{{ url_for('items_list') }}" class="btn btn-outline-secondary">رجوع</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
"""

TPL_SALES_FORM = r"""
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold text-primary mb-1">
      <i class="bi bi-cart-plus me-2"></i>تسجيل بيع سريع
    </h2>
    <p class="text-muted">اختر الأصناف وأضفها إلى سلة البيع</p>
  </div>
  <a href="{{ url_for('index') }}" class="btn btn-outline-secondary">
    <i class="bi bi-arrow-right me-2"></i>العودة للرئيسية
  </a>
</div>

<!-- Search Bar -->
<div class="card mb-4">
  <div class="card-body">
    <div class="row g-3">
      <div class="col-md-8">
        <div class="input-group input-group-lg">
          <span class="input-group-text">
            <i class="bi bi-search"></i>
          </span>
          <input type="text" id="itemSearch" class="form-control" placeholder="البحث عن الأصناف...">
        </div>
      </div>
      <div class="col-md-4">
        <select id="categoryFilter" class="form-select form-select-lg">
          <option value="">جميع الفئات</option>
          {% for category in categories %}
          <option value="{{ category['id'] }}">{{ category['name'] }}</option>
          {% endfor %}
        </select>
      </div>
    </div>
  </div>
</div>

<div class="row">
  <!-- Items Grid -->
  <div class="col-md-8">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-grid me-2"></i>الأصناف المتاحة
        </h5>
      </div>
      <div class="card-body">
        <div id="itemsGrid" class="row g-3">
          {% for item in items %}
          <div class="col-md-4 item-card" data-name="{{ item['name']|lower }}" data-category="{{ item['category_id'] or '' }}">
            <div class="card h-100 item-card-inner" data-item-id="{{ item['id'] }}" data-price="{{ item['selling_price'] or 0 }}">
              <div class="card-body text-center">
                <div class="mb-3">
                  {% if item['image_url'] %}
                    <img src="{{ item['image_url'] }}" class="img-fluid rounded" style="max-height: 100px; object-fit: cover;">
                  {% else %}
                    <i class="bi bi-box display-1 text-muted"></i>
                  {% endif %}
                </div>
                <h6 class="card-title">{{ item['name'] }}</h6>
                <p class="text-muted small mb-2">{{ item['category_name'] or 'بدون فئة' }}</p>
                <div class="mb-2">
                  <span class="badge bg-info">الكمية: {{ item['quantity'] }}</span>
                  {% if item['sku'] %}
                    <br><small class="text-muted">{{ item['sku'] }}</small>
                  {% endif %}
                </div>
                <div class="mb-3">
                  <strong class="text-success">{{ '%.2f'|format(item['selling_price']) if item['selling_price'] else '0.00' }} ج.س</strong>
                </div>
                <button class="btn btn-primary btn-sm add-to-cart" data-item-id="{{ item['id'] }}" data-name="{{ item['name'] }}" data-price="{{ item['selling_price'] or 0 }}">
                  <i class="bi bi-plus-circle me-1"></i>إضافة
                </button>
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
      </div>
    </div>
  </div>
  
  <!-- Cart -->
  <div class="col-md-4">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-cart me-2"></i>سلة البيع
        </h5>
      </div>
      <div class="card-body">
        <form method="post" id="salesForm">
          <div id="cartItems">
            <p class="text-muted text-center">لا توجد أصناف في السلة</p>
          </div>
          <div id="cartTotal" class="mt-3" style="display: none;">
            <hr>
            <div class="d-flex justify-content-between">
              <strong>المجموع:</strong>
              <strong id="totalAmount">0.00 ج.س</strong>
            </div>
          </div>
          <div class="mt-3">
            <button type="submit" class="btn btn-success w-100" id="submitBtn" disabled>
              <i class="bi bi-check-circle me-2"></i>تسجيل البيع
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('itemSearch');
  const categoryFilter = document.getElementById('categoryFilter');
  const itemsGrid = document.getElementById('itemsGrid');
  const cartItems = document.getElementById('cartItems');
  const cartTotal = document.getElementById('cartTotal');
  const totalAmount = document.getElementById('totalAmount');
  const submitBtn = document.getElementById('submitBtn');
  const salesForm = document.getElementById('salesForm');
  
  let cart = [];
  
  // Search functionality
  function filterItems() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    
    const itemCards = document.querySelectorAll('.item-card');
    itemCards.forEach(card => {
      const name = card.dataset.name;
      const category = card.dataset.category;
      
      const matchesSearch = name.includes(searchTerm);
      const matchesCategory = !selectedCategory || category === selectedCategory;
      
      if (matchesSearch && matchesCategory) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  }
  
  searchInput.addEventListener('input', filterItems);
  categoryFilter.addEventListener('change', filterItems);
  
  // Add to cart functionality
  function addToCart(itemId, name, price) {
    const existingItem = cart.find(item => item.id === itemId);
    
    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      cart.push({
        id: itemId,
        name: name,
        price: parseFloat(price),
        quantity: 1
      });
    }
    
    updateCartDisplay();
  }
  
  function removeFromCart(itemId) {
    cart = cart.filter(item => item.id !== itemId);
    updateCartDisplay();
  }
  
  function updateQuantity(itemId, newQuantity) {
    const item = cart.find(item => item.id === itemId);
    if (item) {
      if (newQuantity <= 0) {
        removeFromCart(itemId);
      } else {
        item.quantity = newQuantity;
        updateCartDisplay();
      }
    }
  }
  
  function updateCartDisplay() {
    if (cart.length === 0) {
      cartItems.innerHTML = '<p class="text-muted text-center">لا توجد أصناف في السلة</p>';
      cartTotal.style.display = 'none';
      submitBtn.disabled = true;
      return;
    }
    
    let html = '';
    let total = 0;
    
    cart.forEach(item => {
      const itemTotal = item.price * item.quantity;
      total += itemTotal;
      
      html += `
        <div class="card mb-2">
          <div class="card-body p-2">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="mb-1">${item.name}</h6>
                <small class="text-muted">${item.price.toFixed(2)} ج.س</small>
              </div>
              <div class="d-flex align-items-center">
                <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                <span class="mx-2">${item.quantity}</span>
                <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeFromCart(${item.id})">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            <div class="text-end">
              <strong>${itemTotal.toFixed(2)} ج.س</strong>
            </div>
          </div>
        </div>
      `;
    });
    
    cartItems.innerHTML = html;
    totalAmount.textContent = total.toFixed(2) + ' ج.س';
    cartTotal.style.display = 'block';
    submitBtn.disabled = false;
    
    // Add hidden inputs for form submission
    salesForm.innerHTML = `
      <div id="cartItems">${html}</div>
      <div id="cartTotal" class="mt-3">
        <hr>
        <div class="d-flex justify-content-between">
          <strong>المجموع:</strong>
          <strong id="totalAmount">${total.toFixed(2)} ج.س</strong>
        </div>
      </div>
      <div class="mt-3">
        <button type="submit" class="btn btn-success w-100" id="submitBtn">
          <i class="bi bi-check-circle me-2"></i>تسجيل البيع
        </button>
      </div>
    `;
    
    // Add hidden inputs for each cart item
    cart.forEach(item => {
      const itemIdInput = document.createElement('input');
      itemIdInput.type = 'hidden';
      itemIdInput.name = 'item_ids';
      itemIdInput.value = item.id;
      salesForm.appendChild(itemIdInput);
      
      const quantityInput = document.createElement('input');
      quantityInput.type = 'hidden';
      quantityInput.name = 'quantities';
      quantityInput.value = item.quantity;
      salesForm.appendChild(quantityInput);
      
      const priceInput = document.createElement('input');
      priceInput.type = 'hidden';
      priceInput.name = 'prices';
      priceInput.value = item.price;
      salesForm.appendChild(priceInput);
    });
  }
  
  // Add to cart event listeners
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('add-to-cart')) {
      const itemId = parseInt(e.target.dataset.itemId);
      const name = e.target.dataset.name;
      const price = parseFloat(e.target.dataset.price);
      
      addToCart(itemId, name, price);
      
      // Visual feedback
      e.target.innerHTML = '<i class="bi bi-check me-1"></i>تمت الإضافة';
      e.target.classList.remove('btn-primary');
      e.target.classList.add('btn-success');
      
      setTimeout(() => {
        e.target.innerHTML = '<i class="bi bi-plus-circle me-1"></i>إضافة';
        e.target.classList.remove('btn-success');
        e.target.classList.add('btn-primary');
      }, 1000);
    }
  });
  
  // Make functions global for onclick handlers
  window.updateQuantity = updateQuantity;
  window.removeFromCart = removeFromCart;
});
</script>
"""

TPL_SALES_LIST = r"""
<h4>سجل المبيعات</h4>
<table class="table table-striped table-sm">
  <thead><tr><th>#</th><th>الصنف</th><th>الكمية</th><th>السعر للوحدة</th><th>المجموع</th><th>التاريخ</th></tr></thead>
  <tbody>
    {% for r in rows %}
    <tr>
      <td>{{ r['id'] }}</td>
      <td>{{ r['name'] }}</td>
      <td>{{ r['quantity'] }}</td>
      <td>{{ '%.2f'|format(r['unit_price']) }}</td>
      <td><strong>{{ '%.2f'|format(r['total_price']) }}</strong></td>
      <td>{{ r['created_at'] }}</td>
    </tr>
    {% else %}
    <tr><td colspan="6" class="text-center text-muted">لا توجد عمليات بعد</td></tr>
    {% endfor %}
  </tbody>
</table>
"""

TPL_USERS_LIST = r"""
<div class="d-flex justify-content-between align-items-center mb-3">
  <h4 class="m-0">المستخدمون</h4>
  <a href="{{ url_for('users_new') }}" class="btn btn-sm btn-primary">إضافة مستخدم</a>
</div>
<table class="table table-hover table-sm">
  <thead><tr><th>#</th><th>اسم المستخدم</th><th>الدور</th><th>أُنشئ</th></tr></thead>
  <tbody>
    {% for r in rows %}
    <tr><td>{{ r['id'] }}</td><td>{{ r['username'] }}</td><td>{{ 'مدير' if r['role']=='manager' else 'كاشير' }}</td><td>{{ r['created_at'] }}</td></tr>
    {% else %}
    <tr><td colspan="4" class="text-center text-muted">لا يوجد مستخدمون</td></tr>
    {% endfor %}
  </tbody>
</table>
"""

TPL_USERS_FORM = r"""
<div class="row justify-content-center">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-body">
        <h5 class="mb-3">مستخدم جديد</h5>
        <form method="post">
          <div class="mb-3">
            <label class="form-label">اسم المستخدم</label>
            <input name="username" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">كلمة المرور</label>
            <input name="password" type="password" class="form-control" required>
          </div>
          <div class="mb-3">
            <label class="form-label">الدور</label>
            <select name="role" class="form-select">
              <option value="clerk">كاشير / مشرف</option>
              <option value="manager">مدير</option>
            </select>
          </div>
          <button class="btn btn-primary">حفظ</button>
          <a href="{{ url_for('users_list') }}" class="btn btn-outline-secondary ms-2">رجوع</a>
        </form>
      </div>
    </div>
  </div>
</div>
"""

TPL_CATEGORIES_LIST = r"""
<div class="d-flex justify-content-between align-items-center mb-3">
  <h4 class="m-0">الفئات</h4>
  <a href="{{ url_for('categories_new') }}" class="btn btn-sm btn-primary">إضافة فئة</a>
</div>
<table class="table table-hover table-sm">
  <thead><tr><th>#</th><th>الاسم</th><th>الوصف</th><th>تاريخ الإنشاء</th><th>إجراءات</th></tr></thead>
  <tbody>
    {% for r in rows %}
    <tr>
      <td>{{ r['id'] }}</td>
      <td><strong>{{ r['name'] }}</strong></td>
      <td>{{ r['description'] or '-' }}</td>
      <td>{{ r['created_at'] }}</td>
      <td>
        <a class="btn btn-sm btn-outline-secondary" href="{{ url_for('categories_edit', category_id=r['id']) }}">تعديل</a>
        <form action="{{ url_for('categories_delete', category_id=r['id']) }}" method="post" style="display:inline" onsubmit="return confirm('حذف الفئة؟');">
          <button class="btn btn-sm btn-outline-danger">حذف</button>
        </form>
      </td>
    </tr>
    {% else %}
    <tr><td colspan="5" class="text-center text-muted">لا توجد فئات</td></tr>
    {% endfor %}
  </tbody>
</table>
"""

TPL_CATEGORIES_FORM = r"""
<div class="row justify-content-center">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-body">
        <h5 class="mb-3">{{ 'تعديل الفئة' if category else 'إضافة فئة جديدة' }}</h5>
        <form method="post">
          <div class="mb-3">
            <label class="form-label">اسم الفئة</label>
            <input name="name" class="form-control" required value="{{ category['name'] if category else '' }}">
          </div>
          <div class="mb-3">
            <label class="form-label">الوصف</label>
            <textarea name="description" class="form-control" rows="3">{{ category['description'] if category else '' }}</textarea>
          </div>
          <div class="d-flex gap-2">
            <button class="btn btn-primary">حفظ</button>
            <a href="{{ url_for('categories_list') }}" class="btn btn-outline-secondary">رجوع</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>
"""

TPL_REPORTS = r"""
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold text-primary mb-1">
      <i class="bi bi-graph-up me-2"></i>التقارير والإحصائيات
    </h2>
    <p class="text-muted">تحليل شامل لأداء المبيعات والمخزون</p>
  </div>
  <div class="d-flex gap-2">
    <button class="btn btn-outline-primary" onclick="window.print()">
      <i class="bi bi-printer me-2"></i>طباعة التقرير
    </button>
  </div>
</div>

<!-- Report Navigation -->
<div class="row g-3 mb-4">
  <div class="col-md-3">
    <div class="card text-center">
      <div class="card-body">
        <i class="bi bi-calendar-day display-4 text-primary mb-3"></i>
        <h5>التقرير اليومي</h5>
        <p class="text-muted">مبيعات اليوم</p>
        <a href="{{ url_for('reports_daily') }}" class="btn btn-primary">عرض</a>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-center">
      <div class="card-body">
        <i class="bi bi-calendar-month display-4 text-info mb-3"></i>
        <h5>التقرير الشهري</h5>
        <p class="text-muted">مبيعات الشهر</p>
        <a href="{{ url_for('reports_monthly') }}" class="btn btn-info">عرض</a>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-center">
      <div class="card-body">
        <i class="bi bi-calendar3 display-4 text-success mb-3"></i>
        <h5>التقرير السنوي</h5>
        <p class="text-muted">مبيعات السنة</p>
        <a href="{{ url_for('reports_yearly') }}" class="btn btn-success">عرض</a>
      </div>
    </div>
  </div>
  <div class="col-md-3">
    <div class="card text-center">
      <div class="card-body">
        <i class="bi bi-graph-up display-4 text-warning mb-3"></i>
        <h5>التقرير العام</h5>
        <p class="text-muted">جميع المبيعات</p>
        <a href="{{ url_for('reports') }}" class="btn btn-warning">عرض</a>
      </div>
    </div>
  </div>
</div>

<div class="row g-4 mb-5">
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-cart-check feature-icon"></i>
      <h3>{{ data['sales_summary']['total_sales'] or 0 }}</h3>
      <p>إجمالي المبيعات</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-stack feature-icon"></i>
      <h3>{{ data['sales_summary']['total_quantity'] or 0 }}</h3>
      <p>إجمالي الكمية المباعة</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-currency-dollar feature-icon"></i>
      <h3>{{ '%.2f'|format(data['sales_summary']['total_revenue'] or 0) }}</h3>
      <p>إجمالي الإيرادات (ج.س)</p>
    </div>
  </div>
</div>

<div class="row g-4">
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-trophy me-2"></i>أكثر الأصناف مبيعاً
        </h5>
      </div>
      <div class="card-body">
        {% if data['top_items'] %}
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><i class="bi bi-medal me-1"></i>الترتيب</th>
                <th><i class="bi bi-box me-1"></i>الصنف</th>
                <th><i class="bi bi-stack me-1"></i>الكمية</th>
                <th><i class="bi bi-currency-dollar me-1"></i>الإيراد</th>
              </tr>
            </thead>
            <tbody>
              {% for item in data['top_items'] %}
              <tr>
                <td>
                  <span class="badge {% if loop.index == 1 %}bg-warning{% elif loop.index == 2 %}bg-secondary{% elif loop.index == 3 %}bg-info{% else %}bg-light text-dark{% endif %}">
                    {{ loop.index }}
                  </span>
                </td>
                <td><strong>{{ item['name'] }}</strong></td>
                <td><span class="badge bg-success">{{ item['total_sold'] }}</span></td>
                <td><strong class="text-success">{{ '%.2f'|format(item['total_revenue']) }} ج.س</strong></td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <div class="text-center text-muted py-4">
          <i class="bi bi-inbox display-4 d-block mb-3"></i>
          <p>لا توجد بيانات مبيعات بعد</p>
        </div>
        {% endif %}
      </div>
    </div>
  </div>
  
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-exclamation-triangle me-2"></i>أصناف منخفضة المخزون
        </h5>
      </div>
      <div class="card-body">
        {% if data['low_stock'] %}
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><i class="bi bi-box me-1"></i>الصنف</th>
                <th><i class="bi bi-stack me-1"></i>الكمية الحالية</th>
                <th><i class="bi bi-exclamation-triangle me-1"></i>حد إعادة الطلب</th>
                <th><i class="bi bi-gear me-1"></i>إجراءات</th>
              </tr>
            </thead>
            <tbody>
              {% for item in data['low_stock'] %}
              <tr class="table-warning">
                <td><strong>{{ item['name'] }}</strong></td>
                <td>
                  <span class="badge bg-warning fs-6">{{ item['quantity'] }}</span>
                </td>
                <td>
                  <span class="badge bg-secondary">{{ item['reorder_level'] }}</span>
                </td>
                <td>
                  <a href="{{ url_for('stock_adjust') }}" class="btn btn-outline-warning btn-sm">
                    <i class="bi bi-plus-circle me-1"></i>إضافة مخزون
                  </a>
                </td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <div class="text-center text-success py-4">
          <i class="bi bi-check-circle display-4 d-block mb-3"></i>
          <p>جميع الأصناف في مستوى جيد</p>
        </div>
        {% endif %}
      </div>
    </div>
  </div>
</div>
"""

TPL_SETTINGS = r"""
<div class="row justify-content-center">
  <div class="col-md-8">
    <div class="card shadow-sm">
      <div class="card-body">
        <h5 class="mb-4">إعدادات النظام</h5>
        <div class="row g-3">
          <div class="col-md-6">
            <div class="card border">
              <div class="card-body">
                <h6 class="card-title">إعدادات المخزون</h6>
                <p class="card-text">تكوين حدود إعادة الطلب الافتراضية وإعدادات التنبيهات</p>
                <button class="btn btn-outline-primary btn-sm">تعديل</button>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card border">
              <div class="card-body">
                <h6 class="card-title">إعدادات المبيعات</h6>
                <p class="card-text">تكوين الضرائب والخصومات وطرق الدفع</p>
                <button class="btn btn-outline-primary btn-sm">تعديل</button>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card border">
              <div class="card-body">
                <h6 class="card-title">إعدادات النظام</h6>
                <p class="card-text">تكوين اسم المتجر والعنوان ومعلومات الاتصال</p>
                <button class="btn btn-outline-primary btn-sm">تعديل</button>
              </div>
            </div>
          </div>
          <div class="col-md-6">
            <div class="card border">
              <div class="card-body">
                <h6 class="card-title">النسخ الاحتياطي</h6>
                <p class="card-text">إدارة النسخ الاحتياطية واستعادة البيانات</p>
                <button class="btn btn-outline-primary btn-sm">إدارة</button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
"""

TPL_INVOICES_LIST = r"""
<div class="d-flex justify-content-between align-items-center mb-3">
  <h4 class="m-0">الفواتير</h4>
  <a href="{{ url_for('invoices_new') }}" class="btn btn-sm btn-primary">فاتورة جديدة</a>
</div>
<table class="table table-hover table-sm">
  <thead><tr><th>#</th><th>رقم الفاتورة</th><th>العميل</th><th>المجموع</th><th>طريقة الدفع</th><th>التاريخ</th><th>إجراءات</th></tr></thead>
  <tbody>
    {% for r in rows %}
    <tr>
      <td>{{ r['id'] }}</td>
      <td><strong>{{ r['invoice_number'] }}</strong></td>
      <td>{{ r['customer_name'] or 'عميل نقدي' }}</td>
      <td>{{ '%.2f'|format(r['final_amount']) }}</td>
      <td>{{ 'نقدي' if r['payment_method'] == 'cash' else 'بطاقة' }}</td>
      <td>{{ r['created_at'] }}</td>
      <td>
        <a class="btn btn-sm btn-outline-primary" href="{{ url_for('invoices_view', invoice_id=r['id']) }}">عرض</a>
      </td>
    </tr>
    {% else %}
    <tr><td colspan="7" class="text-center text-muted">لا توجد فواتير</td></tr>
    {% endfor %}
  </tbody>
</table>
"""

TPL_INVOICES_FORM = r"""
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold text-primary mb-1">
      <i class="bi bi-receipt me-2"></i>فاتورة جديدة
    </h2>
    <p class="text-muted">إنشاء فاتورة متعددة الأصناف</p>
  </div>
  <a href="{{ url_for('invoices_list') }}" class="btn btn-outline-secondary">
    <i class="bi bi-arrow-right me-2"></i>عرض الفواتير
  </a>
</div>

<!-- Customer Info -->
<div class="card mb-4">
  <div class="card-header">
    <h5 class="mb-0">
      <i class="bi bi-person me-2"></i>معلومات العميل
    </h5>
  </div>
  <div class="card-body">
    <div class="row g-3">
      <div class="col-md-4">
        <label class="form-label fw-semibold">اسم العميل</label>
        <input name="customer_name" class="form-control form-control-lg" placeholder="أدخل اسم العميل">
      </div>
      <div class="col-md-4">
        <label class="form-label fw-semibold">رقم الهاتف</label>
        <input name="customer_phone" class="form-control form-control-lg" placeholder="أدخل رقم الهاتف">
      </div>
      <div class="col-md-4">
        <label class="form-label fw-semibold">طريقة الدفع</label>
        <select name="payment_method" class="form-select form-select-lg">
          <option value="cash">نقدي</option>
          <option value="card">بطاقة</option>
        </select>
      </div>
    </div>
  </div>
</div>

<!-- Search Bar -->
<div class="card mb-4">
  <div class="card-body">
    <div class="row g-3">
      <div class="col-md-8">
        <div class="input-group input-group-lg">
          <span class="input-group-text">
            <i class="bi bi-search"></i>
          </span>
          <input type="text" id="itemSearch" class="form-control" placeholder="البحث عن الأصناف...">
        </div>
      </div>
      <div class="col-md-4">
        <select id="categoryFilter" class="form-select form-select-lg">
          <option value="">جميع الفئات</option>
          {% for category in categories %}
          <option value="{{ category['id'] }}">{{ category['name'] }}</option>
          {% endfor %}
        </select>
      </div>
    </div>
  </div>
</div>

<div class="row">
  <!-- Items Grid -->
  <div class="col-md-8">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-grid me-2"></i>الأصناف المتاحة
        </h5>
      </div>
      <div class="card-body">
        <div id="itemsGrid" class="row g-3">
          {% for item in items %}
          <div class="col-md-4 item-card" data-name="{{ item['name']|lower }}" data-category="{{ item['category_id'] or '' }}">
            <div class="card h-100 item-card-inner" data-item-id="{{ item['id'] }}" data-price="{{ item['selling_price'] or 0 }}">
              <div class="card-body text-center">
                <div class="mb-3">
                  {% if item['image_url'] %}
                    <img src="{{ item['image_url'] }}" class="img-fluid rounded" style="max-height: 100px; object-fit: cover;">
                  {% else %}
                    <i class="bi bi-box display-1 text-muted"></i>
                  {% endif %}
                </div>
                <h6 class="card-title">{{ item['name'] }}</h6>
                <p class="text-muted small mb-2">{{ item['category_name'] or 'بدون فئة' }}</p>
                <div class="mb-2">
                  <span class="badge bg-info">الكمية: {{ item['quantity'] }}</span>
                  {% if item['sku'] %}
                    <br><small class="text-muted">{{ item['sku'] }}</small>
                  {% endif %}
                </div>
                <div class="mb-3">
                  <strong class="text-success">{{ '%.2f'|format(item['selling_price']) if item['selling_price'] else '0.00' }} ج.س</strong>
                </div>
                <button class="btn btn-primary btn-sm add-to-invoice" data-item-id="{{ item['id'] }}" data-name="{{ item['name'] }}" data-price="{{ item['selling_price'] or 0 }}">
                  <i class="bi bi-plus-circle me-1"></i>إضافة للفاتورة
                </button>
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
      </div>
    </div>
  </div>
  
  <!-- Invoice Items -->
  <div class="col-md-4">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-receipt me-2"></i>أصناف الفاتورة
        </h5>
      </div>
      <div class="card-body">
        <form method="post" id="invoiceForm">
          <div id="invoiceItems">
            <p class="text-muted text-center">لا توجد أصناف في الفاتورة</p>
          </div>
          
          <div class="mt-3" id="invoiceTotals" style="display: none;">
            <hr>
            <div class="row g-2">
              <div class="col-6">
                <label class="form-label small">الخصم</label>
                <input name="discount_amount" type="number" step="0.01" class="form-control form-control-sm" value="0" id="discountInput">
              </div>
              <div class="col-6">
                <label class="form-label small">الضريبة</label>
                <input name="tax_amount" type="number" step="0.01" class="form-control form-control-sm" value="0" id="taxInput">
              </div>
            </div>
            <hr>
            <div class="d-flex justify-content-between">
              <strong>المجموع النهائي:</strong>
              <strong id="finalTotal">0.00 ج.س</strong>
            </div>
          </div>
          
          <div class="mt-3">
            <button type="submit" class="btn btn-success w-100" id="submitBtn" disabled>
              <i class="bi bi-check-circle me-2"></i>إنشاء الفاتورة
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const container = document.getElementById('itemsContainer');
    const addBtn = document.getElementById('addItem');
    const finalTotal = document.getElementById('finalTotal');
    
    function addItemRow() {
        const newRow = container.querySelector('.item-row').cloneNode(true);
        newRow.querySelectorAll('input, select').forEach(input => input.value = '');
        container.appendChild(newRow);
        attachRowEvents(newRow);
    }
    
    function attachRowEvents(row) {
        const itemSelect = row.querySelector('.item-select');
        const quantityInput = row.querySelector('.quantity-input');
        const priceInput = row.querySelector('.price-input');
        const totalInput = row.querySelector('.total-input');
        const removeBtn = row.querySelector('.remove-item');
        
        function updateRowTotal() {
            const price = parseFloat(priceInput.value) || parseFloat(itemSelect.options[itemSelect.selectedIndex]?.dataset.price) || 0;
            const quantity = parseInt(quantityInput.value) || 0;
            const total = price * quantity;
            totalInput.value = total.toFixed(2);
            updateFinalTotal();
        }
        
        itemSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            const defaultPrice = parseFloat(selectedOption?.dataset.price) || 0;
            priceInput.value = defaultPrice;
            updateRowTotal();
        });
        
        quantityInput.addEventListener('input', updateRowTotal);
        priceInput.addEventListener('input', updateRowTotal);
        
        removeBtn.addEventListener('click', function() {
            if (container.children.length > 1) {
                row.remove();
                updateFinalTotal();
            }
        });
        
        updateRowTotal();
    }
    
    function updateFinalTotal() {
        let total = 0;
        container.querySelectorAll('.total-input').forEach(input => {
            total += parseFloat(input.value) || 0;
        });
        finalTotal.textContent = total.toFixed(2);
    }
    
  // Search functionality
  function filterItems() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    
    const itemCards = document.querySelectorAll('.item-card');
    itemCards.forEach(card => {
      const name = card.dataset.name;
      const category = card.dataset.category;
      
      const matchesSearch = name.includes(searchTerm);
      const matchesCategory = !selectedCategory || category === selectedCategory;
      
      if (matchesSearch && matchesCategory) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  }
  
  searchInput.addEventListener('input', filterItems);
  categoryFilter.addEventListener('change', filterItems);
  
  // Add to invoice functionality
  function addToInvoice(itemId, name, price) {
    const existingItem = invoiceCart.find(item => item.id === itemId);
    
    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      invoiceCart.push({
        id: itemId,
        name: name,
        price: parseFloat(price),
        quantity: 1
      });
    }
    
    updateInvoiceDisplay();
  }
  
  function removeFromInvoice(itemId) {
    invoiceCart = invoiceCart.filter(item => item.id !== itemId);
    updateInvoiceDisplay();
  }
  
  function updateQuantity(itemId, newQuantity) {
    const item = invoiceCart.find(item => item.id === itemId);
    if (item) {
      if (newQuantity <= 0) {
        removeFromInvoice(itemId);
      } else {
        item.quantity = newQuantity;
        updateInvoiceDisplay();
      }
    }
  }
  
  function updateInvoiceDisplay() {
    if (invoiceCart.length === 0) {
      invoiceItems.innerHTML = '<p class="text-muted text-center">لا توجد أصناف في الفاتورة</p>';
      invoiceTotals.style.display = 'none';
      submitBtn.disabled = true;
      return;
    }
    
    let html = '';
    let subtotal = 0;
    
    invoiceCart.forEach(item => {
      const itemTotal = item.price * item.quantity;
      subtotal += itemTotal;
      
      html += `
        <div class="card mb-2">
          <div class="card-body p-2">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="mb-1">${item.name}</h6>
                <small class="text-muted">${item.price.toFixed(2)} ج.س</small>
              </div>
              <div class="d-flex align-items-center">
                <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                <span class="mx-2">${item.quantity}</span>
                <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeFromInvoice(${item.id})">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            <div class="text-end">
              <strong>${itemTotal.toFixed(2)} ج.س</strong>
            </div>
          </div>
        </div>
      `;
    });
    
    invoiceItems.innerHTML = html;
    invoiceTotals.style.display = 'block';
    submitBtn.disabled = false;
    
    updateFinalTotal();
  }
  
  function updateFinalTotal() {
    const subtotal = invoiceCart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    const discount = parseFloat(discountInput.value) || 0;
    const tax = parseFloat(taxInput.value) || 0;
    const final = subtotal - discount + tax;
    
    finalTotal.textContent = final.toFixed(2) + ' ج.س';
    
    // Update form with hidden inputs
    updateFormInputs();
  }
  
  function updateFormInputs() {
    // Clear existing hidden inputs
    const existingInputs = invoiceForm.querySelectorAll('input[type="hidden"]');
    existingInputs.forEach(input => input.remove());
    
    // Add hidden inputs for each invoice item
    invoiceCart.forEach(item => {
      const itemIdInput = document.createElement('input');
      itemIdInput.type = 'hidden';
      itemIdInput.name = 'item_ids';
      itemIdInput.value = item.id;
      invoiceForm.appendChild(itemIdInput);
      
      const quantityInput = document.createElement('input');
      quantityInput.type = 'hidden';
      quantityInput.name = 'quantities';
      quantityInput.value = item.quantity;
      invoiceForm.appendChild(quantityInput);
      
      const priceInput = document.createElement('input');
      priceInput.type = 'hidden';
      priceInput.name = 'prices';
      priceInput.value = item.price;
      invoiceForm.appendChild(priceInput);
    });
  }
  
  // Add to invoice event listeners
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('add-to-invoice')) {
      const itemId = parseInt(e.target.dataset.itemId);
      const name = e.target.dataset.name;
      const price = parseFloat(e.target.dataset.price);
      
      addToInvoice(itemId, name, price);
      
      // Visual feedback
      e.target.innerHTML = '<i class="bi bi-check me-1"></i>تمت الإضافة';
      e.target.classList.remove('btn-primary');
      e.target.classList.add('btn-success');
      
      setTimeout(() => {
        e.target.innerHTML = '<i class="bi bi-plus-circle me-1"></i>إضافة للفاتورة';
        e.target.classList.remove('btn-success');
        e.target.classList.add('btn-primary');
      }, 1000);
    }
  });
  
  // Update totals when discount or tax changes
  discountInput.addEventListener('input', updateFinalTotal);
  taxInput.addEventListener('input', updateFinalTotal);
  
  // Make functions global for onclick handlers
  window.updateQuantity = updateQuantity;
  window.removeFromInvoice = removeFromInvoice;
});
</script>
"""

TPL_INVOICE_VIEW = r"""
<div class="row justify-content-center">
  <div class="col-md-8">
    <div class="card shadow-sm">
      <div class="card-header no-print">
        <h5 class="mb-0">فاتورة رقم: {{ invoice['invoice_number'] }}</h5>
        <small class="text-muted">تاريخ الإنشاء: {{ invoice['created_at'] }}</small>
      </div>
      <div class="card-body printable">
        <!-- Print Header -->
        <div class="text-center mb-4 no-print" id="printHeader">
          <h2 class="fw-bold">فاتورة مبيعات</h2>
          <h4>رقم الفاتورة: {{ invoice['invoice_number'] }}</h4>
          <p>تاريخ: {{ invoice['created_at'] }}</p>
        </div>
        
        <div class="row mb-4">
          <div class="col-md-6">
            <h6>بيانات العميل:</h6>
            <p><strong>الاسم:</strong> {{ invoice['customer_name'] or 'عميل نقدي' }}</p>
            <p><strong>الهاتف:</strong> {{ invoice['customer_phone'] or '-' }}</p>
          </div>
          <div class="col-md-6">
            <h6>بيانات الفاتورة:</h6>
            <p><strong>طريقة الدفع:</strong> {{ 'نقدي' if invoice['payment_method'] == 'cash' else 'بطاقة' }}</p>
            <p><strong>أنشأها:</strong> {{ invoice['created_by_name'] }}</p>
          </div>
        </div>
        
        <h6>الأصناف:</h6>
        <table class="table table-sm">
          <thead><tr><th>الصنف</th><th>الكمية</th><th>السعر</th><th>المجموع</th></tr></thead>
          <tbody>
            {% for item in items %}
            <tr>
              <td>{{ item['item_name'] }}</td>
              <td>{{ item['quantity'] }}</td>
              <td>{{ '%.2f'|format(item['unit_price']) }} ج.س</td>
              <td>{{ '%.2f'|format(item['total_price']) }} ج.س</td>
            </tr>
            {% endfor %}
          </tbody>
          <tfoot>
            <tr><td colspan="3"><strong>المجموع الفرعي:</strong></td><td><strong>{{ '%.2f'|format(invoice['total_amount']) }} ج.س</strong></td></tr>
            {% if invoice['discount_amount'] > 0 %}
            <tr><td colspan="3"><strong>الخصم:</strong></td><td><strong>-{{ '%.2f'|format(invoice['discount_amount']) }} ج.س</strong></td></tr>
            {% endif %}
            {% if invoice['tax_amount'] > 0 %}
            <tr><td colspan="3"><strong>الضريبة:</strong></td><td><strong>{{ '%.2f'|format(invoice['tax_amount']) }} ج.س</strong></td></tr>
            {% endif %}
            <tr class="table-primary"><td colspan="3"><strong>المجموع النهائي:</strong></td><td><strong>{{ '%.2f'|format(invoice['final_amount']) }} ج.س</strong></td></tr>
          </tfoot>
        </table>
        
        <div class="mt-4 d-flex gap-2 no-print">
          <button class="btn btn-primary" onclick="printInvoice()">طباعة الفاتورة</button>
          <a href="{{ url_for('invoices_list') }}" class="btn btn-outline-secondary">رجوع</a>
        </div>
      </div>
    </div>
  </div>
</div>

<script>
function printInvoice() {
  // Show print header
  document.getElementById('printHeader').style.display = 'block';
  
  // Print the page
  window.print();
  
  // Hide print header after printing
  setTimeout(() => {
    document.getElementById('printHeader').style.display = 'none';
  }, 1000);
}
</script>
"""

TPL_STOCK_ADJUST = r"""
<div class="row justify-content-center">
  <div class="col-md-6">
    <div class="card shadow-sm">
      <div class="card-body">
        <h5 class="mb-3">تعديل المخزون</h5>
        <form method="post">
          <div class="mb-3">
            <label class="form-label">الصنف</label>
            <select name="item_id" class="form-select" required id="itemSelect">
              <option value="">اختر الصنف</option>
              {% for item in items %}
              <option value="{{ item['id'] }}" data-current="{{ item['quantity'] }}">
                {{ item['name'] }} 
                {% if item['category_name'] %}({{ item['category_name'] }}){% endif %}
                - الكمية الحالية: {{ item['quantity'] }}
              </option>
              {% endfor %}
            </select>
          </div>
          
          <div class="mb-3">
            <label class="form-label">نوع التعديل</label>
            <select name="adjustment_type" class="form-select" required>
              <option value="add">إضافة للمخزون</option>
              <option value="subtract">خصم من المخزون</option>
            </select>
          </div>
          
          <div class="mb-3">
            <label class="form-label">الكمية</label>
            <input name="quantity" type="number" min="1" class="form-control" required>
          </div>
          
          <div class="mb-3">
            <label class="form-label">السبب (اختياري)</label>
            <textarea name="reason" class="form-control" rows="2" placeholder="سبب التعديل"></textarea>
          </div>
          
          <div class="mb-3">
            <div class="card bg-light">
              <div class="card-body">
                <h6>الكمية الحالية: <span id="currentQty">-</span></h6>
                <h6>الكمية بعد التعديل: <span id="newQty">-</span></h6>
              </div>
            </div>
          </div>
          
          <div class="d-flex gap-2">
            <button type="submit" class="btn btn-warning">تطبيق التعديل</button>
            <a href="{{ url_for('index') }}" class="btn btn-outline-secondary">رجوع</a>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
    const itemSelect = document.getElementById('itemSelect');
    const adjustmentType = document.querySelector('select[name="adjustment_type"]');
    const quantityInput = document.querySelector('input[name="quantity"]');
    const currentQty = document.getElementById('currentQty');
    const newQty = document.getElementById('newQty');
    
    function updateQuantities() {
        const selectedOption = itemSelect.options[itemSelect.selectedIndex];
        const current = parseInt(selectedOption?.dataset.current) || 0;
        const quantity = parseInt(quantityInput.value) || 0;
        const type = adjustmentType.value;
        
        currentQty.textContent = current;
        
        if (type === 'add') {
            newQty.textContent = current + quantity;
        } else {
            newQty.textContent = Math.max(0, current - quantity);
        }
    }
    
    itemSelect.addEventListener('change', updateQuantities);
    adjustmentType.addEventListener('change', updateQuantities);
    quantityInput.addEventListener('input', updateQuantities);
});
</script>
"""

TPL_STOCK_ALERTS = r"""
<div class="row">
  <div class="col-md-6">
    <div class="card border-danger">
      <div class="card-header bg-danger text-white">
        <h5 class="mb-0">أصناف نفدت من المخزون</h5>
      </div>
      <div class="card-body">
        {% if data['out_of_stock'] %}
        <table class="table table-sm">
          <thead><tr><th>الصنف</th><th>الفئة</th><th>إجراءات</th></tr></thead>
          <tbody>
            {% for item in data['out_of_stock'] %}
            <tr>
              <td><strong>{{ item['name'] }}</strong></td>
              <td>{{ item['category_name'] or '-' }}</td>
              <td>
                <a href="{{ url_for('items_edit', item_id=item['id']) }}" class="btn btn-sm btn-outline-primary">تعديل</a>
                <a href="{{ url_for('stock_adjust') }}" class="btn btn-sm btn-outline-warning">تعديل المخزون</a>
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        {% else %}
        <p class="text-muted">لا توجد أصناف نفدت من المخزون</p>
        {% endif %}
      </div>
    </div>
  </div>
  
  <div class="col-md-6">
    <div class="card border-warning">
      <div class="card-header bg-warning text-dark">
        <h5 class="mb-0">أصناف منخفضة المخزون</h5>
      </div>
      <div class="card-body">
        {% if data['low_stock'] %}
        <table class="table table-sm">
          <thead><tr><th>الصنف</th><th>الكمية</th><th>حد إعادة الطلب</th><th>إجراءات</th></tr></thead>
          <tbody>
            {% for item in data['low_stock'] %}
            <tr>
              <td><strong>{{ item['name'] }}</strong></td>
              <td><span class="badge bg-warning">{{ item['quantity'] }}</span></td>
              <td>{{ item['reorder_level'] }}</td>
              <td>
                <a href="{{ url_for('items_edit', item_id=item['id']) }}" class="btn btn-sm btn-outline-primary">تعديل</a>
                <a href="{{ url_for('stock_adjust') }}" class="btn btn-sm btn-outline-warning">تعديل المخزون</a>
              </td>
            </tr>
            {% endfor %}
          </tbody>
        </table>
        {% else %}
        <p class="text-muted">لا توجد أصناف منخفضة المخزون</p>
        {% endif %}
      </div>
    </div>
  </div>
</div>

<div class="mt-4 d-flex gap-2">
  <a href="{{ url_for('stock_adjust') }}" class="btn btn-warning">تعديل المخزون</a>
  <a href="{{ url_for('items_list') }}" class="btn btn-outline-secondary">إدارة الأصناف</a>
  <a href="{{ url_for('index') }}" class="btn btn-outline-secondary">الرئيسية</a>
</div>
"""

TPL_PURCHASES_LIST = r"""
<div class="d-flex justify-content-between align-items-center mb-3">
  <h4 class="m-0">أوامر الشراء</h4>
  <a href="{{ url_for('purchases_new') }}" class="btn btn-sm btn-primary">شراء جديد</a>
</div>
<table class="table table-hover table-sm">
  <thead><tr><th>#</th><th>المورد</th><th>المجموع</th><th>طريقة الدفع</th><th>التاريخ</th><th>إجراءات</th></tr></thead>
  <tbody>
    {% for r in rows %}
    <tr>
      <td>{{ r['id'] }}</td>
      <td><strong>{{ r['supplier_name'] or 'مورد نقدي' }}</strong></td>
      <td>{{ '%.2f'|format(r['final_amount']) }}</td>
      <td>{{ 'نقدي' if r['payment_method'] == 'cash' else 'بطاقة' }}</td>
      <td>{{ r['created_at'] }}</td>
      <td>
        <a class="btn btn-sm btn-outline-primary" href="{{ url_for('purchases_view', purchase_id=r['id']) }}">عرض</a>
      </td>
    </tr>
    {% else %}
    <tr><td colspan="6" class="text-center text-muted">لا توجد أوامر شراء</td></tr>
    {% endfor %}
  </tbody>
</table>
"""

TPL_PURCHASES_FORM = r"""
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold text-primary mb-1">
      <i class="bi bi-cart-dash me-2"></i>أمر شراء جديد
    </h2>
    <p class="text-muted">إضافة أصناف للمخزون</p>
  </div>
  <a href="{{ url_for('purchases_list') }}" class="btn btn-outline-secondary">
    <i class="bi bi-arrow-right me-2"></i>عرض أوامر الشراء
  </a>
</div>

<!-- Supplier Info -->
<div class="card mb-4">
  <div class="card-header">
    <h5 class="mb-0">
      <i class="bi bi-building me-2"></i>معلومات المورد
    </h5>
  </div>
  <div class="card-body">
    <div class="row g-3">
      <div class="col-md-4">
        <label class="form-label fw-semibold">اسم المورد</label>
        <input name="supplier_name" class="form-control form-control-lg" placeholder="أدخل اسم المورد">
      </div>
      <div class="col-md-4">
        <label class="form-label fw-semibold">رقم الهاتف</label>
        <input name="supplier_phone" class="form-control form-control-lg" placeholder="أدخل رقم الهاتف">
      </div>
      <div class="col-md-4">
        <label class="form-label fw-semibold">طريقة الدفع</label>
        <select name="payment_method" class="form-select form-select-lg">
          <option value="cash">نقدي</option>
          <option value="card">بطاقة</option>
        </select>
      </div>
    </div>
  </div>
</div>

<!-- Search Bar -->
<div class="card mb-4">
  <div class="card-body">
    <div class="row g-3">
      <div class="col-md-8">
        <div class="input-group input-group-lg">
          <span class="input-group-text">
            <i class="bi bi-search"></i>
          </span>
          <input type="text" id="itemSearch" class="form-control" placeholder="البحث عن الأصناف...">
        </div>
      </div>
      <div class="col-md-4">
        <select id="categoryFilter" class="form-select form-select-lg">
          <option value="">جميع الفئات</option>
          {% for category in categories %}
          <option value="{{ category['id'] }}">{{ category['name'] }}</option>
          {% endfor %}
        </select>
      </div>
    </div>
  </div>
</div>

<div class="row">
  <!-- Items Grid -->
  <div class="col-md-8">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-grid me-2"></i>الأصناف المتاحة
        </h5>
      </div>
      <div class="card-body">
        <div id="itemsGrid" class="row g-3">
          {% for item in items %}
          <div class="col-md-4 item-card" data-name="{{ item['name']|lower }}" data-category="{{ item['category_id'] or '' }}">
            <div class="card h-100 item-card-inner" data-item-id="{{ item['id'] }}" data-cost="{{ item['cost_price'] or 0 }}">
              <div class="card-body text-center">
                <div class="mb-3">
                  {% if item['image_url'] %}
                    <img src="{{ item['image_url'] }}" class="img-fluid rounded" style="max-height: 100px; object-fit: cover;">
                  {% else %}
                    <i class="bi bi-box display-1 text-muted"></i>
                  {% endif %}
                </div>
                <h6 class="card-title">{{ item['name'] }}</h6>
                <p class="text-muted small mb-2">{{ item['category_name'] or 'بدون فئة' }}</p>
                <div class="mb-2">
                  <span class="badge bg-info">الكمية: {{ item['quantity'] }}</span>
                  {% if item['sku'] %}
                    <br><small class="text-muted">{{ item['sku'] }}</small>
                  {% endif %}
                </div>
                <div class="mb-3">
                  <strong class="text-success">{{ '%.2f'|format(item['cost_price']) if item['cost_price'] else '0.00' }} ج.س</strong>
                </div>
                <button class="btn btn-warning btn-sm add-to-purchase" data-item-id="{{ item['id'] }}" data-name="{{ item['name'] }}" data-cost="{{ item['cost_price'] or 0 }}">
                  <i class="bi bi-plus-circle me-1"></i>إضافة للشراء
                </button>
              </div>
            </div>
          </div>
          {% endfor %}
        </div>
      </div>
    </div>
  </div>
  
  <!-- Purchase Items -->
  <div class="col-md-4">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-cart-dash me-2"></i>أصناف الشراء
        </h5>
      </div>
      <div class="card-body">
        <form method="post" id="purchaseForm">
          <div id="purchaseItems">
            <p class="text-muted text-center">لا توجد أصناف في الشراء</p>
          </div>
          
          <div class="mt-3" id="purchaseTotals" style="display: none;">
            <hr>
            <div class="row g-2">
              <div class="col-6">
                <label class="form-label small">الخصم</label>
                <input name="discount_amount" type="number" step="0.01" class="form-control form-control-sm" value="0" id="discountInput">
              </div>
              <div class="col-6">
                <label class="form-label small">الضريبة</label>
                <input name="tax_amount" type="number" step="0.01" class="form-control form-control-sm" value="0" id="taxInput">
              </div>
            </div>
            <hr>
            <div class="d-flex justify-content-between">
              <strong>المجموع النهائي:</strong>
              <strong id="finalTotal">0.00 ج.س</strong>
            </div>
          </div>
          
          <div class="mt-3">
            <button type="submit" class="btn btn-warning w-100" id="submitBtn" disabled>
              <i class="bi bi-check-circle me-2"></i>إنشاء أمر الشراء
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</div>

<script>
document.addEventListener('DOMContentLoaded', function() {
  const searchInput = document.getElementById('itemSearch');
  const categoryFilter = document.getElementById('categoryFilter');
  const itemsGrid = document.getElementById('itemsGrid');
  const purchaseItems = document.getElementById('purchaseItems');
  const purchaseTotals = document.getElementById('purchaseTotals');
  const finalTotal = document.getElementById('finalTotal');
  const submitBtn = document.getElementById('submitBtn');
  const purchaseForm = document.getElementById('purchaseForm');
  const discountInput = document.getElementById('discountInput');
  const taxInput = document.getElementById('taxInput');
  
  let purchaseCart = [];
  
  // Search functionality
  function filterItems() {
    const searchTerm = searchInput.value.toLowerCase();
    const selectedCategory = categoryFilter.value;
    
    const itemCards = document.querySelectorAll('.item-card');
    itemCards.forEach(card => {
      const name = card.dataset.name;
      const category = card.dataset.category;
      
      const matchesSearch = name.includes(searchTerm);
      const matchesCategory = !selectedCategory || category === selectedCategory;
      
      if (matchesSearch && matchesCategory) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  }
  
  searchInput.addEventListener('input', filterItems);
  categoryFilter.addEventListener('change', filterItems);
  
  // Add to purchase functionality
  function addToPurchase(itemId, name, cost) {
    const existingItem = purchaseCart.find(item => item.id === itemId);
    
    if (existingItem) {
      existingItem.quantity += 1;
    } else {
      purchaseCart.push({
        id: itemId,
        name: name,
        cost: parseFloat(cost),
        quantity: 1
      });
    }
    
    updatePurchaseDisplay();
  }
  
  function removeFromPurchase(itemId) {
    purchaseCart = purchaseCart.filter(item => item.id !== itemId);
    updatePurchaseDisplay();
  }
  
  function updateQuantity(itemId, newQuantity) {
    const item = purchaseCart.find(item => item.id === itemId);
    if (item) {
      if (newQuantity <= 0) {
        removeFromPurchase(itemId);
      } else {
        item.quantity = newQuantity;
        updatePurchaseDisplay();
      }
    }
  }
  
  function updatePurchaseDisplay() {
    if (purchaseCart.length === 0) {
      purchaseItems.innerHTML = '<p class="text-muted text-center">لا توجد أصناف في الشراء</p>';
      purchaseTotals.style.display = 'none';
      submitBtn.disabled = true;
      return;
    }
    
    let html = '';
    let subtotal = 0;
    
    purchaseCart.forEach(item => {
      const itemTotal = item.cost * item.quantity;
      subtotal += itemTotal;
      
      html += `
        <div class="card mb-2">
          <div class="card-body p-2">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h6 class="mb-1">${item.name}</h6>
                <small class="text-muted">${item.cost.toFixed(2)} ج.س</small>
              </div>
              <div class="d-flex align-items-center">
                <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, ${item.quantity - 1})">-</button>
                <span class="mx-2">${item.quantity}</span>
                <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${item.id}, ${item.quantity + 1})">+</button>
                <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeFromPurchase(${item.id})">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
            <div class="text-end">
              <strong>${itemTotal.toFixed(2)} ج.س</strong>
            </div>
          </div>
        </div>
      `;
    });
    
    purchaseItems.innerHTML = html;
    purchaseTotals.style.display = 'block';
    submitBtn.disabled = false;
    
    updateFinalTotal();
  }
  
  function updateFinalTotal() {
    const subtotal = purchaseCart.reduce((sum, item) => sum + (item.cost * item.quantity), 0);
    const discount = parseFloat(discountInput.value) || 0;
    const tax = parseFloat(taxInput.value) || 0;
    const final = subtotal - discount + tax;
    
    finalTotal.textContent = final.toFixed(2) + ' ج.س';
    
    // Update form with hidden inputs
    updateFormInputs();
  }
  
  function updateFormInputs() {
    // Clear existing hidden inputs
    const existingInputs = purchaseForm.querySelectorAll('input[type="hidden"]');
    existingInputs.forEach(input => input.remove());
    
    // Add hidden inputs for each purchase item
    purchaseCart.forEach(item => {
      const itemIdInput = document.createElement('input');
      itemIdInput.type = 'hidden';
      itemIdInput.name = 'item_ids';
      itemIdInput.value = item.id;
      purchaseForm.appendChild(itemIdInput);
      
      const quantityInput = document.createElement('input');
      quantityInput.type = 'hidden';
      quantityInput.name = 'quantities';
      quantityInput.value = item.quantity;
      purchaseForm.appendChild(quantityInput);
      
      const costInput = document.createElement('input');
      costInput.type = 'hidden';
      costInput.name = 'costs';
      costInput.value = item.cost;
      purchaseForm.appendChild(costInput);
    });
  }
  
  // Add to purchase event listeners
  document.addEventListener('click', function(e) {
    if (e.target.classList.contains('add-to-purchase')) {
      const itemId = parseInt(e.target.dataset.itemId);
      const name = e.target.dataset.name;
      const cost = parseFloat(e.target.dataset.cost);
      
      addToPurchase(itemId, name, cost);
      
      // Visual feedback
      e.target.innerHTML = '<i class="bi bi-check me-1"></i>تمت الإضافة';
      e.target.classList.remove('btn-warning');
      e.target.classList.add('btn-success');
      
      setTimeout(() => {
        e.target.innerHTML = '<i class="bi bi-plus-circle me-1"></i>إضافة للشراء';
        e.target.classList.remove('btn-success');
        e.target.classList.add('btn-warning');
      }, 1000);
    }
  });
  
  // Update totals when discount or tax changes
  discountInput.addEventListener('input', updateFinalTotal);
  taxInput.addEventListener('input', updateFinalTotal);
  
  // Make functions global for onclick handlers
  window.updateQuantity = updateQuantity;
  window.removeFromPurchase = removeFromPurchase;
});
</script>
"""

TPL_PURCHASE_VIEW = r"""
<div class="row justify-content-center">
  <div class="col-md-8">
    <div class="card shadow-sm">
      <div class="card-header">
        <h5 class="mb-0">أمر شراء رقم: {{ purchase['id'] }}</h5>
        <small class="text-muted">تاريخ الإنشاء: {{ purchase['created_at'] }}</small>
      </div>
      <div class="card-body">
        <div class="row mb-4">
          <div class="col-md-6">
            <h6>بيانات المورد:</h6>
            <p><strong>الاسم:</strong> {{ purchase['supplier_name'] or 'مورد نقدي' }}</p>
            <p><strong>الهاتف:</strong> {{ purchase['supplier_phone'] or '-' }}</p>
          </div>
          <div class="col-md-6">
            <h6>بيانات الأمر:</h6>
            <p><strong>طريقة الدفع:</strong> {{ 'نقدي' if purchase['payment_method'] == 'cash' else 'بطاقة' }}</p>
            <p><strong>أنشأه:</strong> {{ purchase['created_by_name'] }}</p>
          </div>
        </div>
        
        <h6>الأصناف:</h6>
        <table class="table table-sm">
          <thead><tr><th>الصنف</th><th>الكمية</th><th>سعر التكلفة</th><th>المجموع</th></tr></thead>
          <tbody>
            {% for item in items %}
            <tr>
              <td>{{ item['item_name'] }}</td>
              <td>{{ item['quantity'] }}</td>
              <td>{{ '%.2f'|format(item['unit_cost']) }}</td>
              <td>{{ '%.2f'|format(item['total_cost']) }}</td>
            </tr>
            {% endfor %}
          </tbody>
          <tfoot>
            <tr><td colspan="3"><strong>المجموع الفرعي:</strong></td><td><strong>{{ '%.2f'|format(purchase['total_amount']) }}</strong></td></tr>
            {% if purchase['discount_amount'] > 0 %}
            <tr><td colspan="3"><strong>الخصم:</strong></td><td><strong>-{{ '%.2f'|format(purchase['discount_amount']) }}</strong></td></tr>
            {% endif %}
            {% if purchase['tax_amount'] > 0 %}
            <tr><td colspan="3"><strong>الضريبة:</strong></td><td><strong>{{ '%.2f'|format(purchase['tax_amount']) }}</strong></td></tr>
            {% endif %}
            <tr class="table-primary"><td colspan="3"><strong>المجموع النهائي:</strong></td><td><strong>{{ '%.2f'|format(purchase['final_amount']) }}</strong></td></tr>
          </tfoot>
        </table>
        
        <div class="mt-4 d-flex gap-2">
          <button class="btn btn-primary" onclick="window.print()">طباعة</button>
          <a href="{{ url_for('purchases_list') }}" class="btn btn-outline-secondary">رجوع</a>
        </div>
      </div>
    </div>
  </div>
</div>
"""

TPL_DAILY_REPORTS = r"""
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold text-primary mb-1">
      <i class="bi bi-calendar-day me-2"></i>التقرير اليومي
    </h2>
    <p class="text-muted">تقرير مبيعات يوم {{ data['date'] }}</p>
  </div>
  <div class="d-flex gap-2">
    <button class="btn btn-outline-primary" onclick="window.print()">
      <i class="bi bi-printer me-2"></i>طباعة التقرير
    </button>
    <a href="{{ url_for('reports') }}" class="btn btn-outline-secondary">
      <i class="bi bi-arrow-right me-2"></i>جميع التقارير
    </a>
  </div>
</div>

<div class="row g-4 mb-5">
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-cart-check feature-icon"></i>
      <h3>{{ data['sales_summary']['total_sales'] or 0 }}</h3>
      <p>إجمالي المبيعات</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-stack feature-icon"></i>
      <h3>{{ data['sales_summary']['total_quantity'] or 0 }}</h3>
      <p>إجمالي الكمية المباعة</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-currency-dollar feature-icon"></i>
      <h3>{{ '%.2f'|format(data['sales_summary']['total_revenue'] or 0) }}</h3>
      <p>إجمالي الإيرادات (ج.س)</p>
    </div>
  </div>
</div>

<div class="row g-4">
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-trophy me-2"></i>أكثر الأصناف مبيعاً اليوم
        </h5>
      </div>
      <div class="card-body">
        {% if data['top_items'] %}
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><i class="bi bi-medal me-1"></i>الترتيب</th>
                <th><i class="bi bi-box me-1"></i>الصنف</th>
                <th><i class="bi bi-stack me-1"></i>الكمية</th>
                <th><i class="bi bi-currency-dollar me-1"></i>الإيراد</th>
              </tr>
            </thead>
            <tbody>
              {% for item in data['top_items'] %}
              <tr>
                <td>
                  <span class="badge {% if loop.index == 1 %}bg-warning{% elif loop.index == 2 %}bg-secondary{% elif loop.index == 3 %}bg-info{% else %}bg-light text-dark{% endif %}">
                    {{ loop.index }}
                  </span>
                </td>
                <td><strong>{{ item['name'] }}</strong></td>
                <td><span class="badge bg-success">{{ item['total_sold'] }}</span></td>
                <td><strong class="text-success">{{ '%.2f'|format(item['total_revenue']) }} ج.س</strong></td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <div class="text-center text-muted py-4">
          <i class="bi bi-inbox display-4 d-block mb-3"></i>
          <p>لا توجد مبيعات اليوم</p>
        </div>
        {% endif %}
      </div>
    </div>
  </div>
  
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-receipt me-2"></i>فواتير اليوم
        </h5>
      </div>
      <div class="card-body">
        {% if data['invoices'] %}
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><i class="bi bi-hash me-1"></i>رقم الفاتورة</th>
                <th><i class="bi bi-person me-1"></i>العميل</th>
                <th><i class="bi bi-currency-dollar me-1"></i>المبلغ</th>
                <th><i class="bi bi-clock me-1"></i>الوقت</th>
              </tr>
            </thead>
            <tbody>
              {% for invoice in data['invoices'] %}
              <tr>
                <td><strong>{{ invoice['invoice_number'] }}</strong></td>
                <td>{{ invoice['customer_name'] or 'عميل نقدي' }}</td>
                <td><strong class="text-success">{{ '%.2f'|format(invoice['final_amount']) }} ج.س</strong></td>
                <td><small class="text-muted">{{ invoice['created_at'] }}</small></td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <div class="text-center text-muted py-4">
          <i class="bi bi-inbox display-4 d-block mb-3"></i>
          <p>لا توجد فواتير اليوم</p>
        </div>
        {% endif %}
      </div>
    </div>
  </div>
</div>
"""

TPL_MONTHLY_REPORTS = r"""
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold text-primary mb-1">
      <i class="bi bi-calendar-month me-2"></i>التقرير الشهري
    </h2>
    <p class="text-muted">تقرير مبيعات شهر {{ data['month'] }}</p>
  </div>
  <div class="d-flex gap-2">
    <button class="btn btn-outline-primary" onclick="window.print()">
      <i class="bi bi-printer me-2"></i>طباعة التقرير
    </button>
    <a href="{{ url_for('reports') }}" class="btn btn-outline-secondary">
      <i class="bi bi-arrow-right me-2"></i>جميع التقارير
    </a>
  </div>
</div>

<div class="row g-4 mb-5">
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-cart-check feature-icon"></i>
      <h3>{{ data['sales_summary']['total_sales'] or 0 }}</h3>
      <p>إجمالي المبيعات</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-stack feature-icon"></i>
      <h3>{{ data['sales_summary']['total_quantity'] or 0 }}</h3>
      <p>إجمالي الكمية المباعة</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-currency-dollar feature-icon"></i>
      <h3>{{ '%.2f'|format(data['sales_summary']['total_revenue'] or 0) }}</h3>
      <p>إجمالي الإيرادات (ج.س)</p>
    </div>
  </div>
</div>

<div class="row g-4">
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-graph-up me-2"></i>توزيع المبيعات اليومية
        </h5>
      </div>
      <div class="card-body">
        {% if data['daily_breakdown'] %}
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><i class="bi bi-calendar me-1"></i>التاريخ</th>
                <th><i class="bi bi-cart me-1"></i>عدد المبيعات</th>
                <th><i class="bi bi-currency-dollar me-1"></i>الإيراد</th>
              </tr>
            </thead>
            <tbody>
              {% for day in data['daily_breakdown'] %}
              <tr>
                <td><strong>{{ day['date'] }}</strong></td>
                <td><span class="badge bg-info">{{ day['sales_count'] }}</span></td>
                <td><strong class="text-success">{{ '%.2f'|format(day['daily_revenue']) }} ج.س</strong></td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <div class="text-center text-muted py-4">
          <i class="bi bi-inbox display-4 d-block mb-3"></i>
          <p>لا توجد مبيعات هذا الشهر</p>
        </div>
        {% endif %}
      </div>
    </div>
  </div>
  
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-trophy me-2"></i>أكثر الأصناف مبيعاً
        </h5>
      </div>
      <div class="card-body">
        {% if data['top_items'] %}
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><i class="bi bi-medal me-1"></i>الترتيب</th>
                <th><i class="bi bi-box me-1"></i>الصنف</th>
                <th><i class="bi bi-stack me-1"></i>الكمية</th>
                <th><i class="bi bi-currency-dollar me-1"></i>الإيراد</th>
              </tr>
            </thead>
            <tbody>
              {% for item in data['top_items'] %}
              <tr>
                <td>
                  <span class="badge {% if loop.index == 1 %}bg-warning{% elif loop.index == 2 %}bg-secondary{% elif loop.index == 3 %}bg-info{% else %}bg-light text-dark{% endif %}">
                    {{ loop.index }}
                  </span>
                </td>
                <td><strong>{{ item['name'] }}</strong></td>
                <td><span class="badge bg-success">{{ item['total_sold'] }}</span></td>
                <td><strong class="text-success">{{ '%.2f'|format(item['total_revenue']) }} ج.س</strong></td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <div class="text-center text-muted py-4">
          <i class="bi bi-inbox display-4 d-block mb-3"></i>
          <p>لا توجد مبيعات هذا الشهر</p>
        </div>
        {% endif %}
      </div>
    </div>
  </div>
</div>
"""

TPL_YEARLY_REPORTS = r"""
<div class="d-flex justify-content-between align-items-center mb-4">
  <div>
    <h2 class="fw-bold text-primary mb-1">
      <i class="bi bi-calendar3 me-2"></i>التقرير السنوي
    </h2>
    <p class="text-muted">تقرير مبيعات سنة {{ data['year'] }}</p>
  </div>
  <div class="d-flex gap-2">
    <button class="btn btn-outline-primary" onclick="window.print()">
      <i class="bi bi-printer me-2"></i>طباعة التقرير
    </button>
    <a href="{{ url_for('reports') }}" class="btn btn-outline-secondary">
      <i class="bi bi-arrow-right me-2"></i>جميع التقارير
    </a>
  </div>
</div>

<div class="row g-4 mb-5">
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-cart-check feature-icon"></i>
      <h3>{{ data['sales_summary']['total_sales'] or 0 }}</h3>
      <p>إجمالي المبيعات</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-stack feature-icon"></i>
      <h3>{{ data['sales_summary']['total_quantity'] or 0 }}</h3>
      <p>إجمالي الكمية المباعة</p>
    </div>
  </div>
  <div class="col-md-4">
    <div class="stats-card">
      <i class="bi bi-currency-dollar feature-icon"></i>
      <h3>{{ '%.2f'|format(data['sales_summary']['total_revenue'] or 0) }}</h3>
      <p>إجمالي الإيرادات (ج.س)</p>
    </div>
  </div>
</div>

<div class="row g-4">
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-graph-up me-2"></i>توزيع المبيعات الشهرية
        </h5>
      </div>
      <div class="card-body">
        {% if data['monthly_breakdown'] %}
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><i class="bi bi-calendar me-1"></i>الشهر</th>
                <th><i class="bi bi-cart me-1"></i>عدد المبيعات</th>
                <th><i class="bi bi-currency-dollar me-1"></i>الإيراد</th>
              </tr>
            </thead>
            <tbody>
              {% for month in data['monthly_breakdown'] %}
              <tr>
                <td><strong>{{ month['month'] }}</strong></td>
                <td><span class="badge bg-info">{{ month['sales_count'] }}</span></td>
                <td><strong class="text-success">{{ '%.2f'|format(month['monthly_revenue']) }} ج.س</strong></td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <div class="text-center text-muted py-4">
          <i class="bi bi-inbox display-4 d-block mb-3"></i>
          <p>لا توجد مبيعات هذه السنة</p>
        </div>
        {% endif %}
      </div>
    </div>
  </div>
  
  <div class="col-md-6">
    <div class="card">
      <div class="card-header">
        <h5 class="mb-0">
          <i class="bi bi-tags me-2"></i>أداء الفئات
        </h5>
      </div>
      <div class="card-body">
        {% if data['category_performance'] %}
        <div class="table-responsive">
          <table class="table table-hover">
            <thead>
              <tr>
                <th><i class="bi bi-tag me-1"></i>الفئة</th>
                <th><i class="bi bi-cart me-1"></i>المبيعات</th>
                <th><i class="bi bi-stack me-1"></i>الكمية</th>
                <th><i class="bi bi-currency-dollar me-1"></i>الإيراد</th>
              </tr>
            </thead>
            <tbody>
              {% for category in data['category_performance'] %}
              <tr>
                <td><strong>{{ category['category_name'] or 'بدون فئة' }}</strong></td>
                <td><span class="badge bg-info">{{ category['sales_count'] }}</span></td>
                <td><span class="badge bg-success">{{ category['total_quantity'] }}</span></td>
                <td><strong class="text-success">{{ '%.2f'|format(category['total_revenue']) }} ج.س</strong></td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <div class="text-center text-muted py-4">
          <i class="bi bi-inbox display-4 d-block mb-3"></i>
          <p>لا توجد مبيعات هذه السنة</p>
        </div>
        {% endif %}
      </div>
    </div>
  </div>
</div>
"""

if __name__ == '__main__':
    with app.app_context():
        init_db()
    # Use a different port and host configuration for Windows
    app.run(debug=True, host='127.0.0.1', port=8080, use_reloader=False)
