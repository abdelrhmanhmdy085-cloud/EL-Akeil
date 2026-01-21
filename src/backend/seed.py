from app import app
from models import db, Category, Level, Dish

def seed_data():
    with app.app_context():
        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Categories
        categories = [
            Category(name_ar="لحوم", name_en="Meat", icon="🥩"),
            Category(name_ar="فراخ", name_en="Chicken", icon="🍗"),
            Category(name_ar="أسماك", name_en="Fish", icon="🐟"),
            Category(name_ar="حلويات", name_en="Sweets", icon="🍰"),
            Category(name_ar="مشروبات", name_en="Drinks", icon="🥤"),
        ]

        # Levels
        levels = [
            Level(name_ar="أكلات سريعة", name_en="Fast Food", color_tag="red"),
            Level(name_ar="أكلات بيتية", name_en="Home Cooked", color_tag="green"),
            Level(name_ar="أكلات مميزة", name_en="Specialty", color_tag="gold"),
            Level(name_ar="دايت", name_en="Diet", color_tag="blue"),
            Level(name_ar="مناسبات وأعياد", name_en="Occasions & Holidays", color_tag="purple"),
        ]

        db.session.add_all(categories)
        db.session.add_all(levels)
        db.session.commit()

        # Some sample dishes
        dishes = [
            # Meat
            Dish(name="Kebab & Kofta", image="https://images.unsplash.com/photo-1529692236671-f1f6cf9683ba", price=150.0, chef_name="Chef Ahmed", category_id=categories[0].id, level_id=levels[2].id),
            Dish(name="Burger XL", image="https://images.unsplash.com/photo-1568901346375-23c9450c58cd", price=85.0, chef_name="Fast Bites", category_id=categories[0].id, level_id=levels[0].id),
            Dish(name="Stuffed Pigeon", image="https://images.unsplash.com/photo-1626074353765-517a681e40be", price=120.0, chef_name="Mama Kitchen", category_id=categories[0].id, level_id=levels[1].id),

            # Chicken
            Dish(name="Fried Chicken", image="https://images.unsplash.com/photo-1562967914-608f82629710", price=90.0, chef_name="Crispy King", category_id=categories[1].id, level_id=levels[0].id),
            Dish(name="Grilled Chicken", image="https://images.unsplash.com/photo-1598103442097-8b74394b95c6", price=110.0, chef_name="Healthy Grill", category_id=categories[1].id, level_id=levels[3].id),

            # Fish
            Dish(name="Grilled Tilapia", image="https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2", price=130.0, chef_name="Sea Breeze", category_id=categories[2].id, level_id=levels[1].id),

            # Sweets
            Dish(name="Kunafa", image="https://images.unsplash.com/photo-1512414776101-2185521ef34e", price=60.0, chef_name="Sweet Palace", category_id=categories[3].id, level_id=levels[4].id),

            # Occasions
            Dish(name="Fattah Royale", image="https://images.unsplash.com/photo-1541529086526-db283c563270", price=200.0, chef_name="Traditional Tastes", category_id=categories[0].id, level_id=levels[4].id),
        ]

        db.session.add_all(dishes)
        db.session.commit()
        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_data()
