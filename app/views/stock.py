# -*- coding: utf-8 -*-
"""
إدارة المخزون
نظام إدارة المخزون - مخزن الزينة

جميع الحقوق محفوظة © 2025
تم تطوير هذا النظام بواسطة: محمد فاروق
تاريخ آخر تحديث: 9/9/2025
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.database import get_db
from ..utils.auth import login_required

bp = Blueprint('stock', __name__)

@bp.route('/stock/alerts')
@login_required()
def alerts():
    """تنبيهات المخزون المنخفض"""
    db = get_db()
    
    # الأصناف المنخفضة
    low_stock_items = db.execute('''
        SELECT i.*, c.name as category_name
        FROM items i
        LEFT JOIN categories c ON c.id = i.category_id
        WHERE i.quantity <= i.reorder_level
        ORDER BY i.quantity ASC
    ''').fetchall()
    
    # الأصناف النافدة
    out_of_stock_items = db.execute('''
        SELECT i.*, c.name as category_name
        FROM items i
        LEFT JOIN categories c ON c.id = i.category_id
        WHERE i.quantity = 0
        ORDER BY i.name ASC
    ''').fetchall()
    
    return render_template('stock/alerts.html', 
                         low_stock_items=low_stock_items,
                         out_of_stock_items=out_of_stock_items)

@bp.route('/stock/adjust')
@login_required()
def adjust():
    """تعديل المخزون"""
    db = get_db()
    items = db.execute('''
        SELECT i.*, c.name as category_name
        FROM items i
        LEFT JOIN categories c ON c.id = i.category_id
        ORDER BY i.name ASC
    ''').fetchall()
    
    return render_template('stock/adjust.html', items=items)

@bp.route('/stock/adjust', methods=['POST'])
@login_required()
def adjust_post():
    """تعديل المخزون - معالجة النموذج"""
    item_id = request.form.get('item_id')
    adjustment_type = request.form.get('adjustment_type')
    quantity = int(request.form.get('quantity', 0))
    reason = request.form.get('reason', '').strip()
    
    if not item_id or not adjustment_type or quantity <= 0:
        flash('يرجى ملء جميع الحقول بشكل صحيح', 'danger')
        return redirect(url_for('stock.adjust'))
    
    db = get_db()
    item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    
    if not item:
        flash('الصنف غير موجود', 'danger')
        return redirect(url_for('stock.adjust'))
    
    try:
        if adjustment_type == 'add':
            new_quantity = item['quantity'] + quantity
            db.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_quantity, item_id))
            flash(f'تم إضافة {quantity} قطعة إلى {item["name"]}. الكمية الجديدة: {new_quantity}', 'success')
        elif adjustment_type == 'subtract':
            if item['quantity'] < quantity:
                flash(f'الكمية المتاحة ({item["quantity"]}) أقل من الكمية المطلوب خصمها ({quantity})', 'danger')
                return redirect(url_for('stock.adjust'))
            new_quantity = item['quantity'] - quantity
            db.execute('UPDATE items SET quantity = ? WHERE id = ?', (new_quantity, item_id))
            flash(f'تم خصم {quantity} قطعة من {item["name"]}. الكمية الجديدة: {new_quantity}', 'success')
        elif adjustment_type == 'set':
            db.execute('UPDATE items SET quantity = ? WHERE id = ?', (quantity, item_id))
            flash(f'تم تعيين كمية {item["name"]} إلى {quantity}', 'success')
        
        db.commit()
        return redirect(url_for('stock.adjust'))
        
    except Exception as e:
        flash(f'خطأ في تعديل المخزون: {str(e)}', 'danger')
        return redirect(url_for('stock.adjust'))