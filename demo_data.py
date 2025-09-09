# -*- coding: utf-8 -*-
"""
إضافة البيانات التجريبية
نظام إدارة المخزون - مخزن الزينة

جميع الحقوق محفوظة © 2025
تم تطوير هذا النظام بواسطة: محمد فاروق
تاريخ آخر تحديث: 9/9/2025
"""

import sqlite3
from datetime import datetime, timedelta
import random

def add_demo_data():
    """إضافة بيانات تجريبية شاملة"""
    try:
        # الاتصال بقاعدة البيانات
        conn = sqlite3.connect('inventory.db')
        cursor = conn.cursor()
        
        print("🔄 بدء إضافة البيانات التجريبية...")
        
        # إضافة أصناف تجريبية
        add_demo_items(cursor)
        
        # إضافة مبيعات تجريبية
        add_demo_sales(cursor)
        
        # إضافة فواتير تجريبية
        add_demo_invoices(cursor)
        
        # إضافة مشتريات تجريبية
        add_demo_purchases(cursor)
        
        # حفظ التغييرات
        conn.commit()
        conn.close()
        
        print("✅ تم إضافة البيانات التجريبية بنجاح!")
        
    except Exception as e:
        print(f"❌ خطأ في إضافة البيانات التجريبية: {str(e)}")

def add_demo_items(cursor):
    """إضافة أصناف تجريبية"""
    print("📦 إضافة أصناف تجريبية...")
    
    demo_items = [
        # إطارات
        ('إطار بريدجستون 205/55R16', 1, 'BRIDGE-001', 'إطار بريدجستون عالي الجودة', 50, 10, 800.0, 1200.0),
        ('إطار ميشلان 215/60R17', 1, 'MICHELIN-002', 'إطار ميشلان للطرق الوعرة', 30, 5, 900.0, 1400.0),
        ('إطار كونتيننتال 225/50R18', 1, 'CONTINENTAL-003', 'إطار كونتيننتال رياضية', 25, 5, 1000.0, 1600.0),
        
        # زينة خارجية
        ('مصد أمامي كاربون', 2, 'BUMPER-001', 'مصد أمامي من ألياف الكربون', 15, 3, 500.0, 800.0),
        ('شبك أمامي رياضية', 2, 'GRILLE-002', 'شبك أمامي بتصميم رياضي', 20, 5, 200.0, 350.0),
        ('جناح خلفي', 2, 'SPOILER-003', 'جناح خلفي رياضي', 10, 2, 300.0, 500.0),
        
        # زينة داخلية
        ('مقعد رياضي', 3, 'SEAT-001', 'مقعد رياضي جلدي', 8, 2, 800.0, 1200.0),
        ('ستيرنج سبورت', 3, 'STEERING-002', 'عجلة قيادة رياضية', 12, 3, 400.0, 600.0),
        ('بساط أرضي', 3, 'MAT-003', 'بساط أرضي مطاطي', 25, 5, 50.0, 80.0),
        
        # إضاءة
        ('لمبة LED أمامية', 4, 'LED-001', 'لمبة LED عالية الإضاءة', 40, 10, 100.0, 150.0),
        ('لمبة LED خلفية', 4, 'LED-002', 'لمبة LED خلفية', 35, 8, 80.0, 120.0),
        ('إضاءة داخلية LED', 4, 'LED-003', 'إضاءة داخلية متعددة الألوان', 20, 5, 60.0, 90.0),
        
        # صوتيات
        ('سماعة أمامية 6.5', 5, 'SPEAKER-001', 'سماعة أمامية عالية الجودة', 30, 5, 200.0, 300.0),
        ('سماعة خلفية 6x9', 5, 'SPEAKER-002', 'سماعة خلفية قوية', 25, 5, 250.0, 380.0),
        ('أمبليفاير 4 قنوات', 5, 'AMP-003', 'أمبليفاير 4 قنوات 1000 وات', 10, 2, 500.0, 750.0),
        
        # أدوات
        ('مفتاح ربط 10-24', 6, 'WRENCH-001', 'مجموعة مفاتيح ربط', 50, 10, 30.0, 45.0),
        ('مفك براغي', 6, 'SCREWDRIVER-002', 'مجموعة مفاتيح براغي', 40, 8, 25.0, 35.0),
        ('كماشة', 6, 'PLIERS-003', 'كماشة متعددة الاستخدام', 35, 7, 40.0, 60.0),
        
        # زيوت ومواد تشحيم
        ('زيت محرك 5W-30', 7, 'OIL-001', 'زيت محرك عالي الجودة', 100, 20, 80.0, 120.0),
        ('زيت فرامل DOT4', 7, 'BRAKE-002', 'زيت فرامل DOT4', 50, 10, 25.0, 40.0),
        ('مضاد تجمد', 7, 'ANTIFREEZE-003', 'مضاد تجمد للرادياتير', 30, 5, 35.0, 55.0),
        
        # بطاريات
        ('بطارية 12V 60Ah', 8, 'BATTERY-001', 'بطارية 12 فولت 60 أمبير', 20, 3, 400.0, 600.0),
        ('بطارية 12V 70Ah', 8, 'BATTERY-002', 'بطارية 12 فولت 70 أمبير', 15, 3, 450.0, 700.0),
        ('شاحن بطارية', 8, 'CHARGER-003', 'شاحن بطارية ذكي', 25, 5, 150.0, 220.0),
    ]
    
    for item in demo_items:
        cursor.execute('''
            INSERT INTO items (name, category_id, sku, description, quantity, reorder_level, cost_price, selling_price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', item)
    
    print(f"✅ تم إضافة {len(demo_items)} صنف تجريبي")

def add_demo_sales(cursor):
    """إضافة مبيعات تجريبية"""
    print("💰 إضافة مبيعات تجريبية...")
    
    # الحصول على الأصناف
    cursor.execute('SELECT id, selling_price FROM items')
    items = cursor.fetchall()
    
    if not items:
        print("❌ لا توجد أصناف لإضافة مبيعات")
        return
    
    # إضافة مبيعات للـ 30 يوم الماضية
    for i in range(100):
        item_id, price = random.choice(items)
        quantity = random.randint(1, 5)
        total_price = quantity * price
        
        # تاريخ عشوائي في الـ 30 يوم الماضية
        days_ago = random.randint(0, 30)
        sale_date = datetime.now() - timedelta(days=days_ago)
        
        cursor.execute('''
            INSERT INTO sales (item_id, quantity, unit_price, total_price, final_price, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (item_id, quantity, price, total_price, total_price, sale_date.strftime('%Y-%m-%d %H:%M:%S')))
    
    print("✅ تم إضافة 100 عملية بيع تجريبية")

def add_demo_invoices(cursor):
    """إضافة فواتير تجريبية"""
    print("🧾 إضافة فواتير تجريبية...")
    
    # الحصول على الأصناف
    cursor.execute('SELECT id, selling_price FROM items')
    items = cursor.fetchall()
    
    if not items:
        print("❌ لا توجد أصناف لإضافة فواتير")
        return
    
    customers = [
        ('أحمد محمد', '01234567890'),
        ('فاطمة علي', '01234567891'),
        ('محمد حسن', '01234567892'),
        ('عائشة أحمد', '01234567893'),
        ('علي محمود', '01234567894'),
        ('نور الدين', '01234567895'),
        ('سارة محمد', '01234567896'),
        ('خالد أحمد', '01234567897'),
        ('مريم علي', '01234567898'),
        ('يوسف حسن', '01234567899'),
    ]
    
    # إضافة فواتير للـ 30 يوم الماضية
    for i in range(50):
        customer_name, customer_phone = random.choice(customers)
        payment_method = random.choice(['cash', 'card'])
        
        # تاريخ عشوائي
        days_ago = random.randint(0, 30)
        invoice_date = datetime.now() - timedelta(days=days_ago)
        
        # إنشاء رقم فاتورة
        invoice_number = f"INV-{invoice_date.strftime('%Y%m%d')}-{i+1:03d}"
        
        # إضافة الفاتورة
        cursor.execute('''
            INSERT INTO invoices (invoice_number, customer_name, customer_phone, payment_method, created_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (invoice_number, customer_name, customer_phone, payment_method, 1, invoice_date.strftime('%Y-%m-%d %H:%M:%S')))
        
        invoice_id = cursor.lastrowid
        
        # إضافة أصناف للفاتورة
        num_items = random.randint(1, 5)
        total_amount = 0
        
        for j in range(num_items):
            item_id, price = random.choice(items)
            quantity = random.randint(1, 3)
            item_total = quantity * price
            total_amount += item_total
            
            cursor.execute('''
                INSERT INTO sales (invoice_id, item_id, quantity, unit_price, total_price, final_price, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (invoice_id, item_id, quantity, price, item_total, item_total, invoice_date.strftime('%Y-%m-%d %H:%M:%S')))
        
        # تحديث إجمالي الفاتورة
        discount = random.randint(0, 50)
        tax = random.randint(0, 20)
        final_amount = total_amount - discount + tax
        
        cursor.execute('''
            UPDATE invoices 
            SET total_amount = ?, discount_amount = ?, tax_amount = ?, final_amount = ?
            WHERE id = ?
        ''', (total_amount, discount, tax, final_amount, invoice_id))
    
    print("✅ تم إضافة 50 فاتورة تجريبية")

def add_demo_purchases(cursor):
    """إضافة مشتريات تجريبية"""
    print("🛒 إضافة مشتريات تجريبية...")
    
    suppliers = [
        ('شركة الإطارات المتحدة', '01234567001'),
        ('مؤسسة الزينة المتقدمة', '01234567002'),
        ('شركة الصوتيات الحديثة', '01234567003'),
        ('مؤسسة الإضاءة الذكية', '01234567004'),
        ('شركة الأدوات المهنية', '01234567005'),
    ]
    
    # الحصول على الأصناف
    cursor.execute('SELECT id, cost_price FROM items')
    items = cursor.fetchall()
    
    if not items:
        print("❌ لا توجد أصناف لإضافة مشتريات")
        return
    
    # إضافة مشتريات للـ 30 يوم الماضية
    for i in range(30):
        supplier_name, supplier_phone = random.choice(suppliers)
        payment_method = random.choice(['cash', 'card'])
        
        # تاريخ عشوائي
        days_ago = random.randint(0, 30)
        purchase_date = datetime.now() - timedelta(days=days_ago)
        
        # إضافة أمر الشراء
        cursor.execute('''
            INSERT INTO purchases (supplier_name, supplier_phone, payment_method, created_by, created_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (supplier_name, supplier_phone, payment_method, 1, purchase_date.strftime('%Y-%m-%d %H:%M:%S')))
        
        purchase_id = cursor.lastrowid
        
        # إضافة أصناف للشراء
        num_items = random.randint(2, 8)
        total_amount = 0
        
        for j in range(num_items):
            item_id, cost_price = random.choice(items)
            quantity = random.randint(10, 50)
            item_total = quantity * cost_price
            total_amount += item_total
            
            cursor.execute('''
                INSERT INTO purchase_items (purchase_id, item_id, quantity, unit_cost, total_cost, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (purchase_id, item_id, quantity, cost_price, item_total, purchase_date.strftime('%Y-%m-%d %H:%M:%S')))
            
            # تحديث كمية الصنف
            cursor.execute('''
                UPDATE items 
                SET quantity = quantity + ?
                WHERE id = ?
            ''', (quantity, item_id))
        
        # تحديث إجمالي الشراء
        discount = random.randint(0, 100)
        tax = random.randint(0, 50)
        final_amount = total_amount - discount + tax
        
        cursor.execute('''
            UPDATE purchases 
            SET total_amount = ?, discount_amount = ?, tax_amount = ?, final_amount = ?
            WHERE id = ?
        ''', (total_amount, discount, tax, final_amount, purchase_id))
    
    print("✅ تم إضافة 30 أمر شراء تجريبي")

if __name__ == "__main__":
    add_demo_data()
