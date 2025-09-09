# -*- coding: utf-8 -*-
"""
إعدادات التطبيق
Application Configuration
"""

import os
from datetime import timedelta

class Config:
    """الإعدادات الأساسية للتطبيق"""
    
    # إعدادات Flask الأساسية
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'inventory-system-secret-key-2024'
    DEBUG = False
    TESTING = False
    
    # إعدادات قاعدة البيانات
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'inventory.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات الجلسة
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # True في الإنتاج مع HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # إعدادات النسخ الاحتياطي
    BACKUP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backups')
    BACKUP_RETENTION_DAYS = 30
    BACKUP_COMPRESSION = True
    
    # إعدادات التطبيق
    APP_NAME = 'نظام إدارة المخزون والمبيعات'
    APP_VERSION = '2.0.0'
    CURRENCY_SYMBOL = 'ج.س'
    CURRENCY_NAME = 'جنيه سوداني'
    
    # إعدادات الطباعة
    PRINT_MARGIN = 10  # هامش الطباعة بالبكسل
    PRINT_FONT_SIZE = 12  # حجم الخط للطباعة
    
    # إعدادات الأمان
    PASSWORD_MIN_LENGTH = 6
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION = 300  # 5 دقائق بالثواني
    
    # إعدادات التقارير
    REPORTS_PER_PAGE = 20
    EXPORT_FORMATS = ['csv', 'excel', 'pdf']
    
    # إعدادات الأداء
    CACHE_TIMEOUT = 300  # 5 دقائق
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # إعدادات التطوير
    DEVELOPMENT = False
    LOG_LEVEL = 'INFO'
    
    @staticmethod
    def init_app(app):
        """تهيئة التطبيق مع الإعدادات"""
        pass

class DevelopmentConfig(Config):
    """إعدادات التطوير"""
    DEBUG = True
    DEVELOPMENT = True
    LOG_LEVEL = 'DEBUG'
    
    # إعدادات قاعدة البيانات للتطوير
    SQLALCHEMY_ECHO = False  # True لعرض استعلامات SQL
    
    # إعدادات الأمان للتطوير
    SESSION_COOKIE_SECURE = False
    WTF_CSRF_ENABLED = True

class ProductionConfig(Config):
    """إعدادات الإنتاج"""
    DEBUG = False
    DEVELOPMENT = False
    LOG_LEVEL = 'WARNING'
    
    # إعدادات الأمان للإنتاج
    SESSION_COOKIE_SECURE = True  # يتطلب HTTPS
    WTF_CSRF_ENABLED = True
    
    # إعدادات الأداء للإنتاج
    CACHE_TIMEOUT = 600  # 10 دقائق
    
    @classmethod
    def init_app(cls, app):
        """تهيئة التطبيق للإنتاج"""
        Config.init_app(app)
        
        # إعدادات السجلات
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                'logs/inventory_system.log',
                maxBytes=10240000,  # 10MB
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('نظام إدارة المخزون والمبيعات - بدء التشغيل')

class TestingConfig(Config):
    """إعدادات الاختبار"""
    TESTING = True
    DEBUG = True
    
    # قاعدة بيانات منفصلة للاختبار
    DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test_inventory.db')
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    
    # تعطيل CSRF للاختبار
    WTF_CSRF_ENABLED = False

# قاموس الإعدادات
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# إعدادات إضافية
DEFAULT_USER_ROLES = {
    'manager': {
        'name': 'مدير',
        'permissions': ['all']
    },
    'clerk': {
        'name': 'كاشير',
        'permissions': ['sales', 'invoices']
    }
}

# إعدادات الفئات الافتراضية
DEFAULT_CATEGORIES = [
    {'name': 'أغذية', 'description': 'منتجات غذائية'},
    {'name': 'مشروبات', 'description': 'مشروبات متنوعة'},
    {'name': 'منظفات', 'description': 'منتجات التنظيف'},
    {'name': 'أدوات', 'description': 'أدوات متنوعة'}
]

# إعدادات الطباعة
PRINT_TEMPLATES = {
    'invoice_a4': 'invoices/print_a4.html',
    'invoice_58mm': 'invoices/print_58mm.html',
    'receipt': 'invoices/print_58mm.html'
}

# إعدادات التصدير
EXPORT_SETTINGS = {
    'csv': {
        'encoding': 'utf-8',
        'delimiter': ','
    },
    'excel': {
        'sheet_name': 'البيانات',
        'encoding': 'utf-8'
    },
    'pdf': {
        'page_size': 'A4',
        'orientation': 'portrait'
    }
}


# الحصول على المسار الحالي للمجلد الذي يحتوي على التطبيق
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'inventory.db')

# إنشاء المجلدات إذا لم تكن موجودة
os.makedirs(BASE_DIR, exist_ok=True)