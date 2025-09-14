# -*- coding: utf-8 -*-
"""
أدوات المصادقة والصلاحيات
"""

from functools import wraps
from flask import request, redirect, url_for, flash, session
from ..models.database import get_db

def check_user_permissions(username, required_role):
    """التحقق من صلاحيات المستخدم من قاعدة البيانات"""
    try:
        db = get_db()
        user = db.execute('SELECT role, permissions FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            # Check if user has the required role or has "all_permissions"
            return user['role'] == required_role or user['permissions'] == 'all_permissions'
        return False
    except:
        return False

def check_user_status(username):
    """التحقق من حالة المستخدم (hidden/visible)"""
    try:
        db = get_db()
        user = db.execute('SELECT status FROM users WHERE username = ?', (username,)).fetchone()
        if user:
            return user['status']
        return 'visible'
    except:
        return 'visible'

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
    """مطلوب دور المطور للوصول"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('الرجاء تسجيل الدخول', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        
        # التحقق من اسم المستخدم أو الدور
        username = session.get('username')
        role = session.get('role')
        
        # التحقق من أن المستخدم هو dev أو له دور dev أو all_permissions
        if (username == 'dev' or role == 'dev' or 
            check_user_permissions(username, 'dev') or 
            check_user_permissions(username, 'all_permissions')):
            return f(*args, **kwargs)
        else:
            flash('لا تملك صلاحية الوصول. هذه الصفحة متاحة للمطور فقط.', 'danger')
            return redirect(url_for('main.index'))
    return wrapper

def owner_user_required(f):
    """مطلوب دور المالك للوصول"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('الرجاء تسجيل الدخول', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        
        # التحقق من اسم المستخدم أو الدور
        username = session.get('username')
        role = session.get('role')
        
        # التحقق من أن المستخدم هو owner أو له دور owner أو all_permissions
        if (username == 'owner' or role == 'owner' or 
            check_user_permissions(username, 'owner') or 
            check_user_permissions(username, 'all_permissions')):
            return f(*args, **kwargs)
        else:
            flash('لا تملك صلاحية الوصول. هذه الصفحة متاحة للمالك فقط.', 'danger')
            return redirect(url_for('main.index'))
    return wrapper

def dev_or_owner_required(f):
    """مطلوب دور المطور أو المالك للوصول"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('الرجاء تسجيل الدخول', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        
        # التحقق من اسم المستخدم أو الدور
        username = session.get('username')
        role = session.get('role')
        
        # التحقق من أن المستخدم هو dev أو owner أو له دور dev أو owner أو all_permissions
        if (username in ['dev', 'owner'] or role in ['dev', 'owner'] or 
            check_user_permissions(username, 'dev') or 
            check_user_permissions(username, 'owner') or 
            check_user_permissions(username, 'all_permissions')):
            return f(*args, **kwargs)
        else:
            flash('لا تملك صلاحية الوصول. هذه الصفحة متاحة للمطور والمالك فقط.', 'danger')
            return redirect(url_for('main.index'))
    return wrapper