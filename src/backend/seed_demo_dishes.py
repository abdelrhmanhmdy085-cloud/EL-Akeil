"""
Seed Demo Dishes for El Akeil Food Browsing System
Run with: python -m src.backend.seed_demo_dishes
"""

import sys
from pathlib import Path

# Add src to path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR.parent))

from backend.app import create_app
from backend.models import db, Category, Level, Dish, ChefProfile, User

def seed_demo_dishes():
    app = create_app()
    
    with app.app_context():
        # Get existing categories and levels
        categories = {cat.name_en: cat.id for cat in Category.query.all()}
        levels = {lvl.name_en: lvl.id for lvl in Level.query.all()}
        
        if not categories or not levels:
            print("Error: Categories or Levels not found. Run seed_categories_levels.py first.")
            return

        # Find or create a demo chef
        chef_user = User.query.filter_by(username='demo_chef').first()
        if not chef_user:
            chef_user = User(username='demo_chef', password_hash='hash', role='chef', name='Chef Ahmed')
            db.session.add(chef_user)
            db.session.flush()
            
            chef_profile = ChefProfile(user_id=chef_user.id, address='Cairo, Egypt')
            db.session.add(chef_profile)
            db.session.flush()
        else:
            chef_profile = chef_user.chef_profile

        # Demo Dishes
        demo_dishes = [
            # Meat
            {
                'name': 'Kebab & Kofta',
                'description': 'Grilled mix of lamb kebab and seasoned kofta.',
                'price': 250.0,
                'category_en': 'Meat',
                'level_en': 'Home Cooked',
                'image_url': 'https://images.unsplash.com/photo-1544025162-d76694265947'
            },
            {
                'name': 'Steak with Mushroom Sauce',
                'description': 'Juicy tenderloin steak with creamy mushroom sauce.',
                'price': 450.0,
                'category_en': 'Meat',
                'level_en': 'Special Dishes',
                'image_url': 'https://images.unsplash.com/photo-1546833999-b9f581a1996d'
            },
            # Chicken
            {
                'name': 'Grilled Chicken',
                'description': 'Perfectly seasoned charcoal-grilled chicken.',
                'price': 180.0,
                'category_en': 'Chicken',
                'level_en': 'Fast Food',
                'image_url': 'https://images.unsplash.com/photo-1598103442097-8b74394b95c6'
            },
            {
                'name': 'Chicken Mansaf',
                'description': 'Traditional chicken dish with rice and yogurt sauce.',
                'price': 220.0,
                'category_en': 'Chicken',
                'level_en': 'Occasions & Holidays',
                'image_url': 'https://images.unsplash.com/photo-1626777553755-9388147d79b2'
            },
            # Seafood
            {
                'name': 'Seafood Platter',
                'description': 'Lobster, shrimp, and mussels with butter sauce.',
                'price': 600.0,
                'category_en': 'Seafood',
                'level_en': 'Special Dishes',
                'image_url': 'https://images.unsplash.com/photo-1551248429-07f9c898c805'
            },
            # Healthy
            {
                'name': 'Quinoa Salad',
                'description': 'Nutritious quinoa with fresh vegetables.',
                'price': 120.0,
                'category_en': 'Meat', # Could be any type or add a "Salad" category
                'level_en': 'Diet & Healthy',
                'image_url': 'https://images.unsplash.com/photo-1512621776951-a57141f2eefd'
            },
            # Sweets
            {
                'name': 'Om Ali',
                'description': 'Traditional Egyptian bread pudding with nuts.',
                'price': 85.0,
                'category_en': 'Sweets',
                'level_en': 'Home Cooked',
                'image_url': 'https://images.unsplash.com/photo-1579372781848-61d9d987bb0a'
            }
        ]

        # Add dishes
        for d in demo_dishes:
            cat_id = categories.get(d['category_en'])
            lvl_id = levels.get(d['level_en'])
            
            if not Dish.query.filter_by(name=d['name']).first():
                dish = Dish(
                    name=d['name'],
                    description=d['description'],
                    price=d['price'],
                    chef_profile_id=chef_profile.id,
                    category_id=cat_id,
                    level_id=lvl_id,
                    image_url=d['image_url'],
                    is_available=True
                )
                db.session.add(dish)
                print(f"Added Dish: {d['name']}")

        db.session.commit()
        print("✓ Demo dishes seeded successfully!")

if __name__ == '__main__':
    seed_demo_dishes()
