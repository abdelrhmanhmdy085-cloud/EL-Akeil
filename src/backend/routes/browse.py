from flask import Blueprint, jsonify, request, current_app
import jwt
from backend.models import db, Category, Level, Dish, User
from datetime import datetime

bp = Blueprint('browse', __name__)

def get_current_user():
    """Get current user from JWT token (optional for public routes)"""
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
            uid = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])['sub']
            return User.query.get(uid)
    except:
        pass
    return None

# ============================================================
# PUBLIC NAVIGATION ROUTES (Standardized for request)
# ============================================================

@bp.route("/categories", methods=["GET"])
def get_categories_root():
    """Alias for /api/categories as requested"""
    return get_categories()

@bp.route("/levels", methods=["GET"])
def get_levels_root():
    """Alias for /api/levels as requested"""
    return get_levels()

@bp.route("/category/<int:id>/dishes", methods=["GET"])
def get_category_dishes(id):
    """Returns dishes filtered by category as requested"""
    lang = request.args.get('lang', 'en')
    
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    
    # Get all dishes in this category
    dishes = Dish.query.filter_by(category_id=id, is_available=True).all()
    
    dishes_data = [dish.to_dict() for dish in dishes]
    
    return jsonify({
        "category_name": category.name_ar if lang == 'ar' else category.name_en,
        "dishes": dishes_data
    })

@bp.route("/level/<int:id>/dishes", methods=["GET"])
def get_level_dishes(id):
    """Returns dishes filtered by level as requested"""
    lang = request.args.get('lang', 'en')
    
    level = Level.query.get(id)
    if not level:
        return jsonify({"error": "Level not found"}), 404
    
    # Get all dishes in this level
    dishes = Dish.query.filter_by(level_id=id, is_available=True).all()
    
    dishes_data = [dish.to_dict() for dish in dishes]
    
    return jsonify({
        "level_name": level.name_ar if lang == 'ar' else level.name_en,
        "dishes": dishes_data
    })

@bp.route("/dishes", methods=["GET"])
def get_all_dishes():
    """Returns all available dishes"""
    lang = request.args.get('lang', 'en')
    
    dishes = Dish.query.filter_by(is_available=True).all()
    
    dishes_data = [dish.to_dict() for dish in dishes]
    
    return jsonify(dishes_data)

# ============================================================
# CATEGORY ROUTES
# ============================================================

@bp.route("/categories", methods=["GET"])
def get_categories():
    """Get all food categories"""
    lang = request.args.get('lang', 'en')
    
    categories = Category.query.order_by(Category.display_order).all()
    
    result = []
    for cat in categories:
        data = cat.to_dict()
        # Keep only the language requested
        if lang == 'ar':
            data = {
                "id": data["id"],
                "name": data["name_ar"],
                "description": data["description_ar"],
                "icon": data["icon"],
                "dish_count": data["dish_count"]
            }
        else:
            data = {
                "id": data["id"],
                "name": data["name_en"],
                "description": data["description_en"],
                "icon": data["icon"],
                "dish_count": data["dish_count"]
            }
        result.append(data)
    
    return jsonify(result)

@bp.route("/category/<int:category_id>", methods=["GET"])
def get_category_detail(category_id):
    """Get category details with dishes grouped by level"""
    lang = request.args.get('lang', 'en')
    
    category = Category.query.get(category_id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    
    # Get all dishes in this category grouped by level
    dishes = Dish.query.filter_by(category_id=category_id, is_available=True).all()
    
    # Group by level
    grouped = {}
    for dish in dishes:
        level_name = dish.level_obj.name_en if dish.level_obj else "Other"
        if lang == 'ar':
            level_name = dish.level_obj.name_ar if dish.level_obj else "أخرى"
        
        if level_name not in grouped:
            grouped[level_name] = []
        grouped[level_name].append(dish.to_dict())
    
    cat_name = category.name_ar if lang == 'ar' else category.name_en
    
    return jsonify({
        "id": category_id,
        "name": cat_name,
        "icon": category.icon,
        "grouped_by_level": grouped
    })

# ============================================================
# LEVEL ROUTES
# ============================================================

@bp.route("/levels", methods=["GET"])
def get_levels():
    """Get all food levels"""
    lang = request.args.get('lang', 'en')
    
    levels = Level.query.order_by(Level.display_order).all()
    
    result = []
    for level in levels:
        data = level.to_dict()
        # Keep only the language requested
        if lang == 'ar':
            data = {
                "id": data["id"],
                "name": data["name_ar"],
                "description": data["description_ar"],
                "icon": data["icon"],
                "color_tag": data["color_tag"],
                "is_special": data["is_special"],
                "dish_count": data["dish_count"]
            }
        else:
            data = {
                "id": data["id"],
                "name": data["name_en"],
                "description": data["description_en"],
                "icon": data["icon"],
                "color_tag": data["color_tag"],
                "is_special": data["is_special"],
                "dish_count": data["dish_count"]
            }
        result.append(data)
    
    return jsonify(result)

@bp.route("/level/<int:level_id>", methods=["GET"])
def get_level_detail(level_id):
    """Get level details with dishes grouped by category"""
    lang = request.args.get('lang', 'en')
    
    level = Level.query.get(level_id)
    if not level:
        return jsonify({"error": "Level not found"}), 404
    
    # Get all dishes in this level grouped by category
    dishes = Dish.query.filter_by(level_id=level_id, is_available=True).all()
    
    # Group by category
    grouped = {}
    for dish in dishes:
        cat_name = dish.category_obj.name_en if dish.category_obj else "Other"
        if lang == 'ar':
            cat_name = dish.category_obj.name_ar if dish.category_obj else "أخرى"
        
        if cat_name not in grouped:
            grouped[cat_name] = []
        grouped[cat_name].append(dish.to_dict())
    
    level_name = level.name_ar if lang == 'ar' else level.name_en
    
    return jsonify({
        "id": level_id,
        "name": level_name,
        "icon": level.icon,
        "color_tag": level.color_tag,
        "grouped_by_category": grouped
    })

# ============================================================
# SEARCH & FILTER ROUTES
# ============================================================

@bp.route("/dishes/search", methods=["GET"])
def search_dishes():
    """Search dishes by category and/or level"""
    category_id = request.args.get('category_id', type=int)
    level_id = request.args.get('level_id', type=int)
    query = request.args.get('q', '')
    
    filters = Dish.query.filter_by(is_available=True)
    
    if category_id:
        filters = filters.filter_by(category_id=category_id)
    
    if level_id:
        filters = filters.filter_by(level_id=level_id)
    
    if query:
        filters = filters.filter(Dish.name.ilike(f"%{query}%"))
    
    dishes = filters.limit(50).all()
    
    return jsonify([d.to_dict() for d in dishes])

@bp.route("/category/<int:cat_id>/level/<int:level_id>/dishes", methods=["GET"])
def get_filtered_dishes(cat_id, level_id):
    """Get dishes filtered by both category and level"""
    dishes = Dish.query.filter_by(
        category_id=cat_id,
        level_id=level_id,
        is_available=True
    ).all()
    
    return jsonify([d.to_dict() for d in dishes])

# ============================================================
# ADMIN ROUTES (For managing categories and levels)
# ============================================================

@bp.route("/admin/categories", methods=["POST"])
def create_category():
    """Create a new category (admin only)"""
    data = request.get_json()
    
    cat = Category(
        name_ar=data.get('name_ar'),
        name_en=data.get('name_en'),
        icon=data.get('icon'),
        description_ar=data.get('description_ar'),
        description_en=data.get('description_en'),
        display_order=data.get('display_order', 0)
    )
    
    db.session.add(cat)
    db.session.commit()
    
    return jsonify({"ok": True, "category": cat.to_dict()})

@bp.route("/admin/levels", methods=["POST"])
def create_level():
    """Create a new level (admin only)"""
    data = request.get_json()
    
    level = Level(
        name_ar=data.get('name_ar'),
        name_en=data.get('name_en'),
        icon=data.get('icon'),
        color_tag=data.get('color_tag'),
        description_ar=data.get('description_ar'),
        description_en=data.get('description_en'),
        display_order=data.get('display_order', 0),
        is_special=data.get('is_special', False)
    )
    
    db.session.add(level)
    db.session.commit()
    
    return jsonify({"ok": True, "level": level.to_dict()})

@bp.route("/admin/category/<int:cat_id>", methods=["PUT"])
def update_category(cat_id):
    """Update category"""
    cat = Category.query.get(cat_id)
    if not cat:
        return jsonify({"error": "Not found"}), 404
    
    data = request.get_json()
    cat.name_ar = data.get('name_ar', cat.name_ar)
    cat.name_en = data.get('name_en', cat.name_en)
    cat.icon = data.get('icon', cat.icon)
    cat.description_ar = data.get('description_ar', cat.description_ar)
    cat.description_en = data.get('description_en', cat.description_en)
    cat.display_order = data.get('display_order', cat.display_order)
    
    db.session.commit()
    return jsonify({"ok": True, "category": cat.to_dict()})

@bp.route("/admin/level/<int:level_id>", methods=["PUT"])
def update_level(level_id):
    """Update level"""
    level = Level.query.get(level_id)
    if not level:
        return jsonify({"error": "Not found"}), 404
    
    data = request.get_json()
    level.name_ar = data.get('name_ar', level.name_ar)
    level.name_en = data.get('name_en', level.name_en)
    level.icon = data.get('icon', level.icon)
    level.color_tag = data.get('color_tag', level.color_tag)
    level.description_ar = data.get('description_ar', level.description_ar)
    level.description_en = data.get('description_en', level.description_en)
    level.display_order = data.get('display_order', level.display_order)
    level.is_special = data.get('is_special', level.is_special)
    
    db.session.commit()
    return jsonify({"ok": True, "level": level.to_dict()})
