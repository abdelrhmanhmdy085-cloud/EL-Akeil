from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
from models import db, Category, Level, Dish

app = Flask(__name__)
CORS(app)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'elakeil.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/api/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([c.to_dict() for c in categories])

@app.route('/api/levels', methods=['GET'])
def get_levels():
    levels = Level.query.all()
    return jsonify([l.to_dict() for l in levels])

@app.route('/api/category/<int:id>/dishes', methods=['GET'])
def get_category_dishes(id):
    category = Category.query.get_or_404(id)
    dishes = Dish.query.filter_by(category_id=id).all()
    return jsonify({
        "category": category.to_dict(),
        "dishes": [d.to_dict() for d in dishes]
    })

@app.route('/api/level/<int:id>/dishes', methods=['GET'])
def get_level_dishes(id):
    level = Level.query.get_or_404(id)
    dishes = Dish.query.filter_by(level_id=id).all()
    return jsonify({
        "level": level.to_dict(),
        "dishes": [d.to_dict() for d in dishes]
    })

@app.route('/')
def home():
    return jsonify({"message": "Backend شغال ✅", "status": "running"})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
