#!/usr/bin/env python3
"""
Script to update 'Diet' level to 'Healthy'
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / 'src'))

from backend.app import create_app
from backend.models import db, Level, Dish

def update_level_name():
    app = create_app()
    
    with app.app_context():
        print("[🔄] تحديث اسم المستوى من 'Diet' إلى 'Healthy'...")
        
        try:
            # Find the old Diet level
            old_level = Level.query.filter_by(name_en='Diet').first()
            
            if old_level:
                print(f"[✅] تم العثور على المستوى القديم: {old_level.name_en}")
                
                # Update it
                old_level.name_en = 'Healthy'
                old_level.name_ar = 'صحي'
                old_level.icon = '🥗'  # Change icon to salad
                
                db.session.commit()
                print(f"[✅] تم التحديث بنجاح!")
                print(f"    - الاسم الجديد: {old_level.name_en} ({old_level.name_ar})")
                print(f"    - الأيقونة الجديدة: {old_level.icon}")
                
                # Check dishes with this level
                dishes_count = Dish.query.filter_by(level_id=old_level.id).count()
                print(f"    - عدد الأطباق المرتبطة: {dishes_count}")
                
            else:
                print("[ℹ️] المستوى 'Diet' غير موجود في قاعدة البيانات")
                
                # Create new Healthy level if doesn't exist
                healthy_level = Level.query.filter_by(name_en='Healthy').first()
                if not healthy_level:
                    print("[🔄] إنشاء مستوى 'Healthy' جديد...")
                    healthy_level = Level(
                        name_en='Healthy',
                        name_ar='صحي',
                        icon='🥗',
                        color_tag='blue',
                        display_order=4
                    )
                    db.session.add(healthy_level)
                    db.session.commit()
                    print(f"[✅] تم إنشاء المستوى الجديد: {healthy_level.name_en}")
                else:
                    print(f"[ℹ️] المستوى 'Healthy' موجود بالفعل")
                
        except Exception as e:
            db.session.rollback()
            print(f"[❌] خطأ: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    return True

if __name__ == "__main__":
    success = update_level_name()
    sys.exit(0 if success else 1)
