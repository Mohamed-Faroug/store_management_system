# -*- coding: utf-8 -*-
"""
API endpoints للتطبيق
"""

from flask import Blueprint, jsonify
from ..models.database import get_db
from ..utils.auth import dev_user_required

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/statistics/items')
@dev_user_required
def get_items_statistics():
    """إحصائيات الأصناف"""
    try:
        db = get_db()
        count = db.execute('SELECT COUNT(*) FROM items').fetchone()[0]
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/statistics/categories')
@dev_user_required
def get_categories_statistics():
    """إحصائيات الفئات"""
    try:
        db = get_db()
        count = db.execute('SELECT COUNT(*) FROM categories').fetchone()[0]
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/statistics/invoices')
@dev_user_required
def get_invoices_statistics():
    """إحصائيات الفواتير"""
    try:
        db = get_db()
        count = db.execute('SELECT COUNT(*) FROM invoices').fetchone()[0]
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/api/statistics/sales')
@dev_user_required
def get_sales_statistics():
    """إحصائيات المبيعات"""
    try:
        db = get_db()
        count = db.execute('SELECT COUNT(*) FROM sales').fetchone()[0]
        return jsonify({'count': count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
