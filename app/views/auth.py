# -*- coding: utf-8 -*-
"""
صفحات المصادقة
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash
from ..models.database import get_db

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """صفحة تسجيل الدخول"""
    if request.method == 'POST':
        username = request.form.get('username','').strip()
        password = request.form.get('password','')
        db = get_db()
        user = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            flash('تم تسجيل الدخول بنجاح.', 'success')
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('بيانات الدخول غير صحيحة.', 'danger')
    
    return render_template('login.html')

@bp.route('/logout')
def logout():
    """تسجيل الخروج"""
    session.clear()
    flash('تم تسجيل الخروج.', 'info')
    return redirect(url_for('auth.login'))
