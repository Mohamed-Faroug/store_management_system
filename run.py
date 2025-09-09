#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
تشغيل التطبيق
"""

import os
import sys

# إضافة مسار التطبيق
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

if __name__ == '__main__':
    print("🚀 تشغيل التطبيق...")
    print("📱 المتصفح: http://127.0.0.1:5000")
    print("⏹️  لإيقاف التطبيق: Ctrl+C")
    print("-" * 50)
    
    app = create_app()
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=False
    )