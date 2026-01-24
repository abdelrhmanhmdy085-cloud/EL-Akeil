# Railway Setup Instructions (خطوات الإعداد)

## الخطوات الأساسية:

### 1️⃣ تثبيت Railway CLI (اختياري)
```powershell
npm install -g @railway/cli
```

### 2️⃣ تسجيل الدخول إلى Railway
```powershell
railway login
```

### 3️⃣ إنشاء مشروع جديد
```powershell
cd D:\3abdo\El Akeil
railway init
```

### 4️⃣ ربط المشروع بـ GitHub
بدلاً من استخدام CLI، الطريقة الأسهل:
- اذهب إلى [railway.app](https://railway.app)
- انقر على "Create a new project"
- اختر "Deploy from GitHub"
- اختر مستودع `EL-Akeil`
- Railway سيكتشف `Dockerfile` تلقائياً

### 5️⃣ اضبط متغيرات البيئة في Railway Dashboard
```
FLASK_ENV=production
FLASK_DEBUG=0
SECRET_KEY=your_random_secret_key_here
```

### 6️⃣ انقر "Deploy"
والسرفر سيبدأ تلقائياً!

## ملفات التكوين المرفوعة:

✅ **Dockerfile** - صورة Docker للتطبيق
✅ **railway.json** - تكوين Railway
✅ **.dockerignore** - ملفات يجب تجاهلها
✅ **RAILWAY_DEPLOYMENT.md** - دليل تفصيلي
✅ **updated app.py** - يدعم متغيرات البيئة من Railway

## بعد النشر:

- سيحصل مشروعك على رابط فريد: `https://your-app.railway.app`
- أي تغيير تدفعه إلى main سيُنشر تلقائياً
- استخدم Logs في Dashboard لمراقبة الخادم

## استكشاف الأخطاء:

إذا واجهت مشاكل:
1. تحقق من Logs في Railway Dashboard
2. تأكد من أن جميع المتغيرات البيئية صحيحة
3. تأكد من أن requirements.txt محدث
4. اقرأ RAILWAY_DEPLOYMENT.md للتفاصيل الكاملة
