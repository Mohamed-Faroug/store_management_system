#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نظام النسخ الاحتياطي
Backup System
"""

import os
import shutil
import sqlite3
import json
from datetime import datetime
import zipfile

class BackupManager:
    def __init__(self, db_path='inventory.db', backup_dir='backups'):
        self.db_path = db_path
        self.backup_dir = backup_dir
        self.ensure_backup_dir()
    
    def ensure_backup_dir(self):
        """إنشاء مجلد النسخ الاحتياطية إذا لم يكن موجوداً"""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self):
        """إنشاء نسخة احتياطية شاملة"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # إنشاء مجلد النسخة الاحتياطية
            os.makedirs(backup_path, exist_ok=True)
            
            # نسخ قاعدة البيانات
            if os.path.exists(self.db_path):
                shutil.copy2(self.db_path, os.path.join(backup_path, 'inventory.db'))
            
            # نسخ الملفات المهمة
            important_files = [
                'config.py',
                'requirements.txt',
                'main.py',
                'app.py'
            ]
            
            for file in important_files:
                if os.path.exists(file):
                    shutil.copy2(file, backup_path)
            
            # نسخ مجلد التطبيق
            if os.path.exists('app'):
                shutil.copytree('app', os.path.join(backup_path, 'app'))
            
            # إنشاء ملف معلومات النسخة الاحتياطية
            backup_info = {
                'timestamp': timestamp,
                'created_at': datetime.now().isoformat(),
                'database_size': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0,
                'files_count': len([f for f in os.listdir(backup_path) if os.path.isfile(os.path.join(backup_path, f))]),
                'version': '2.0.0'
            }
            
            with open(os.path.join(backup_path, 'backup_info.json'), 'w', encoding='utf-8') as f:
                json.dump(backup_info, f, ensure_ascii=False, indent=2)
            
            # ضغط النسخة الاحتياطية
            zip_path = f"{backup_path}.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(backup_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, backup_path)
                        zipf.write(file_path, arcname)
            
            # حذف المجلد المؤقت
            shutil.rmtree(backup_path)
            
            return {
                'success': True,
                'backup_path': zip_path,
                'backup_name': backup_name,
                'size': os.path.getsize(zip_path),
                'message': f'تم إنشاء النسخة الاحتياطية بنجاح: {backup_name}.zip'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'فشل في إنشاء النسخة الاحتياطية: {str(e)}'
            }
    
    def list_backups(self):
        """قائمة بالنسخ الاحتياطية المتاحة"""
        try:
            backups = []
            if os.path.exists(self.backup_dir):
                for file in os.listdir(self.backup_dir):
                    if file.endswith('.zip'):
                        file_path = os.path.join(self.backup_dir, file)
                        stat = os.stat(file_path)
                        backups.append({
                            'name': file,
                            'size': stat.st_size,
                            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                            'path': file_path
                        })
            
            # ترتيب حسب التاريخ (الأحدث أولاً)
            backups.sort(key=lambda x: x['created'], reverse=True)
            return backups
            
        except Exception as e:
            return []
    
    def restore_backup(self, backup_name):
        """استعادة نسخة احتياطية"""
        try:
            backup_path = os.path.join(self.backup_dir, backup_name)
            if not os.path.exists(backup_path):
                return {
                    'success': False,
                    'message': 'النسخة الاحتياطية غير موجودة'
                }
            
            # إنشاء مجلد استعادة مؤقت
            temp_dir = f"restore_temp_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(temp_dir, exist_ok=True)
            
            # استخراج النسخة الاحتياطية
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(temp_dir)
            
            # نسخ الملفات المستعادة
            for item in os.listdir(temp_dir):
                src = os.path.join(temp_dir, item)
                if os.path.isdir(src):
                    if os.path.exists(item):
                        shutil.rmtree(item)
                    shutil.copytree(src, item)
                else:
                    shutil.copy2(src, item)
            
            # حذف المجلد المؤقت
            shutil.rmtree(temp_dir)
            
            return {
                'success': True,
                'message': f'تم استعادة النسخة الاحتياطية بنجاح: {backup_name}'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': f'فشل في استعادة النسخة الاحتياطية: {str(e)}'
            }

def main():
    """وظيفة رئيسية للاختبار"""
    backup_manager = BackupManager()
    
    print("🔄 إنشاء نسخة احتياطية...")
    result = backup_manager.create_backup()
    
    if result['success']:
        print(f"✅ {result['message']}")
        print(f"📁 المسار: {result['backup_path']}")
        print(f"📊 الحجم: {result['size'] / 1024 / 1024:.2f} MB")
    else:
        print(f"❌ {result['message']}")
    
    print("\n📋 قائمة النسخ الاحتياطية:")
    backups = backup_manager.list_backups()
    for backup in backups[:5]:  # عرض آخر 5 نسخ
        size_mb = backup['size'] / 1024 / 1024
        print(f"  • {backup['name']} ({size_mb:.2f} MB) - {backup['created']}")

if __name__ == "__main__":
    main()
