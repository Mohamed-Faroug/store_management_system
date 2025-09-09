# -*- coding: utf-8 -*-
"""
نظام إدارة المخزون - مخزن الزينة
التطبيق الرئيسي

جميع الحقوق محفوظة © 2025
تم تطوير هذا النظام بواسطة: محمد فاروق
تاريخ آخر تحديث: 9/9/2025
"""

import os
import sys
from app import create_app
from app.models.database import init_db
from config import config

def get_config():
    """اختيار الإعدادات حسب البيئة"""
    env = os.environ.get('FLASK_ENV', 'development')
    return config.get(env, config['default'])

app = create_app()

@app.teardown_appcontext
def close_db(exception=None):
    """إغلاق اتصال قاعدة البيانات"""
    from app.models.database import close_db
    close_db(exception)

def create_directories():
    """إنشاء المجلدات المطلوبة"""
    directories = ['logs', 'backups', 'temp', 'uploads', 'data']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

if __name__ == '__main__':
    # إنشاء المجلدات المطلوبة
    create_directories()
    
    # تهيئة قاعدة البيانات
    with app.app_context():
        init_db()
    
    # تشغيل التطبيق
    config_obj = get_config()
    
    if config_obj.DEBUG:
        print("🚀 تشغيل في وضع التطوير")
        app.run(debug=True, host='127.0.0.1', port=8080, use_reloader=False)
    else:
        print("🚀 تشغيل في وضع الإنتاج")
        from waitress import serve
        serve(app, host='0.0.0.0', port=8080)
