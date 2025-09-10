# -*- coding: utf-8 -*-
"""
نظام إدارة المخزون - مخزن الزينة
تطبيق Flask لإدارة المخزون والمبيعات

المطور: محمد فاروق
التاريخ: 10/9/2025
"""

from flask import Flask
import os
import sys

def create_app():
    """إنشاء تطبيق Flask"""
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
    # إعداد مسارات الملفات
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
        app.config['DATABASE'] = os.path.join(base_path, 'inventory.db')
    else:
        app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), '..', 'inventory.db')
    
    # تهيئة قاعدة البيانات
    from .models.database import init_db, close_db
    with app.app_context():
        try:
            init_db()
        except Exception as e:
            print(f"Database warning: {e}")
    app.teardown_appcontext(close_db)
    
    # تسجيل المعالجات
    from .utils.context_processors import inject_store_settings
    app.context_processor(inject_store_settings)
    
    # تسجيل Blueprints
    from .views import (
        main, auth, items, sales, purchases, reports, 
        users, categories, invoices, stock, settings, 
        advanced_settings, data_management, api
    )
    
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(items.bp, url_prefix='/items')
    app.register_blueprint(sales.bp, url_prefix='/sales')
    app.register_blueprint(purchases.bp, url_prefix='/purchases')
    app.register_blueprint(reports.bp, url_prefix='/reports')
    app.register_blueprint(users.bp, url_prefix='/users')
    app.register_blueprint(categories.bp, url_prefix='/categories')
    app.register_blueprint(invoices.bp, url_prefix='/invoices')
    app.register_blueprint(stock.bp, url_prefix='/stock')
    app.register_blueprint(settings.settings_bp)
    app.register_blueprint(advanced_settings.advanced_settings_bp)
    app.register_blueprint(data_management.data_management_bp)
    app.register_blueprint(api.api_bp)
    
    return app
