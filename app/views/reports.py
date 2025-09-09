# -*- coding: utf-8 -*-
"""
التقارير والإحصائيات
"""

from flask import Blueprint, render_template, request
from ..models.database import get_db
from ..utils.auth import login_required
from datetime import datetime, timedelta

bp = Blueprint('reports', __name__)

@bp.route('/reports')
@login_required()
def index():
    """صفحة التقارير الرئيسية"""
    return render_template('reports/index.html')

@bp.route('/reports/daily')
@login_required()
def daily():
    """التقرير اليومي"""
    db = get_db()
    today = datetime.now().strftime('%Y-%m-%d')
    
    # Daily sales summary
    summary = db.execute('''
        SELECT 
            COUNT(DISTINCT s.id) as total_sales,
            SUM(s.quantity) as total_quantity,
            SUM(s.final_price) as total_amount
        FROM sales s
        WHERE DATE(s.created_at) = ?
    ''', (today,)).fetchone()
    
    # Top selling items today
    top_items = db.execute('''
        SELECT i.name, SUM(s.quantity) as total_qty, SUM(s.final_price) as total_amount
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE DATE(s.created_at) = ?
        GROUP BY i.id, i.name
        ORDER BY total_qty DESC
        LIMIT 10
    ''', (today,)).fetchall()
    
    # Recent sales
    recent_sales = db.execute('''
        SELECT s.*, i.name as item_name
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE DATE(s.created_at) = ?
        ORDER BY s.created_at DESC
        LIMIT 20
    ''', (today,)).fetchall()
    
    return render_template('reports/daily.html', 
                         summary=summary, 
                         top_items=top_items, 
                         recent_sales=recent_sales,
                         date=today)

@bp.route('/reports/monthly')
@login_required()
def monthly():
    """التقرير الشهري"""
    db = get_db()
    current_month = datetime.now().strftime('%Y-%m')
    
    # Monthly summary
    summary = db.execute('''
        SELECT 
            COUNT(DISTINCT s.id) as total_sales,
            SUM(s.quantity) as total_quantity,
            SUM(s.final_price) as total_amount
        FROM sales s
        WHERE strftime('%Y-%m', s.created_at) = ?
    ''', (current_month,)).fetchone()
    
    # Top selling items this month
    top_items = db.execute('''
        SELECT i.name, SUM(s.quantity) as total_qty, SUM(s.final_price) as total_amount
        FROM sales s
        JOIN items i ON i.id = s.item_id
        WHERE strftime('%Y-%m', s.created_at) = ?
        GROUP BY i.id, i.name
        ORDER BY total_qty DESC
        LIMIT 10
    ''', (current_month,)).fetchall()
    
    # Daily breakdown
    daily_breakdown = db.execute('''
        SELECT 
            DATE(s.created_at) as sale_date,
            COUNT(DISTINCT s.id) as sales_count,
            SUM(s.quantity) as total_quantity,
            SUM(s.final_price) as total_amount
        FROM sales s
        WHERE strftime('%Y-%m', s.created_at) = ?
        GROUP BY DATE(s.created_at)
        ORDER BY sale_date DESC
    ''', (current_month,)).fetchall()
    
    return render_template('reports/monthly.html', 
                         summary=summary, 
                         top_items=top_items, 
                         daily_breakdown=daily_breakdown,
                         month=current_month)

@bp.route('/reports/yearly')
@login_required()
def yearly():
    """التقرير السنوي"""
    db = get_db()
    current_year = datetime.now().strftime('%Y')
    
    # Yearly summary
    summary = db.execute('''
        SELECT 
            COUNT(DISTINCT s.id) as total_sales,
            SUM(s.quantity) as total_quantity,
            SUM(s.final_price) as total_amount
        FROM sales s
        WHERE strftime('%Y', s.created_at) = ?
    ''', (current_year,)).fetchone()
    
    # Monthly breakdown
    monthly_breakdown = db.execute('''
        SELECT 
            strftime('%Y-%m', s.created_at) as sale_month,
            COUNT(DISTINCT s.id) as sales_count,
            SUM(s.quantity) as total_quantity,
            SUM(s.final_price) as total_amount
        FROM sales s
        WHERE strftime('%Y', s.created_at) = ?
        GROUP BY strftime('%Y-%m', s.created_at)
        ORDER BY sale_month DESC
    ''', (current_year,)).fetchall()
    
    # Category performance
    category_performance = db.execute('''
        SELECT 
            c.name as category_name,
            COUNT(DISTINCT s.id) as sales_count,
            SUM(s.quantity) as total_quantity,
            SUM(s.final_price) as total_amount
        FROM sales s
        JOIN items i ON i.id = s.item_id
        LEFT JOIN categories c ON c.id = i.category_id
        WHERE strftime('%Y', s.created_at) = ?
        GROUP BY c.id, c.name
        ORDER BY total_amount DESC
    ''', (current_year,)).fetchall()
    
    return render_template('reports/yearly.html', 
                         summary=summary, 
                         monthly_breakdown=monthly_breakdown,
                         category_performance=category_performance,
                         year=current_year)
