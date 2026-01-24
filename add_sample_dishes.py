#!/usr/bin/env python3
"""
Script to add sample dishes with different availability statuses
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from backend.app import create_app
from backend.models import db, Dish, ChefProfile, Category, Level, User

def add_sample_dishes():
    app = create_app()
    
    with app.app_context():
        print("[🔄] Adding sample dishes with availability status...")
        
        try:
            # Get or create a test chef
            test_user = User.query.filter_by(username='test_chef').first()
            if not test_user:
                test_user = User(username='test_chef', name='الشيف جاسم', role='chef', password_hash='hashed')
                db.session.add(test_user)
                db.session.flush()
            
            # Get or create chef profile
            chef_profile = ChefProfile.query.filter_by(user_id=test_user.id).first()
            if not chef_profile:
                chef_profile = ChefProfile(
                    user_id=test_user.id,
                    address='المعادي، القاهرة',
                    prep_time_avg=25
                )
                db.session.add(chef_profile)
                db.session.flush()
            
            # Get categories
            fish_cat = Category.query.filter_by(name_ar='أسماك').first()
            chicken_cat = Category.query.filter_by(name_ar='دواجن').first()
            meat_cat = Category.query.filter_by(name_ar='لحوم').first()
            veg_cat = Category.query.filter_by(name_ar='خضروات').first()
            
            # Get levels
            economic = Level.query.filter_by(name_ar='اقتصادي').first()
            regular = Level.query.filter_by(name_ar='عادي').first()
            premium = Level.query.filter_by(name_ar='متميز').first()
            
            # Sample dishes
            sample_dishes = [
                # Ready dishes (أكل جاهز)
                {
                    'name': 'سمك بالفرن',
                    'price': 85,
                    'description': 'سمك طازة مشوي بالأعشاب والليمون',
                    'category': fish_cat or None,
                    'level': regular or None,
                    'prep_time': 10,
                    'is_available': True,
                },
                {
                    'name': 'دجاج مشوي',
                    'price': 65,
                    'description': 'دجاج مشوي بالبهارات والثوم',
                    'category': chicken_cat or None,
                    'level': economic or None,
                    'prep_time': 15,
                    'is_available': True,
                },
                {
                    'name': 'كنتالوب لحم',
                    'price': 95,
                    'description': 'لحم بقري متبل بالتوابل الشرقية',
                    'category': meat_cat or None,
                    'level': premium or None,
                    'prep_time': 20,
                    'is_available': True,
                },
                {
                    'name': 'سلطة خضار',
                    'price': 35,
                    'description': 'خضار طازة مع صلصة زيت الزيتون',
                    'category': veg_cat or None,
                    'level': economic or None,
                    'prep_time': 5,
                    'is_available': True,
                },
                # Not ready dishes (أكل غير جاهز)
                {
                    'name': 'سمك مشوي بالملح',
                    'price': 120,
                    'description': 'سمك مشوي بطريقة تقليدية بالملح الخشن',
                    'category': fish_cat or None,
                    'level': premium or None,
                    'prep_time': 30,
                    'is_available': False,  # Not ready
                },
                {
                    'name': 'دجاج بالزيتون',
                    'price': 75,
                    'description': 'دجاج مطهي مع الزيتون والليمون',
                    'category': chicken_cat or None,
                    'level': regular or None,
                    'prep_time': 25,
                    'is_available': False,  # Not ready
                },
                {
                    'name': 'شاورما لحم',
                    'price': 55,
                    'description': 'لحم محمر بالفرن مع الخضار',
                    'category': meat_cat or None,
                    'level': economic or None,
                    'prep_time': 35,
                    'is_available': False,  # Not ready
                },
                {
                    'name': 'خضار مشكل',
                    'price': 45,
                    'description': 'خضار متنوع مشوي بزيت الزيتون',
                    'category': veg_cat or None,
                    'level': regular or None,
                    'prep_time': 28,
                    'is_available': False,  # Not ready
                },
            ]
            
            # Add dishes
            added_count = 0
            for dish_data in sample_dishes:
                # Check if dish already exists
                existing = Dish.query.filter_by(
                    name=dish_data['name'],
                    chef_profile_id=chef_profile.id
                ).first()
                
                if not existing:
                    dish = Dish(
                        chef_profile_id=chef_profile.id,
                        name=dish_data['name'],
                        price=dish_data['price'],
                        description=dish_data['description'],
                        category_id=dish_data['category'].id if dish_data['category'] else None,
                        level_id=dish_data['level'].id if dish_data['level'] else None,
                        prep_time=dish_data['prep_time'],
                        is_available=dish_data['is_available'],
                        image_url=None
                    )
                    db.session.add(dish)
                    added_count += 1
                    status = '🟢 جاهز' if dish_data['is_available'] else '🟠 غير جاهز'
                    print(f"  ✅ {status} - {dish_data['name']} ({dish_data['price']} EGP)")
            
            if added_count > 0:
                db.session.commit()
                print(f"\n✅ تم إضافة {added_count} طبق بنجاح!")
                print(f"  - أطباق جاهزة: 4")
                print(f"  - أطباق غير جاهزة: 4")
            else:
                print("ℹ️  جميع الأطباق موجودة بالفعل")
                
        except Exception as e:
            db.session.rollback()
            print(f"❌ خطأ: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == "__main__":
    success = add_sample_dishes()
    sys.exit(0 if success else 1)
