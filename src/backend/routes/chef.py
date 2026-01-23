from flask import Blueprint, request, jsonify, current_app
import jwt
from backend.models import db, User, Dish, Order
from backend.socket_instance import socketio

bp = Blueprint('chef', __name__)

def get_chef_user():
    token = request.headers.get('Authorization').split(" ")[1]
    uid = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['sub']
    user = User.query.get(uid)
    return user if user and user.role == 'chef' else None

@bp.route("/dishes", methods=["GET", "POST"])
def handle_dishes():
    user = get_chef_user()
    if not user: return jsonify({"error": "Unauthorized"}), 403

    if request.method == "GET":
        return jsonify([d.to_dict() for d in user.chef_profile.dishes])
    
    data = request.get_json()
    dish = Dish(
        chef_profile_id=user.chef_profile.id,
        name=data.get("name"),
        price=data.get("price"),
        description=data.get("description"),
        category=data.get("category"),
        prep_time=data.get("prep_time"),
        image_url=data.get("image_url"),
        food_level=data.get("food_level", "home"),
        occasion_tag=data.get("occasion_tag")
    )
    db.session.add(dish)
    db.session.commit()
    return jsonify({"ok": True, "dish": dish.to_dict()})

@bp.route("/orders", methods=["GET"])
def chef_orders():
    user = get_chef_user()
    if not user: return jsonify({"error": "Unauthorized"}), 403
    orders = user.chef_profile.orders
    return jsonify([o.to_dict() for o in orders])

@bp.route("/order/<int:oid>/status", methods=["POST"])
def update_order_status(oid):
    user = get_chef_user()
    order = Order.query.get(oid)
    if order and order.chef_id == user.chef_profile.id:
        data = request.get_json()
        order.status = data.get("status") # cooking, ready
        if order.status == 'ready_for_pickup':
             socketio.emit('job_available', {'id': order.id, 'chef': user.name}, room='drivers_all')
        
        socketio.emit('order_update', {'id': order.id, 'status': order.status}, room=f"customer_{order.customer_id}")
        return jsonify({"ok": True})
    return jsonify({"error": "Unauthorized"}), 403

