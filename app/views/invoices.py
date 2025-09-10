# -*- coding: utf-8 -*-
"""
إدارة الفواتير
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.database import get_db, now_str
from ..models.settings_models import tax_settings, payment_method_settings, currency_settings
from ..utils.auth import login_required, dev_user_required
from ..utils.payment_utils import get_payment_method_display_name

bp = Blueprint('invoices', __name__)

@bp.route('/invoices')
@login_required()
def list():
    """قائمة الفواتير - للكاشير والمدير"""
    
    db = get_db()
    
    # Get search parameters
    search_date = request.args.get('date', '')
    search_customer = request.args.get('customer', '')
    search_invoice = request.args.get('invoice', '')
    
    # Build query
    query = '''
        SELECT i.*, u.username as created_by_name
        FROM invoices i
        LEFT JOIN users u ON u.id = i.created_by
        WHERE 1=1
    '''
    params = []
    
    if search_date:
        query += ' AND DATE(i.created_at) = ?'
        params.append(search_date)
    
    if search_customer:
        query += ' AND (i.customer_name LIKE ? OR i.customer_phone LIKE ?)'
        params.append(f'%{search_customer}%')
        params.append(f'%{search_customer}%')
    
    if search_invoice:
        query += ' AND i.invoice_number LIKE ?'
        params.append(f'%{search_invoice}%')
    
    query += ' ORDER BY i.created_at DESC'
    
    invoices = db.execute(query, params).fetchall()
    
    # إضافة أسماء طرق الدفع للفواتير
    invoices_with_payment_names = []
    for invoice in invoices:
        invoice_dict = dict(invoice)
        invoice_dict['payment_method_name'] = get_payment_method_display_name(invoice['payment_method'])
        invoices_with_payment_names.append(invoice_dict)
    
    return render_template('invoices/list.html', 
                         invoices=invoices_with_payment_names, 
                         search_date=search_date,
                         search_customer=search_customer,
                         search_invoice=search_invoice)

@bp.route('/invoices/new', methods=['GET', 'POST'])
@login_required()
def new():
    """فاتورة جديدة - للكاشير والمدير"""
    if request.method == 'POST':
        customer_name = request.form.get('customer_name', '').strip()
        customer_phone = request.form.get('customer_phone', '').strip()
        payment_method = request.form.get('payment_method', 'cash')
        
        # Get items from form
        items = []
        for key, value in request.form.items():
            if key.startswith('item_') and key.endswith('_id'):
                item_id = value
                quantity = int(request.form.get(f'item_{item_id}_quantity', 0))
                unit_price = float(request.form.get(f'item_{item_id}_price', 0))
                
                if quantity > 0 and unit_price > 0:
                    items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'unit_price': unit_price,
                        'total_price': quantity * unit_price
                    })
        
        if not items:
            flash('يرجى إضافة أصناف للفاتورة', 'danger')
            return redirect(url_for('invoices.new'))
        
        db = get_db()
        try:
            # Calculate totals
            total_amount = sum(item['total_price'] for item in items)
            discount_amount = float(request.form.get('discount_amount', 0))
            tax_amount = float(request.form.get('tax_amount', 0))
            final_amount = total_amount - discount_amount + tax_amount
            
            # Generate invoice number
            invoice_number = f"INV-{now_str().replace(':', '').replace('-', '').replace(' ', '')}"
            
            # Create invoice record
            invoice_id = db.execute('''
                INSERT INTO invoices (invoice_number, customer_name, customer_phone, total_amount, discount_amount, tax_amount, final_amount, payment_method, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (invoice_number, customer_name, customer_phone, total_amount, discount_amount, tax_amount, final_amount, payment_method, session['user_id'])).lastrowid
            
            # Add invoice items and update inventory
            for item in items:
                db.execute('''
                    INSERT INTO sales (invoice_id, item_id, quantity, unit_price, total_price, final_price)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (invoice_id, item['item_id'], item['quantity'], item['unit_price'], item['total_price'], item['total_price']))
                
                # Update item quantity
                db.execute('''
                    UPDATE items 
                    SET quantity = quantity - ?
                    WHERE id = ?
                ''', (item['quantity'], item['item_id']))
            
            db.commit()
            flash('تم إنشاء الفاتورة بنجاح', 'success')
            return redirect(url_for('invoices.view', invoice_id=invoice_id))
        except Exception as e:
            flash(f'خطأ في إنشاء الفاتورة: {str(e)}', 'danger')
    
    db = get_db()
    items = db.execute('SELECT * FROM items WHERE quantity > 0 ORDER BY name').fetchall()
    
    # Load settings for the form
    payment_methods = payment_method_settings.get_enabled_methods()
    tax_config = tax_settings.get_all_settings()
    currency_config = currency_settings.get_default_currency()
    
    return render_template('invoices/new.html', 
                         items=items, 
                         payment_methods=payment_methods,
                         tax_config=tax_config,
                         currency_config=currency_config)

@bp.route('/invoices/<int:invoice_id>')
@login_required()
def view(invoice_id):
    """عرض تفاصيل الفاتورة - للكاشير والمدير"""
    db = get_db()
    invoice = db.execute('''
        SELECT i.*, u.username as created_by_name
        FROM invoices i
        LEFT JOIN users u ON u.id = i.created_by
        WHERE i.id = ?
    ''', (invoice_id,)).fetchone()
    
    if not invoice:
        flash('الفاتورة غير موجودة', 'danger')
        return redirect(url_for('invoices.list'))
    
    # Get invoice items from sales table
    items = db.execute('''
        SELECT s.*, i.name as item_name
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE s.invoice_id = ?
        ORDER BY s.id
    ''', (invoice_id,)).fetchall()
    
    # الحصول على اسم طريقة الدفع
    payment_method_name = get_payment_method_display_name(invoice['payment_method'])
    
    return render_template('invoices/view.html', 
                         invoice=invoice, 
                         items=items, 
                         payment_method_name=payment_method_name)

@bp.route('/invoices/<int:invoice_id>/print')
@login_required()
def print_invoice(invoice_id):
    """طباعة الفاتورة A4 - للكاشير والمدير"""
    db = get_db()
    invoice = db.execute('''
        SELECT i.*, u.username as created_by_name
        FROM invoices i
        LEFT JOIN users u ON u.id = i.created_by
        WHERE i.id = ?
    ''', (invoice_id,)).fetchone()
    
    if not invoice:
        flash('الفاتورة غير موجودة', 'danger')
        return redirect(url_for('invoices.list'))
    
    items = db.execute('''
        SELECT s.*, i.name as item_name
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE s.invoice_id = ?
        ORDER BY s.id
    ''', (invoice_id,)).fetchall()
    
    # الحصول على اسم طريقة الدفع
    payment_method_name = get_payment_method_display_name(invoice['payment_method'])
    
    return render_template('invoices/print_a4.html', 
                         invoice=invoice, 
                         items=items, 
                         payment_method_name=payment_method_name)

@bp.route('/invoices/<int:invoice_id>/print-58mm')
@login_required()
def print_invoice_58mm(invoice_id):
    """طباعة الفاتورة 58mm - للكاشير والمدير"""
    db = get_db()
    invoice = db.execute('''
        SELECT i.*, u.username as created_by_name
        FROM invoices i
        LEFT JOIN users u ON u.id = i.created_by
        WHERE i.id = ?
    ''', (invoice_id,)).fetchone()
    
    if not invoice:
        flash('الفاتورة غير موجودة', 'danger')
        return redirect(url_for('invoices.list'))
    
    items = db.execute('''
        SELECT s.*, i.name as item_name
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE s.invoice_id = ?
        ORDER BY s.id
    ''', (invoice_id,)).fetchall()
    
    # الحصول على اسم طريقة الدفع
    payment_method_name = get_payment_method_display_name(invoice['payment_method'])
    
    return render_template('invoices/print_58mm.html', 
                         invoice=invoice, 
                         items=items, 
                         payment_method_name=payment_method_name)

@bp.route('/api/invoices/<int:invoice_id>/data')
@dev_user_required
def get_invoice_data(invoice_id):
    """جلب بيانات الفاتورة كـ JSON - لمستخدم dev فقط"""
    from flask import jsonify
    
    try:
        db = get_db()
        invoice = db.execute('''
            SELECT i.*, u.username as created_by_name
            FROM invoices i
            LEFT JOIN users u ON u.id = i.created_by
            WHERE i.id = ?
        ''', (invoice_id,)).fetchone()
        
        if not invoice:
            return jsonify({'error': 'الفاتورة غير موجودة'}), 404
        
        items = db.execute('''
            SELECT s.*, i.name as item_name
            FROM sales s
            JOIN items i ON i.id = s.item_id
            WHERE s.invoice_id = ?
            ORDER BY s.id
        ''', (invoice_id,)).fetchall()
        
        # Convert to dictionary
        invoice_data = dict(invoice)
        items_data = [dict(item) for item in items]
        
        return jsonify({
            'invoice': invoice_data,
            'items': items_data,
            'summary': {
                'total_items': len(items_data),
                'total_amount': float(invoice_data['total_amount']),
                'final_amount': float(invoice_data['final_amount']),
                'discount_amount': float(invoice_data['discount_amount']),
                'tax_amount': float(invoice_data['tax_amount'])
            }
        })
    except Exception as e:
        return jsonify({'error': f'خطأ في جلب البيانات: {str(e)}'}), 500

@bp.route('/api/invoices/export')
@dev_user_required
def export_invoices():
    """تصدير جميع الفواتير كـ JSON - لمستخدم dev فقط"""
    from flask import jsonify
    
    try:
        db = get_db()
        
        # Get date range from query parameters
        start_date = request.args.get('start_date', '')
        end_date = request.args.get('end_date', '')
        
        query = '''
            SELECT i.*, u.username as created_by_name
            FROM invoices i
            LEFT JOIN users u ON u.id = i.created_by
            WHERE 1=1
        '''
        params = []
        
        if start_date:
            query += ' AND DATE(i.created_at) >= ?'
            params.append(start_date)
        
        if end_date:
            query += ' AND DATE(i.created_at) <= ?'
            params.append(end_date)
        
        query += ' ORDER BY i.created_at DESC'
        
        invoices = db.execute(query, params).fetchall()
        
        # Convert to list of dictionaries
        invoices_data = []
        for invoice in invoices:
            invoice_dict = dict(invoice)
            
            # Get items for each invoice
            items = db.execute('''
                SELECT s.*, i.name as item_name
                FROM sales s
                JOIN items i ON i.id = s.item_id
                WHERE s.invoice_id = ?
                ORDER BY s.id
            ''', (invoice['id'],)).fetchall()
            
            invoice_dict['items'] = [dict(item) for item in items]
            invoices_data.append(invoice_dict)
        
        return jsonify({
            'invoices': invoices_data,
            'total_count': len(invoices_data),
            'export_date': now_str(),
            'filters': {
                'start_date': start_date,
                'end_date': end_date
            }
        })
    except Exception as e:
        return jsonify({'error': f'خطأ في تصدير البيانات: {str(e)}'}), 500

@bp.route('/invoices/export-page')
@dev_user_required
def export_page():
    """صفحة تصدير البيانات - لمستخدم dev فقط"""
    return render_template('invoices/export.html')

@bp.route('/api/test')
@dev_user_required
def test_api():
    """اختبار API - لمستخدم dev فقط"""
    from flask import jsonify
    return jsonify({'status': 'success', 'message': 'API يعمل بشكل صحيح'})

@bp.route('/api/status')
@dev_user_required
def api_status():
    """حالة API - لمستخدم dev فقط"""
    from flask import jsonify
    return jsonify({
        'status': 'active',
        'message': 'API نشط ويعمل بشكل صحيح',
        'version': '1.0.0',
        'endpoints': [
            '/invoices/api/invoices/export',
            '/invoices/api/invoices/<id>/data',
            '/invoices/api/test'
        ]
    })