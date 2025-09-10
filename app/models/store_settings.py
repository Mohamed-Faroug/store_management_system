import json
import os
from datetime import datetime

class StoreSettings:
    def __init__(self, settings_file='store_settings.json'):
        self.settings_file = settings_file
        self.default_settings = {
            'store_name': 'مخزن الزينة - إدارة المخزون',
            'store_address': 'شارع الملك فيصل، الرياض، المملكة العربية السعودية',
            'store_phone': '+966 50 123 4567',
            'store_email': 'info@zina-store.com',
            'tax_number': '123456789012345',
            'commercial_register': '1010123456',
            'app_name': 'نظام إدارة المخزون - مخزن الزينة',
            'app_version': '2.1',
            'store_description': 'نظام متكامل لإدارة المخزون والمبيعات والمشتريات',
            'last_updated': datetime.now().isoformat()
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """تحميل الإعدادات من الملف"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    # دمج الإعدادات الافتراضية مع المحملة
                    merged_settings = {**self.default_settings, **settings}
                    return merged_settings
            else:
                # إنشاء ملف الإعدادات بالبيانات الافتراضية
                self.save_settings(self.default_settings)
                return self.default_settings
        except Exception as e:
            print(f"خطأ في تحميل إعدادات المتجر: {e}")
            return self.default_settings
    
    def save_settings(self, settings):
        """حفظ الإعدادات في الملف"""
        try:
            settings['last_updated'] = datetime.now().isoformat()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطأ في حفظ إعدادات المتجر: {e}")
            return False
    
    def get_setting(self, key, default=None):
        """الحصول على إعداد محدد"""
        return self.settings.get(key, default)
    
    def update_settings(self, new_settings):
        """تحديث الإعدادات"""
        try:
            # دمج الإعدادات الجديدة مع الموجودة
            self.settings.update(new_settings)
            return self.save_settings(self.settings)
        except Exception as e:
            print(f"خطأ في تحديث إعدادات المتجر: {e}")
            return False
    
    def get_all_settings(self):
        """الحصول على جميع الإعدادات"""
        return self.settings
    
    def reset_to_defaults(self):
        """إعادة تعيين الإعدادات إلى القيم الافتراضية"""
        return self.save_settings(self.default_settings)

# إنشاء مثيل عام للإعدادات
store_settings = StoreSettings()
