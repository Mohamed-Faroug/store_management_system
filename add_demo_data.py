# -*- coding: utf-8 -*-
"""
إضافة البيانات التجريبية - نظام إدارة المخزون
نظام إدارة المخزون - مخزن الزينة

جميع الحقوق محفوظة © 2025
تم تطوير هذا النظام بواسطة: محمد فاروق
تاريخ آخر تحديث: 9/9/2025
"""

import sqlite3
from datetime import datetime, timedelta
import random
from werkzeug.security import generate_password_hash

def add_demo_data():
    """إضافة بيانات تجريبية شاملة للنظام"""
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        print("🔄 بدء إضافة البيانات التجريبية...")
        print("=" * 50)
        
        # 1. إضافة المستخدمين الافتراضيين
        add_default_users(cursor)
        
        # 2. إضافة الفئات الافتراضية
        add_default_categories(cursor)
        
        # 3. إضافة أصناف تجريبية
        add_demo_items(cursor)
        
        # 4. إضافة مبيعات تجريبية
        add_demo_sales(cursor)
        
        # 5. إضافة فواتير تجريبية
        add_demo_invoices(cursor)
        
        # 6. إضافة مشتريات تجريبية
        add_demo_purchases(cursor)
        
        # حفظ التغييرات
        conn.commit()
        conn.close()
        
        print("=" * 50)
        print("✅ تم إضافة البيانات التجريبية بنجاح!")
        print("📊 ملخص البيانات المضافة:")
        print("   👥 المستخدمون: 2 (مدير + كاشير)")
        print("   📂 الفئات: 15 فئة")
        print("   📦 الأصناف: 24 صنف")
        print("   💰 المبيعات: 100 عملية بيع")
        print("   🧾 الفواتير: 50 فاتورة")
        print("   🛒 المشتريات: 30 أمر شراء")
        print("=" * 50)
        print("🚀 يمكنك الآن تشغيل النظام باستخدام: python main.py")
        
    except Exception as e:
        print(f"❌ خطأ في إضافة البيانات التجريبية: {str(e)}")

def add_default_users(cursor):
    """إضافة المستخدمين الافتراضيين"""
    print("👥 إضافة المستخدمين الافتراضيين...")
    
    # التحقق من وجود المستخدمين
    cursor.execute('SELECT COUNT(*) FROM users')
    if cursor.fetchone()[0] > 0:
        print("   ⚠️ المستخدمون موجودون بالفعل")
        return
    
    users = [
        ('admin', 'admin123', 'manager', 'مدير النظام'),
        ('cashier', 'cashier123', 'cashier', 'كاشير')
    ]
    
    for username, password, role, full_name in users:
        cursor.execute('''
            INSERT INTO users (username, password_hash, role, full_name)
            VALUES (?, ?, ?, ?)
        ''', (username, generate_password_hash(password), role, full_name))
    
    print("   ✅ تم إضافة 2 مستخدم")

def add_default_categories(cursor):
    """إضافة الفئات الافتراضية"""
    print("📂 إضافة الفئات الافتراضية...")
    
    # التحقق من وجود الفئات
    cursor.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] > 0:
        print("   ⚠️ الفئات موجودة بالفعل")
        return
    
    categories = [
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
    
    for name, description in categories:
        cursor.execute('''
            INSERT INTO categories (name, description)
            VALUES (?, ?)
        ''', (name, description))
    
    print("   ✅ تم إضافة 15 فئة")

def add_demo_items(cursor):
    """إضافة أصناف تجريبية"""
    print("📦 إضافة أصناف تجريبية...")
    
    # الحصول على معرفات الفئات
    cursor.execute('SELECT id FROM categories')
    category_ids = [row[0] for row in cursor.fetchall()]
    
    if not category_ids:
        print("   ❌ لا توجد فئات متاحة")
        return
    
    demo_items = [
        # إطارات
        ("إطار ميشلان 17 بوصة", category_ids[0], "MICH17", "إطار عالي الأداء", 50, 10, 1500.00, 2000.00),
        ("إطار بريدجستون 16 بوصة", category_ids[0], "BRID16", "إطار اقتصادي", 30, 8, 1200.00, 1600.00),
        ("إطار كونتيننتال 18 بوصة", category_ids[0], "CONT18", "إطار فاخر", 20, 5, 2000.00, 2800.00),
        
        # زينة خارجية
        ("مرايا جانبية كروم", category_ids[1], "CRMMIR", "مرايا كروم للزينة", 30, 5, 200.00, 350.00),
        ("مصد أمامي رياضي", category_ids[1], "SPOILER", "مصد رياضي للزينة", 15, 3, 800.00, 1200.00),
        ("شعار سيارة مضيء", category_ids[1], "LEDLOGO", "شعار LED للزينة", 25, 5, 150.00, 250.00),
        
        # زينة داخلية
        ("غطاء مقعد جلد فاخر", category_ids[2], "LUXSEAT", "غطاء مقعد من الجلد الصناعي", 20, 3, 400.00, 650.00),
        ("ستائر جانبية", category_ids[2], "SIDECUR", "ستائر جانبية للسيارة", 40, 8, 80.00, 150.00),
        ("سجادة أرضية", category_ids[2], "FLOORMAT", "سجادة أرضية مقاومة للماء", 60, 12, 50.00, 90.00),
        
        # إضاءة
        ("لمبات LED أمامية", category_ids[3], "LEDHEAD", "لمبات LED عالية السطوع", 70, 15, 100.00, 180.00),
        ("لمبات LED خلفية", category_ids[3], "LEDTAIL", "لمبات LED للخلف", 50, 10, 80.00, 140.00),
        ("إضاءة داخلية LED", category_ids[3], "LEDINT", "إضاءة داخلية متعددة الألوان", 35, 7, 120.00, 200.00),
        
        # صوتيات
        ("نظام صوت بايونير", category_ids[4], "PIONAUD", "نظام صوت للسيارة مع مضخم", 15, 2, 1200.00, 1800.00),
        ("سماعات أمامية", category_ids[4], "FRONTSPK", "سماعات أمامية عالية الجودة", 25, 5, 300.00, 450.00),
        ("مضخم صوت", category_ids[4], "AMPLIFIER", "مضخم صوت قوي", 18, 3, 800.00, 1200.00),
        
        # أدوات
        ("طقم مفاتيح صيانة", category_ids[5], "TOOLSET", "طقم مفاتيح متعدد الاستخدامات", 40, 8, 80.00, 150.00),
        ("مفتاح ربط", category_ids[5], "WRENCH", "مفتاح ربط قابل للتعديل", 60, 12, 30.00, 55.00),
        ("مطرقة", category_ids[5], "HAMMER", "مطرقة صيانة", 25, 5, 25.00, 45.00),
        
        # زيوت
        ("زيت محرك تخليقي 5W-30", category_ids[6], "OIL5W30", "زيت محرك تخليقي بالكامل", 100, 20, 80.00, 120.00),
        ("زيت فرامل DOT4", category_ids[6], "BRAKEOIL", "زيت فرامل عالي الجودة", 50, 10, 40.00, 70.00),
        ("مضاد تجمد", category_ids[6], "ANTIFREEZE", "مضاد تجمد للمحرك", 30, 6, 60.00, 100.00),
        
        # بطاريات
        ("بطارية سيارة 60 أمبير", category_ids[7], "BAT60AH", "بطارية سيارة عالية الجودة", 25, 5, 700.00, 950.00),
        ("بطارية سيارة 70 أمبير", category_ids[7], "BAT70AH", "بطارية سيارة قوية", 20, 4, 900.00, 1200.00),
        
        # إطارات احتياطية
        ("إطار احتياطي صغير", category_ids[8], "SPARET", "إطار احتياطي للطوارئ", 10, 2, 300.00, 450.00),
        
        # أجهزة إنذار
        ("جهاز إنذار متقدم", category_ids[9], "ADVSEC", "نظام إنذار مع حساسات حركة", 12, 3, 600.00, 900.00),
        ("قفل عجلة", category_ids[9], "WHEELLOCK", "قفل عجلة للأمان", 35, 7, 150.00, 250.00)
    ]
    
    for item_data in demo_items:
        name, category_id, sku, description, quantity, reorder_level, cost_price, selling_price = item_data
        try:
            cursor.execute('''
                INSERT INTO items (name, category_id, sku, description, quantity, reorder_level, cost_price, selling_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, category_id, sku, description, quantity, reorder_level, cost_price, selling_price))
        except sqlite3.IntegrityError:
            print(f"   ⚠️ الصنف {name} موجود بالفعل")
    
    print(f"   ✅ تم إضافة {len(demo_items)} صنف تجريبي")

def add_demo_sales(cursor):
    """إضافة مبيعات تجريبية"""
    print("💰 إضافة مبيعات تجريبية...")
    
    # الحصول على الأصناف والمستخدمين
    cursor.execute('SELECT id, selling_price, quantity FROM items')
    items = cursor.fetchall()
    
    cursor.execute('SELECT id FROM users')
    users = cursor.fetchall()
    
    if not items or not users:
        print("   ❌ لا توجد أصناف أو مستخدمين متاحين")
        return
    
    sales_count = 0
    for i in range(100):
        item_id, selling_price, available_qty = random.choice(items)
        quantity = random.randint(1, min(3, available_qty))
        user_id = random.choice(users)[0]
        
        # إنشاء تاريخ عشوائي في آخر 60 يوم
        sale_date = (datetime.now() - timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S')
        
        total_price = selling_price * quantity
        discount_amount = round(total_price * random.uniform(0, 0.1), 2)
        tax_amount = round((total_price - discount_amount) * 0.05, 2)
        final_price = total_price - discount_amount + tax_amount
        
        try:
            cursor.execute('''
                INSERT INTO sales (item_id, quantity, unit_price, total_price, discount_amount, tax_amount, final_price, created_at, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (item_id, quantity, selling_price, total_price, discount_amount, tax_amount, final_price, sale_date, user_id))
            
            # تحديث كمية الصنف
            cursor.execute('UPDATE items SET quantity = quantity - ? WHERE id = ?', (quantity, item_id))
            sales_count += 1
            
        except Exception as e:
            print(f"   ⚠️ خطأ في إضافة مبيعة: {str(e)}")
    
    print(f"   ✅ تم إضافة {sales_count} عملية بيع تجريبية")

def add_demo_invoices(cursor):
    """إضافة فواتير تجريبية"""
    print("🧾 إضافة فواتير تجريبية...")
    
    # الحصول على الأصناف والمستخدمين
    cursor.execute('SELECT id, selling_price, quantity FROM items')
    items = cursor.fetchall()
    
    cursor.execute('SELECT id FROM users')
    users = cursor.fetchall()
    
    if not items or not users:
        print("   ❌ لا توجد أصناف أو مستخدمين متاحين")
        return
    
    invoices_count = 0
    for i in range(50):
        # بيانات العميل
        customer_name = f"عميل {i+1}" if random.random() > 0.3 else None
        customer_phone = f"09{random.randint(10000000, 99999999)}" if customer_name else None
        payment_method = random.choice(['cash', 'card'])
        user_id = random.choice(users)[0]
        
        # إنشاء تاريخ عشوائي
        invoice_date = (datetime.now() - timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d %H:%M:%S')
        
        # اختيار أصناف عشوائية
        selected_items = random.sample(items, random.randint(1, 3))
        
        total_amount = 0
        invoice_items = []
        
        for item_id, selling_price, available_qty in selected_items:
            quantity = random.randint(1, min(2, available_qty))
            item_total = selling_price * quantity
            total_amount += item_total
            invoice_items.append((item_id, quantity, selling_price, item_total))
        
        if not invoice_items:
            continue
        
        # حساب الخصم والضريبة
        discount_amount = round(total_amount * random.uniform(0, 0.15), 2)
        tax_amount = round((total_amount - discount_amount) * 0.05, 2)
        final_amount = total_amount - discount_amount + tax_amount
        
        # رقم الفاتورة
        invoice_number = f"INV-{invoices_count + 1:06d}"
        
        try:
            # إدراج الفاتورة
            cursor.execute('''
                INSERT INTO invoices (invoice_number, customer_name, customer_phone, total_amount, discount_amount, tax_amount, final_amount, payment_method, created_at, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (invoice_number, customer_name, customer_phone, total_amount, discount_amount, tax_amount, final_amount, payment_method, invoice_date, user_id))
            
            invoice_id = cursor.lastrowid
            
            # إدراج أصناف الفاتورة
            for item_id, quantity, unit_price, total_price in invoice_items:
                cursor.execute('''
                    INSERT INTO sales (invoice_id, item_id, quantity, unit_price, total_price, discount_amount, tax_amount, final_price, created_at, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (invoice_id, item_id, quantity, unit_price, total_price, 0, 0, total_price, invoice_date, user_id))
                
                # تحديث كمية الصنف
                cursor.execute('UPDATE items SET quantity = quantity - ? WHERE id = ?', (quantity, item_id))
            
            invoices_count += 1
            
        except Exception as e:
            print(f"   ⚠️ خطأ في إضافة فاتورة: {str(e)}")
    
    print(f"   ✅ تم إضافة {invoices_count} فاتورة تجريبية")

def add_demo_purchases(cursor):
    """إضافة مشتريات تجريبية"""
    print("🛒 إضافة مشتريات تجريبية...")
    
    # الحصول على الأصناف والمستخدمين
    cursor.execute('SELECT id, cost_price FROM items')
    items = cursor.fetchall()
    
    cursor.execute('SELECT id FROM users WHERE role = "manager"')
    managers = cursor.fetchall()
    
    if not items or not managers:
        print("   ❌ لا توجد أصناف أو مديرين متاحين")
        return
    
    purchases_count = 0
    for i in range(30):
        # بيانات المورد
        supplier_name = f"مورد {i+1}" if random.random() > 0.2 else None
        supplier_phone = f"09{random.randint(10000000, 99999999)}" if supplier_name else None
        payment_method = random.choice(['cash', 'card'])
        manager_id = random.choice(managers)[0]
        
        # إنشاء تاريخ عشوائي
        purchase_date = (datetime.now() - timedelta(days=random.randint(0, 90))).strftime('%Y-%m-%d %H:%M:%S')
        
        # اختيار أصناف عشوائية
        selected_items = random.sample(items, random.randint(1, 4))
        
        total_amount = 0
        purchase_items = []
        
        for item_id, cost_price in selected_items:
            quantity = random.randint(5, 20)
            item_total = cost_price * quantity
            total_amount += item_total
            purchase_items.append((item_id, quantity, cost_price, item_total))
        
        if not purchase_items:
            continue
        
        # حساب الخصم والضريبة
        discount_amount = round(total_amount * random.uniform(0, 0.05), 2)
        tax_amount = round((total_amount - discount_amount) * 0.02, 2)
        final_amount = total_amount - discount_amount + tax_amount
        
        try:
            # إدراج أمر الشراء
            cursor.execute('''
                INSERT INTO purchases (supplier_name, supplier_phone, total_amount, discount_amount, tax_amount, final_amount, payment_method, created_at, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (supplier_name, supplier_phone, total_amount, discount_amount, tax_amount, final_amount, payment_method, purchase_date, manager_id))
            
            purchase_id = cursor.lastrowid
            
            # إدراج أصناف أمر الشراء
            for item_id, quantity, unit_cost, total_cost in purchase_items:
                cursor.execute('''
                    INSERT INTO purchase_items (purchase_id, item_id, quantity, unit_cost, total_cost, created_at)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (purchase_id, item_id, quantity, unit_cost, total_cost, purchase_date))
                
                # تحديث كمية الصنف
                cursor.execute('UPDATE items SET quantity = quantity + ? WHERE id = ?', (quantity, item_id))
            
            purchases_count += 1
            
        except Exception as e:
            print(f"   ⚠️ خطأ في إضافة أمر شراء: {str(e)}")
    
    print(f"   ✅ تم إضافة {purchases_count} أمر شراء تجريبي")

if __name__ == '__main__':
    add_demo_data()
