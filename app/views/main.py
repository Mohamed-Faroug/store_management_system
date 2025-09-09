# -*- coding: utf-8 -*-
"""
الصفحة الرئيسية ولوحة التحكم
"""

from flask import Blueprint, render_template, session, g
from ..models.database import get_db
from ..utils.auth import login_required

bp = Blueprint('main', __name__)

@bp.route('/')
@login_required()
def index():
    """الصفحة الرئيسية - لوحة التحكم"""
    db = get_db()
    total_items = db.execute('SELECT COUNT(*) as c FROM items').fetchone()['c']
    total_qty = db.execute('SELECT IFNULL(SUM(quantity),0) as s FROM items').fetchone()['s']
    low_stock = db.execute('SELECT COUNT(*) as c FROM items WHERE quantity <= reorder_level').fetchone()['c']
    recent_sales = db.execute('''
        SELECT s.id, i.name, s.quantity, s.unit_price, s.total_price, s.created_at
        FROM sales s JOIN items i ON i.id = s.item_id
        ORDER BY s.created_at DESC LIMIT 10
    ''').fetchall()
    
    return render_template('dashboard.html', data={
        'total_items': total_items,
        'total_qty': total_qty,
        'low_stock': low_stock,
        'recent_sales': recent_sales
    })
