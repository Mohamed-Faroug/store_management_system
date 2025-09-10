#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
نظام إدارة المخزون - مخزن الزينة
ملف التشغيل الرئيسي

المطور: inkplus اينك بلس
التاريخ: 10/9/2025
"""

import os
import sys
from datetime import datetime

def main():
    """تشغيل التطبيق"""
    print("=" * 50)
    print("🏪 نظام إدارة المخزون - مخزن الزينة")
    print("=" * 50)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🚀 جاري التشغيل...")
    print("📱 http://localhost")
    print("📱 http://localhost:5000")
    print("📱 http://127.0.0.1")
    print("📱 http://127.0.0.1:5000")
    print("⏹️  Ctrl+C للإيقاف")
    print("=" * 50)
    
    try:
        # إضافة مسار التطبيق
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        
        # استيراد وإنشاء التطبيق
        from app import create_app
        app = create_app()
        
        # تشغيل التطبيق على المنفذ 5000
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        
    except KeyboardInterrupt:
        print("\n⏹️  تم الإيقاف")
    except Exception as e:
        print(f"❌ خطأ: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()