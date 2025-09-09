# -*- coding: utf-8 -*-
"""
أدوات المصادقة والصلاحيات
"""

from functools import wraps
from flask import request, redirect, url_for, flash, session

def login_required(role=None):
    """مطلوب تسجيل الدخول مع اختياري للدور"""
    def decorator(f):
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
    return decorator
