# -*- coding: utf-8 -*-
"""
إعدادات التطبيق للإنتاج
"""

import os
from pathlib import Path

class Config:
    """الإعدادات الأساسية"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DATABASE = os.path.join(os.path.dirname(__file__), 'inventory.db')
    
    # إعدادات قاعدة البيانات
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات الجلسة
    PERMANENT_SESSION_LIFETIME = 3600  # ساعة واحدة
    
    # إعدادات الأمان
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600
    
    # إعدادات التطبيق
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    UPLOAD_FOLDER = 'uploads'
    
    # إعدادات الطباعة
    PRINT_MARGIN = 20
    PRINT_FONT_SIZE = 12
    
    # إعدادات النسخ الاحتياطي
    BACKUP_FOLDER = 'backups'
    BACKUP_RETENTION_DAYS = 30

class DevelopmentConfig(Config):
    """إعدادات التطوير"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """إعدادات الإنتاج"""
    DEBUG = False
    TESTING = False
    
    # إعدادات الأمان للإنتاج
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'production-secret-key-change-this'
    
    # إعدادات قاعدة البيانات للإنتاج
    DATABASE = os.path.join(os.path.dirname(__file__), 'data', 'inventory.db')
    
    # إعدادات النسخ الاحتياطي للإنتاج
    BACKUP_FOLDER = os.path.join(os.path.dirname(__file__), 'backups')

class TestingConfig(Config):
    """إعدادات الاختبار"""
    DEBUG = True
    TESTING = True
    DATABASE = ':memory:'

# اختيار الإعدادات حسب البيئة
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
