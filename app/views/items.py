# -*- coding: utf-8 -*-
"""
إدارة الأصناف
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from ..models.database import get_db
from ..utils.auth import login_required

bp = Blueprint('items', __name__)

@bp.route('/items')
@login_required()
def list():
    """قائمة الأصناف - للمدير فقط"""
    if session.get('role') != 'manager':
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('main.index'))
    db = get_db()
    search = request.args.get('search', '').strip()
    category_id = request.args.get('category', '')
    
    query = '''
        SELECT i.*, c.name as category_name 
        FROM items i 
        LEFT JOIN categories c ON c.id = i.category_id
        WHERE 1=1
    '''
    params = []
    
    if search:
        query += ' AND (i.name LIKE ? OR i.sku LIKE ?)'
        params.extend([f'%{search}%', f'%{search}%'])
    
    if category_id:
        query += ' AND i.category_id = ?'
        params.append(category_id)
    
    query += ' ORDER BY i.name'
    
    items = db.execute(query, params).fetchall()
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    
    return render_template('items/list.html', items=items, categories=categories, 
                         search=search, selected_category=category_id)

@bp.route('/items/new', methods=['GET', 'POST'])
@login_required()
def new():
    """إضافة صنف جديد - للمدير فقط"""
    if session.get('role') != 'manager':
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category_id = request.form.get('category_id', '')
        sku = request.form.get('sku', '').strip()
        description = request.form.get('description', '').strip()
        quantity = int(request.form.get('quantity', 0))
        reorder_level = int(request.form.get('reorder_level', 5))
        cost_price = float(request.form.get('cost_price', 0))
        selling_price = float(request.form.get('selling_price', 0))
        
        if not name:
            flash('اسم الصنف مطلوب', 'danger')
            return redirect(url_for('items.new'))
        
        db = get_db()
        try:
            db.execute('''
                INSERT INTO items (name, category_id, sku, description, quantity, reorder_level, cost_price, selling_price)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, category_id or None, sku or None, description, quantity, reorder_level, cost_price, selling_price))
            db.commit()
            flash('تم إضافة الصنف بنجاح', 'success')
            return redirect(url_for('items.list'))
        except Exception as e:
            flash(f'خطأ في إضافة الصنف: {str(e)}', 'danger')
    
    db = get_db()
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    return render_template('items/new.html', categories=categories)

@bp.route('/items/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required()
def edit(item_id):
    """تعديل صنف - للمدير فقط"""
    if session.get('role') != 'manager':
        flash('ليس لديك صلاحية للوصول إلى هذه الصفحة', 'danger')
        return redirect(url_for('main.index'))
    db = get_db()
    item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    
    if not item:
        flash('الصنف غير موجود', 'danger')
        return redirect(url_for('items.list'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        category_id = request.form.get('category_id', '')
        sku = request.form.get('sku', '').strip()
        description = request.form.get('description', '').strip()
        quantity = int(request.form.get('quantity', 0))
        reorder_level = int(request.form.get('reorder_level', 5))
        cost_price = float(request.form.get('cost_price', 0))
        selling_price = float(request.form.get('selling_price', 0))
        
        if not name:
            flash('اسم الصنف مطلوب', 'danger')
            return redirect(url_for('items.edit', item_id=item_id))
        
        try:
            db.execute('''
                UPDATE items 
                SET name=?, category_id=?, sku=?, description=?, quantity=?, reorder_level=?, cost_price=?, selling_price=?
                WHERE id=?
            ''', (name, category_id or None, sku or None, description, quantity, reorder_level, cost_price, selling_price, item_id))
            db.commit()
            flash('تم تحديث الصنف بنجاح', 'success')
            return redirect(url_for('items.list'))
        except Exception as e:
            flash(f'خطأ في تحديث الصنف: {str(e)}', 'danger')
    
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    return render_template('items/edit.html', item=item, categories=categories)

@bp.route('/items/<int:item_id>/delete', methods=['POST'])
@login_required('manager')
def delete(item_id):
    """حذف صنف"""
    db = get_db()
    item = db.execute('SELECT * FROM items WHERE id = ?', (item_id,)).fetchone()
    
    if not item:
        flash('الصنف غير موجود', 'danger')
        return redirect(url_for('items.list'))
    
    try:
        db.execute('DELETE FROM items WHERE id = ?', (item_id,))
        db.commit()
        flash('تم حذف الصنف بنجاح', 'success')
    except Exception as e:
        flash(f'خطأ في حذف الصنف: {str(e)}', 'danger')
    
    return redirect(url_for('items.list'))
