from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from pathlib import Path
import os
from datetime import datetime

# This will be imported from main models
# For now, assume the models are available

chef_dishes_bp = Blueprint('chef_dishes', __name__, url_prefix='/api/chef')

# Configuration
UPLOAD_FOLDER = Path(__file__).parent.parent.parent.parent / 'uploads' / 'dishes'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@chef_dishes_bp.route('/dishes', methods=['GET'])
def get_chef_dishes():
    """الحصول على جميع أطباق الشيف"""
    try:
        chef_id = request.headers.get('Chef-ID') or request.args.get('chef_id')
        
        if not chef_id:
            return jsonify({'error': 'Chef ID required'}), 400
        
        # Import here to avoid circular imports
        from backend.models import Dish
        
        dishes = Dish.query.filter_by(chef_id=chef_id).all()
        
        return jsonify({
            'status': 'success',
            'count': len(dishes),
            'dishes': [d.to_dict() for d in dishes]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chef_dishes_bp.route('/dishes', methods=['POST'])
def add_dish():
    """إضافة طبق جديد"""
    try:
        chef_id = request.form.get('chef_id')
        
        if not chef_id:
            return jsonify({'error': 'Chef ID required'}), 400
        
        # Get form data
        name = request.form.get('name')
        description = request.form.get('description', '')
        price = request.form.get('price')
        category_id = request.form.get('category_id')
        level_id = request.form.get('level_id')
        availability = request.form.get('availability', True)
        
        # Validate required fields
        if not all([name, price, category_id, level_id]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        try:
            price = float(price)
        except ValueError:
            return jsonify({'error': 'Price must be a number'}), 400
        
        # Handle image upload
        image_path = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
                filename = secure_filename(f"{chef_id}_{datetime.now().timestamp()}_{file.filename}")
                file.save(UPLOAD_FOLDER / filename)
                image_path = f"/uploads/dishes/{filename}"
        
        # Create dish
        from backend.models import db, Dish
        
        dish = Dish(
            chef_id=int(chef_id),
            name=name,
            description=description,
            price=price,
            category_id=int(category_id),
            level_id=int(level_id),
            image_path=image_path,
            available=availability
        )
        
        db.session.add(dish)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Dish added successfully',
            'dish_id': dish.id
        }), 201
        
    except Exception as e:
        from backend.models import db
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chef_dishes_bp.route('/dishes/<int:dish_id>', methods=['PUT'])
def update_dish(dish_id):
    """تحديث طبق"""
    try:
        from backend.models import db, Dish
        
        dish = Dish.query.get(dish_id)
        if not dish:
            return jsonify({'error': 'Dish not found'}), 404
        
        chef_id = request.headers.get('Chef-ID') or request.form.get('chef_id')
        
        if dish.chef_id != int(chef_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Update fields
        if 'name' in request.form:
            dish.name = request.form.get('name')
        if 'description' in request.form:
            dish.description = request.form.get('description')
        if 'price' in request.form:
            dish.price = float(request.form.get('price'))
        if 'category_id' in request.form:
            dish.category_id = int(request.form.get('category_id'))
        if 'level_id' in request.form:
            dish.level_id = int(request.form.get('level_id'))
        if 'availability' in request.form:
            dish.available = request.form.get('availability').lower() == 'true'
        
        # Handle image update
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
                filename = secure_filename(f"{chef_id}_{datetime.now().timestamp()}_{file.filename}")
                file.save(UPLOAD_FOLDER / filename)
                dish.image_path = f"/uploads/dishes/{filename}"
        
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Dish updated successfully'
        }), 200
        
    except Exception as e:
        from backend.models import db
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chef_dishes_bp.route('/dishes/<int:dish_id>', methods=['DELETE'])
def delete_dish(dish_id):
    """حذف طبق"""
    try:
        from backend.models import db, Dish
        
        dish = Dish.query.get(dish_id)
        if not dish:
            return jsonify({'error': 'Dish not found'}), 404
        
        chef_id = request.headers.get('Chef-ID')
        
        if dish.chef_id != int(chef_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        db.session.delete(dish)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Dish deleted successfully'
        }), 200
        
    except Exception as e:
        from backend.models import db
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@chef_dishes_bp.route('/dishes/<int:dish_id>/toggle-availability', methods=['POST'])
def toggle_availability(dish_id):
    """تبديل توفر الطبق"""
    try:
        from backend.models import db, Dish
        
        dish = Dish.query.get(dish_id)
        if not dish:
            return jsonify({'error': 'Dish not found'}), 404
        
        chef_id = request.headers.get('Chef-ID')
        
        if dish.chef_id != int(chef_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        dish.available = not dish.available
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'available': dish.available
        }), 200
        
    except Exception as e:
        from backend.models import db
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
