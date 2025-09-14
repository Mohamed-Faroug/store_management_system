# -*- coding: utf-8 -*-
"""
إدارة المستخدمين
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from ..models.database import get_db
from ..utils.auth import login_required, dev_or_owner_required

bp = Blueprint('users', __name__)

@bp.route('/users')
@login_required('manager')
def list():
    """قائمة المستخدمين"""
    db = get_db()
    users = db.execute('SELECT * FROM users WHERE username NOT IN (?, ?) ORDER BY created_at DESC', ('dev', 'owner')).fetchall()
    return render_template('users/list.html', users=users)

@bp.route('/users/new', methods=['GET', 'POST'])
@login_required('manager')
def new():
    """إضافة مستخدم جديد"""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'clerk')
        
        if not username or not password:
            flash('اسم المستخدم وكلمة المرور مطلوبان', 'danger')
            return redirect(url_for('users.new'))
        
        if len(password) < 6:
            flash('كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'danger')
            return redirect(url_for('users.new'))
        
        db = get_db()
        try:
            db.execute('''
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
            ''', (username, generate_password_hash(password), role))
            db.commit()
            flash('تم إضافة المستخدم بنجاح', 'success')
            return redirect(url_for('users.list'))
        except Exception as e:
            flash(f'خطأ في إضافة المستخدم: {str(e)}', 'danger')
    
    return render_template('users/new.html')

@bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required('manager')
def edit(user_id):
    """تعديل مستخدم"""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        flash('المستخدم غير موجود', 'danger')
        return redirect(url_for('users.list'))
    
    if user['username'] in ['dev', 'owner']:
        flash('لا يمكن تعديل مستخدمي dev و owner', 'danger')
        return redirect(url_for('users.list'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        role = request.form.get('role', 'clerk')
        
        if not username:
            flash('اسم المستخدم مطلوب', 'danger')
            return redirect(url_for('users.edit', user_id=user_id))
        
        try:
            if password:
                if len(password) < 6:
                    flash('كلمة المرور يجب أن تكون 6 أحرف على الأقل', 'danger')
                    return redirect(url_for('users.edit', user_id=user_id))
                db.execute('''
                    UPDATE users 
                    SET username=?, password_hash=?, role=?
                    WHERE id=?
                ''', (username, generate_password_hash(password), role, user_id))
            else:
                db.execute('''
                    UPDATE users 
                    SET username=?, role=?
                    WHERE id=?
                ''', (username, role, user_id))
            
            db.commit()
            flash('تم تحديث المستخدم بنجاح', 'success')
            return redirect(url_for('users.list'))
        except Exception as e:
            flash(f'خطأ في تحديث المستخدم: {str(e)}', 'danger')
    
    return render_template('users/edit.html', user=user)

@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required('manager')
def delete(user_id):
    """حذف مستخدم"""
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        flash('المستخدم غير موجود', 'danger')
        return redirect(url_for('users.list'))
    
    if user['username'] == 'admin':
        flash('لا يمكن حذف المستخدم الرئيسي', 'danger')
        return redirect(url_for('users.list'))
    
    if user['username'] in ['dev', 'owner']:
        flash('لا يمكن حذف مستخدمي dev و owner', 'danger')
        return redirect(url_for('users.list'))
    
    try:
        db.execute('DELETE FROM users WHERE id = ?', (user_id,))
        db.commit()
        flash('تم حذف المستخدم بنجاح', 'success')
    except Exception as e:
        flash(f'خطأ في حذف المستخدم: {str(e)}', 'danger')
    
    return redirect(url_for('users.list'))
