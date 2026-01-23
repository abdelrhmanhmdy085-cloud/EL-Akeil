"""
Backend API Routes for Navigation, Push Notifications & Heatmap
"""
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, timedelta
import os
import requests
import json
import logging
from backend.models_enhanced import (
    db, User, Order, DriverProfile, ChefProfile, CustomerProfile,
    RouteNavigation, DeviceToken, Notification, HeatmapDataPoint, HeatmapZone, NavigationSession
)

logger = logging.getLogger(__name__)

# Create blueprints
navigation_bp = Blueprint('navigation', __name__, url_prefix='/api/navigation')
notification_bp = Blueprint('notifications', __name__, url_prefix='/api/notifications')
heatmap_bp = Blueprint('heatmap', __name__, url_prefix='/api/heatmap')

# ============================================================
# NAVIGATION ROUTES
# ============================================================

@navigation_bp.route('/route/<int:order_id>', methods=['GET'])
@jwt_required()
def get_route(order_id):
    """Get navigation route for an order"""
    user_id = get_jwt_identity()
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Verify access (driver, customer, or chef)
    user = User.query.get(user_id)
    driver = DriverProfile.query.filter_by(user_id=user_id).first()
    
    if user.role == 'driver' and (not driver or order.driver_id != driver.id):
        return jsonify({'error': 'Not assigned to this order'}), 403
    elif user.role == 'customer' and order.customer_id != user_id:
        return jsonify({'error': 'Not authorized'}), 403
    
    route = RouteNavigation.query.filter_by(order_id=order_id).first()
    if not route:
        return jsonify({'error': 'Route not found'}), 404
    
    return jsonify(route.to_dict()), 200

@navigation_bp.route('/route/create', methods=['POST'])
@jwt_required()
def create_route():
    """
    Create navigation route using Google Maps or OpenStreetMap API
    Expected: { 'order_id': 123 }
    """
    user_id = get_jwt_identity()
    data = request.get_json()
    order_id = data.get('order_id')
    
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Verify driver
    driver = DriverProfile.query.filter_by(user_id=user_id).first()
    if not driver or order.driver_id != driver.id:
        return jsonify({'error': 'Not assigned to this order'}), 403
    
    try:
        # Get locations
        chef_profile = ChefProfile.query.get(order.chef_id)
        customer_profile = CustomerProfile.query.filter_by(user_id=order.customer_id).first()
        
        if not chef_profile or not chef_profile.lat or not chef_profile.long:
            return jsonify({'error': 'Chef location not available'}), 400
        if not customer_profile or not customer_profile.location_lat or not customer_profile.location_long:
            return jsonify({'error': 'Customer location not available'}), 400
        
        # Use Google Maps Directions API (requires API key in env)
        GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
        
        pickup_route_data = None
        delivery_route_data = None
        pickup_distance = 0
        pickup_duration = 0
        delivery_distance = 0
        delivery_duration = 0
        
        if GOOGLE_MAPS_API_KEY:
            # Route: driver current location -> chef location (pickup)
            pickup_url = (
                f"https://maps.googleapis.com/maps/api/directions/json?"
                f"origin={driver.current_lat},{driver.current_long}&"
                f"destination={chef_profile.lat},{chef_profile.long}&"
                f"key={GOOGLE_MAPS_API_KEY}"
            )
            pickup_resp = requests.get(pickup_url, timeout=10)
            if pickup_resp.status_code == 200:
                pickup_data = pickup_resp.json()
                if pickup_data.get('routes'):
                    route = pickup_data['routes'][0]
                    pickup_route_data = json.dumps(route)
                    if route.get('legs'):
                        leg = route['legs'][0]
                        pickup_distance = leg['distance']['value'] / 1000  # Convert to km
                        pickup_duration = leg['duration']['value'] // 60  # Convert to minutes
            
            # Route: chef location -> customer location (delivery)
            delivery_url = (
                f"https://maps.googleapis.com/maps/api/directions/json?"
                f"origin={chef_profile.lat},{chef_profile.long}&"
                f"destination={customer_profile.location_lat},{customer_profile.location_long}&"
                f"key={GOOGLE_MAPS_API_KEY}"
            )
            delivery_resp = requests.get(delivery_url, timeout=10)
            if delivery_resp.status_code == 200:
                delivery_data = delivery_resp.json()
                if delivery_data.get('routes'):
                    route = delivery_data['routes'][0]
                    delivery_route_data = json.dumps(route)
                    if route.get('legs'):
                        leg = route['legs'][0]
                        delivery_distance = leg['distance']['value'] / 1000
                        delivery_duration = leg['duration']['value'] // 60
        else:
            # Fallback: simple distance calculation (Haversine formula)
            from math import radians, cos, sin, asin, sqrt
            def haversine(lon1, lat1, lon2, lat2):
                lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
                dlon, dlat = lon2 - lon1, lat2 - lat1
                a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                c = 2 * asin(sqrt(a))
                return c * 6371  # km
            
            pickup_distance = haversine(
                driver.current_long, driver.current_lat,
                chef_profile.long, chef_profile.lat
            )
            pickup_duration = int(pickup_distance / 30 * 60)  # Assume 30 km/h
            
            delivery_distance = haversine(
                chef_profile.long, chef_profile.lat,
                customer_profile.location_long, customer_profile.location_lat
            )
            delivery_duration = int(delivery_distance / 30 * 60)
        
        # Create or update route
        route = RouteNavigation.query.filter_by(order_id=order_id).first()
        if not route:
            route = RouteNavigation(
                order_id=order_id,
                driver_id=driver.id
            )
            db.session.add(route)
        
        route.pickup_route_json = pickup_route_data
        route.pickup_distance_km = pickup_distance
        route.pickup_duration_mins = pickup_duration
        route.delivery_route_json = delivery_route_data
        route.delivery_distance_km = delivery_distance
        route.delivery_duration_mins = delivery_duration
        route.eta_pickup = datetime.utcnow() + timedelta(minutes=pickup_duration)
        route.eta_delivery = datetime.utcnow() + timedelta(minutes=pickup_duration + delivery_duration)
        route.current_lat = driver.current_lat
        route.current_long = driver.current_long
        
        db.session.commit()
        
        return jsonify({
            'message': 'Route created successfully',
            'route': route.to_dict()
        }), 201
        
    except requests.RequestException as e:
        logger.error(f'Google Maps API error: {str(e)}')
        return jsonify({'error': 'Failed to fetch route data'}), 500
    except Exception as e:
        logger.error(f'Create route error: {str(e)}')
        return jsonify({'error': 'Failed to create route'}), 500

@navigation_bp.route('/active-orders', methods=['GET'])
@jwt_required()
def get_active_orders():
    """Get driver's active delivery orders with navigation"""
    user_id = get_jwt_identity()
    driver = DriverProfile.query.filter_by(user_id=user_id).first()
    
    if not driver:
        return jsonify({'error': 'Driver not found'}), 404
    
    # Get active orders
    orders = Order.query.filter(
        Order.driver_id == driver.id,
        Order.status.in_(['delivering', 'ready'])
    ).all()
    
    result = []
    for order in orders:
        route = RouteNavigation.query.filter_by(order_id=order.id).first()
        result.append({
            'order': order.to_dict(),
            'route': route.to_dict() if route else None
        })
    
    return jsonify({'active_orders': result, 'count': len(result)}), 200

# ============================================================
# NOTIFICATION ROUTES
# ============================================================

@notification_bp.route('/send', methods=['POST'])
@jwt_required()
def send_notification():
    """
    Send notification to user(s)
    Expected: { 'user_ids': [1, 2], 'title': 'str', 'message': 'str', 'type': 'order_status', 'data': {...} }
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only admins and system can send notifications
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    user_ids = data.get('user_ids', [])
    title = data.get('title', '')
    message = data.get('message', '')
    notification_type = data.get('type', 'general')
    extra_data = data.get('data', {})
    order_id = data.get('order_id')
    
    if not user_ids or not title or not message:
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        created_notifications = []
        for uid in user_ids:
            notif = Notification(
                user_id=uid,
                title=title,
                message=message,
                notification_type=notification_type,
                order_id=order_id,
                data=extra_data
            )
            db.session.add(notif)
            created_notifications.append(notif)
        
        db.session.commit()
        
        # Send push notifications via FCM if device tokens exist
        for uid in user_ids:
            tokens = DeviceToken.query.filter_by(user_id=uid, is_active=True).all()
            if tokens and os.getenv('FCM_SERVER_KEY'):
                send_fcm_notifications(tokens, title, message, extra_data)
        
        return jsonify({
            'message': 'Notifications sent',
            'count': len(created_notifications)
        }), 201
        
    except Exception as e:
        logger.error(f'Send notification error: {str(e)}')
        return jsonify({'error': 'Failed to send notifications'}), 500

def send_fcm_notifications(device_tokens, title, message, data):
    """Send Firebase Cloud Messaging notifications"""
    FCM_SERVER_KEY = os.getenv('FCM_SERVER_KEY')
    FCM_URL = 'https://fcm.googleapis.com/fcm/send'
    
    headers = {
        'Authorization': f'key={FCM_SERVER_KEY}',
        'Content-Type': 'application/json'
    }
    
    for token_obj in device_tokens:
        payload = {
            'to': token_obj.token,
            'notification': {
                'title': title,
                'body': message,
                'sound': 'default'
            },
            'data': data
        }
        
        try:
            response = requests.post(FCM_URL, json=payload, headers=headers, timeout=10)
            if response.status_code == 200:
                token_obj.is_sent = True
                token_obj.sent_at = datetime.utcnow()
            logger.info(f'FCM sent to token: {token_obj.token[:20]}...')
        except Exception as e:
            logger.error(f'FCM send error: {str(e)}')

@notification_bp.route('/list', methods=['GET'])
@jwt_required()
def get_notifications():
    """Get user's notifications"""
    user_id = get_jwt_identity()
    unread_only = request.args.get('unread_only', 'false').lower() == 'true'
    limit = request.args.get('limit', 50, type=int)
    
    query = Notification.query.filter_by(user_id=user_id)
    if unread_only:
        query = query.filter_by(is_read=False)
    
    notifications = query.order_by(Notification.created_at.desc()).limit(limit).all()
    
    return jsonify({
        'count': len(notifications),
        'notifications': [n.to_dict() for n in notifications]
    }), 200

@notification_bp.route('/<int:notification_id>/read', methods=['PUT'])
@jwt_required()
def mark_notification_read(notification_id):
    """Mark notification as read"""
    user_id = get_jwt_identity()
    notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
    
    if not notification:
        return jsonify({'error': 'Notification not found'}), 404
    
    notification.is_read = True
    db.session.commit()
    
    return jsonify({'message': 'Notification marked as read'}), 200

@notification_bp.route('/device-token/register', methods=['POST'])
@jwt_required()
def register_device_token():
    """Register device token for push notifications"""
    user_id = get_jwt_identity()
    data = request.get_json()
    device_token = data.get('device_token')
    platform = data.get('platform', 'web')  # android, ios, web
    
    if not device_token:
        return jsonify({'error': 'Device token required'}), 400
    
    try:
        # Check if already registered
        existing = DeviceToken.query.filter_by(token=device_token).first()
        if existing:
            existing.user_id = user_id
            existing.is_active = True
            existing.last_used = datetime.utcnow()
        else:
            token_obj = DeviceToken(
                user_id=user_id,
                token=device_token,
                platform=platform
            )
            db.session.add(token_obj)
        
        db.session.commit()
        return jsonify({'message': 'Device token registered'}), 201
        
    except Exception as e:
        logger.error(f'Register device token error: {str(e)}')
        return jsonify({'error': 'Failed to register device token'}), 500

# ============================================================
# HEATMAP ROUTES
# ============================================================

@heatmap_bp.route('/zones', methods=['GET'])
@jwt_required()
def get_heatmap_zones():
    """
    Get heatmap zones based on user role
    Query params: time_range (daily/weekly/monthly), radius_km (for chef)
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    time_range = request.args.get('time_range', 'daily')
    
    try:
        query = HeatmapZone.query
        
        if user.role == 'admin':
            # Admin sees all zones
            zones = query.all()
        elif user.role == 'chef':
            # Chef sees zones near his kitchen
            chef_profile = ChefProfile.query.filter_by(user_id=user_id).first()
            if chef_profile and chef_profile.lat and chef_profile.long:
                zones = query.all()
                # Filter by distance (25 km)
                from math import radians, cos, sin, asin, sqrt
                def haversine(lon1, lat1, lon2, lat2):
                    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
                    dlon, dlat = lon2 - lon1, lat2 - lat1
                    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                    c = 2 * asin(sqrt(a))
                    return c * 6371
                
                zones = [
                    z for z in zones
                    if haversine(chef_profile.long, chef_profile.lat, z.center_long, z.center_lat) <= 25
                ]
            else:
                zones = []
        elif user.role == 'driver':
            # Driver sees all zones (general demand visualization)
            zones = query.all()
        else:
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify({
            'zones': [z.to_dict() for z in zones],
            'time_range': time_range,
            'count': len(zones)
        }), 200
        
    except Exception as e:
        logger.error(f'Get heatmap zones error: {str(e)}')
        return jsonify({'error': 'Failed to get heatmap data'}), 500

@heatmap_bp.route('/raw-points', methods=['GET'])
@jwt_required()
def get_heatmap_raw_points():
    """Get raw heatmap data points (granular data)"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    # Only admin and operations team can see raw points
    if user.role not in ['admin', 'chef']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        days_back = request.args.get('days', 7, type=int)
        since_date = datetime.utcnow() - timedelta(days=days_back)
        
        points = HeatmapDataPoint.query.filter(
            HeatmapDataPoint.timestamp >= since_date
        ).all()
        
        return jsonify({
            'points': [p.to_dict() for p in points],
            'count': len(points),
            'time_range': f'Last {days_back} days'
        }), 200
        
    except Exception as e:
        logger.error(f'Get raw points error: {str(e)}')
        return jsonify({'error': 'Failed to get heatmap points'}), 500

@heatmap_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_heatmap_stats():
    """Get heatmap statistics"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        total_zones = HeatmapZone.query.count()
        high_demand = HeatmapZone.query.filter(HeatmapZone.demand_intensity >= 75).count()
        medium_demand = HeatmapZone.query.filter(
            (HeatmapZone.demand_intensity >= 50) & (HeatmapZone.demand_intensity < 75)
        ).count()
        
        return jsonify({
            'total_zones': total_zones,
            'high_demand_zones': high_demand,
            'medium_demand_zones': medium_demand,
            'low_demand_zones': total_zones - high_demand - medium_demand
        }), 200
        
    except Exception as e:
        logger.error(f'Get stats error: {str(e)}')
        return jsonify({'error': 'Failed to get statistics'}), 500

# Register blueprints in app
def register_navigation_blueprints(app):
    """Register all navigation-related blueprints"""
    app.register_blueprint(navigation_bp)
    app.register_blueprint(notification_bp)
    app.register_blueprint(heatmap_bp)
