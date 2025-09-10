# -*- coding: utf-8 -*-
"""
الصفحة الرئيسية ولوحة التحكم

المطور: محمد فاروق
التاريخ: 10/9/2025
"""

from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for
from ..models.database import get_db
from ..utils.auth import login_required
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required()
def index():
    """الصفحة الرئيسية - لوحة التحكم"""
    # توجيه الكاشير إلى نقطة البيع مباشرة
    if session.get('role') == 'clerk':
        return redirect(url_for('sales.new'))
    
    try:
        db = get_db()
        
        # جمع الإحصائيات الأساسية
        stats = _get_dashboard_stats(db)
        
        # جمع البيانات الإضافية
        recent_data = _get_recent_data(db)
        
        # تجميع البيانات للعرض
        context = {
            'total_items': stats['total_items'],
            'total_qty': stats['total_qty'],
            'low_stock': stats['low_stock'],
            'today_sales': stats['today_sales'],
            'today_invoices': stats['today_invoices'],
            'recent_sales': recent_data['sales'],
            'low_stock_items': recent_data['low_stock'],
            'recent_invoices': recent_data['invoices']
        }
        
        return render_template('dashboard.html', **context)
        
    except Exception as e:
        print(f"❌ خطأ في تحميل لوحة التحكم: {e}")
        return render_template('dashboard.html', 
                             total_items=0,
                             total_qty=0,
                             low_stock=0,
                             today_sales=0,
                             today_invoices=0,
                             recent_sales=[], 
                             low_stock_items=[], 
                             recent_invoices=[])

def _get_dashboard_stats(db):
    """جمع الإحصائيات الأساسية للوحة التحكم"""
    try:
        # إحصائيات المخزون
        total_items = db.execute('SELECT COUNT(*) as c FROM items').fetchone()['c']
        total_qty = db.execute('SELECT IFNULL(SUM(quantity),0) as s FROM items').fetchone()['s']
        low_stock = db.execute('SELECT COUNT(*) as c FROM items WHERE quantity <= reorder_level').fetchone()['c']
        
        # إحصائيات المبيعات اليوم
        today_sales = db.execute('''
            SELECT IFNULL(SUM(total_price), 0) as total
            FROM sales 
            WHERE DATE(created_at) = DATE('now')
        ''').fetchone()['total']
        
        today_invoices = db.execute('''
            SELECT COUNT(*) as count
            FROM invoices 
            WHERE DATE(created_at) = DATE('now')
        ''').fetchone()['count']
        
        return {
            'total_items': total_items,
            'total_qty': total_qty,
            'low_stock': low_stock,
            'today_sales': today_sales,
            'today_invoices': today_invoices
        }
        
    except Exception as e:
        print(f"❌ خطأ في جمع الإحصائيات: {e}")
        return {
            'total_items': 0,
            'total_qty': 0,
            'low_stock': 0,
            'today_sales': 0,
            'today_invoices': 0
        }

def _get_recent_data(db):
    """جمع البيانات الحديثة للعرض"""
    try:
        # المبيعات الأخيرة (آخر 10 مبيعات)
        recent_sales = db.execute('''
            SELECT s.id, i.name, s.quantity, s.unit_price, s.total_price, s.created_at
            FROM sales s JOIN items i ON i.id = s.item_id
            ORDER BY s.created_at DESC LIMIT 10
        ''').fetchall()
        
        # المنتجات على وشك النفاذ
        low_stock_items = db.execute('''
            SELECT id, name, quantity, reorder_level
            FROM items
            WHERE quantity <= reorder_level
            ORDER BY quantity ASC LIMIT 5
        ''').fetchall()
        
        # إحصائيات الفواتير الأخيرة
        recent_invoices = db.execute('''
            SELECT i.id, i.customer_name, i.total_amount, i.created_at, u.username as created_by
            FROM invoices i
            LEFT JOIN users u ON u.id = i.created_by
            ORDER BY i.created_at DESC
            LIMIT 5
        ''').fetchall()
        
        return {
            'sales': recent_sales,
            'low_stock': low_stock_items,
            'invoices': recent_invoices
        }
        
    except Exception as e:
        print(f"❌ خطأ في جمع البيانات الحديثة: {e}")
        return {
            'sales': [],
            'low_stock': [],
            'invoices': []
        }