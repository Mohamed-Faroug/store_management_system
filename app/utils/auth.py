# -*- coding: utf-8 -*-
"""
أدوات المصادقة والصلاحيات
"""

from functools import wraps
from flask import request, redirect, url_for, flash, session

def login_required(role=None):
    """مطلوب تسجيل الدخول مع اختياري للدور"""
    def auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                flash('الرجاء تسجيل الدخول', 'warning')
                return redirect(url_for('auth.login', next=request.path))
            if role:
                if session.get('role') != role:
                    flash('لا تملك صلاحية الوصول.', 'danger')
                    return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return wrapper
    return auth_decorator

def manager_required(f):
    """مطلوب دور مدير للوصول"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('الرجاء تسجيل الدخول', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        if session.get('role') != 'manager':
            flash('لا تملك صلاحية الوصول. مطلوب دور مدير.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return wrapper

def dev_user_required(f):
    """مطلوب دور dev للوصول"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('الرجاء تسجيل الدخول', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        
        # التحقق من اسم المستخدم أو الدور
        username = session.get('username')
        role = session.get('role')
        
        if username != 'dev' and role != 'dev':
            flash('لا تملك صلاحية الوصول. هذه الصفحة متاحة لمستخدم dev فقط.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return wrapper