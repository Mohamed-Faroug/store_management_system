# -*- coding: utf-8 -*-
"""
إدارة المشتريات
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.database import get_db, now_str
from ..utils.auth import login_required
from ..utils.payment_utils import get_payment_method_display_name

bp = Blueprint('purchases', __name__)

@bp.route('/purchases')
@login_required()
def list():
    """قائمة المشتريات"""
    db = get_db()
    purchases = db.execute('''
        SELECT p.*, u.username as created_by_name
        FROM purchases p
        LEFT JOIN users u ON u.id = p.created_by
        ORDER BY p.created_at DESC
    ''').fetchall()
    
    # إضافة أسماء طرق الدفع للمشتريات
    purchases_with_payment_names = []
    for purchase in purchases:
        purchase_dict = dict(purchase)
        purchase_dict['payment_method_name'] = get_payment_method_display_name(purchase['payment_method'])
        purchases_with_payment_names.append(purchase_dict)
    
    return render_template('purchases/list.html', purchases=purchases_with_payment_names)

@bp.route('/purchases/new', methods=['GET', 'POST'])
@login_required()
def new():
    """شراء جديد"""
    if request.method == 'POST':
        supplier_name = request.form.get('supplier_name', '').strip()
        supplier_phone = request.form.get('supplier_phone', '').strip()
        payment_method = request.form.get('payment_method', 'cash')
        
        # Get items from form
        items = []
        for key, value in request.form.items():
            if key.startswith('item_') and key.endswith('_id'):
                item_id = value
                quantity = int(request.form.get(f'item_{item_id}_quantity', 0))
                unit_cost = float(request.form.get(f'item_{item_id}_cost', 0))
                
                if quantity > 0 and unit_cost > 0:
                    items.append({
                        'item_id': item_id,
                        'quantity': quantity,
                        'unit_cost': unit_cost,
                        'total_cost': quantity * unit_cost
                    })
        
        if not items:
            flash('يرجى إضافة أصناف للشراء', 'danger')
            return redirect(url_for('purchases.new'))
        
        db = get_db()
        try:
            # Calculate totals
            total_amount = sum(item['total_cost'] for item in items)
            discount_amount = float(request.form.get('discount_amount', 0))
            tax_amount = float(request.form.get('tax_amount', 0))
            final_amount = total_amount - discount_amount + tax_amount
            
            # Create purchase record
            purchase_id = db.execute('''
                INSERT INTO purchases (supplier_name, supplier_phone, total_amount, discount_amount, tax_amount, final_amount, payment_method, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (supplier_name, supplier_phone, total_amount, discount_amount, tax_amount, final_amount, payment_method, session['user_id'])).lastrowid
            
            # Add purchase items and update inventory
            for item in items:
                db.execute('''
                    INSERT INTO purchase_items (purchase_id, item_id, quantity, unit_cost, total_cost)
                    VALUES (?, ?, ?, ?, ?)
                ''', (purchase_id, item['item_id'], item['quantity'], item['unit_cost'], item['total_cost']))
                
                # Update item quantity
                db.execute('''
                    UPDATE items 
                    SET quantity = quantity + ?, cost_price = ?
                    WHERE id = ?
                ''', (item['quantity'], item['unit_cost'], item['item_id']))
            
            db.commit()
            flash('تم إنشاء أمر الشراء بنجاح', 'success')
            return redirect(url_for('purchases.view', purchase_id=purchase_id))
        except Exception as e:
            flash(f'خطأ في إنشاء أمر الشراء: {str(e)}', 'danger')
    
    db = get_db()
    items = db.execute('SELECT * FROM items ORDER BY name').fetchall()
    return render_template('purchases/new.html', items=items)

@bp.route('/purchases/<int:purchase_id>')
@login_required()
def view(purchase_id):
    """عرض تفاصيل الشراء"""
    db = get_db()
    purchase = db.execute('''
        SELECT p.*, u.username as created_by_name
        FROM purchases p
        LEFT JOIN users u ON u.id = p.created_by
        WHERE p.id = ?
    ''', (purchase_id,)).fetchone()
    
    if not purchase:
        flash('أمر الشراء غير موجود', 'danger')
        return redirect(url_for('purchases.list'))
    
    items = db.execute('''
        SELECT pi.*, i.name as item_name
        FROM purchase_items pi
        JOIN items i ON i.id = pi.item_id
        WHERE pi.purchase_id = ?
    ''', (purchase_id,)).fetchall()
    
    # الحصول على اسم طريقة الدفع
    payment_method_name = get_payment_method_display_name(purchase['payment_method'])
    
    return render_template('purchases/view.html', 
                         purchase=purchase, 
                         items=items, 
                         payment_method_name=payment_method_name)
