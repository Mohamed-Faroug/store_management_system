#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
اختبار سريع للتطبيق
"""

import os
import sys

def test_templates():
    """اختبار القوالب"""
    print("🔍 اختبار القوالب...")
    
    # فحص وجود ملف dashboard.html
    template_path = os.path.join('app', 'templates', 'dashboard.html')
    if os.path.exists(template_path):
        print("✅ dashboard.html موجود")
        return True
    else:
        print("❌ dashboard.html مفقود")
        return False

def test_app():
    """اختبار التطبيق"""
    print("🔍 اختبار التطبيق...")
    
    try:
        from app import create_app
        app = create_app()
        print("✅ تم إنشاء التطبيق بنجاح")
        
        # اختبار العثور على القالب
        with app.app_context():
            from flask import render_template
            try:
                # محاولة عرض القالب
                return render_template('dashboard.html', data={})
            except Exception as e:
                print(f"❌ خطأ في عرض القالب: {e}")
                return False
                
    except Exception as e:
        print(f"❌ خطأ في إنشاء التطبيق: {e}")
        return False

def main():
    """الدالة الرئيسية"""
    print("=" * 40)
    print("🔧 اختبار سريع")
    print("=" * 40)
    
    # اختبار القوالب
    if test_templates():
        # اختبار التطبيق
        if test_app():
            print("\n✅ جميع الاختبارات نجحت!")
        else:
            print("\n❌ فشل في اختبار التطبيق")
    else:
        print("\n❌ فشل في اختبار القوالب")

if __name__ == "__main__":
    main()
