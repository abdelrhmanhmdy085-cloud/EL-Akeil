from flask import Blueprint, jsonify, request, current_app
import json
import jwt
from backend.models import db, Dish, User, Order, Review, ChefProfile, Category, Level
from backend.socket_instance import socketio
from datetime import datetime
import math

bp = Blueprint('customer', __name__)

def get_current_user():
    token = request.headers.get('Authorization').split(" ")[1]
    uid = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['sub']
    return User.query.get(uid)

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calculate distance between two points on Earth (in km)"""
    R = 6371  # Earth's radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    
    a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

# ---------------------------------------------------------
# NEW CATEGORY & LEVEL ENDPOINTS
# ---------------------------------------------------------
@bp.route("/categories", methods=["GET"])
def get_all_categories():
    cats = Category.query.all()
    return jsonify([c.to_dict() for c in cats])

@bp.route("/levels", methods=["GET"])
def get_all_levels():
    lvls = Level.query.all()
    return jsonify([l.to_dict() for l in lvls])

@bp.route("/category/<int:cat_id>/dishes", methods=["GET"])
def get_dishes_by_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    # Group dishes keys by Level
    dishes = Dish.query.filter_by(category_id=cat_id).all()
    
    # Manual grouping (or just return flat list and frontend groups)
    # Returning flat list is easier for standard API, but let's conform to requirement "Grouped visually"
    # Actually, returning a flat list with full metadata is flexible. 
    # But user asked for specific grouped response? 
    # "Displays: ... All dishes ... Grouped visually by food level" -> This is a UI requirement, API can return flat list.
    return jsonify({
        "category": cat.to_dict(),
        "dishes": [d.to_dict() for d in dishes]
    })

@bp.route("/level/<int:lvl_id>/dishes", methods=["GET"])
def get_dishes_by_level(lvl_id):
    lvl = Level.query.get_or_404(lvl_id)
    dishes = Dish.query.filter_by(level_id=lvl_id).all()
    
    return jsonify({
        "level": lvl.to_dict(),
        "dishes": [d.to_dict() for d in dishes]
    })

# ---------------------------------------------------------
# EXISTING ROUTES (Preserved)
# ---------------------------------------------------------

@bp.route("/chefs", methods=["GET"])
def list_chefs():
    """Get all chefs with their locations and ratings"""
    user_lat = request.args.get('lat', type=float)
    user_long = request.args.get('long', type=float)
    max_distance = request.args.get('max_distance', 50, type=float)  # km
    
    chefs = User.query.filter_by(role='chef').all()
    result = []
    
    for chef in chefs:
        if chef.chef_profile:
            chef_data = {
                "id": chef.id,
                "user_id": chef.id,
                "name": chef.name,
                "address": chef.chef_profile.address or "",
                "lat": chef.chef_profile.lat,
                "long": chef.chef_profile.long,
                "rating": chef.chef_profile.to_dict().get('rating', 0),
                "review_count": chef.chef_profile.to_dict().get('review_count', 0),
                "prep_time": chef.chef_profile.prep_time_avg or 30,
                "distance": None
            }
            
            # Calculate distance if user location provided
            if user_lat and user_long and chef.chef_profile.lat and chef.chef_profile.long:
                distance = haversine_distance(user_lat, user_long, 
                                             chef.chef_profile.lat, chef.chef_profile.long)
                chef_data["distance"] = round(distance, 2)
                
                # Filter by max distance
                if distance > max_distance:
                    continue
            
            result.append(chef_data)
    
    # Sort by distance if available
    if user_lat and user_long:
        result.sort(key=lambda x: x["distance"] if x["distance"] else float('inf'))
    
    return jsonify(result)

@bp.route("/dishes", methods=["GET"])
def public_dishes():
    category = request.args.get('category')
    food_level = request.args.get('food_level')
    occasion_tag = request.args.get('occasion_tag')
    
    query = Dish.query
    if category:
        query = query.filter_by(category=category)
    if food_level:
        query = query.filter_by(food_level=food_level)
    if occasion_tag:
        query = query.filter_by(occasion_tag=occasion_tag)
        
    dishes = query.all()
    return jsonify([d.to_dict() for d in dishes])

@bp.route("/order", methods=["POST"])
def place_order():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    items = data.get("items")  # List of {dish_id, qty, price}
    chef_id = data.get("chef_id")  # This should be user_id of chef
    
    if not items or not chef_id:
        return jsonify({"error": "Missing items or chef_id"}), 400
    
    # Get chef profile from chef user_id
    chef_user = User.query.get(chef_id)
    if not chef_user or chef_user.role != 'chef' or not chef_user.chef_profile:
        return jsonify({"error": "Invalid chef"}), 400
    
    chef_profile = chef_user.chef_profile
    total = sum([i['price'] * i['qty'] for i in items])

    order = Order(
        customer_id=user.id,
        chef_id=chef_profile.id,  # Use chef_profile.id
        items=json.dumps(items),
        total_price=total,
        status="pending",
        created_at=datetime.utcnow()
    )
    db.session.add(order)
    db.session.commit()
    
    # Notify Chef via Socket
    try:
        socketio.emit('new_order', {
            'id': order.id, 
            'dishes': items, 
            'status': 'pending',
            'customer': user.name or user.username,
            'total': total
        }, room=f"chef_{chef_id}")
    except Exception as e:
        print(f"Error notifying chef: {e}")
    
    return jsonify({"ok": True, "order_id": order.id})

@bp.route("/orders", methods=["GET"])
def my_orders():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 403
    
    orders = Order.query.filter_by(customer_id=user.id).order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders])

@bp.route("/review", methods=["POST"])
def submit_review():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    
    if not data.get("chef_id") or not data.get("rating"):
        return jsonify({"error": "Missing chef_id or rating"}), 400
    
    try:
        rating = int(data.get("rating"))
        if rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1-5"}), 400
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid rating"}), 400
    
    review = Review(
        customer_id=user.id,
        chef_id=data.get("chef_id"),
        rating=rating,
        comment=data.get("comment", ""),
        created_at=datetime.utcnow()
    )
    db.session.add(review)
    db.session.commit()
    return jsonify({"ok": True, "review_id": review.id})

@bp.route("/heatmap-data", methods=["GET"])
def get_heatmap_data():
    """Get heatmap data for completed orders (geographic distribution)"""
    # Get last 1000 completed orders with locations
    orders = Order.query.filter_by(status='delivered').order_by(Order.created_at.desc()).limit(1000).all()
    
    heatmap_points = []
    for order in orders:
        if order.customer_lat and order.customer_long:
            heatmap_points.append({
                "lat": order.customer_lat,
                "lng": order.customer_long,
                "intensity": 1  # Can be adjusted based on order value
            })
    
    return jsonify(heatmap_points)

@bp.route("/chef-analytics", methods=["GET"])
def get_chef_analytics():
    """Get analytics about active chefs and orders"""
    from datetime import datetime, timedelta
    
    # Count total and active chefs
    total_chefs = User.query.filter_by(role='chef').count()
    
    # Active chefs: have an order in last 24 hours
    last_24h = datetime.utcnow() - timedelta(hours=24)
    active_chef_ids = db.session.query(Order.chef_id).filter(
        Order.created_at >= last_24h
    ).distinct().all()
    active_chefs = len(active_chef_ids)
    
    # Orders today
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    orders_today = Order.query.filter(Order.created_at >= today_start).count()
    
    # Average rating
    avg_rating = 0
    reviews = Review.query.all()
    if reviews:
        avg_rating = sum([r.rating for r in reviews]) / len(reviews)
    
    return jsonify({
        "total_chefs": total_chefs,
        "active_chefs": active_chefs,
        "orders_today": orders_today,
        "avg_rating": round(avg_rating, 1)
    })

@bp.route("/busy-areas", methods=["GET"])
def get_busy_areas():
    """Identify busy/high-demand geographic areas"""
    from datetime import datetime, timedelta
    
    # Get orders from last 24 hours grouped by location
    last_24h = datetime.utcnow() - timedelta(hours=24)
    recent_orders = Order.query.filter(Order.created_at >= last_24h).all()
    
    # Group orders by proximity (simple grid-based approach)
    # Group into 0.1 degree squares (roughly 10km)
    areas = {}
    for order in recent_orders:
        if order.customer_lat and order.customer_long:
            # Round to nearest grid point
            grid_lat = round(order.customer_lat * 10) / 10
            grid_lng = round(order.customer_long * 10) / 10
            key = f"{grid_lat},{grid_lng}"
            
            if key not in areas:
                areas[key] = {"lat": grid_lat, "lng": grid_lng, "count": 0, "active_chefs": 0}
            
            areas[key]["count"] += 1
    
    # Calculate intensity and determine status
    busy_areas = []
    max_count = max([a["count"] for a in areas.values()]) if areas else 1
    
    for area in areas.values():
        intensity = area["count"] / max_count
        status = "low"
        if intensity >= 0.7:
            status = "critical"
        elif intensity >= 0.5:
            status = "high"
        elif intensity >= 0.3:
            status = "medium"
        
        # Count active chefs in this area
        area_chefs = ChefProfile.query.filter(
            ChefProfile.lat.between(area["lat"] - 0.05, area["lat"] + 0.05),
            ChefProfile.long.between(area["lng"] - 0.05, area["lng"] + 0.05)
        ).count()
        
        busy_areas.append({
            "lat": area["lat"],
            "lng": area["lng"],
            "intensity": intensity,
            "status": status,
            "order_count": area["count"],
            "active_chefs": area_chefs
        })
    
    # Sort by intensity
    busy_areas.sort(key=lambda x: x["intensity"], reverse=True)
    
    return jsonify(busy_areas[:20])  # Return top 20 busy areas
