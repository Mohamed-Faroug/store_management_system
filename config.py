#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
إعدادات التطبيق - نظام إدارة المخزون
ملف الإعدادات للإنتاج والتطوير
"""

import os
from datetime import timedelta

class Config:
    """إعدادات التطبيق الأساسية"""
    
    # إعدادات الأمان
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # إعدادات قاعدة البيانات
    DATABASE = os.environ.get('DATABASE_URL') or 'inventory.db'
    
    # إعدادات التطبيق
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    TESTING = False
    
    # إعدادات الجلسة
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = False  # True للإنتاج مع HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # إعدادات الملفات
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    
    # إعدادات التقارير
    REPORTS_PER_PAGE = 50
    
    # إعدادات النظام
    APP_NAME = 'نظام إدارة المخزون - مخزن الزينة'
    STORE_NAME = 'مخزن الزينة'
    VERSION = '1.0.0'
    
    # معلومات التواصل
    SUPPORT_EMAIL = 'mfh1134@gmail.com'
    DEVELOPER_NAME = 'inkplus اينك بلس'
    DEVELOPER_EMAIL = 'mfh1134@gmail.com'
    
    # إعدادات URL
    BASE_URL = 'http://localhost'
    LOCAL_URL = 'http://localhost'
    BASE_URL_WITH_PORT = 'http://localhost:5000'
    LOCAL_URL_WITH_PORT = 'http://localhost:5000'
    
    @staticmethod
    def init_app(app):
        """تهيئة التطبيق"""
        pass

class DevelopmentConfig(Config):
    """إعدادات التطوير"""
    DEBUG = True
    SECRET_KEY = 'dev-secret-key'
    
class ProductionConfig(Config):
    """إعدادات الإنتاج"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_COOKIE_SECURE = True
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # إعدادات الأمان للإنتاج
        import logging
        from logging.handlers import RotatingFileHandler
        
        if not app.debug and not app.testing:
            # إعداد تسجيل الأخطاء
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                'logs/inventory.log', 
                maxBytes=10240, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.setLevel(logging.INFO)
            app.logger.info('نظام إدارة المخزون - بدء التشغيل')

class TestingConfig(Config):
    """إعدادات الاختبار"""
    TESTING = True
    DATABASE = ':memory:'
    SECRET_KEY = 'test-secret-key'

# إعدادات البيئة
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
