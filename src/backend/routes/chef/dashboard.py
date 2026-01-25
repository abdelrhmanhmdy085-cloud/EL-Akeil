from flask import Blueprint, request, jsonify
from sqlalchemy import func

chef_dashboard_bp = Blueprint('chef_dashboard', __name__, url_prefix='/api/chef')

@chef_dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    """الحصول على بيانات لوحة التحكم"""
    try:
        chef_id = request.headers.get('Chef-ID') or request.args.get('chef_id')
        
        if not chef_id:
            return jsonify({'error': 'Chef ID required'}), 400
        
        chef_id = int(chef_id)
        
        from backend.models import (
            ChefProfile, Dish, Order, OrderItem, Review
        )
        
        # Get chef info
        chef = ChefProfile.query.get(chef_id)
        if not chef:
            return jsonify({'error': 'Chef not found'}), 404
        
        # Count dishes
        total_dishes = Dish.query.filter_by(chef_id=chef_id).count()
        available_dishes = Dish.query.filter_by(chef_id=chef_id, available=True).count()
        
        # Get recent orders
        recent_orders = Order.query.join(OrderItem).join(Dish).filter(
            Dish.chef_id == chef_id
        ).order_by(Order.created_at.desc()).limit(5).all()
        
        # Calculate revenue
        from datetime import datetime, timedelta
        
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        
        daily_revenue = {}
        for i in range(7):
            day = today - timedelta(days=i)
            revenue = 0
            orders = Order.query.filter(
                Order.created_at >= day,
                Order.created_at < day + timedelta(days=1)
            ).join(OrderItem).join(Dish).filter(
                Dish.chef_id == chef_id
            ).all()
            
            for order in orders:
                for item in order.items:
                    if item.dish.chef_id == chef_id:
                        revenue += item.quantity * item.price
            
            daily_revenue[day.isoformat()] = revenue
        
        # Get ratings
        reviews = Review.query.join(Dish).filter(
            Dish.chef_id == chef_id
        ).all()
        
        avg_rating = 0
        if reviews:
            avg_rating = round(sum(r.rating for r in reviews) / len(reviews), 1)
        
        return jsonify({
            'status': 'success',
            'dashboard': {
                'chef_info': {
                    'id': chef.id,
                    'name': chef.user.username if chef.user else 'Unknown',
                    'phone': chef.phone,
                    'bio': chef.bio
                },
                'statistics': {
                    'total_dishes': total_dishes,
                    'available_dishes': available_dishes,
                    'total_reviews': len(reviews),
                    'average_rating': avg_rating,
                    'total_orders': len(recent_orders)
                },
                'revenue': daily_revenue,
                'recent_orders': [
                    {
                        'id': o.id,
                        'customer_name': o.customer.user.username if o.customer else 'Unknown',
                        'total': float(o.total),
                        'status': o.status,
                        'created_at': o.created_at.isoformat()
                    }
                    for o in recent_orders
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chef_dashboard_bp.route('/stats/top-dishes', methods=['GET'])
def get_top_dishes():
    """الأطباق الأفضل أداءً"""
    try:
        chef_id = request.headers.get('Chef-ID') or request.args.get('chef_id')
        limit = request.args.get('limit', 10, type=int)
        
        if not chef_id:
            return jsonify({'error': 'Chef ID required'}), 400
        
        from backend.models import Dish, OrderItem
        from sqlalchemy import func
        
        top_dishes = Dish.query.filter_by(
            chef_id=int(chef_id)
        ).outerjoin(OrderItem).group_by(
            Dish.id
        ).order_by(
            func.count(OrderItem.id).desc()
        ).limit(limit).all()
        
        return jsonify({
            'status': 'success',
            'dishes': [
                {
                    'id': d.id,
                    'name': d.name,
                    'price': float(d.price),
                    'orders': len(d.order_items) if d.order_items else 0
                }
                for d in top_dishes
            ]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
