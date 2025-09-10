def inject_store_settings():
    """حقن إعدادات المتجر في جميع القوالب"""
    try:
        from app.models.store_settings import store_settings
        # إعادة تحميل الإعدادات للتأكد من الحصول على أحدث البيانات
        store_settings.settings = store_settings.load_settings()
        return {
            'store_settings': store_settings.get_all_settings()
        }
    except Exception as e:
        print(f"خطأ في تحميل إعدادات المتجر: {e}")
        # إرجاع إعدادات افتراضية في حالة الخطأ
        return {
            'store_settings': {
                'store_name': 'مخزن الزينة - إدارة المخزون',
                'store_address': 'شارع الملك فيصل، الرياض، المملكة العربية السعودية',
                'store_phone': '+966 50 123 4567',
                'store_email': 'info@zina-store.com',
                'tax_number': '123456789012345',
                'commercial_register': '1010123456',
                'app_name': 'نظام إدارة المخزون - مخزن الزينة',
                'app_version': '2.1',
                'store_description': 'نظام متكامل لإدارة المخزون والمبيعات والمشتريات',
                'last_updated': '2025-09-09T12:00:00'
            }
        }
