# -*- coding: utf-8 -*-
"""
الصفحة الرئيسية ولوحة التحكم
"""

from flask import Blueprint, render_template, session, g, jsonify, request, send_file
from ..models.database import get_db
from ..utils.auth import login_required
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from backup import BackupManager

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required()
def index():
    """الصفحة الرئيسية - لوحة التحكم"""
    # توجيه الكاشير إلى نقطة البيع
    if session.get('role') == 'clerk':
        from flask import redirect, url_for
        return redirect(url_for('sales.new'))
    
    db = get_db()
    
    # إحصائيات عامة
    total_items = db.execute('SELECT COUNT(*) as c FROM items').fetchone()['c']
    total_qty = db.execute('SELECT IFNULL(SUM(quantity),0) as s FROM items').fetchone()['s']
    low_stock = db.execute('SELECT COUNT(*) as c FROM items WHERE quantity <= reorder_level').fetchone()['c']
    
    # مبيعات اليوم
    today_sales = db.execute('''
        SELECT IFNULL(SUM(total_price), 0) as total
        FROM sales 
        WHERE DATE(created_at) = DATE('now')
    ''').fetchone()['total']
    
    # عدد الفواتير اليوم
    today_invoices = db.execute('''
        SELECT COUNT(*) as count
        FROM invoices 
        WHERE DATE(created_at) = DATE('now')
    ''').fetchone()['count']
    
    # إجمالي المنتجات
    total_products = db.execute('SELECT COUNT(*) as c FROM items').fetchone()['c']
    
    # المبيعات الأخيرة (آخر 10 مبيعات)
    recent_sales = db.execute('''
        SELECT s.id, i.name, s.quantity, s.unit_price, s.total_price, s.created_at
        FROM sales s JOIN items i ON i.id = s.item_id
        ORDER BY s.created_at DESC LIMIT 10
    ''').fetchall()
    
    # أكثر المنتجات مبيعاً (آخر 7 أيام)
    top_selling_items = db.execute('''
        SELECT i.name, SUM(s.quantity) as total_sold, SUM(s.total_price) as total_revenue
        FROM sales s 
        JOIN items i ON i.id = s.item_id
        WHERE s.created_at >= DATE('now', '-7 days')
        GROUP BY i.id, i.name
        ORDER BY total_sold DESC
        LIMIT 5
    ''').fetchall()
    
    # إحصائيات الفواتير الأخيرة
    recent_invoices = db.execute('''
        SELECT i.id, i.customer_name, i.total_amount, i.created_at, u.username as created_by
        FROM invoices i
        LEFT JOIN users u ON u.id = i.created_by
        ORDER BY i.created_at DESC
        LIMIT 5
    ''').fetchall()
    
    return render_template('dashboard.html', data={
        'total_items': total_items,
        'total_qty': total_qty,
        'low_stock': low_stock,
        'today_sales': today_sales,
        'today_invoices': today_invoices,
        'total_products': total_products,
        'recent_sales': recent_sales,
        'top_selling_items': top_selling_items,
        'recent_invoices': recent_invoices
    })

@bp.route('/api/backup/create', methods=['POST'])
@login_required()
def create_backup():
    """إنشاء نسخة احتياطية"""
    try:
        # التحقق من الصلاحيات (المدير فقط)
        if session.get('role') != 'manager':
            return jsonify({
                'success': False,
                'message': 'ليس لديك صلاحية لإنشاء نسخة احتياطية'
            }), 403
        
        backup_manager = BackupManager()
        result = backup_manager.create_backup()
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message'],
                'backup_name': result['backup_name'],
                'size': result['size']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في إنشاء النسخة الاحتياطية: {str(e)}'
        }), 500

@bp.route('/api/backup/list')
@login_required()
def list_backups():
    """قائمة النسخ الاحتياطية"""
    try:
        # التحقق من الصلاحيات (المدير فقط)
        if session.get('role') != 'manager':
            return jsonify({
                'success': False,
                'message': 'ليس لديك صلاحية لعرض النسخ الاحتياطية'
            }), 403
        
        backup_manager = BackupManager()
        backups = backup_manager.list_backups()
        
        return jsonify({
            'success': True,
            'backups': backups
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في جلب قائمة النسخ الاحتياطية: {str(e)}'
        }), 500

@bp.route('/api/backup/download/<backup_name>')
@login_required()
def download_backup(backup_name):
    """تحميل نسخة احتياطية"""
    try:
        # التحقق من الصلاحيات (المدير فقط)
        if session.get('role') != 'manager':
            return jsonify({
                'success': False,
                'message': 'ليس لديك صلاحية لتحميل النسخ الاحتياطية'
            }), 403
        
        backup_manager = BackupManager()
        backup_path = os.path.join(backup_manager.backup_dir, backup_name)
        
        if not os.path.exists(backup_path):
            return jsonify({
                'success': False,
                'message': 'النسخة الاحتياطية غير موجودة'
            }), 404
        
        return send_file(backup_path, as_attachment=True, download_name=backup_name)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في تحميل النسخة الاحتياطية: {str(e)}'
        }), 500

@bp.route('/api/backup/restore', methods=['POST'])
@login_required()
def restore_backup():
    """استعادة نسخة احتياطية"""
    try:
        # التحقق من الصلاحيات (المدير فقط)
        if session.get('role') != 'manager':
            return jsonify({
                'success': False,
                'message': 'ليس لديك صلاحية لاستعادة النسخ الاحتياطية'
            }), 403
        
        data = request.get_json()
        backup_name = data.get('backup_name')
        
        if not backup_name:
            return jsonify({
                'success': False,
                'message': 'اسم النسخة الاحتياطية مطلوب'
            }), 400
        
        backup_manager = BackupManager()
        result = backup_manager.restore_backup(backup_name)
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': result['message']
            })
        else:
            return jsonify({
                'success': False,
                'message': result['message']
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'خطأ في استعادة النسخة الاحتياطية: {str(e)}'
        }), 500
