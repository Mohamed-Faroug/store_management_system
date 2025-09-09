#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام إدارة المخزون - ملف التشغيل الرئيسي
تم تطوير هذا النظام بواسطة: محمد فاروق
تاريخ آخر تحديث: 9/9/2025
جميع الحقوق محفوظة © 2025
"""

import os
import sys
import webbrowser
import threading
import time
from pathlib import Path

# إضافة مسار التطبيق
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

def check_dependencies():
    """فحص المتطلبات الأساسية"""
    try:
        import flask
        import werkzeug
        import sqlite3
        print("✅ جميع المتطلبات متوفرة")
        return True
    except ImportError as e:
        print(f"❌ مكتبة مفقودة: {e}")
        return False

def setup_environment():
    """إعداد البيئة"""
    try:
        # إنشاء مجلدات ضرورية
        os.makedirs('logs', exist_ok=True)
        os.makedirs('backups', exist_ok=True)
        os.makedirs('temp', exist_ok=True)
        
        # تعيين متغيرات البيئة
        os.environ['FLASK_ENV'] = 'production'
        os.environ['FLASK_DEBUG'] = 'False'
        
        print("✅ تم إعداد البيئة بنجاح")
        return True
    except Exception as e:
        print(f"❌ خطأ في إعداد البيئة: {e}")
        return False

def start_server():
    """تشغيل الخادم"""
    try:
        from app import create_app
        
        app = create_app()
        
        # إعداد مسار القوالب للـ EXE
        import sys
        if getattr(sys, 'frozen', False):
            # إذا كان التطبيق يعمل كـ EXE
            template_dir = os.path.join(os.path.dirname(sys.executable), 'app', 'templates')
            static_dir = os.path.join(os.path.dirname(sys.executable), 'app', 'static')
            
            if os.path.exists(template_dir):
                app.template_folder = template_dir
            if os.path.exists(static_dir):
                app.static_folder = static_dir
        
        # تشغيل الخادم
        print("🚀 بدء تشغيل نظام إدارة المخزون...")
        print("📱 سيتم فتح المتصفح تلقائياً...")
        
        # فتح المتصفح بعد ثانيتين
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://127.0.0.1:8080')
        
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        # تشغيل التطبيق
        app.run(
            host='127.0.0.1',
            port=8080,
            debug=False,
            use_reloader=False,
            threaded=True
        )
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل الخادم: {e}")
        import traceback
        traceback.print_exc()
        input("اضغط Enter للخروج...")

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("🏪 نظام إدارة المخزون - مخزن الزينة")
    print("👨‍💻 تم تطوير هذا النظام بواسطة: محمد فاروق")
    print("📅 تاريخ آخر تحديث: 9/9/2025")
    print("© جميع الحقوق محفوظة 2025")
    print("=" * 50)
    
    # فحص المتطلبات
    if not check_dependencies():
        print("\n❌ يرجى تثبيت المتطلبات أولاً:")
        print("pip install -r requirements.txt")
        input("اضغط Enter للخروج...")
        return
    
    # إعداد البيئة
    if not setup_environment():
        input("اضغط Enter للخروج...")
        return
    
    # تشغيل الخادم
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n👋 تم إغلاق التطبيق بواسطة المستخدم")
    except Exception as e:
        print(f"\n❌ خطأ غير متوقع: {e}")
        input("اضغط Enter للخروج...")

if __name__ == "__main__":
    main()
