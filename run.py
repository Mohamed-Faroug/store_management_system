# -*- coding: utf-8 -*-
"""
ملف تشغيل التطبيق
"""

from main import app

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)
