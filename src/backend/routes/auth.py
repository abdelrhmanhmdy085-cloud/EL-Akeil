from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import jwt
import os
from backend.models import db, User, ChefProfile, CustomerProfile, DriverProfile, Dish
from werkzeug.utils import secure_filename

bp = Blueprint('auth', __name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_token(user):
    payload = {
        "sub": user.id,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(minutes=current_app.config["JWT_EXP_MINUTES"])
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

@bp.route("/register/<role>", methods=["POST"])
def register(role):
    if role not in ['chef', 'customer', 'driver']: return jsonify({"error": "Invalid role"}), 400
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    name = data.get("name")

    if not username or not password: return jsonify({"error": "Missing credentials"}), 400
    if User.query.filter_by(username=username).first(): return jsonify({"error": "User exists"}), 409

    user = User(username=username, password_hash=generate_password_hash(password), name=name, role=role)
    db.session.add(user)
    db.session.flush()

    try:
        if role == 'chef':
            if not data.get("national_id"): return jsonify({"error": "National ID required"}), 400
            db.session.add(ChefProfile(user_id=user.id, address=data.get("address"), national_id=data.get("national_id")))
        elif role == 'customer':
            db.session.add(CustomerProfile(user_id=user.id, phone=data.get("phone"), location_lat=data.get("lat"), location_long=data.get("long")))
        elif role == 'driver':
            if not data.get("national_id"):
                db.session.rollback()
                return jsonify({"error": "Missing driver info"}), 400
            db.session.add(DriverProfile(user_id=user.id, national_id=data.get("national_id")))
        
        db.session.commit()
        return jsonify({"ok": True, "token": create_token(user), "user": user.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@bp.route("/chef-register", methods=["POST"])
def chef_register():
    try:
        # Get form data
        fullName = request.form.get("fullName")
        email = request.form.get("email")
        password = request.form.get("password")
        kitchenName = request.form.get("kitchenName")
        kitchenAddress = request.form.get("kitchenAddress")
        nationalId = request.form.get("nationalId")
        
        if not all([fullName, email, password, kitchenName, kitchenAddress, nationalId]):
            return jsonify({"message": "Missing required fields"}), 400
        
        # Check if email exists
        if User.query.filter_by(username=email).first():
            return jsonify({"message": "Email already registered"}), 409
        
        # Create user
        user = User(
            username=email,
            password_hash=generate_password_hash(password),
            name=fullName,
            role='chef'
        )
        db.session.add(user)
        db.session.flush()
        
        # Create chef profile
        chef_profile = ChefProfile(
            user_id=user.id,
            national_id=nationalId,
            address=kitchenAddress
        )
        db.session.add(chef_profile)
        db.session.flush()
        
        # Process dishes with images
        dishes_data = request.form.getlist('dishes')
        if dishes_data:
            import json
            for idx, dish_str in enumerate(dishes_data):
                try:
                    # Get dish files
                    dish_name = request.form.get(f'dishes[{idx}][name]')
                    dish_price = request.form.get(f'dishes[{idx}][price]')
                    dish_serving = request.form.get(f'dishes[{idx}][serving]')
                    dish_desc = request.form.get(f'dishes[{idx}][description]')
                    
                    if dish_name and dish_price:
                        dish = Dish(
                            chef_profile_id=chef_profile.id,
                            name=dish_name,
                            price=float(dish_price),
                            description=dish_desc
                        )
                        db.session.add(dish)
                        db.session.flush()
                        
                        # Handle dish images
                        dish_images = request.files.getlist(f'dishes[{idx}][images]')
                        for image_file in dish_images:
                            if image_file and allowed_file(image_file.filename):
                                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                                filename = secure_filename(f"dish_{dish.id}_{image_file.filename}")
                                image_path = os.path.join(UPLOAD_FOLDER, filename)
                                image_file.save(image_path)
                except Exception as e:
                    print(f"Error processing dish: {e}")
                    continue
        
        db.session.commit()
        token = create_token(user)
        
        return jsonify({
            "token": token,
            "user": user.to_dict(),
            "user_id": user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Chef registration error: {e}")
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500

@bp.route("/driver-register", methods=["POST"])
def driver_register():
    try:
        data = request.get_json()
        
        fullName = data.get("fullName")
        email = data.get("email")
        password = data.get("password")
        vehicleType = data.get("vehicleType")
        licenseNumber = data.get("licenseNumber")
        nationalId = data.get("nationalId")
        phoneNumber = data.get("phoneNumber")
        
        if not all([fullName, email, password, vehicleType, licenseNumber, nationalId, phoneNumber]):
            return jsonify({"message": "Missing required fields"}), 400
        
        # Check if email exists
        if User.query.filter_by(username=email).first():
            return jsonify({"message": "Email already registered"}), 409
        
        # Create user
        user = User(
            username=email,
            password_hash=generate_password_hash(password),
            name=fullName,
            role='driver'
        )
        db.session.add(user)
        db.session.flush()
        
        # Create driver profile
        driver_profile = DriverProfile(
            user_id=user.id,
            national_id=nationalId,
            vehicle_type=vehicleType,
            license_number=licenseNumber,
            phone_number=phoneNumber
        )
        db.session.add(driver_profile)
        db.session.commit()
        
        token = create_token(user)
        
        return jsonify({
            "token": token,
            "user": user.to_dict(),
            "user_id": user.id
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"Driver registration error: {e}")
        return jsonify({"message": f"Registration failed: {str(e)}"}), 500

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first()
    if not user or not check_password_hash(user.password_hash, data.get("password")):
        return jsonify({"error": "Invalid credentials"}), 401
    return jsonify({"ok": True, "token": create_token(user), "user": user.to_dict()})
