# -*- coding: utf-8 -*-
"""
إدارة الفئات
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..models.database import get_db
from ..utils.auth import login_required

bp = Blueprint('categories', __name__)

@bp.route('/categories')
@login_required()
def list():
    """قائمة الفئات"""
    db = get_db()
    categories = db.execute('SELECT * FROM categories ORDER BY name').fetchall()
    return render_template('categories/list.html', categories=categories)

@bp.route('/categories/new', methods=['GET', 'POST'])
@login_required('manager')
def new():
    """إضافة فئة جديدة"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('اسم الفئة مطلوب', 'danger')
            return redirect(url_for('categories.new'))
        
        db = get_db()
        try:
            db.execute('INSERT INTO categories (name, description) VALUES (?, ?)', (name, description))
            db.commit()
            flash('تم إضافة الفئة بنجاح', 'success')
            return redirect(url_for('categories.list'))
        except Exception as e:
            flash(f'خطأ في إضافة الفئة: {str(e)}', 'danger')
    
    return render_template('categories/new.html')

@bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required('manager')
def edit(category_id):
    """تعديل فئة"""
    db = get_db()
    category = db.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
    
    if not category:
        flash('الفئة غير موجودة', 'danger')
        return redirect(url_for('categories.list'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('اسم الفئة مطلوب', 'danger')
            return redirect(url_for('categories.edit', category_id=category_id))
        
        try:
            db.execute('UPDATE categories SET name=?, description=? WHERE id=?', 
                      (name, description, category_id))
            db.commit()
            flash('تم تحديث الفئة بنجاح', 'success')
            return redirect(url_for('categories.list'))
        except Exception as e:
            flash(f'خطأ في تحديث الفئة: {str(e)}', 'danger')
    
    return render_template('categories/edit.html', category=category)

@bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required('manager')
def delete(category_id):
    """حذف فئة"""
    db = get_db()
    category = db.execute('SELECT * FROM categories WHERE id = ?', (category_id,)).fetchone()
    
    if not category:
        flash('الفئة غير موجودة', 'danger')
        return redirect(url_for('categories.list'))
    
    # Check if category has items
    items_count = db.execute('SELECT COUNT(*) as c FROM items WHERE category_id = ?', (category_id,)).fetchone()['c']
    if items_count > 0:
        flash(f'لا يمكن حذف الفئة لأنها تحتوي على {items_count} صنف', 'danger')
        return redirect(url_for('categories.list'))
    
    try:
        db.execute('DELETE FROM categories WHERE id = ?', (category_id,))
        db.commit()
        flash('تم حذف الفئة بنجاح', 'success')
    except Exception as e:
        flash(f'خطأ في حذف الفئة: {str(e)}', 'danger')
    
    return redirect(url_for('categories.list'))
