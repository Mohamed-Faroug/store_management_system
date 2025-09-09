# -*- coding: utf-8 -*-
"""
نظام إدارة المخزون - مخزن الزينة
تطبيق Flask لإدارة المخزون والمبيعات

جميع الحقوق محفوظة © 2025
تم تطوير هذا النظام بواسطة: محمد فاروق
تاريخ آخر تحديث: 9/9/2025
"""

from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), '..', 'inventory.db')
    
    # إعداد مسارات القوالب والملفات الثابتة للـ EXE
    import sys
    if getattr(sys, 'frozen', False):
        # إذا كان التطبيق يعمل كـ EXE
        base_path = os.path.dirname(sys.executable)
        template_path = os.path.join(base_path, 'app', 'templates')
        static_path = os.path.join(base_path, 'app', 'static')
        
        if os.path.exists(template_path):
            app.template_folder = template_path
        if os.path.exists(static_path):
            app.static_folder = static_path
    
    # Register blueprints
    from .views import main, auth, items, sales, purchases, reports, users, categories, invoices, stock
    
    # Register blueprints with URL prefixes
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
    
    return app
