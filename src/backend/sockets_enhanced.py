"""
Enhanced Socket.IO handlers for real-time navigation, push notifications & heatmap
"""
import os
import jwt
from datetime import datetime
from flask_socketio import emit, join_room, leave_room, rooms
from backend.socket_instance import socketio
from backend.models_enhanced import (
    db, User, DriverProfile, CustomerProfile, ChefProfile, Order, 
    DeviceToken, Notification, RouteNavigation, NavigationSession, HeatmapDataPoint
)
import logging

logger = logging.getLogger(__name__)

# ============================================================
# CONNECTION MANAGEMENT
# ============================================================

@socketio.on('connect')
def handle_connect():
    """Handle new WebSocket connection"""
    print(f'Client connected: {request.sid}')
    emit('connect_response', {'data': 'Connected to server'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle WebSocket disconnection"""
    print(f'Client disconnected: {request.sid}')
    # Clean up active navigation sessions for this socket
    NavSession = NavigationSession.query.filter_by(socket_id=request.sid).first()
    if NavSession:
        NavSession.is_active = False
        NavSession.ended_at = datetime.utcnow()
        db.session.commit()

# ============================================================
# AUTHENTICATION & ROOM MANAGEMENT
# ============================================================

@socketio.on('auth_join')
def on_auth_join(data):
    """
    Authenticate user and join role-based rooms
    Expected data: { 'token': 'jwt_token' }
    """
    token = data.get('token')
    if not token:
        emit('auth_error', {'message': 'No token provided'})
        return
    
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        uid = payload['sub']
        user = User.query.get(uid)
        
        if not user:
            emit('auth_error', {'message': 'User not found'})
            return
        
        # Join role-based room
        room_name = f"{user.role}_{user.id}"  # customer_1, chef_2, driver_3
        join_room(room_name)
        
        # Additional rooms based on role
        if user.role == 'driver':
            join_room('drivers_all')  # Join driver pool for assignment notifications
        elif user.role == 'admin':
            join_room('admin_notifications')
        
        emit('auth_success', {
            'message': f'Joined as {user.role}',
            'user_id': user.id,
            'role': user.role,
            'room': room_name
        })
        
    except jwt.ExpiredSignatureError:
        emit('auth_error', {'message': 'Token expired'})
    except jwt.InvalidTokenError:
        emit('auth_error', {'message': 'Invalid token'})
    except Exception as e:
        logger.error(f'Auth error: {str(e)}')
        emit('auth_error', {'message': 'Authentication failed'})

# ============================================================
# REAL-TIME LOCATION & NAVIGATION
# ============================================================

@socketio.on('start_navigation')
def on_start_navigation(data):
    """
    Start navigation session for a driver on an order
    Expected data: { 'token': 'jwt_token', 'order_id': 123 }
    """
    token = data.get('token')
    order_id = data.get('order_id')
    
    if not token or not order_id:
        emit('nav_error', {'message': 'Missing required fields'})
        return
    
    try:
        # Verify token
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        user_id = payload['sub']
        user = User.query.get(user_id)
        
        if not user or user.role != 'driver':
            emit('nav_error', {'message': 'Only drivers can start navigation'})
            return
        
        # Get order and verify driver assignment
        order = Order.query.get(order_id)
        driver_profile = DriverProfile.query.filter_by(user_id=user_id).first()
        
        if not order or order.driver_id != driver_profile.id:
            emit('nav_error', {'message': 'Not assigned to this order'})
            return
        
        # Get or create route
        route = RouteNavigation.query.filter_by(order_id=order_id).first()
        if not route:
            route = RouteNavigation(
                order_id=order_id,
                driver_id=driver_profile.id,
                current_lat=driver_profile.current_lat,
                current_long=driver_profile.current_long
            )
            db.session.add(route)
            db.session.commit()
        
        # Create or update navigation session
        nav_session = NavigationSession.query.filter_by(order_id=order_id).first()
        if nav_session:
            nav_session.is_active = True
            nav_session.socket_id = request.sid
        else:
            nav_session = NavigationSession(
                order_id=order_id,
                driver_id=driver_profile.id,
                socket_id=request.sid
            )
            db.session.add(nav_session)
        
        db.session.commit()
        
        # Notify customer that navigation started
        emit('navigation_started', {
            'order_id': order_id,
            'driver_id': driver_profile.id,
            'status': 'driver_started'
        }, to=f'customer_{order.customer_id}')
        
        # Confirm to driver
        emit('nav_success', {
            'message': 'Navigation started',
            'order_id': order_id,
            'current_leg': route.current_leg,
            'route': route.to_dict()
        })
        
    except jwt.InvalidTokenError:
        emit('nav_error', {'message': 'Invalid token'})
    except Exception as e:
        logger.error(f'Start navigation error: {str(e)}')
        emit('nav_error', {'message': 'Failed to start navigation'})

@socketio.on('update_location')
def on_update_location(data):
    """
    Update driver's current location during navigation
    Expected data: { 'token': 'jwt_token', 'order_id': 123, 'lat': 30.0444, 'long': 31.2357 }
    """
    token = data.get('token')
    order_id = data.get('order_id')
    lat = data.get('lat')
    long = data.get('long')
    
    if not all([token, order_id, lat is not None, long is not None]):
        emit('location_error', {'message': 'Missing required fields'})
        return
    
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        user_id = payload['sub']
        driver_profile = DriverProfile.query.filter_by(user_id=user_id).first()
        
        if not driver_profile:
            emit('location_error', {'message': 'Driver not found'})
            return
        
        # Update driver profile location
        driver_profile.current_lat = lat
        driver_profile.current_long = long
        
        # Update route navigation
        route = RouteNavigation.query.filter_by(order_id=order_id).first()
        if route:
            route.current_lat = lat
            route.current_long = long
            route.last_updated = datetime.utcnow()
        
        db.session.commit()
        
        # Get order details for broadcasting
        order = Order.query.get(order_id)
        if order:
            # Broadcast location to customer
            emit('driver_location_update', {
                'order_id': order_id,
                'driver_id': driver_profile.id,
                'latitude': lat,
                'longitude': long,
                'timestamp': datetime.utcnow().isoformat(),
                'current_leg': route.current_leg if route else 'unknown'
            }, to=f'customer_{order.customer_id}')
            
            # Broadcast to admin/dispatch
            emit('driver_location_update_admin', {
                'order_id': order_id,
                'driver_id': driver_profile.id,
                'driver_name': driver_profile.user.name,
                'latitude': lat,
                'longitude': long,
                'timestamp': datetime.utcnow().isoformat()
            }, to='admin_notifications')
        
        emit('location_update_success', {'message': 'Location updated'})
        
    except jwt.InvalidTokenError:
        emit('location_error', {'message': 'Invalid token'})
    except Exception as e:
        logger.error(f'Update location error: {str(e)}')
        emit('location_error', {'message': 'Failed to update location'})

@socketio.on('leg_completed')
def on_leg_completed(data):
    """
    Driver indicates completion of a leg (pickup or delivery)
    Expected data: { 'token': 'jwt_token', 'order_id': 123 }
    """
    token = data.get('token')
    order_id = data.get('order_id')
    
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        user_id = payload['sub']
        driver_profile = DriverProfile.query.filter_by(user_id=user_id).first()
        
        order = Order.query.get(order_id)
        route = RouteNavigation.query.filter_by(order_id=order_id).first()
        
        if not order or not route:
            emit('nav_error', {'message': 'Order or route not found'})
            return
        
        if route.current_leg == 'pickup':
            # Completed pickup, move to delivery
            route.current_leg = 'delivery'
            order.status = 'delivering'
            
            # Create notification
            notification = Notification(
                user_id=order.customer_id,
                title='Driver Started Delivery',
                message=f'{driver_profile.user.name} is delivering your order',
                notification_type='driver_started_delivery',
                order_id=order_id,
                data={'driver_id': driver_profile.id, 'driver_name': driver_profile.user.name}
            )
            db.session.add(notification)
            
            emit('leg_update', {
                'order_id': order_id,
                'current_leg': 'delivery',
                'message': 'Driver picked up food and is now delivering'
            }, to=f'customer_{order.customer_id}')
            
        elif route.current_leg == 'delivery':
            # Completed delivery
            route.current_leg = 'completed'
            order.status = 'delivered'
            
            # End navigation session
            nav_session = NavigationSession.query.filter_by(order_id=order_id).first()
            if nav_session:
                nav_session.is_active = False
                nav_session.ended_at = datetime.utcnow()
            
            # Record heatmap data point
            if not order.heatmap_recorded and order.customer_lat and order.customer_long:
                heatmap_point = HeatmapDataPoint(
                    order_id=order_id,
                    latitude=order.customer_lat,
                    longitude=order.customer_long,
                    day_of_week=datetime.now().weekday(),
                    hour_of_day=datetime.now().hour
                )
                db.session.add(heatmap_point)
                order.heatmap_recorded = True
            
            # Create notification
            notification = Notification(
                user_id=order.customer_id,
                title='Order Delivered',
                message=f'Your order from {order.chef.user.name} has been delivered',
                notification_type='order_delivered',
                order_id=order_id,
                data={'driver_id': driver_profile.id}
            )
            db.session.add(notification)
            
            emit('order_completed', {
                'order_id': order_id,
                'status': 'delivered',
                'message': 'Your order has been delivered!'
            }, to=f'customer_{order.customer_id}')
        
        db.session.commit()
        emit('leg_completed_success', {'message': 'Leg completed', 'current_leg': route.current_leg})
        
    except jwt.InvalidTokenError:
        emit('nav_error', {'message': 'Invalid token'})
    except Exception as e:
        logger.error(f'Leg completed error: {str(e)}')
        emit('nav_error', {'message': 'Failed to update leg'})

# ============================================================
# PUSH NOTIFICATIONS
# ============================================================

@socketio.on('register_device_token')
def on_register_device_token(data):
    """
    Register device token for push notifications
    Expected data: { 'token': 'jwt_token', 'device_token': 'fcm_token', 'platform': 'android|ios|web' }
    """
    jwt_token = data.get('token')
    device_token = data.get('device_token')
    platform = data.get('platform', 'web')
    
    if not jwt_token or not device_token:
        emit('token_error', {'message': 'Missing required fields'})
        return
    
    try:
        payload = jwt.decode(jwt_token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        user_id = payload['sub']
        
        # Check if token already registered
        existing = DeviceToken.query.filter_by(token=device_token).first()
        if existing:
            existing.is_active = True
            existing.last_used = datetime.utcnow()
        else:
            dev_token = DeviceToken(
                user_id=user_id,
                token=device_token,
                platform=platform
            )
            db.session.add(dev_token)
        
        db.session.commit()
        emit('token_registered', {'message': 'Device token registered successfully'})
        
    except jwt.InvalidTokenError:
        emit('token_error', {'message': 'Invalid token'})
    except Exception as e:
        logger.error(f'Register device token error: {str(e)}')
        emit('token_error', {'message': 'Failed to register device token'})

@socketio.on('get_notifications')
def on_get_notifications(data):
    """
    Get user's notifications
    Expected data: { 'token': 'jwt_token', 'unread_only': True/False }
    """
    jwt_token = data.get('token')
    unread_only = data.get('unread_only', True)
    
    try:
        payload = jwt.decode(jwt_token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        user_id = payload['sub']
        
        query = Notification.query.filter_by(user_id=user_id)
        if unread_only:
            query = query.filter_by(is_read=False)
        
        notifications = query.order_by(Notification.created_at.desc()).limit(50).all()
        
        emit('notifications_list', {
            'count': len(notifications),
            'notifications': [n.to_dict() for n in notifications]
        })
        
    except jwt.InvalidTokenError:
        emit('notification_error', {'message': 'Invalid token'})
    except Exception as e:
        logger.error(f'Get notifications error: {str(e)}')
        emit('notification_error', {'message': 'Failed to get notifications'})

@socketio.on('mark_notification_read')
def on_mark_notification_read(data):
    """Mark notification as read"""
    jwt_token = data.get('token')
    notification_id = data.get('notification_id')
    
    try:
        payload = jwt.decode(jwt_token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        user_id = payload['sub']
        
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notification:
            notification.is_read = True
            db.session.commit()
            emit('notification_updated', {'notification_id': notification_id, 'is_read': True})
        
    except jwt.InvalidTokenError:
        emit('notification_error', {'message': 'Invalid token'})
    except Exception as e:
        logger.error(f'Mark notification read error: {str(e)}')

# ============================================================
# HEATMAP DATA
# ============================================================

@socketio.on('get_heatmap_data')
def on_get_heatmap_data(data):
    """
    Get heatmap data based on user role and location
    Expected data: { 'token': 'jwt_token', 'time_range': 'daily|weekly|monthly', 'radius_km': 25 }
    """
    jwt_token = data.get('token')
    time_range = data.get('time_range', 'daily')
    
    try:
        payload = jwt.decode(jwt_token, os.getenv("SECRET_KEY", "secret"), algorithms=["HS256"])
        user_id = payload['sub']
        user = User.query.get(user_id)
        
        if not user:
            emit('heatmap_error', {'message': 'User not found'})
            return
        
        # Role-based heatmap filtering
        query = HeatmapZone.query
        
        if user.role == 'admin':
            # Admin sees all zones
            pass
        elif user.role == 'chef':
            # Chef sees zones near his kitchen
            chef_profile = ChefProfile.query.filter_by(user_id=user_id).first()
            if chef_profile and chef_profile.lat and chef_profile.long:
                # Get zones within 25 km
                from math import radians, cos, sin, asin, sqrt
                def haversine(lon1, lat1, lon2, lat2):
                    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
                    dlon, dlat = lon2 - lon1, lat2 - lat1
                    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                    c = 2 * asin(sqrt(a))
                    return c * 6371  # Radius of earth in km
                
                all_zones = query.all()
                nearby_zones = [
                    z for z in all_zones 
                    if haversine(chef_profile.long, chef_profile.lat, z.center_long, z.center_lat) <= 25
                ]
                query = nearby_zones
        elif user.role == 'driver':
            # Driver sees zones where drivers typically work
            # This could be based on historical delivery areas
            pass
        
        # If query is list (from manual filtering), convert to proper response
        if isinstance(query, list):
            zones = query
        else:
            zones = query.all()
        
        emit('heatmap_data', {
            'zones': [z.to_dict() if hasattr(z, 'to_dict') else z for z in zones],
            'time_range': time_range,
            'access_level': user.role
        })
        
    except jwt.InvalidTokenError:
        emit('heatmap_error', {'message': 'Invalid token'})
    except Exception as e:
        logger.error(f'Get heatmap data error: {str(e)}')
        emit('heatmap_error', {'message': 'Failed to get heatmap data'})
