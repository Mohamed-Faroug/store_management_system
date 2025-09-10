# -*- coding: utf-8 -*-
"""
إدارة المبيعات
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.database import get_db, now_str
from ..utils.auth import login_required
from ..models.settings_models import pos_settings, tax_settings, payment_method_settings, currency_settings

bp = Blueprint('sales', __name__)

@bp.route('/sales/new', methods=['GET', 'POST'])
@login_required()
def new():
    """نقطة البيع (POS)"""
    if request.method == 'POST':
        # Handle POS form submission
        items_data = request.form.get('items_data')
        total_amount = float(request.form.get('total_amount', 0))
        discount_amount = float(request.form.get('discount_amount', 0))
        tax_amount = float(request.form.get('tax_amount', 0))
        final_amount = float(request.form.get('final_amount', 0))
        
        if not items_data:
            flash('لا توجد أصناف في السلة', 'danger')
            return redirect(url_for('sales.new'))
        
        try:
            import json
            items = json.loads(items_data)
            
            if not items:
                flash('لا توجد أصناف في السلة', 'danger')
                return redirect(url_for('sales.new'))
            
            # Load settings
            pos_config = pos_settings.get_all_settings()
            tax_config = tax_settings.get_all_settings()
            payment_methods = payment_method_settings.get_all_methods()
            
            # Get payment method from form or default to cash
            payment_method = request.form.get('payment_method', 'cash')
            
            # Calculate taxable amount
            taxable_amount = total_amount - discount_amount
            
            # Calculate tax based on settings
            if tax_config.get('enabled', False):
                tax_rate = tax_config.get('rate', 0) / 100
                calculated_tax = taxable_amount * tax_rate
            else:
                calculated_tax = 0
            
            # Use the tax amount from form if provided, otherwise use calculated tax
            if tax_amount > 0:
                final_tax_amount = tax_amount
            else:
                final_tax_amount = calculated_tax
            
            db = get_db()
            cursor = db.cursor()
            user_id = session.get('user_id')
            
            # Create invoice
            invoice_number = f"POS-{db.execute('SELECT COUNT(*) FROM invoices').fetchone()[0] + 1:06d}"
            cursor.execute('''
                INSERT INTO invoices (invoice_number, customer_name, customer_phone, total_amount, 
                                    discount_amount, tax_amount, final_amount, payment_method, created_at, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (invoice_number, None, None, total_amount, discount_amount, final_tax_amount, 
                  taxable_amount + final_tax_amount, payment_method, now_str(), user_id))
            
            invoice_id = cursor.lastrowid
            
            # Process each item
            for item in items:
                item_id = item['item_id']
                quantity = item['quantity']
                unit_price = item['unit_price']
                total_price = item['total_price']
                
                # Check stock availability
                current_item = cursor.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
                if not current_item:
                    flash(f'الصنف غير موجود: {item_id}', 'warning')
                    continue
                
                if current_item['quantity'] < quantity:
                    flash(f'الكمية المتاحة من {current_item["name"]}: {current_item["quantity"]} فقط', 'warning')
                    continue
                
                # Update item quantity
                new_quantity = current_item['quantity'] - quantity
                cursor.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_quantity, item_id))
                
                # Update selling price if not set
                if not current_item['selling_price'] or current_item['selling_price'] == 0:
                    cursor.execute('UPDATE items SET selling_price = ? WHERE id = ?', (unit_price, item_id))
                
                # Record sale
                cursor.execute('''
                    INSERT INTO sales (invoice_id, item_id, quantity, unit_price, total_price, 
                                     discount_amount, tax_amount, final_price, created_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (invoice_id, item_id, quantity, unit_price, total_price, 
                      0, 0, total_price, now_str()))
            
            db.commit()
            
            # Debug: Check if data was saved correctly
            print(f"Debug: Created invoice with ID: {invoice_id}")
            print(f"Debug: Invoice number: {invoice_number}")
            
            # Check sales records
            sales_check = cursor.execute('SELECT COUNT(*) FROM sales WHERE invoice_id = ?', (invoice_id,)).fetchone()
            print(f"Debug: Sales records count: {sales_check[0]}")
            
            flash(f'تم إتمام البيع بنجاح! رقم الفاتورة: {invoice_number}', 'success')
            return redirect(url_for('invoices.view', invoice_id=invoice_id))
        except Exception as e:
            print(f"Debug: Error in sales: {str(e)}")
            flash(f'خطأ في البيع: {str(e)}', 'danger')
    
    db = get_db()
    items = db.execute('''
        SELECT i.*, c.name as category_name,
               CASE 
                   WHEN i.selling_price > 0 THEN i.selling_price
                   ELSE i.cost_price
               END as display_price
        FROM items i 
        LEFT JOIN categories c ON c.id = i.category_id 
        WHERE i.quantity > 0 
        ORDER BY i.name
    ''').fetchall()
    
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    
    # Load settings
    pos_config = pos_settings.get_all_settings()
    tax_config = tax_settings.get_all_settings()
    payment_methods = payment_method_settings.get_all_methods()
    currency_config = currency_settings.get_all_settings()
    
    return render_template('sales/new.html', 
                         items=items, 
                         categories=categories,
                         pos_settings=pos_config,
                         tax_config=tax_config,
                         payment_methods=payment_methods,
                         currency_config=currency_config)

@bp.route('/sales')
@login_required()
def list():
    """قائمة المبيعات"""
    db = get_db()
    sales = db.execute('''
        SELECT s.*, i.name as item_name, inv.invoice_number
        FROM sales s 
        JOIN items i ON i.id = s.item_id 
        LEFT JOIN invoices inv ON inv.id = s.invoice_id
        ORDER BY s.created_at DESC 
        LIMIT 100
    ''').fetchall()
    return render_template('sales/list.html', sales=sales)
