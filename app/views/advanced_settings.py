# -*- coding: utf-8 -*-
"""
إعدادات متقدمة - الضرائب، طرق الدفع، العملات، نقطة البيع
"""

from flask import Blueprint, render_template, request, jsonify, session
from app.models.settings_models import tax_settings, payment_method_settings, currency_settings, pos_settings
from app.utils.auth import dev_user_required, login_required

advanced_settings_bp = Blueprint('advanced_settings', __name__, url_prefix='/settings')

# ==================== إعدادات الضرائب ====================

@advanced_settings_bp.route('/tax')
@dev_user_required
def tax_page():
    """صفحة إعدادات الضرائب"""
    settings = tax_settings.get_all_settings()
    return render_template('settings/tax.html', tax_settings=settings)

@advanced_settings_bp.route('/api/tax', methods=['POST'])
@dev_user_required
def update_tax_settings():
    """تحديث إعدادات الضرائب"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        if 'tax_rate' in data:
            tax_rate = float(data['tax_rate'])
            if tax_rate < 0 or tax_rate > 100:
                return jsonify({
                    'success': False,
                    'message': 'نسبة الضريبة يجب أن تكون بين 0 و 100'
                }), 400
        
        # تحديث الإعدادات
        success = tax_settings.update_settings(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'تم حفظ إعدادات الضرائب بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'خطأ في حفظ إعدادات الضرائب'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

@advanced_settings_bp.route('/api/tax', methods=['GET'])
@dev_user_required
def get_tax_settings():
    """الحصول على إعدادات الضرائب"""
    try:
        settings = tax_settings.get_all_settings()
        return jsonify({
            'success': True,
            'settings': settings
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

# ==================== إعدادات طرق الدفع ====================

@advanced_settings_bp.route('/payment-methods')
@dev_user_required
def payment_methods_page():
    """صفحة إدارة طرق الدفع"""
    methods = payment_method_settings.get_all_methods()
    return render_template('settings/payment_methods.html', payment_methods=methods)

@advanced_settings_bp.route('/api/payment-methods', methods=['GET'])
@dev_user_required
def get_payment_methods():
    """الحصول على طرق الدفع"""
    try:
        methods = payment_method_settings.get_all_methods()
        return jsonify({
            'success': True,
            'payment_methods': methods
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

@advanced_settings_bp.route('/api/payment-methods', methods=['POST'])
@dev_user_required
def add_payment_method():
    """إضافة طريقة دفع جديدة"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['name', 'name_en']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'حقل {field} مطلوب'
                }), 400
        
        # إضافة طريقة الدفع
        success = payment_method_settings.add_method(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'تم إضافة طريقة الدفع بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'خطأ في إضافة طريقة الدفع'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

@advanced_settings_bp.route('/api/payment-methods/<method_id>', methods=['PUT'])
@dev_user_required
def update_payment_method(method_id):
    """تحديث طريقة دفع"""
    try:
        data = request.get_json()
        
        # تحديث طريقة الدفع
        success = payment_method_settings.update_method(method_id, data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'تم تحديث طريقة الدفع بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'خطأ في تحديث طريقة الدفع'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

@advanced_settings_bp.route('/api/payment-methods/<method_id>', methods=['DELETE'])
@dev_user_required
def delete_payment_method(method_id):
    """حذف طريقة دفع"""
    try:
        # منع حذف طرق الدفع الأساسية
        if method_id in ['cash', 'card']:
            return jsonify({
                'success': False,
                'message': 'لا يمكن حذف طريقة الدفع الأساسية'
            }), 400
        
        # حذف طريقة الدفع
        success = payment_method_settings.delete_method(method_id)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'تم حذف طريقة الدفع بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'خطأ في حذف طريقة الدفع'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

@advanced_settings_bp.route('/payment-methods/<method_id>/edit')
@dev_user_required
def edit_payment_method(method_id):
    """صفحة تعديل طريقة دفع"""
    methods = payment_method_settings.get_all_methods()
    method = next((m for m in methods if m['id'] == method_id), None)
    
    if not method:
        return render_template('settings/payment_methods.html', 
                             payment_methods=methods, 
                             error_message='طريقة الدفع غير موجودة')
    
    return render_template('settings/payment_methods.html', 
                         payment_methods=methods, 
                         edit_method=method)

# ==================== إعدادات العملات ====================

@advanced_settings_bp.route('/currency')
@dev_user_required
def currency_page():
    """صفحة إعدادات العملات"""
    settings = currency_settings.get_all_settings()
    return render_template('settings/currency.html', currency_settings=settings)

@advanced_settings_bp.route('/api/currency', methods=['POST'])
@dev_user_required
def update_currency_settings():
    """تحديث إعدادات العملات"""
    try:
        data = request.get_json()
        
        # تحديث الإعدادات
        success = currency_settings.update_settings(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'تم حفظ إعدادات العملات بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'خطأ في حفظ إعدادات العملات'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

@advanced_settings_bp.route('/api/currency', methods=['GET'])
@dev_user_required
def get_currency_settings():
    """الحصول على إعدادات العملات"""
    try:
        settings = currency_settings.get_all_settings()
        return jsonify({
            'success': True,
            'settings': settings
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

# ==================== إعدادات نقطة البيع ====================

@advanced_settings_bp.route('/pos')
@dev_user_required
def pos_page():
    """صفحة إعدادات نقطة البيع"""
    settings = pos_settings.get_all_settings()
    return render_template('settings/pos.html', pos_settings=settings)

@advanced_settings_bp.route('/api/pos', methods=['POST'])
@dev_user_required
def update_pos_settings():
    """تحديث إعدادات نقطة البيع"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'لم يتم استلام البيانات'
            }), 400
        
        print(f"Received POS data: {data}")
        
        # تحديث الإعدادات
        success = pos_settings.update_settings(data)
        
        if success:
            print("POS settings updated successfully")
            return jsonify({
                'success': True,
                'message': 'تم حفظ إعدادات نقطة البيع بنجاح'
            })
        else:
            print("Failed to update POS settings")
            return jsonify({
                'success': False,
                'message': 'خطأ في حفظ إعدادات نقطة البيع'
            }), 500
            
    except Exception as e:
        print(f"Error updating POS settings: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

@advanced_settings_bp.route('/api/pos', methods=['GET'])
@dev_user_required
def get_pos_settings():
    """الحصول على إعدادات نقطة البيع"""
    try:
        settings = pos_settings.get_all_settings()
        return jsonify({
            'success': True,
            'settings': settings
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500
