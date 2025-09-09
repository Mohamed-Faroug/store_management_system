#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
إصلاح مشكلة EXE
"""

import os
import sys
import shutil
from pathlib import Path

def copy_templates_to_exe():
    """نسخ القوالب إلى مجلد EXE"""
    print("🔧 نسخ القوالب إلى مجلد EXE...")
    
    # مجلد EXE
    exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
    exe_dir = Path(exe_dir)
    
    # مجلدات المصدر
    source_templates = Path('app/templates')
    source_static = Path('app/static')
    
    # مجلدات الوجهة
    dest_templates = exe_dir / 'app' / 'templates'
    dest_static = exe_dir / 'app' / 'static'
    
    print(f"📁 مجلد EXE: {exe_dir}")
    print(f"📁 مجلد القوالب المصدر: {source_templates}")
    print(f"📁 مجلد القوالب الوجهة: {dest_templates}")
    
    try:
        # إنشاء المجلدات
        dest_templates.mkdir(parents=True, exist_ok=True)
        dest_static.mkdir(parents=True, exist_ok=True)
        
        # نسخ القوالب
        if source_templates.exists():
            shutil.copytree(source_templates, dest_templates, dirs_exist_ok=True)
            print("✅ تم نسخ القوالب بنجاح")
        else:
            print("❌ مجلد القوالب المصدر غير موجود")
        
        # نسخ الملفات الثابتة
        if source_static.exists():
            shutil.copytree(source_static, dest_static, dirs_exist_ok=True)
            print("✅ تم نسخ الملفات الثابتة بنجاح")
        else:
            print("❌ مجلد الملفات الثابتة المصدر غير موجود")
        
        # نسخ قاعدة البيانات
        db_source = Path('inventory.db')
        db_dest = exe_dir / 'inventory.db'
        
        if db_source.exists():
            shutil.copy2(db_source, db_dest)
            print("✅ تم نسخ قاعدة البيانات بنجاح")
        else:
            print("❌ قاعدة البيانات المصدر غير موجودة")
        
        return True
        
    except Exception as e:
        print(f"❌ خطأ في النسخ: {e}")
        return False

def test_exe_paths():
    """اختبار مسارات EXE"""
    print("\n🔍 اختبار مسارات EXE...")
    
    exe_dir = os.path.dirname(sys.executable) if getattr(sys, 'frozen', False) else os.getcwd()
    exe_dir = Path(exe_dir)
    
    # فحص الملفات المطلوبة
    required_files = [
        'app/templates/dashboard.html',
        'app/templates/base.html',
        'app/static/css/style.css',
        'inventory.db'
    ]
    
    for file_path in required_files:
        full_path = exe_dir / file_path
        if full_path.exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - مفقود")
    
    return True

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("🔧 إصلاح مشكلة EXE")
    print("=" * 50)
    
    # نسخ الملفات
    if copy_templates_to_exe():
        # اختبار المسارات
        test_exe_paths()
        
        print("\n✅ تم إصلاح المشكلة!")
        print("🚀 يمكنك الآن تشغيل EXE")
    else:
        print("\n❌ فشل في إصلاح المشكلة")

if __name__ == "__main__":
    main()
