#!/bin/bash

# نظام إدارة المخزون والمبيعات
# Inventory Management System

echo "========================================"
echo "   نظام إدارة المخزون والمبيعات"
echo "========================================"
echo

# فحص Python
echo "🔍 فحص المتطلبات..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 غير مثبت أو غير موجود في PATH"
    echo "يرجى تثبيت Python 3.8 أو أحدث"
    exit 1
fi

echo "✅ Python متوفر"
echo

# فحص ملف المتطلبات
echo "📦 فحص المتطلبات..."
if [ ! -f "requirements.txt" ]; then
    echo "❌ ملف requirements.txt غير موجود"
    exit 1
fi

echo "✅ ملف المتطلبات موجود"
echo

# تثبيت المتطلبات
echo "🔧 تثبيت المتطلبات..."
pip3 install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "❌ فشل في تثبيت المتطلبات"
    exit 1
fi

echo "✅ تم تثبيت المتطلبات بنجاح"
echo

# فحص قاعدة البيانات
echo "🗄️ فحص قاعدة البيانات..."
if [ ! -f "inventory.db" ]; then
    echo "⚠️  قاعدة البيانات غير موجودة، سيتم إنشاؤها تلقائياً"
fi

echo "✅ قاعدة البيانات جاهزة"
echo

# تشغيل التطبيق
echo "🚀 تشغيل التطبيق..."
echo
echo "📱 المتصفح: http://127.0.0.1:5000"
echo "⏹️  لإيقاف التطبيق: Ctrl+C"
echo "========================================"
echo

python3 run.py

echo
echo "👋 تم إيقاف التطبيق"
