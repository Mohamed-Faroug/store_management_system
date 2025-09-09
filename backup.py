# -*- coding: utf-8 -*-
"""
نظام النسخ الاحتياطي التلقائي
نظام إدارة المخزون - مخزن الزينة

جميع الحقوق محفوظة © 2025
تم تطوير هذا النظام بواسطة: محمد فاروق
تاريخ آخر تحديث: 9/9/2025
"""

import os
import shutil
import schedule
import time
from datetime import datetime
import sqlite3

def create_backup_directory():
    """إنشاء مجلد النسخ الاحتياطية إذا لم يكن موجوداً"""
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"تم إنشاء مجلد النسخ الاحتياطية: {backup_dir}")
    return backup_dir

def backup_database():
    """إنشاء نسخة احتياطية من قاعدة البيانات"""
    try:
        # التحقق من وجود قاعدة البيانات
        if not os.path.exists("inventory.db"):
            print("تحذير: قاعدة البيانات غير موجودة!")
            return False
        
        # إنشاء مجلد النسخ الاحتياطية
        backup_dir = create_backup_directory()
        
        # إنشاء اسم الملف مع التاريخ والوقت
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"inventory_backup_{timestamp}.db"
        backup_path = os.path.join(backup_dir, backup_name)
        
        # نسخ قاعدة البيانات
        shutil.copy2("inventory.db", backup_path)
        
        # التحقق من صحة النسخة الاحتياطية
        if verify_backup(backup_path):
            print(f"✅ تم إنشاء نسخة احتياطية بنجاح: {backup_name}")
            
            # حذف النسخ القديمة (الاحتفاظ بآخر 10 نسخ)
            cleanup_old_backups(backup_dir)
            
            return True
        else:
            print(f"❌ فشل في إنشاء النسخة الاحتياطية: {backup_name}")
            return False
            
    except Exception as e:
        print(f"❌ خطأ في إنشاء النسخة الاحتياطية: {str(e)}")
        return False

def verify_backup(backup_path):
    """التحقق من صحة النسخة الاحتياطية"""
    try:
        conn = sqlite3.connect(backup_path)
        cursor = conn.cursor()
        
        # التحقق من وجود الجداول الأساسية
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        required_tables = ['users', 'categories', 'items', 'invoices', 'sales']
        existing_tables = [table[0] for table in tables]
        
        for table in required_tables:
            if table not in existing_tables:
                print(f"تحذير: الجدول {table} غير موجود في النسخة الاحتياطية")
                conn.close()
                return False
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"خطأ في التحقق من النسخة الاحتياطية: {str(e)}")
        return False

def cleanup_old_backups(backup_dir, keep_count=10):
    """حذف النسخ القديمة والاحتفاظ بآخر عدد محدد"""
    try:
        backup_files = []
        for file in os.listdir(backup_dir):
            if file.startswith("inventory_backup_") and file.endswith(".db"):
                file_path = os.path.join(backup_dir, file)
                file_time = os.path.getmtime(file_path)
                backup_files.append((file_path, file_time))
        
        # ترتيب الملفات حسب التاريخ (الأحدث أولاً)
        backup_files.sort(key=lambda x: x[1], reverse=True)
        
        # حذف الملفات الزائدة
        if len(backup_files) > keep_count:
            files_to_delete = backup_files[keep_count:]
            for file_path, _ in files_to_delete:
                os.remove(file_path)
                print(f"تم حذف النسخة القديمة: {os.path.basename(file_path)}")
                
    except Exception as e:
        print(f"خطأ في حذف النسخ القديمة: {str(e)}")

def restore_backup(backup_path):
    """استعادة نسخة احتياطية"""
    try:
        if not os.path.exists(backup_path):
            print(f"النسخة الاحتياطية غير موجودة: {backup_path}")
            return False
        
        # التحقق من صحة النسخة الاحتياطية
        if not verify_backup(backup_path):
            print("النسخة الاحتياطية تالفة!")
            return False
        
        # إنشاء نسخة احتياطية من الملف الحالي
        if os.path.exists("inventory.db"):
            current_backup = f"inventory_current_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
            shutil.copy2("inventory.db", current_backup)
            print(f"تم إنشاء نسخة احتياطية من الملف الحالي: {current_backup}")
        
        # استعادة النسخة الاحتياطية
        shutil.copy2(backup_path, "inventory.db")
        print(f"✅ تم استعادة النسخة الاحتياطية بنجاح: {os.path.basename(backup_path)}")
        return True
        
    except Exception as e:
        print(f"❌ خطأ في استعادة النسخة الاحتياطية: {str(e)}")
        return False

def list_backups():
    """عرض قائمة النسخ الاحتياطية المتاحة"""
    backup_dir = "backups"
    if not os.path.exists(backup_dir):
        print("لا توجد نسخ احتياطية")
        return []
    
    backup_files = []
    for file in os.listdir(backup_dir):
        if file.startswith("inventory_backup_") and file.endswith(".db"):
            file_path = os.path.join(backup_dir, file)
            file_time = os.path.getmtime(file_path)
            file_size = os.path.getsize(file_path)
            backup_files.append((file, file_time, file_size))
    
    # ترتيب الملفات حسب التاريخ (الأحدث أولاً)
    backup_files.sort(key=lambda x: x[1], reverse=True)
    
    print("\n📋 قائمة النسخ الاحتياطية:")
    print("-" * 80)
    for i, (file, file_time, file_size) in enumerate(backup_files, 1):
        date_str = datetime.fromtimestamp(file_time).strftime("%Y-%m-%d %H:%M:%S")
        size_str = f"{file_size / 1024:.1f} KB"
        print(f"{i:2d}. {file}")
        print(f"    التاريخ: {date_str}")
        print(f"    الحجم: {size_str}")
        print()
    
    return backup_files

def main():
    """الدالة الرئيسية"""
    print("🔄 نظام النسخ الاحتياطي التلقائي")
    print("=" * 50)
    
    # جدولة النسخ الاحتياطي
    schedule.every().sunday.at("02:00").do(backup_database)
    schedule.every().monday.at("02:00").do(backup_database)
    schedule.every().tuesday.at("02:00").do(backup_database)
    schedule.every().wednesday.at("02:00").do(backup_database)
    schedule.every().thursday.at("02:00").do(backup_database)
    schedule.every().friday.at("02:00").do(backup_database)
    schedule.every().saturday.at("02:00").do(backup_database)
    
    print("✅ تم جدولة النسخ الاحتياطي اليومي في الساعة 2:00 صباحاً")
    print("📋 الأوامر المتاحة:")
    print("  - backup: إنشاء نسخة احتياطية فورية")
    print("  - list: عرض قائمة النسخ الاحتياطية")
    print("  - restore <filename>: استعادة نسخة احتياطية")
    print("  - quit: إنهاء البرنامج")
    print()
    
    while True:
        try:
            command = input("أدخل الأمر: ").strip().lower()
            
            if command == "backup":
                backup_database()
            elif command == "list":
                list_backups()
            elif command.startswith("restore "):
                filename = command.split(" ", 1)[1]
                backup_path = os.path.join("backups", filename)
                restore_backup(backup_path)
            elif command == "quit":
                print("👋 تم إنهاء البرنامج")
                break
            else:
                print("❌ أمر غير صحيح!")
            
            print()
            
        except KeyboardInterrupt:
            print("\n👋 تم إنهاء البرنامج")
            break
        except Exception as e:
            print(f"❌ خطأ: {str(e)}")
        
        # تشغيل المهام المجدولة
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
