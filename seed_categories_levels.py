"""
Seed Categories and Levels for El Akeil Food Browsing System
Run with: python -m src.backend.seed_categories_levels
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.backend.app import create_app
from src.backend.models import db, Category, Level

def seed_categories_and_levels():
    """Seed the database with predefined categories and levels"""
    
    app = create_app()
    
    with app.app_context():
        # Clear existing data
        Category.query.delete()
        Level.query.delete()
        db.session.commit()
        
        print("Creating Categories...")
        
        # Categories (Food Types)
        categories = [
            {
                'name_ar': 'لحوم',
                'name_en': 'Meat',
                'icon': '🥩',
                'description_ar': 'أطباق اللحوم اللذيذة',
                'description_en': 'Delicious meat dishes',
                'display_order': 1
            },
            {
                'name_ar': 'فراخ',
                'name_en': 'Chicken',
                'icon': '🍗',
                'description_ar': 'أطباق الدجاج المميزة',
                'description_en': 'Special chicken dishes',
                'display_order': 2
            },
            {
                'name_ar': 'أسماك',
                'name_en': 'Seafood',
                'icon': '🐟',
                'description_ar': 'أطباق البحريات الطازة',
                'description_en': 'Fresh seafood dishes',
                'display_order': 3
            },
            {
                'name_ar': 'حلويات',
                'name_en': 'Sweets',
                'icon': '🍰',
                'description_ar': 'حلويات شهية وفاخرة',
                'description_en': 'Delicious and premium desserts',
                'display_order': 4
            },
            {
                'name_ar': 'مشروبات',
                'name_en': 'Drinks',
                'icon': '🥤',
                'description_ar': 'مشروبات منعشة',
                'description_en': 'Refreshing drinks',
                'display_order': 5
            }
        ]
        
        for cat_data in categories:
            cat = Category(**cat_data)
            db.session.add(cat)
        
        db.session.commit()
        print(f"✓ Created {len(categories)} categories")
        
        print("Creating Levels...")
        
        # Levels (Food Preparation Styles)
        levels = [
            {
                'name_ar': 'أكلات سريعة',
                'name_en': 'Fast Food',
                'icon': '⚡',
                'color_tag': '#FF6B35',
                'description_ar': 'أكلات جاهزة بسرعة',
                'description_en': 'Quick and ready meals',
                'display_order': 1,
                'is_special': False
            },
            {
                'name_ar': 'أكلات بيتية',
                'name_en': 'Home Cooked',
                'icon': '🏠',
                'color_tag': '#FFB703',
                'description_ar': 'أطباق بيتية تقليدية',
                'description_en': 'Traditional homemade dishes',
                'display_order': 2,
                'is_special': False
            },
            {
                'name_ar': 'أكلات مميزة',
                'name_en': 'Special Dishes',
                'icon': '👑',
                'color_tag': '#8338EC',
                'description_ar': 'أطباق فاخرة ومميزة',
                'description_en': 'Premium and special dishes',
                'display_order': 3,
                'is_special': False
            },
            {
                'name_ar': 'صحي',
                'name_en': 'Healthy',
                'icon': '🥗',
                'color_tag': '#06A77D',
                'description_ar': 'أطباق صحية ومفيدة',
                'description_en': 'Healthy and beneficial meals',
                'display_order': 4,
                'is_special': False
            },
            {
                'name_ar': 'مناسبات وأعياد',
                'name_en': 'Occasions & Holidays',
                'icon': '🎉',
                'color_tag': '#FFD700',
                'description_ar': 'أطباق خاصة للمناسبات',
                'description_en': 'Special occasion dishes',
                'display_order': 5,
                'is_special': True
            }
        ]
        
        for lvl_data in levels:
            lvl = Level(**lvl_data)
            db.session.add(lvl)
        
        db.session.commit()
        print(f"✓ Created {len(levels)} levels")
        
        print("\n" + "="*50)
        print("✓ Database seeding completed successfully!")
        print("="*50)
        print("\nCategories:")
        for cat in Category.query.all():
            print(f"  - {cat.name_en} ({cat.name_ar})")
        
        print("\nLevels:")
        for lvl in Level.query.all():
            special = " [SPECIAL]" if lvl.is_special else ""
            print(f"  - {lvl.name_en} ({lvl.name_ar}){special}")

if __name__ == '__main__':
    seed_categories_and_levels()
