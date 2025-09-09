#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تشخيص مسارات الملفات في EXE
"""

import os
import sys
from pathlib import Path

def check_exe_paths():
    """فحص مسارات الملفات في EXE"""
    print("🔍 فحص مسارات الملفات...")
    
    # فحص إذا كان التطبيق يعمل كـ EXE
    is_frozen = getattr(sys, 'frozen', False)
    print(f"📦 التطبيق يعمل كـ EXE: {is_frozen}")
    
    if is_frozen:
        # مسار EXE
        exe_path = sys.executable
        exe_dir = os.path.dirname(exe_path)
        print(f"📁 مجلد EXE: {exe_dir}")
        
        # مسارات القوالب والملفات الثابتة
        template_dir = os.path.join(exe_dir, 'app', 'templates')
        static_dir = os.path.join(exe_dir, 'app', 'static')
        db_path = os.path.join(exe_dir, 'inventory.db')
        
        print(f"📁 مجلد القوالب: {template_dir}")
        print(f"📁 مجلد الملفات الثابتة: {static_dir}")
        print(f"📁 قاعدة البيانات: {db_path}")
        
        # فحص وجود الملفات
        print("\n🔍 فحص وجود الملفات:")
        
        if os.path.exists(template_dir):
            print(f"✅ مجلد القوالب موجود")
            dashboard_file = os.path.join(template_dir, 'dashboard.html')
            if os.path.exists(dashboard_file):
                print(f"✅ dashboard.html موجود")
            else:
                print(f"❌ dashboard.html مفقود")
        else:
            print(f"❌ مجلد القوالب مفقود")
        
        if os.path.exists(static_dir):
            print(f"✅ مجلد الملفات الثابتة موجود")
        else:
            print(f"❌ مجلد الملفات الثابتة مفقود")
        
        if os.path.exists(db_path):
            print(f"✅ قاعدة البيانات موجودة")
        else:
            print(f"❌ قاعدة البيانات مفقودة")
        
        # فحص محتويات مجلد القوالب
        if os.path.exists(template_dir):
            print(f"\n📋 محتويات مجلد القوالب:")
            try:
                for file in os.listdir(template_dir):
                    file_path = os.path.join(template_dir, file)
                    if os.path.isfile(file_path):
                        print(f"  📄 {file}")
                    elif os.path.isdir(file_path):
                        print(f"  📁 {file}/")
            except Exception as e:
                print(f"❌ خطأ في قراءة مجلد القوالب: {e}")
    
    else:
        # مسار Python العادي
        current_dir = Path(__file__).parent.absolute()
        print(f"📁 المجلد الحالي: {current_dir}")
        
        template_dir = current_dir / 'app' / 'templates'
        static_dir = current_dir / 'app' / 'static'
        db_path = current_dir / 'inventory.db'
        
        print(f"📁 مجلد القوالب: {template_dir}")
        print(f"📁 مجلد الملفات الثابتة: {static_dir}")
        print(f"📁 قاعدة البيانات: {db_path}")
        
        # فحص وجود الملفات
        print("\n🔍 فحص وجود الملفات:")
        
        if template_dir.exists():
            print(f"✅ مجلد القوالب موجود")
            dashboard_file = template_dir / 'dashboard.html'
            if dashboard_file.exists():
                print(f"✅ dashboard.html موجود")
            else:
                print(f"❌ dashboard.html مفقود")
        else:
            print(f"❌ مجلد القوالب مفقود")
        
        if static_dir.exists():
            print(f"✅ مجلد الملفات الثابتة موجود")
        else:
            print(f"❌ مجلد الملفات الثابتة مفقود")
        
        if db_path.exists():
            print(f"✅ قاعدة البيانات موجودة")
        else:
            print(f"❌ قاعدة البيانات مفقودة")

def test_flask_app():
    """اختبار تطبيق Flask"""
    print("\n🔍 اختبار تطبيق Flask...")
    
    try:
        from app import create_app
        
        app = create_app()
        print("✅ تم إنشاء التطبيق بنجاح")
        
        # فحص مسارات القوالب
        print(f"📁 مسار القوالب: {app.template_folder}")
        print(f"📁 مسار الملفات الثابتة: {app.static_folder}")
        
        # اختبار العثور على القالب
        try:
            with app.app_context():
                from flask import render_template_string
                template = app.jinja_env.get_template('dashboard.html')
                print("✅ تم العثور على قالب dashboard.html")
        except Exception as e:
            print(f"❌ خطأ في العثور على القالب: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في إنشاء التطبيق: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """الدالة الرئيسية"""
    print("=" * 60)
    print("🔧 تشخيص مسارات الملفات في EXE")
    print("=" * 60)
    
    # فحص مسارات الملفات
    check_exe_paths()
    
    # اختبار تطبيق Flask
    test_flask_app()
    
    print("\n" + "=" * 60)
    print("✅ انتهى التشخيص")
    print("=" * 60)
    
    input("\nاضغط Enter للخروج...")

if __name__ == "__main__":
    main()
