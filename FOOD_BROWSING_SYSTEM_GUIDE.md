# El Akeil Food Browsing System - Implementation Guide

## Overview

The Food Browsing System is a complete two-dimensional navigation solution for El Akeil that allows users to browse food by:
1. **Categories** (Food Types) - لحوم، فراخ، أسماك، حلويات، مشروبات
2. **Levels** (Preparation Styles) - سريعة، بيتية، مميزة، دايت، مناسبات
3. **Combined Filters** - Browse by both category and level simultaneously

## Architecture

### Database Models

#### Category Model
```python
class Category(db.Model):
    id              # Primary Key
    name_ar         # Arabic name
    name_en         # English name
    icon            # Emoji or icon URL
    description_ar  # Arabic description
    description_en  # English description
    display_order   # Sort order
    created_at      # Timestamp
    
    dishes          # Relationship to Dish model
```

**Predefined Categories:**
- 🥩 لحوم (Meat)
- 🍗 فراخ (Chicken)
- 🐟 أسماك (Seafood)
- 🍰 حلويات (Sweets)
- 🥤 مشروبات (Drinks)

#### Level Model
```python
class Level(db.Model):
    id              # Primary Key
    name_ar         # Arabic name
    name_en         # English name
    icon            # Emoji or icon URL
    color_tag       # Color code for UI styling
    description_ar  # Arabic description
    description_en  # English description
    display_order   # Sort order
    is_special      # Flag for special occasions
    created_at      # Timestamp
    
    dishes          # Relationship to Dish model
```

**Predefined Levels:**
- ⚡ أكلات سريعة (Fast Food) - `#FF6B35`
- 🏠 أكلات بيتية (Home Cooked) - `#FFB703`
- 👑 أكلات مميزة (Special Dishes) - `#8338EC`
- 🥗 دايت وصحي (Diet & Healthy) - `#06A77D`
- 🎉 مناسبات وأعياد (Occasions & Holidays) - `#FFD700` [SPECIAL]

#### Dish Model (Enhanced)
```python
class Dish(db.Model):
    # ... existing fields ...
    category_id     # Foreign Key to Category
    level_id        # Foreign Key to Level
    is_available    # Availability status
    
    # Relationships
    category_obj    # Category instance
    level_obj       # Level instance
```

## API Endpoints

### Browse Routes

#### 1. Get All Categories
```
GET /api/browse/categories?lang=en
```
**Response:**
```json
[
    {
        "id": 1,
        "name": "Meat",
        "description": "Delicious meat dishes",
        "icon": "🥩",
        "dish_count": 15
    }
]
```

#### 2. Get Category Details with Dishes
```
GET /api/browse/category/{id}?lang=en
```
**Response:**
```json
{
    "id": 1,
    "name": "Meat",
    "icon": "🥩",
    "grouped_by_level": {
        "Fast Food": [
            {
                "id": 1,
                "name": "Burger",
                "price": 50,
                "chef_name": "Chef Ahmed",
                "rating": 4.5,
                "level_name": "Fast Food",
                "category_name": "Meat",
                "image_url": "..."
            }
        ],
        "Home Cooked": [...]
    }
}
```

#### 3. Get All Levels
```
GET /api/browse/levels?lang=en
```
**Response:**
```json
[
    {
        "id": 1,
        "name": "Fast Food",
        "description": "Quick and ready meals",
        "icon": "⚡",
        "color_tag": "#FF6B35",
        "is_special": false,
        "dish_count": 20
    }
]
```

#### 4. Get Level Details with Dishes
```
GET /api/browse/level/{id}?lang=en
```
**Response:**
```json
{
    "id": 1,
    "name": "Fast Food",
    "icon": "⚡",
    "color_tag": "#FF6B35",
    "grouped_by_category": {
        "Meat": [
            {
                "id": 1,
                "name": "Burger",
                "price": 50,
                "chef_name": "Chef Ahmed",
                "rating": 4.5,
                "category_name": "Meat",
                "level_name": "Fast Food",
                "image_url": "..."
            }
        ]
    }
}
```

#### 5. Search & Filter Dishes
```
GET /api/browse/dishes/search?category_id=1&level_id=1&q=burger&lang=en
```
**Parameters:**
- `category_id` (optional) - Filter by category
- `level_id` (optional) - Filter by level
- `q` (optional) - Search query
- `lang` (optional) - Language (ar/en)

#### 6. Get Filtered Dishes by Both Category and Level
```
GET /api/browse/category/{cat_id}/level/{level_id}/dishes?lang=en
```

### Admin Management Routes

#### Create Category
```
POST /api/browse/admin/categories
```
**Body:**
```json
{
    "name_ar": "لحوم",
    "name_en": "Meat",
    "icon": "🥩",
    "description_ar": "أطباق اللحوم",
    "description_en": "Meat dishes",
    "display_order": 1
}
```

#### Update Category
```
PUT /api/browse/admin/category/{id}
```

#### Create Level
```
POST /api/browse/admin/levels
```
**Body:**
```json
{
    "name_ar": "أكلات سريعة",
    "name_en": "Fast Food",
    "icon": "⚡",
    "color_tag": "#FF6B35",
    "description_ar": "أكلات جاهزة بسرعة",
    "description_en": "Quick meals",
    "display_order": 1,
    "is_special": false
}
```

#### Update Level
```
PUT /api/browse/admin/level/{id}
```

## Frontend Pages

### 1. Categories List Page (`/categories.html`)
- **Route:** `/categories`
- **Features:**
  - Grid display of all food categories
  - Each category shows icon, name, description, dish count
  - Hover effects with elevation
  - Click to navigate to category detail page
  - Language toggle (AR/EN)
  - Responsive mobile-first design

### 2. Category Detail Page (`/category.html`)
- **Route:** `/category.html?id={categoryId}`
- **Features:**
  - Category header with icon
  - Dishes grouped by food level
  - Talabat-style card layout
  - Each dish shows: image, name, price, chef, rating, level badge
  - Back button to categories list
  - Language support
  - Mobile responsive

### 3. Levels List Page (`/levels.html`)
- **Route:** `/levels`
- **Features:**
  - Grid display of all food levels
  - Special occasions highlighted with ✨ badge and gold border
  - Each level shows icon, name, description, dish count
  - Color-coded tags for visual distinction
  - Hover animations
  - Click to navigate to level detail page
  - Language toggle

### 4. Level Detail Page (`/level.html`)
- **Route:** `/level.html?id={levelId}`
- **Features:**
  - Level header with icon
  - Dishes grouped by food category
  - Special occasions marked with star decoration
  - Complete dish information cards
  - Responsive layout
  - Language support

### 5. Home Page Integration (`/index.html`)
- **Sections Added:**
  - Browse by Level (horizontal scroll with cards)
  - Browse by Category (grid view)
  - Occasions & Holidays (special highlighted section)
  - Each section has "View All" button
  - Dish counts displayed
  - Real-time API loading

## Language Support

All pages support:
- **Arabic (ar)** - Default language with RTL layout
- **English (en)** - LTR layout
- **7 Additional Languages** - fr, de, es, it, tr, ru, zh

### Language Switching
- Automatic `body.dir` and `text-align` adjustment
- LocalStorage persistence (`elakeil_lang`)
- Language selector in navbar
- Translation keys in JSON files:
  - `assets/lang/ar.json`
  - `assets/lang/en.json`

### Translation Keys Added
```
categories_title         "تصفح حسب الفئة"
categories_subtitle      "اختر الفئة المفضلة لديك"
levels_title            "تصفح حسب المستوى"
levels_subtitle         "اختر مستوى الأكل المفضل لديك"
category_detail_title   "تفاصيل الفئة"
level_detail_title      "تفاصيل المستوى"
all_categories          "جميع الفئات"
all_levels              "جميع المستويات"
home_button             "الرئيسية"
no_categories           "لا توجد فئات"
no_levels               "لا توجد مستويات"
no_dishes               "لا توجد أطباق"
error_loading           "خطأ في التحميل"
try_again               "يرجى المحاولة مجدداً"
view_all                "عرض الكل"
dishes_count            "عدد الأطباق"
```

## Database Seeding

### Run Seed Script
```bash
# Navigate to project root
cd d:\3abdo\El Akeil

# Run seed script
python seed_categories_levels.py
```

**Output:**
```
Creating Categories...
✓ Created 5 categories

Creating Levels...
✓ Created 5 levels

==================================================
✓ Database seeding completed successfully!
==================================================

Categories:
  - Meat (لحوم)
  - Chicken (فراخ)
  - Seafood (أسماك)
  - Sweets (حلويات)
  - Drinks (مشروبات)

Levels:
  - Fast Food (أكلات سريعة)
  - Home Cooked (أكلات بيتية)
  - Special Dishes (أكلات مميزة)
  - Diet & Healthy (دايت وصحي)
  - Occasions & Holidays (مناسبات وأعياد) [SPECIAL]
```

## UI/UX Features

### Responsive Design
- **Desktop:** Multi-column grids (3-4 columns)
- **Tablet:** 2-3 column grids
- **Mobile:** Single column with optimized cards

### Visual Design
- Premium Orange color scheme (`#FF5A00`, `#FF8C42`)
- Gradient backgrounds
- Smooth hover animations with elevation
- Color-coded level badges
- Circular category icons
- Special occasion highlight (gold border + ✨)

### Card Styling
- **Category Cards:** Icon + Title + Description + Dish Count
- **Level Cards:** Icon + Title + Description + Color Tag + Dish Count
- **Dish Cards:** Image + Title + Chef + Price + Rating + Badges

### Performance
- Lazy loading of images
- Efficient API calls with language parameter
- Cached language preferences
- Minimal re-renders with efficient JavaScript

## File Structure

```
src/Frontend/
├── categories.html          # Categories list page
├── category.html            # Category detail page
├── levels.html              # Levels list page
├── level.html               # Level detail page
├── index.html               # Home page (updated)
├── assets/
│   ├── lang/
│   │   ├── ar.json          # Arabic translations
│   │   ├── en.json          # English translations
│   │   └── ... (others)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       ├── main.js          # Main JS (updated)
│       ├── i18n.js          # Translation system
│       └── common.js

src/backend/
├── routes/
│   └── browse.py            # Browse routes (complete)
├── models.py                # Category, Level models
├── app.py

seed_categories_levels.py     # Database seeding script
```

## Integration Notes

### Backward Compatibility
- ✓ All existing routes and authentication intact
- ✓ Existing Dish model fields preserved
- ✓ New fields are optional and default-friendly
- ✓ Legacy API endpoints unchanged

### Authentication
- Public routes: Browse pages don't require login
- Chef routes: Can see their own dishes
- Admin routes: Protected for admin-only operations

### Database Migrations
- Models already define relationships
- Run seed script after first deployment
- Schema auto-creates on app startup

## Testing Checklist

- [ ] Categories list loads and displays correctly
- [ ] Category detail page shows dishes grouped by level
- [ ] Levels list loads with special occasions highlighted
- [ ] Level detail page shows dishes grouped by category
- [ ] Language toggle works on all new pages
- [ ] RTL/LTR layout switches correctly
- [ ] Mobile responsive on all screen sizes
- [ ] API endpoints return correct data
- [ ] Error states display properly
- [ ] Navigation between pages works smoothly
- [ ] Home page sections load and display correctly
- [ ] "View All" buttons navigate to list pages

## Future Enhancements

1. **Advanced Filtering**
   - Price range filters
   - Rating filters
   - Availability filters

2. **Search & Discovery**
   - Full-text search
   - Auto-complete suggestions
   - Recent searches

3. **Recommendations**
   - Popular dishes
   - Trending categories
   - Personalized suggestions

4. **Analytics**
   - View counts per category/level
   - User browsing patterns
   - Popular combinations

5. **Admin Dashboard**
   - Category/Level management UI
   - Dish management by category/level
   - Analytics and reports

## Support & Maintenance

### Common Issues

**Q: Pages load but show no data**
A: Run the seed script to populate categories and levels

**Q: Language switcher doesn't work**
A: Check browser localStorage is enabled

**Q: Images not loading**
A: Ensure image URLs in database are valid

### Debug Mode
Add to browser console:
```javascript
// Enable logging
localStorage.setItem('debug_browse', 'true');
window.location.reload();
```

---

**Version:** 1.0
**Last Updated:** January 21, 2026
**Status:** Production Ready
