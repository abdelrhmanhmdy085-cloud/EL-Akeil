# 🍽️ El Akeil - إعداد Windows

## الخيار 1: التشغيل السريع (الأسهل) ⚡

```bash
# انقر نقراً مزدوجاً على:
run.bat
```

أو من PowerShell:
```powershell
.\run.ps1
```

## الخيار 2: الإعداد الكامل 🔧

### المرة الأولى فقط:

```bash
# انقر نقراً مزدوجاً على:
setup.bat
```

أو من PowerShell:
```powershell
.\setup.ps1
```

## الخيار 3: الإعداد اليدوي 📝

```powershell
# 1️⃣ الدخول على فولدر المشروع
cd "D:\3abdo\El Akeil"

# 2️⃣ إنشاء Virtual Environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 3️⃣ تثبيت المتطلبات
pip install --upgrade pip
pip install -r requirements.txt

# 4️⃣ متغيرات البيئة
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
$env:SECRET_KEY = "change_this_secret_key_in_production"

# 5️⃣ تشغيل السيرفر
cd "src\backend"
python app.py
```

## الدخول للتطبيق 🌐

بعد تشغيل السيرفر، افتح المتصفح واكتب:

```
http://localhost:5000
```

## المتطلبات 📦

- **Python**: 3.8 أو أحدث
- **Windows**: 10 أو أحدث
- **RAM**: 2 GB على الأقل
- **Internet**: للأيقونات والخطوط من CDN

## الأوامر المتقدمة 🎯

### استخدام PowerShell مع خيارات:

```powershell
# التشغيل الكامل (الافتراضي)
.\setup.ps1

# بدء Flask shell
.\setup.ps1 -Action shell

# تشغيل الاختبارات
.\setup.ps1 -Action test

# ملء قاعدة البيانات بالبيانات التجريبية
.\setup.ps1 -Action seed

# تخطي إنشاء Virtual Environment
.\setup.ps1 -SkipVenv

# تخطي تثبيت المتطلبات
.\setup.ps1 -SkipDeps
```

## البيانات الافتراضية 📊

عند الإعداد الأول، سيتم إنشاء:

- ✅ قاعدة بيانات SQLite (`src/backend/data.db`)
- ✅ جداول النماذج (User, Chef, Driver, Dish, Category, Level)
- ✅ فئات أساسية (أسماك، دواجن، لحوم، خضروات)
- ✅ مستويات الخدمة (اقتصادي، عادي، متميز)

## حل المشاكل 🔧

### المشكلة: Python غير معروف

```bash
# حمّل Python من: https://www.python.org/downloads/
# تأكد من تحديد: "Add Python to PATH"
```

### المشكلة: Virtual Environment لا يعمل

```powershell
# احذف المجلد واعد الإنشاء:
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### المشكلة: الميناء 5000 مشغول

```python
# عدّل في src/backend/app.py:
if __name__ == "__main__":
    socketio.run(app, debug=True, port=8000)  # غيّر إلى 8000
```

### المشكلة: pip لا يعمل

```powershell
# استخدم Python module بدلاً من pip:
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## الهيكل الأساسي 📁

```
D:\3abdo\El Akeil\
├── setup.ps1           ← سكريبت PowerShell
├── setup.bat           ← سكريبت Batch (Windows)
├── run.ps1             ← تشغيل سريع PowerShell
├── run.bat             ← تشغيل سريع Batch
├── requirements.txt    ← المتطلبات
├── src/
│   ├── backend/
│   │   ├── app.py      ← تطبيق Flask الرئيسي
│   │   ├── models.py   ← نماذج قاعدة البيانات
│   │   ├── routes/     ← مسارات API
│   │   └── data.db     ← قاعدة البيانات
│   └── Frontend/
│       ├── index.html
│       ├── chef_register.html
│       ├── driver_register.html
│       └── ...
└── .venv/              ← البيئة الافتراضية (يتم إنشاؤها)
```

## ملاحظات أمان 🔐

⚠️ **قبل النشر على الإنتاج**:

1. غيّر `SECRET_KEY` في ملفات البيئة
2. عدّل `FLASK_DEBUG` إلى `False`
3. استخدم قاعدة بيانات احترافية (PostgreSQL بدلاً من SQLite)
4. عدّل إعدادات CORS حسب الحاجة

## تحديثات المستقبل 🚀

- [ ] Docker support
- [ ] Linux/Mac scripts
- [ ] Database migrations
- [ ] Automated testing
- [ ] CI/CD pipeline

---

**حالة الخادم**: ✅ جاهز للتطوير

**آخر تحديث**: 22 يناير 2026
