from flask import Blueprint, render_template, request, jsonify, session
from app.models.store_settings import store_settings
from app.utils.auth import login_required, manager_required, dev_or_owner_required

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/store')
@dev_or_owner_required
def store_page():
    """صفحة إعدادات المتجر"""
    settings = store_settings.get_all_settings()
    return render_template('settings/store.html', store_settings=settings)

@settings_bp.route('/api/store', methods=['POST'])
@dev_or_owner_required
def update_store_settings():
    """تحديث إعدادات المتجر"""
    try:
        data = request.get_json()
        
        # التحقق من البيانات المطلوبة
        required_fields = ['store_name', 'store_address', 'store_phone', 'store_email']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'حقل {field} مطلوب'
                }), 400
        
        # تحديث الإعدادات
        success = store_settings.update_settings(data)
        
        if success:
            return jsonify({
                'success': True,
                'message': 'تم حفظ الإعدادات بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'خطأ في حفظ الإعدادات'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

@settings_bp.route('/api/store', methods=['GET'])
@dev_or_owner_required
def get_store_settings():
    """الحصول على إعدادات المتجر"""
    try:
        settings = store_settings.get_all_settings()
        return jsonify({
            'success': True,
            'settings': settings
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500

@settings_bp.route('/api/store/reset', methods=['POST'])
@dev_or_owner_required
def reset_store_settings():
    """إعادة تعيين إعدادات المتجر"""
    try:
        success = store_settings.reset_to_defaults()
        
        if success:
            return jsonify({
                'success': True,
                'message': 'تم إعادة تعيين الإعدادات بنجاح'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'خطأ في إعادة تعيين الإعدادات'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في الخادم: {str(e)}'
        }), 500
