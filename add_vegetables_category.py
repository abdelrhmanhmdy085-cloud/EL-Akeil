#!/usr/bin/env python
"""
Script to add Vegetables category to the database
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from backend.app import create_app
from backend.models import db, Category

def add_vegetables_category():
    app = create_app()
    
    with app.app_context():
        # Check if category already exists
        existing = Category.query.filter_by(name_ar="خضروات").first()
        
        if existing:
            print("[OK] Category 'Vegetables' already exists")
            print(f"  - Name: {existing.name_ar}")
            print(f"  - Icon: {existing.icon}")
            print(f"  - ID: {existing.id}")
            return
        
        # Create new category
        vegetables = Category(
            name_ar="خضروات",
            name_en="Vegetables",
            icon="🥬",
            description_ar="أطباق صحية ولذيذة مصنوعة من الخضروات الطازجة",
            description_en="Healthy and delicious dishes made from fresh vegetables",
            display_order=4  # After existing categories
        )
        
        db.session.add(vegetables)
        db.session.commit()
        
        print("[OK] Category 'Vegetables' added successfully!")
        print(f"  - Arabic Name: {vegetables.name_ar}")
        print(f"  - English Name: {vegetables.name_en}")
        print(f"  - Icon: {vegetables.icon}")
        print(f"  - ID: {vegetables.id}")

if __name__ == "__main__":
    add_vegetables_category()
