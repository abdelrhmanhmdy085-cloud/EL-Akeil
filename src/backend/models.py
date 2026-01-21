from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(100), nullable=True)
    dishes = db.relationship('Dish', backref='category', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "icon": self.icon
        }

class Level(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name_ar = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    color_tag = db.Column(db.String(50), nullable=True)
    dishes = db.relationship('Dish', backref='level', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name_ar": self.name_ar,
            "name_en": self.name_en,
            "color_tag": self.color_tag
        }

class Dish(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(500), nullable=True)
    price = db.Column(db.Float, nullable=False)
    chef_name = db.Column(db.String(100), nullable=True) # chef_id in prompt, but chef_name is more direct for display
    chef_id = db.Column(db.Integer, nullable=True)
    rating = db.Column(db.Float, default=5.0)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    level_id = db.Column(db.Integer, db.ForeignKey('level.id'), nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": self.price,
            "chef_name": self.chef_name,
            "chef_id": self.chef_id,
            "rating": self.rating,
            "category_id": self.category_id,
            "level_id": self.level_id,
            "is_available": self.is_available,
            "category": self.category.to_dict() if self.category else None,
            "level": self.level.to_dict() if self.level else None
        }
