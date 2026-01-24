# ✅ تحديث التسمية: من "Diet" إلى "Healthy"

## 📝 الملخص:
تم استبدال كلمة "Diet" بـ "Healthy" (صحي) وتحديث جميع الملفات ذات الصلة.

---

## 🔄 التغييرات التي تمت:

### 1️⃣ **قاعدة البيانات**
- ✅ تغيير اسم المستوى من `Diet` إلى `Healthy`
- ✅ التحديث في قاعدة البيانات الحالية
- ✅ تحديث الأيقونة إلى 🥗 (سلطة)

### 2️⃣ **الملفات المصدرية**

#### `src/backend/seed_db.py`
```python
# قبل:
{"name_en": "Diet", "name_ar": "دايت", "color_tag": "blue", "icon": "💪"}

# بعد:
{"name_en": "Healthy", "name_ar": "صحي", "color_tag": "blue", "icon": "🥗"}
```

#### `src/backend/models.py`
```python
# قبل:
"""Food levels (Fast, Home, Special, Diet, Occasions)"""

# بعد:
"""Food levels (Fast, Home, Special, Healthy, Occasions)"""
```

#### `src/backend/seed_demo_dishes.py`
```python
# قبل:
'level_en': 'Diet & Healthy'

# بعد:
'level_en': 'Healthy'
```

#### `seed_categories_levels.py`
```python
# قبل:
'name_ar': 'دايت وصحي'
'name_en': 'Diet & Healthy'

# بعد:
'name_ar': 'صحي'
'name_en': 'Healthy'
```

---

## 🎯 المستويات الحالية:

| الترتيب | الاسم | العربي | الأيقونة | اللون |
|--------|-------|--------|---------|-------|
| 1 | Fast Food | أكلات سريعة | 🚀 | أحمر |
| 2 | Home Cooked | أكلات بيتية | 🏠 | أخضر |
| 3 | Special | أكلات مميزة | ✨ | ذهبي |
| 4 | **Healthy** | **صحي** | **🥗** | أزرق |
| 5 | Occasions | مناسبات وأعياد | 🎉 | بنفسجي |

---

## 📊 التأثير على الموقع:

### قائمة المستويات (levels.html)
- ✅ سيظهر "Healthy" بدلاً من "Diet"
- ✅ الأيقونة الجديدة: 🥗
- ✅ الوصف: "أطباق صحية ومفيدة"

### صفحة المستوى (level.html)
- ✅ يمكنك فلترة الأطباق حسب الحالة (جاهز/غير جاهز)
- ✅ جميع الأطباق ستعرض المستوى الجديد

---

## 🔧 الملفات المعدلة:

✅ `src/backend/seed_db.py` - تحديث البيانات الأساسية  
✅ `src/backend/models.py` - تحديث التوثيق  
✅ `src/backend/seed_demo_dishes.py` - تحديث الأطباق التجريبية  
✅ `seed_categories_levels.py` - تحديث سكريبت البذور  
✅ `update_diet_to_healthy.py` - سكريبت التحديث (جديد)  

---

## ✨ الأيقونات:

- **قبل**: 💪 (عضلة - للقوة)
- **بعد**: 🥗 (سلطة - للصحة)

الأيقونة الجديدة تعكس بشكل أفضل المقصود من المستوى (أكلات صحية وليس بناء عضلات)

---

## 🚀 التطبيق على الخادم:

إذا كنت تستخدم Python scripts للبذور:

```bash
# تحديث المستوى الموجود:
python update_diet_to_healthy.py

# أو إعادة بذر قاعدة البيانات كاملة:
python seed_categories_levels.py
```

---

**آخر تحديث**: 23 يناير 2026
