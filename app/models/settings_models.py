# -*- coding: utf-8 -*-
"""
نماذج الإعدادات المتقدمة
"""

import json
import os
from datetime import datetime

class TaxSettings:
    def __init__(self, settings_file='tax_settings.json'):
        self.settings_file = settings_file
        self.default_settings = {
            'tax_enabled': True,
            'tax_rate': 15.0,  # 15% VAT
            'tax_name': 'ضريبة القيمة المضافة',
            'tax_short_name': 'VAT',
            'tax_number': '123456789012345',
            'last_updated': datetime.now().isoformat()
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """تحميل إعدادات الضريبة"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    return {**self.default_settings, **settings}
            else:
                self.save_settings(self.default_settings)
                return self.default_settings
        except Exception as e:
            print(f"خطأ في تحميل إعدادات الضريبة: {e}")
            return self.default_settings
    
    def save_settings(self, settings):
        """حفظ إعدادات الضريبة"""
        try:
            settings['last_updated'] = datetime.now().isoformat()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطأ في حفظ إعدادات الضريبة: {e}")
            return False
    
    def update_settings(self, new_settings):
        """تحديث إعدادات الضريبة"""
        try:
            self.settings.update(new_settings)
            return self.save_settings(self.settings)
        except Exception as e:
            print(f"خطأ في تحديث إعدادات الضريبة: {e}")
            return False
    
    def get_all_settings(self):
        """الحصول على جميع إعدادات الضريبة"""
        return self.settings
    
    def calculate_tax(self, amount):
        """حساب الضريبة"""
        if not self.settings.get('tax_enabled', False):
            return 0
        return (amount * self.settings.get('tax_rate', 0)) / 100

class PaymentMethodSettings:
    def __init__(self, settings_file='payment_methods.json'):
        self.settings_file = settings_file
        self.default_settings = {
            'payment_methods': [
                {
                    'id': 'cash',
                    'name': 'نقدي',
                    'name_en': 'Cash',
                    'enabled': True,
                    'icon': 'bi-cash',
                    'color': 'success'
                },
                {
                    'id': 'card',
                    'name': 'بطاقة ائتمان',
                    'name_en': 'Credit Card',
                    'enabled': True,
                    'icon': 'bi-credit-card',
                    'color': 'info'
                },
                {
                    'id': 'bank_transfer',
                    'name': 'تحويل بنكي',
                    'name_en': 'Bank Transfer',
                    'enabled': True,
                    'icon': 'bi-bank',
                    'color': 'primary'
                },
                {
                    'id': 'check',
                    'name': 'شيك',
                    'name_en': 'Check',
                    'enabled': False,
                    'icon': 'bi-file-text',
                    'color': 'warning'
                }
            ],
            'last_updated': datetime.now().isoformat()
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """تحميل طرق الدفع"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    return {**self.default_settings, **settings}
            else:
                self.save_settings(self.default_settings)
                return self.default_settings
        except Exception as e:
            print(f"خطأ في تحميل طرق الدفع: {e}")
            return self.default_settings
    
    def save_settings(self, settings):
        """حفظ طرق الدفع"""
        try:
            settings['last_updated'] = datetime.now().isoformat()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطأ في حفظ طرق الدفع: {e}")
            return False
    
    def get_enabled_methods(self):
        """الحصول على طرق الدفع المفعلة"""
        return [method for method in self.settings.get('payment_methods', []) if method.get('enabled', False)]
    
    def get_all_methods(self):
        """الحصول على جميع طرق الدفع"""
        return self.settings.get('payment_methods', [])
    
    def get_all_settings(self):
        """الحصول على جميع الإعدادات"""
        return self.settings
    
    def update_method(self, method_id, method_data):
        """تحديث طريقة دفع"""
        try:
            methods = self.settings.get('payment_methods', [])
            
            for i, method in enumerate(methods):
                if method.get('id') == method_id:
                    methods[i].update(method_data)
                    break
            else:
                return False
                
            self.settings['payment_methods'] = methods
            return self.save_settings(self.settings)
        except Exception as e:
            print(f"خطأ في تحديث طريقة الدفع: {e}")
            return False
    
    def add_method(self, method_data):
        """إضافة طريقة دفع جديدة"""
        try:
            methods = self.settings.get('payment_methods', [])
            # إنشاء معرف فريد
            method_id = method_data.get('id', f"method_{len(methods) + 1}")
            method_data['id'] = method_id
            methods.append(method_data)
            self.settings['payment_methods'] = methods
            return self.save_settings(self.settings)
        except Exception as e:
            print(f"خطأ في إضافة طريقة الدفع: {e}")
            return False
    
    def delete_method(self, method_id):
        """حذف طريقة دفع"""
        try:
            methods = self.settings.get('payment_methods', [])
            methods = [method for method in methods if method.get('id') != method_id]
            self.settings['payment_methods'] = methods
            return self.save_settings(self.settings)
        except Exception as e:
            print(f"خطأ في حذف طريقة الدفع: {e}")
            return False

class CurrencySettings:
    def __init__(self, settings_file='currency_settings.json'):
        self.settings_file = settings_file
        self.default_settings = {
            'default_currency': 'SAR',
            'currencies': [
                {
                    'code': 'SAR',
                    'name': 'ريال سعودي',
                    'name_en': 'Saudi Riyal',
                    'symbol': 'ر.س',
                    'symbol_position': 'after',
                    'decimal_places': 2,
                    'enabled': True
                },
                {
                    'code': 'USD',
                    'name': 'دولار أمريكي',
                    'name_en': 'US Dollar',
                    'symbol': '$',
                    'symbol_position': 'before',
                    'decimal_places': 2,
                    'enabled': False
                },
                {
                    'code': 'EUR',
                    'name': 'يورو',
                    'name_en': 'Euro',
                    'symbol': '€',
                    'symbol_position': 'after',
                    'decimal_places': 2,
                    'enabled': False
                }
            ],
            'last_updated': datetime.now().isoformat()
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """تحميل إعدادات العملة"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    return {**self.default_settings, **settings}
            else:
                self.save_settings(self.default_settings)
                return self.default_settings
        except Exception as e:
            print(f"خطأ في تحميل إعدادات العملة: {e}")
            return self.default_settings
    
    def save_settings(self, settings):
        """حفظ إعدادات العملة"""
        try:
            settings['last_updated'] = datetime.now().isoformat()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطأ في حفظ إعدادات العملة: {e}")
            return False
    
    def get_default_currency(self):
        """الحصول على العملة الافتراضية"""
        default_code = self.settings.get('default_currency', 'SAR')
        currencies = self.settings.get('currencies', [])
        for currency in currencies:
            if currency.get('code') == default_code:
                return currency
        return currencies[0] if currencies else None
    
    def get_enabled_currencies(self):
        """الحصول على العملات المفعلة"""
        return [currency for currency in self.settings.get('currencies', []) if currency.get('enabled', False)]
    
    def format_amount(self, amount, currency_code=None):
        """تنسيق المبلغ مع العملة"""
        if currency_code is None:
            currency = self.get_default_currency()
        else:
            currencies = self.settings.get('currencies', [])
            currency = next((c for c in currencies if c.get('code') == currency_code), None)
        
        if not currency:
            return f"{amount:.2f}"
        
        symbol = currency.get('symbol', '')
        position = currency.get('symbol_position', 'after')
        decimal_places = currency.get('decimal_places', 2)
        
        formatted_amount = f"{amount:.{decimal_places}f}"
        
        if position == 'before':
            return f"{symbol}{formatted_amount}"
        else:
            return f"{formatted_amount} {symbol}"
    
    def update_settings(self, new_settings):
        """تحديث إعدادات العملة"""
        try:
            self.settings.update(new_settings)
            return self.save_settings(self.settings)
        except Exception as e:
            print(f"خطأ في تحديث إعدادات العملة: {e}")
            return False
    
    def get_all_settings(self):
        """الحصول على جميع إعدادات العملة"""
        return self.settings

class POSSettings:
    def __init__(self, settings_file='pos_settings.json'):
        self.settings_file = settings_file
        self.default_settings = {
            'pos_enabled': True,
            'receipt_printer': {
                'enabled': True,
                'paper_size': '58mm',
                'auto_print': True
            },
            'display_settings': {
                'show_tax': True,
                'show_discount': True,
                'show_payment_method': True,
                'show_customer_info': True
            },
            'business_hours': {
                'enabled': False,
                'start_time': '08:00',
                'end_time': '22:00'
            },
            'last_updated': datetime.now().isoformat()
        }
        self.settings = self.load_settings()
    
    def load_settings(self):
        """تحميل إعدادات نقطة البيع"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    return {**self.default_settings, **settings}
            else:
                self.save_settings(self.default_settings)
                return self.default_settings
        except Exception as e:
            print(f"خطأ في تحميل إعدادات نقطة البيع: {e}")
            return self.default_settings
    
    def save_settings(self, settings):
        """حفظ إعدادات نقطة البيع"""
        try:
            settings['last_updated'] = datetime.now().isoformat()
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"خطأ في حفظ إعدادات نقطة البيع: {e}")
            return False
    
    def update_settings(self, new_settings):
        """تحديث إعدادات نقطة البيع"""
        try:
            self.settings.update(new_settings)
            return self.save_settings(self.settings)
        except Exception as e:
            print(f"خطأ في تحديث إعدادات نقطة البيع: {e}")
            return False
    
    def get_all_settings(self):
        """الحصول على جميع إعدادات نقطة البيع"""
        return self.settings

# إنشاء مثيلات عامة للإعدادات
tax_settings = TaxSettings()
payment_method_settings = PaymentMethodSettings()
currency_settings = CurrencySettings()
pos_settings = POSSettings()
