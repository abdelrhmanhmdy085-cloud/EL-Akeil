"""
Enhanced Models with Navigation, Push Notifications & Heatmap Support
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json

db = SQLAlchemy()

# ============================================================
# EXISTING MODELS (keeping all existing functionality)
# ============================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    chef_profile = db.relationship("ChefProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    customer_profile = db.relationship("CustomerProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    driver_profile = db.relationship("DriverProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    device_tokens = db.relationship("DeviceToken", backref="user", lazy=True, cascade="all, delete-orphan")
    notifications = db.relationship("Notification", backref="user", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        data = { "id": self.id, "username": self.username, "name": self.name, "role": self.role, "created_at": self.created_at.isoformat() }
        if self.role == 'chef' and self.chef_profile: data.update(self.chef_profile.to_dict())
        elif self.role == 'customer' and self.customer_profile: data.update(self.customer_profile.to_dict())
        elif self.role == 'driver' and self.driver_profile: data.update(self.driver_profile.to_dict())
        return data

class ChefProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    national_id = db.Column(db.String(50), unique=True, nullable=True)
    address = db.Column(db.String(500), nullable=True)
    lat = db.Column(db.Float, nullable=True)
    long = db.Column(db.Float, nullable=True)
    prep_time_avg = db.Column(db.Integer, default=30)
    dishes = db.relationship("Dish", backref="chef", lazy=True, cascade="all, delete-orphan")
    reviews = db.relationship("Review", backref="chef", lazy=True)
    orders = db.relationship("Order", backref="chef", lazy=True)

    def to_dict(self): 
        avg = 0
        if self.reviews:
            avg = sum([r.rating for r in self.reviews]) / len(self.reviews)
        return { 
            "id": self.id,
            "address": self.address, 
            "prep_time_avg": self.prep_time_avg,
            "rating": round(avg, 1),
            "review_count": len(self.reviews),
            "location": {"lat": self.lat, "long": self.long}
        }

class CustomerProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    location_lat = db.Column(db.Float, nullable=True)
    location_long = db.Column(db.Float, nullable=True)

    def to_dict(self): 
        return { 
            "phone": self.phone, 
            "location": {"lat": self.location_lat, "long": self.location_long} 
        }

class DriverProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    national_id = db.Column(db.String(50), unique=True, nullable=False)
    face_id_data = db.Column(db.Text, nullable=True)
    current_lat = db.Column(db.Float, nullable=True)
    current_long = db.Column(db.Float, nullable=True)
    is_available = db.Column(db.Boolean, default=False)
    vehicle_type = db.Column(db.String(50), nullable=True)  # motorcycle, scooter, car
    license_number = db.Column(db.String(100), nullable=True)
    phone_number = db.Column(db.String(20), nullable=True)

    def to_dict(self): 
        return { 
            "national_id": self.national_id, 
            "face_id_set": bool(self.face_id_data), 
            "location": {"lat": self.current_lat, "long": self.current_long},
            "is_available": self.is_available,
            "vehicle_type": self.vehicle_type,
            "license_number": self.license_number,
            "phone_number": self.phone_number
        }

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chef_profile_id = db.Column(db.Integer, db.ForeignKey('chef_profile.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)  # NEW
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=True)  # NEW
    prep_time = db.Column(db.Integer, default=15)
    image_url = db.Column(db.String(500), nullable=True)
    is_available = db.Column(db.Boolean, default=True)  # NEW
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Legacy fields (for backward compatibility)
    category = db.Column(db.String(50), nullable=True)
    food_level = db.Column(db.String(50), nullable=True)
    occasion_tag = db.Column(db.String(50), nullable=True)
    
    # Relationships
    chef_profile = db.relationship("ChefProfile", backref=db.backref("dishes_alt", lazy=True))
    category_obj = db.relationship("Category", backref="dishes_obj")
    level_obj = db.relationship("Level", backref="dishes_level")
    
    def to_dict(self): 
        chef_user_id = None
        if self.chef_profile and self.chef_profile.user_id:
            chef_user_id = self.chef_profile.user_id
        
        cat_name = self.category # Fallback
        if hasattr(self, 'category_obj') and self.category_obj:
            cat_name = self.category_obj.name_en

        lvl_name = self.food_level # Fallback
        if hasattr(self, 'level_obj') and self.level_obj:
            lvl_name = self.level_obj.name_en

        return { 
            "id": self.id, 
            "name": self.name, 
            "price": self.price, 
            "description": self.description, 
            "chef_id": self.chef_profile_id,
            "user_id": chef_user_id,
            "category_id": self.category_id,
            "level_id": self.level_id,
            "category_name": cat_name,
            "level_name": lvl_name,
            "prep_time": self.prep_time, 
            "image_url": self.image_url,
            "is_available": self.is_available,
            "rating": self.chef_profile.to_dict().get('rating', 0) if self.chef_profile else 0,
            "chef_name": self.chef_profile.user.name if self.chef_profile and self.chef_profile.user else "Unknown"
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef_profile.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # New FKs
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=True)

    def to_dict(self):
        cat_obj = self.category_obj.to_dict() if self.category_obj else None
        lvl_obj = self.level_obj.to_dict() if self.level_obj else None
        
        return {
            "id": self.id,
            "rating": self.rating,
            "comment": self.comment,
            "customer_id": self.customer_id,
            "created_at": self.created_at.isoformat(),
            # Include extended info if available
            "category_info": cat_obj,
            "level_info": lvl_obj
        }




class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('chef_profile.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver_profile.id'), nullable=True)
    status = db.Column(db.String(50), default='pending') # pending, cooking, ready, delivering, delivered
    items = db.Column(db.Text, nullable=False) # JSON string
    total_price = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # NAVIGATION & LOCATION TRACKING (NEW)
    customer_lat = db.Column(db.Float, nullable=True)
    customer_long = db.Column(db.Float, nullable=True)
    chef_lat = db.Column(db.Float, nullable=True)
    chef_long = db.Column(db.Float, nullable=True)
    # For heatmap
    heatmap_recorded = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "chef_id": self.chef_id,
            "driver_id": self.driver_id,
            "status": self.status,
            "items": self.items,
            "total_price": self.total_price,
            "created_at": self.created_at.isoformat(),
            "customer_location": {"lat": self.customer_lat, "long": self.customer_long},
            "chef_location": {"lat": self.chef_lat, "long": self.chef_long}
        }

# ============================================================
# NEW MODELS FOR NAVIGATION, PUSH NOTIFICATIONS & HEATMAP
# ============================================================

class DeviceToken(db.Model):
    """Store device tokens for push notifications (FCM or Web Push)"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.Text, nullable=False, unique=True)  # Encrypted FCM token
    platform = db.Column(db.String(50), nullable=False)  # 'android', 'ios', 'web'
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "platform": self.platform,
            "is_active": self.is_active,
            "last_used": self.last_used.isoformat()
        }

class Notification(db.Model):
    """Store notifications with delivery status"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # order_accepted, driver_nearby, etc.
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    is_sent = db.Column(db.Boolean, default=False)
    sent_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    data = db.Column(db.JSON, nullable=True)  # Additional data (lat, long, etc.)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "notification_type": self.notification_type,
            "order_id": self.order_id,
            "is_read": self.is_read,
            "is_sent": self.is_sent,
            "created_at": self.created_at.isoformat(),
            "data": self.data
        }

class RouteNavigation(db.Model):
    """Store route navigation for orders"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False, unique=True)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver_profile.id'), nullable=False)
    
    # Route from driver to chef pickup
    pickup_route_json = db.Column(db.Text, nullable=True)  # GeoJSON or encoded polyline
    pickup_distance_km = db.Column(db.Float, nullable=True)
    pickup_duration_mins = db.Column(db.Integer, nullable=True)
    
    # Route from chef to customer delivery
    delivery_route_json = db.Column(db.Text, nullable=True)  # GeoJSON or encoded polyline
    delivery_distance_km = db.Column(db.Float, nullable=True)
    delivery_duration_mins = db.Column(db.Integer, nullable=True)
    
    # Current leg (pickup or delivery)
    current_leg = db.Column(db.String(20), default='pickup')  # 'pickup' or 'delivery'
    current_lat = db.Column(db.Float, nullable=True)
    current_long = db.Column(db.Float, nullable=True)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)
    
    # ETA
    eta_pickup = db.Column(db.DateTime, nullable=True)
    eta_delivery = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "driver_id": self.driver_id,
            "pickup": {
                "distance_km": self.pickup_distance_km,
                "duration_mins": self.pickup_duration_mins,
                "eta": self.eta_pickup.isoformat() if self.eta_pickup else None
            },
            "delivery": {
                "distance_km": self.delivery_distance_km,
                "duration_mins": self.delivery_duration_mins,
                "eta": self.eta_delivery.isoformat() if self.eta_delivery else None
            },
            "current_leg": self.current_leg,
            "current_location": {"lat": self.current_lat, "long": self.current_long}
        }

class HeatmapDataPoint(db.Model):
    """Store order locations for heatmap generation"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    # For analytics
    day_of_week = db.Column(db.Integer, nullable=True)  # 0=Monday, 6=Sunday
    hour_of_day = db.Column(db.Integer, nullable=True)  # 0-23

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "timestamp": self.timestamp.isoformat(),
            "day_of_week": self.day_of_week,
            "hour_of_day": self.hour_of_day
        }

class HeatmapZone(db.Model):
    """Pre-computed heatmap zones (for performance)"""
    id = db.Column(db.Integer, primary_key=True)
    # Grid cell reference (e.g., lat_10_lon_20 for lat 10°, lon 20°)
    grid_ref = db.Column(db.String(100), unique=True, nullable=False)
    center_lat = db.Column(db.Float, nullable=False)
    center_long = db.Column(db.Float, nullable=False)
    
    # Demand metrics
    order_count_daily = db.Column(db.Integer, default=0)
    order_count_weekly = db.Column(db.Integer, default=0)
    average_price = db.Column(db.Float, default=0)
    
    # Intensity level (0-100)
    demand_intensity = db.Column(db.Integer, default=0)  # 0=low, 50=medium, 100=high
    
    last_updated = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "grid_ref": self.grid_ref,
            "center": {"lat": self.center_lat, "long": self.center_long},
            "order_count": {"daily": self.order_count_daily, "weekly": self.order_count_weekly},
            "demand_intensity": self.demand_intensity,
            "last_updated": self.last_updated.isoformat()
        }

class NavigationSession(db.Model):
    """Track active navigation sessions for real-time updates"""
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    driver_id = db.Column(db.Integer, db.ForeignKey('driver_profile.id'), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    socket_id = db.Column(db.String(255), nullable=True)  # For WebSocket communication
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    ended_at = db.Column(db.DateTime, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "driver_id": self.driver_id,
            "is_active": self.is_active,
            "started_at": self.started_at.isoformat()
        }

# ============================================================
# CATEGORY & LEVEL MODELS (FOOD TAXONOMY)
# ============================================================

class Category(db.Model):
    """Food categories (Meat, Chicken, Seafood, etc.)"""
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(255), nullable=False, unique=True)
    name_en = db.Column(db.String(255), nullable=False, unique=True)
    icon = db.Column(db.String(255), nullable=True)  # Emoji or image URL
    description_ar = db.Column(db.Text, nullable=True)
    description_en = db.Column(db.Text, nullable=True)
    display_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    dishes = db.relationship("Dish", foreign_keys="Dish.category_id", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "icon": self.icon,
            "description_ar": self.description_ar,
            "description_en": self.description_en,
            "display_order": self.display_order,
            "dish_count": len(self.dishes) if self.dishes else 0
        }

class Level(db.Model):
    """Food levels (Fast, Home, Special, Healthy, Occasions)"""
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(255), nullable=False, unique=True)
    name_en = db.Column(db.String(255), nullable=False, unique=True)
    color_tag = db.Column(db.String(50), nullable=True)  # For UI styling
    icon = db.Column(db.String(255), nullable=True)  # Emoji or image URL
    description_ar = db.Column(db.Text, nullable=True)
    description_en = db.Column(db.Text, nullable=True)
    display_order = db.Column(db.Integer, default=0)
    is_special = db.Column(db.Boolean, default=False)  # For occasions/holidays
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    dishes = db.relationship("Dish", foreign_keys="Dish.level_id", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "color_tag": self.color_tag,
            "icon": self.icon,
            "description_ar": self.description_ar,
            "description_en": self.description_en,
            "display_order": self.display_order,
            "is_special": self.is_special,
            "dish_count": len(self.dishes) if self.dishes else 0
        }

