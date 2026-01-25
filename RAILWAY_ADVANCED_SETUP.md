# Railway Deployment - Complete Setup Guide

## تحضير المشروع للنشر على Railway

### ✅ ما تم إضافته:

1. **Dockerfile** - محسّن مع:
   - استخدام python 3.13 slim
   - caching محسّن للـ layers
   - health check
   - non-root user

2. **ملفات التكوين:**
   - `railway.yaml` - التكوين الرئيسي
   - `railway.json` - تكوين بديل
   - `runtime.txt` - إصدار Python

3. **Environment:**
   - `.env.railway` - متغيرات الإنتاج
   - `.env.example` - نموذج البيئة

4. **Scripts:**
   - `build.sh` - سكريبت البناء
   - `start.sh` - سكريبت التشغيل
   - `check_railway_deployment.py` - فحص التوافقية

5. **CI/CD:**
   - `.github/workflows/railway-deploy.yml` - فحص تلقائي

---

## خطوات النشر على Railway

### الخطوة 1: تجهيز GitHub
```bash
git add -A
git commit -m "إضافة ملفات Railway المحسّنة"
git push origin main
```

### الخطوة 2: إنشاء حساب Railway
- اذهب إلى https://railway.app
- سجل بـ GitHub Account
- اضغط "Create a new project"

### الخطوة 3: ربط المستودع
- اختر "Deploy from GitHub"
- اختر `EL-Akeil`
- اسمح لـ Railway بالوصول إلى حسابك

### الخطوة 4: إعدادات المتغيرات

في لوحة تحكم Railway، اضبط:

```env
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your-super-secret-random-key-here-min-32-chars
PYTHONUNBUFFERED=1
PORT=5000
HOST=0.0.0.0
```

**مهم:** لا تستخدم القيم الافتراضية في الإنتاج!

### الخطوة 5: النشر
- اضغط على زر Deploy
- انتظر 2-5 دقائق
- Railway سيقدم لك رابط مثل: `https://el-akeil-production.railway.app`

---

## المراقبة والصيانة

### عرض السجلات (Logs)
```bash
# إذا كان لديك Railway CLI مثبت
railway logs
```

### الفحص السريع المحلي
```bash
python check_railway_deployment.py
```

### إعادة النشر
```bash
git commit -m "تحديث"
git push origin main
# Railway سينشر تلقائياً
```

---

## معالجة المشاكل الشائعة

### ❌ الخطأ: "Failed to build image"
- تحقق من `Dockerfile`
- تأكد من `requirements.txt` صحيح
- تحقق من سجلات Build

### ❌ الخطأ: "Port already in use"
- Railway يعين PORT تلقائياً
- تأكد أن `app.py` يستخدم `os.getenv("PORT")`

### ❌ الخطأ: "Static files not loading"
- تحقق من مسار `Frontend`
- تأكد من أن `FRONTEND_DIR` يشير للمجلد الصحيح

### ❌ قاعدة البيانات تفقد البيانات
- SQLite لا يعمل في الإنتاج (صور Docker مؤقتة)
- استخدم PostgreSQL أو قاعدة خارجية
- اضبط `DATABASE_URL` بشكل صحيح

---

## خيارات متقدمة

### إضافة قاعدة بيانات PostgreSQL

في لوحة Railway:
1. اضغط "+ New Service"
2. اختر "PostgreSQL"
3. Railway سيعطيك `DATABASE_URL` تلقائياً
4. حدّث `app.py` إن لزم

### استخدام متغيرات بيئة آمنة

```python
import os
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError("SECRET_KEY must be set in environment!")
```

### تفعيل HTTPS

Railway يفعّل HTTPS تلقائياً. تأكد من:
```python
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
```

---

## الأوامر المفيدة

```bash
# الفحص المحلي
python check_railway_deployment.py

# بناء Docker محلياً
docker build -t el-akeil .
docker run -p 5000:5000 el-akeil

# دفع التغييرات
git push origin main
```

---

## الموارد الإضافية

- [توثيق Railway](https://docs.railway.app)
- [توثيق Flask](https://flask.palletsprojects.com)
- [ملف README](./README.md)
- [دليل السرعة السريعة](./RAILWAY_QUICK_START.md)

---

**ملاحظة:** Railway يوفر 500 ساعة شهرية مجاني للمشاريع الصغيرة!
