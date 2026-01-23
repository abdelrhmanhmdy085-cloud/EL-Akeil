import sys
import os
from pathlib import Path
from sqlalchemy import text

# Add src to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent))

from backend.app import create_app
from backend.models import db, Category, Level

app = create_app()

def seed_data():
    with app.app_context():
        # 1. Ensure tables exist (creates new ones like Category/Level)
        db.create_all()

        # 2. Manual Migration for Dish table (Add new columns)
        try:
            with db.engine.connect() as conn:
                res = conn.execute(text("PRAGMA table_info(dish)"))
                columns = [row[1] for row in res.fetchall()]
                
                if "category_id" not in columns:
                    print("Migrating Dish table: Adding new columns...")
                    # SQLite doesn't support multiple ADD COLUMN in one statement standardly, do one by one
                    conn.execute(text("ALTER TABLE dish ADD COLUMN category_id INTEGER REFERENCES category(id)"))
                    print("Added category_id")
                    
                if "level_id" not in columns:
                    conn.execute(text("ALTER TABLE dish ADD COLUMN level_id INTEGER REFERENCES level(id)"))
                    print("Added level_id")

                if "is_available" not in columns:
                    conn.execute(text("ALTER TABLE dish ADD COLUMN is_available BOOLEAN DEFAULT 1"))
                    print("Added is_available")
                
                conn.commit()
        except Exception as e:
            print(f"Migration logic error (ignoring if columns exist): {e}")

        # 3. SEED DATA
        # CATEGORIES
        categories = [
            {"name_en": "Meat", "name_ar": "لحوم", "icon": "🍖"},
            {"name_en": "Chicken", "name_ar": "فراخ", "icon": "🍗"},
            {"name_en": "Seafood", "name_ar": "أسماك", "icon": "🐟"},
            {"name_en": "Sweets", "name_ar": "حلويات", "icon": "🍰"},
            {"name_en": "Drinks", "name_ar": "مشروبات", "icon": "🥤"},
        ]
        
        for cat_data in categories:
            if not Category.query.filter_by(name_en=cat_data["name_en"]).first():
                cat = Category(
                    name_en=cat_data["name_en"],
                    name_ar=cat_data["name_ar"],
                    icon=cat_data["icon"]
                )
                db.session.add(cat)
                print(f"Added Category: {cat_data['name_en']}")
        
        # LEVELS
        levels = [
            {"name_en": "Fast Food", "name_ar": "أكلات سريعة", "color_tag": "red", "icon": "🚀"},
            {"name_en": "Home Cooked", "name_ar": "أكلات بيتية", "color_tag": "green", "icon": "🏠"},
            {"name_en": "Special", "name_ar": "أكلات مميزة", "color_tag": "gold", "icon": "✨"},
            {"name_en": "Diet", "name_ar": "دايت", "color_tag": "blue", "icon": "💪"},
            {"name_en": "Occasions", "name_ar": "مناسبات وأعياد", "color_tag": "purple", "icon": "🎉", "is_special": True},
        ]

        for lvl_data in levels:
            if not Level.query.filter_by(name_en=lvl_data["name_en"]).first():
                lvl = Level(
                    name_en=lvl_data["name_en"],
                    name_ar=lvl_data["name_ar"],
                    color_tag=lvl_data.get("color_tag"),
                    icon=lvl_data.get("icon"),
                    is_special=lvl_data.get("is_special", False)
                )
                db.session.add(lvl)
                print(f"Added Level: {lvl_data['name_en']}")

        db.session.commit()
        print("Database seeded successfully!")

if __name__ == "__main__":
    seed_data()
