#!/usr/bin/env python3
"""
Seed script for Chef Location Map
إضافة بيانات تجريبية للخريطة
"""

import sys
from pathlib import Path

# Setup path
BASE_DIR = Path(__file__).resolve().parent / "src" / "backend"
sys.path.insert(0, str(BASE_DIR.parent))

from backend.models import db, User, ChefProfile, Dish, Order
from backend.app import create_app
import random
from datetime import datetime, timedelta

# مواقع الشيفات في القاهرة
CAIRO_CHEFS = [
    {"name": "أم أحمد", "address": "المعادي", "lat": 29.9630, "long": 31.3507},
    {"name": "الشيف محمود", "address": "الزمالك", "lat": 30.0669, "long": 31.2584},
    {"name": "فاطمة", "address": "العجوزة", "lat": 30.0222, "long": 31.1989},
    {"name": "مطبخ السلام", "address": "مدينة نصر", "lat": 30.0444, "long": 31.3907},
    {"name": "الحاجة عائشة", "address": "القاهرة الجديدة", "lat": 30.0056, "long": 31.4871},
    {"name": "العم محمد", "address": "الدقي", "lat": 30.0349, "long": 31.2177},
    {"name": "أسطى حسن", "address": "البساتين", "lat": 29.9486, "long": 31.3179},
    {"name": "مطبخ النيل", "address": "الجيزة", "lat": 30.0097, "long": 31.1895},
]

# الأطعمة
DISHES = [
    {"name": "كشري بيتي", "category": "Meat", "price": 35, "prep_time": 15, "description": "كشري أصلي بيتي"},
    {"name": "برجر سريع", "category": "Meat", "price": 50, "prep_time": 10, "description": "برجر لذيذ جداً"},
    {"name": "شاورما دجاج", "category": "Chicken", "price": 45, "prep_time": 12, "description": "شاورما طازة"},
    {"name": "فتة الدجاج", "category": "Chicken", "price": 60, "prep_time": 20, "description": "فتة دجاج شهية"},
    {"name": "فسيخ وفتة", "category": "Seafood", "price": 75, "prep_time": 25, "description": "وجبة سمك مشهورة"},
    {"name": "سمك مشوي", "category": "Seafood", "price": 80, "prep_time": 30, "description": "سمك طازة مشوي"},
    {"name": "بيتزا إيطالية", "category": "Meat", "price": 55, "prep_time": 15, "description": "بيتزا فاخرة"},
    {"name": "معكرونة بولونيز", "category": "Meat", "price": 50, "prep_time": 20, "description": "معكرونة مع صلصة اللحم"},
    {"name": "سلطة خضراء", "category": "Healthy", "price": 40, "prep_time": 5, "description": "سلطة طازة"},
    {"name": "كنافة نابلسية", "category": "Sweets", "price": 80, "prep_time": 10, "description": "حلويات فاخرة"},
]

def seed_database():
    """Add sample data to the database"""
    
    print("🌱 Starting database seeding...")
    print("=" * 60)
    
    # Create app context
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional)
        # db.drop_all()
        # db.create_all()
        
        # Add chefs
        print("\n➕ Adding chefs...")
        added_chefs = 0
        for chef_data in CAIRO_CHEFS:
            # Check if chef exists
            existing_user = User.query.filter_by(username=chef_data["name"].replace(" ", "_")).first()
            if existing_user:
                print(f"   ⏭️  Chef '{chef_data['name']}' already exists, skipping...")
                continue
            
            # Create user
            user = User(
                username=chef_data["name"].replace(" ", "_"),
                password_hash="hashed_password",  # In real app, use proper hashing
                role="chef",
                name=chef_data["name"]
            )
            db.session.add(user)
            db.session.flush()
            
            # Create chef profile
            chef = ChefProfile(
                user_id=user.id,
                address=chef_data["address"],
                lat=chef_data["lat"],
                long=chef_data["long"],
                prep_time_avg=random.randint(15, 40)
            )
            db.session.add(chef)
            db.session.commit()
            
            print(f"   ✅ Added chef: {chef_data['name']} at {chef_data['address']}")
            added_chefs += 1
            
            # Add dishes for this chef
            print(f"      Adding dishes for {chef_data['name']}...")
            dishes_added = 0
            for dish_data in random.sample(DISHES, k=random.randint(3, 6)):
                dish = Dish(
                    chef_profile_id=chef.id,
                    name=dish_data["name"],
                    price=dish_data["price"],
                    description=dish_data["description"],
                    category=dish_data["category"],
                    prep_time=dish_data["prep_time"],
                    food_level="home"
                )
                db.session.add(dish)
                dishes_added += 1
            
            db.session.commit()
            print(f"      ✅ Added {dishes_added} dishes")
        
        print(f"\n✅ Total chefs added: {added_chefs}")
        
        # Add sample orders for heatmap (optional)
        print("\n➕ Adding sample orders for heatmap...")
        
        # Get a chef for orders
        chef = ChefProfile.query.first()
        if chef and chef.user_id:
            customer = User.query.filter_by(role='customer').first()
            if not customer:
                # Create a test customer
                customer = User(
                    username="test_customer",
                    password_hash="hashed_password",
                    role="customer",
                    name="Test Customer"
                )
                db.session.add(customer)
                db.session.commit()
            
            # Add some delivered orders
            for i in range(10):
                order = Order(
                    customer_id=customer.id,
                    chef_id=chef.id,
                    items='[{"name": "Sample Dish", "price": 50}]',
                    total_price=50,
                    status="delivered",
                    customer_lat=29.9500 + random.uniform(-0.1, 0.1),
                    customer_long=31.2500 + random.uniform(-0.1, 0.1),
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 7))
                )
                db.session.add(order)
            
            db.session.commit()
            print("✅ Added 10 sample orders for heatmap")
        
        print("\n" + "=" * 60)
        print("🎉 Database seeding completed successfully!")
        print("=" * 60)
        
        # Print summary
        print("\n📊 Database Summary:")
        print(f"   Chefs: {ChefProfile.query.count()}")
        print(f"   Dishes: {Dish.query.count()}")
        print(f"   Orders: {Order.query.count()}")
        print(f"   Users: {User.query.count()}")

if __name__ == "__main__":
    try:
        seed_database()
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
