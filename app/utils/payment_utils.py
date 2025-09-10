# -*- coding: utf-8 -*-
"""
أدوات مساعدة لإدارة طرق الدفع
"""

from typing import Optional
from ..models.settings_models import payment_method_settings


def get_payment_method_name(payment_method_id: str) -> str:
    """
    الحصول على اسم طريقة الدفع من الإعدادات
    
    Args:
        payment_method_id (str): معرف طريقة الدفع
        
    Returns:
        str: اسم طريقة الدفع أو 'غير محدد' إذا لم توجد
    """
    try:
        # إعادة تحميل الإعدادات للتأكد من الحصول على أحدث البيانات
        payment_method_settings.settings = payment_method_settings.load_settings()
        methods = payment_method_settings.get_all_methods()
        
        for method in methods:
            if method.get('id') == payment_method_id:
                return method.get('name', 'غير محدد')
        
        # إذا لم توجد طريقة الدفع، إرجاع الاسم الافتراضي
        if payment_method_id == 'cash':
            return 'نقدي'
        elif payment_method_id == 'card':
            return 'بطاقة'
        else:
            return 'غير محدد'
    except Exception as e:
        print(f"خطأ في الحصول على اسم طريقة الدفع: {e}")
        return 'غير محدد'


def normalize_payment_method_id(payment_method_id: Optional[str]) -> str:
    """
    تحويل معرف طريقة الدفع إلى المعرف الصحيح
    
    Args:
        payment_method_id (Optional[str]): معرف أو اسم طريقة الدفع
        
    Returns:
        str: المعرف الصحيح لطريقة الدفع
    """
    if not payment_method_id:
        return 'cash'
    
    # إذا كانت طريقة الدفع هي اسم وليس معرف، نحاول العثور عليها
    if payment_method_id in ['نقدي', 'بنكك', 'شيك']:
        if payment_method_id == 'نقدي':
            return 'cash'
        elif payment_method_id == 'بنكك':
            return 'card'
        elif payment_method_id == 'شيك':
            return 'check'
    
    return payment_method_id


def get_payment_method_display_name(payment_method_id: Optional[str]) -> str:
    """
    الحصول على اسم العرض لطريقة الدفع
    
    Args:
        payment_method_id (Optional[str]): معرف طريقة الدفع
        
    Returns:
        str: اسم العرض لطريقة الدفع
    """
    if not payment_method_id:
        return 'غير محدد'
    
    # تحويل المعرف إلى المعرف الصحيح
    normalized_id = normalize_payment_method_id(payment_method_id)
    
    # الحصول على اسم طريقة الدفع
    return get_payment_method_name(normalized_id)
