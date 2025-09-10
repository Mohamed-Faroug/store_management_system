# -*- coding: utf-8 -*-
"""
إدارة البيانات - استيراد وتصدير
"""

import os
import json
import csv
from datetime import datetime

try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas not available. Excel export/import will be limited.")
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify, send_file
from werkzeug.utils import secure_filename
from ..models.database import get_db
from ..utils.auth import dev_user_required

data_management_bp = Blueprint('data_management', __name__)

# إعدادات رفع الملفات
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'xls', 'json'}

# إنشاء مجلد الرفع إذا لم يكن موجوداً
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    """التحقق من نوع الملف المسموح"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@data_management_bp.route('/data-management')
@dev_user_required
def index():
    """الصفحة الرئيسية لإدارة البيانات"""
    return render_template('data_management/index.html')

@data_management_bp.route('/data-management/export')
@dev_user_required
def export_data():
    """تصدير البيانات"""
    export_type = request.args.get('type', 'items')
    
    if export_type == 'items':
        return export_items()
    elif export_type == 'categories':
        return export_categories()
    elif export_type == 'invoices':
        return export_invoices()
    elif export_type == 'sales':
        return export_sales()
    else:
        flash('نوع التصدير غير صحيح', 'danger')
        return redirect(url_for('data_management.index'))

def export_items():
    """تصدير بيانات الأصناف"""
    try:
        if not PANDAS_AVAILABLE:
            flash('مكتبة pandas غير متوفرة. يرجى تثبيتها لاستخدام تصدير Excel', 'danger')
            return redirect(url_for('data_management.index'))
            
        db = get_db()
        items = db.execute('''
            SELECT i.*, c.name as category_name 
            FROM items i 
            LEFT JOIN categories c ON c.id = i.category_id 
            ORDER BY i.name
        ''').fetchall()
        
        # تحويل إلى DataFrame
        data = []
        for item in items:
            data.append({
                'id': item['id'],
                'name': item['name'],
                'sku': item['sku'],
                'price': item['price'],
                'quantity': item['quantity'],
                'min_quantity': item['min_quantity'],
                'category_name': item['category_name'],
                'description': item['description'],
                'created_at': item['created_at']
            })
        
        df = pd.DataFrame(data)
        
        # حفظ كملف Excel
        filename = f'items_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        flash(f'خطأ في تصدير البيانات: {str(e)}', 'danger')
        return redirect(url_for('data_management.index'))

def export_categories():
    """تصدير بيانات الفئات"""
    try:
        if not PANDAS_AVAILABLE:
            flash('مكتبة pandas غير متوفرة. يرجى تثبيتها لاستخدام تصدير Excel', 'danger')
            return redirect(url_for('data_management.index'))
            
        db = get_db()
        categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
        
        data = []
        for cat in categories:
            data.append({
                'id': cat['id'],
                'name': cat['name'],
                'description': cat['description'],
                'created_at': cat['created_at']
            })
        
        df = pd.DataFrame(data)
        
        filename = f'categories_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        flash(f'خطأ في تصدير البيانات: {str(e)}', 'danger')
        return redirect(url_for('data_management.index'))

def export_invoices():
    """تصدير بيانات الفواتير"""
    try:
        if not PANDAS_AVAILABLE:
            flash('مكتبة pandas غير متوفرة. يرجى تثبيتها لاستخدام تصدير Excel', 'danger')
            return redirect(url_for('data_management.index'))
            
        db = get_db()
        invoices = db.execute('''
            SELECT i.*, u.username as created_by_name
            FROM invoices i 
            LEFT JOIN users u ON u.id = i.created_by 
            ORDER BY i.created_at DESC
        ''').fetchall()
        
        data = []
        for inv in invoices:
            data.append({
                'id': inv['id'],
                'invoice_number': inv['invoice_number'],
                'customer_name': inv['customer_name'],
                'customer_phone': inv['customer_phone'],
                'total_amount': inv['total_amount'],
                'discount_amount': inv['discount_amount'],
                'tax_amount': inv['tax_amount'],
                'final_amount': inv['final_amount'],
                'payment_method': inv['payment_method'],
                'status': inv['status'],
                'created_at': inv['created_at'],
                'created_by_name': inv['created_by_name']
            })
        
        df = pd.DataFrame(data)
        
        filename = f'invoices_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        flash(f'خطأ في تصدير البيانات: {str(e)}', 'danger')
        return redirect(url_for('data_management.index'))

def export_sales():
    """تصدير بيانات المبيعات"""
    try:
        if not PANDAS_AVAILABLE:
            flash('مكتبة pandas غير متوفرة. يرجى تثبيتها لاستخدام تصدير Excel', 'danger')
            return redirect(url_for('data_management.index'))
            
        db = get_db()
        sales = db.execute('''
            SELECT s.*, i.name as item_name, inv.invoice_number
            FROM sales s 
            JOIN items i ON i.id = s.item_id 
            JOIN invoices inv ON inv.id = s.invoice_id
            ORDER BY s.created_at DESC
        ''').fetchall()
        
        data = []
        for sale in sales:
            data.append({
                'id': sale['id'],
                'invoice_number': sale['invoice_number'],
                'item_name': sale['item_name'],
                'quantity': sale['quantity'],
                'unit_price': sale['unit_price'],
                'total_price': sale['total_price'],
                'discount_amount': sale['discount_amount'],
                'tax_amount': sale['tax_amount'],
                'final_price': sale['final_price'],
                'created_at': sale['created_at']
            })
        
        df = pd.DataFrame(data)
        
        filename = f'sales_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return send_file(filepath, as_attachment=True, download_name=filename)
        
    except Exception as e:
        flash(f'خطأ في تصدير البيانات: {str(e)}', 'danger')
        return redirect(url_for('data_management.index'))

@data_management_bp.route('/data-management/import', methods=['GET', 'POST'])
@dev_user_required
def import_data():
    """استيراد البيانات"""
    if request.method == 'POST':
        import_type = request.form.get('import_type')
        file = request.files.get('file')
        
        if not file or file.filename == '':
            flash('لم يتم اختيار ملف', 'danger')
            return redirect(url_for('data_management.import_data'))
        
        if not allowed_file(file.filename):
            flash('نوع الملف غير مدعوم. الملفات المدعومة: CSV, Excel', 'danger')
            return redirect(url_for('data_management.import_data'))
        
        try:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)
            
            if import_type == 'items':
                result = import_items(filepath)
            elif import_type == 'categories':
                result = import_categories(filepath)
            else:
                flash('نوع الاستيراد غير صحيح', 'danger')
                return redirect(url_for('data_management.import_data'))
            
            if result['success']:
                flash(f"تم استيراد {result['count']} سجل بنجاح", 'success')
            else:
                flash(f"خطأ في الاستيراد: {result['error']}", 'danger')
            
            # حذف الملف المؤقت
            if os.path.exists(filepath):
                os.remove(filepath)
                
        except Exception as e:
            flash(f'خطأ في معالجة الملف: {str(e)}', 'danger')
    
    return render_template('data_management/import.html')

def import_items(filepath):
    """استيراد بيانات الأصناف"""
    try:
        if not PANDAS_AVAILABLE:
            return {
                'success': False,
                'error': 'مكتبة pandas غير متوفرة. يرجى تثبيتها لاستخدام استيراد Excel'
            }
            
        # قراءة الملف
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # التحقق من الأعمدة المطلوبة
        required_columns = ['name', 'price', 'quantity']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            return {
                'success': False,
                'error': f'الأعمدة المطلوبة مفقودة: {", ".join(missing_columns)}'
            }
        
        db = get_db()
        cursor = db.cursor()
        
        imported_count = 0
        
        for _, row in df.iterrows():
            try:
                # البحث عن الفئة
                category_id = None
                if 'category_name' in df.columns and pd.notna(row['category_name']):
                    category = cursor.execute(
                        'SELECT id FROM categories WHERE name = ?', 
                        (row['category_name'],)
                    ).fetchone()
                    if category:
                        category_id = category['id']
                
                # إدراج الصنف
                cursor.execute('''
                    INSERT INTO items (name, sku, price, quantity, min_quantity, 
                                     category_id, description, created_at, created_by)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    row['name'],
                    row.get('sku', ''),
                    float(row['price']),
                    int(row['quantity']),
                    int(row.get('min_quantity', 0)),
                    category_id,
                    row.get('description', ''),
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    session.get('user_id')
                ))
                
                imported_count += 1
                
            except Exception as e:
                print(f"خطأ في استيراد الصنف {row.get('name', 'غير معروف')}: {e}")
                continue
        
        db.commit()
        
        return {
            'success': True,
            'count': imported_count
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def import_categories(filepath):
    """استيراد بيانات الفئات"""
    try:
        if not PANDAS_AVAILABLE:
            return {
                'success': False,
                'error': 'مكتبة pandas غير متوفرة. يرجى تثبيتها لاستخدام استيراد Excel'
            }
            
        # قراءة الملف
        if filepath.endswith('.csv'):
            df = pd.read_csv(filepath)
        else:
            df = pd.read_excel(filepath)
        
        # التحقق من الأعمدة المطلوبة
        if 'name' not in df.columns:
            return {
                'success': False,
                'error': 'العمود "name" مطلوب'
            }
        
        db = get_db()
        cursor = db.cursor()
        
        imported_count = 0
        
        for _, row in df.iterrows():
            try:
                # التحقق من عدم وجود الفئة مسبقاً
                existing = cursor.execute(
                    'SELECT id FROM categories WHERE name = ?', 
                    (row['name'],)
                ).fetchone()
                
                if not existing:
                    cursor.execute('''
                        INSERT INTO categories (name, description, created_at)
                        VALUES (?, ?, ?)
                    ''', (
                        row['name'],
                        row.get('description', ''),
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ))
                    
                    imported_count += 1
                
            except Exception as e:
                print(f"خطأ في استيراد الفئة {row.get('name', 'غير معروف')}: {e}")
                continue
        
        db.commit()
        
        return {
            'success': True,
            'count': imported_count
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

@data_management_bp.route('/data-management/template/<template_type>')
@dev_user_required
def download_template(template_type):
    """تحميل قالب للبيانات"""
    try:
        if template_type == 'items':
            return download_items_template()
        elif template_type == 'categories':
            return download_categories_template()
        else:
            flash('نوع القالب غير صحيح', 'danger')
            return redirect(url_for('data_management.index'))
    except Exception as e:
        flash(f'خطأ في تحميل القالب: {str(e)}', 'danger')
        return redirect(url_for('data_management.index'))

def download_items_template():
    """تحميل قالب الأصناف"""
    try:
        if not PANDAS_AVAILABLE:
            flash('مكتبة pandas غير متوفرة. يرجى تثبيتها لاستخدام قوالب Excel', 'danger')
            return redirect(url_for('data_management.index'))
            
        # إنشاء DataFrame فارغ بالأعمدة المطلوبة
        df = pd.DataFrame(columns=[
            'name', 'sku', 'price', 'quantity', 'min_quantity', 
            'category_name', 'description'
        ])
        
        # إضافة مثال
        df.loc[0] = [
            'مثال: إطار سيارة', 'SKU001', 500.0, 10, 2, 
            'إطارات', 'إطار سيارة عالي الجودة'
        ]
        
        filename = f'items_template_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        flash(f'خطأ في إنشاء القالب: {str(e)}', 'danger')
        return redirect(url_for('data_management.index'))

def download_categories_template():
    """تحميل قالب الفئات"""
    try:
        if not PANDAS_AVAILABLE:
            flash('مكتبة pandas غير متوفرة. يرجى تثبيتها لاستخدام قوالب Excel', 'danger')
            return redirect(url_for('data_management.index'))
            
        # إنشاء DataFrame فارغ بالأعمدة المطلوبة
        df = pd.DataFrame(columns=['name', 'description'])
        
        # إضافة مثال
        df.loc[0] = ['مثال: إطارات', 'فئة الإطارات والجنوط']
        
        filename = f'categories_template_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        df.to_excel(filepath, index=False, engine='openpyxl')
        
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        flash(f'خطأ في إنشاء القالب: {str(e)}', 'danger')
        return redirect(url_for('data_management.index'))
