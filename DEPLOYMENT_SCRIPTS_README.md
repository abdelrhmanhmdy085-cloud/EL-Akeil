# 🚀 El-Akeil Deployment Scripts

مجموعة شاملة من السكريبتات لنشر وإدارة تطبيق El-Akeil على Linux/Ubuntu.

## 📁 الملفات المتضمنة

### 1. **deploy.sh** - سكريبت النشر الرئيسي
- ✅ النشر الكامل والأول
- ✅ إنشاء البيئة الافتراضية
- ✅ تثبيت المتطلبات
- ✅ إعداد قاعدة البيانات
- ✅ تكوين Nginx و SSL
- ✅ إنشاء خدمة Systemd

**الاستخدام:**
```bash
sudo bash deploy.sh
```

**المدة المتوقعة:** 5-10 دقائق

---

### 2. **health-check.sh** - فحص صحة التطبيق
يفحص:
- ✅ حالة التطبيق (running/stopped)
- ✅ استجابة الموقع (HTTP status)
- ✅ استجابة API
- ✅ استهلاك الذاكرة
- ✅ استخدام CPU
- ✅ المساحة المتاحة على القرص
- ✅ اتصال قاعدة البيانات

**الاستخدام:**
```bash
# فحص شامل
bash health-check.sh full

# فحص التطبيق فقط
bash health-check.sh app

# فحص الموقع فقط
bash health-check.sh website

# فحص API فقط
bash health-check.sh api

# فحص الموارد
bash health-check.sh disk
bash health-check.sh memory
bash health-check.sh cpu

# فحص قاعدة البيانات
bash health-check.sh database
```

---

### 3. **backup.sh** - النسخ الاحتياطية
- ✅ نسخ احتياطية يومية من قاعدة البيانات
- ✅ حفظ مع checksum للتحقق من السلامة
- ✅ حذف نسخ احتياطية قديمة (أكثر من 30 يوم)
- ✅ إمكانية الرفع للسحابة (AWS S3, Google Cloud, etc.)

**الاستخدام:**
```bash
bash backup.sh
```

---

### 4. **setup-cron.sh** - جدولة المهام الآلية
يعد:
- ✅ فحص صحة التطبيق كل 5 دقائق
- ✅ نسخ احتياطية يومية الساعة 2 صباحاً
- ✅ حذف النسخ الاحتياطية القديمة
- ✅ تجديد شهادات SSL
- ✅ مسح السجلات القديمة
- ✅ إعادة تشغيل التطبيق تلقائياً إذا توقف

**الاستخدام:**
```bash
sudo bash setup-cron.sh
```

---

### 5. **.env.production** - إعدادات الإنتاج
يحتوي على:
- ✅ مفاتيح سرية
- ✅ بيانات الاتصال بقاعدة البيانات
- ✅ بيانات بوابات الدفع
- ✅ إعدادات البريد الإلكتروني
- ✅ إعدادات الأمان

**ملاحظة:** لا تنسَ تغيير القيم قبل النشر!

---

## 🚀 البدء السريع

### الخطوة 1: الاتصال بالسيرفر
```bash
ssh root@your-server-ip
```

### الخطوة 2: تحميل السكريبتات
```bash
cd /root
wget https://your-repo-url/deploy.sh
chmod +x deploy.sh
```

### الخطوة 3: تشغيل النشر
```bash
sudo bash deploy.sh
```

### الخطوة 4: التحقق من الحالة
```bash
bash health-check.sh full
```

---

## 📊 الأوامر اليومية

### مراقبة الموقع
```bash
# فحص شامل
bash health-check.sh full

# عرض السجلات
sudo journalctl -u el-akeil -f
```

### إدارة التطبيق
```bash
# إعادة تشغيل
sudo systemctl restart el-akeil

# إيقاف
sudo systemctl stop el-akeil

# بدء
sudo systemctl start el-akeil

# حالة
sudo systemctl status el-akeil
```

### إدارة Nginx
```bash
# اختبار الإعدادات
sudo nginx -t

# إعادة تشغيل
sudo systemctl restart nginx

# مشاهدة السجلات
sudo tail -f /var/log/nginx/access.log
```

### النسخ الاحتياطية
```bash
# نسخة احتياطية يدوية
bash backup.sh

# عرض النسخ الاحتياطية
ls -lh /var/backups/el-akeil/
```

---

## 🔐 الأمان

### 1. غيّر SECRET_KEY
```bash
# على السيرفر
nano /var/www/el-akeil/.env

# أضف:
SECRET_KEY=your_super_secret_key_here
```

### 2. عطّل DEBUG Mode
```bash
# تأكد من أن FLASK_DEBUG=0
```

### 3. كوّن Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 4. حدّث النظام بانتظام
```bash
sudo apt update && sudo apt upgrade -y
```

---

## 🚨 حل المشاكل

### الموقع لا يفتح
```bash
# 1. تحقق من التطبيق
sudo systemctl status el-akeil

# 2. عرض السجلات
sudo journalctl -u el-akeil -n 100

# 3. تحقق من Nginx
sudo nginx -t

# 4. اختبر مباشرة
curl http://127.0.0.1:8000
```

### الأداء بطيء
```bash
# زد عدد العمال
# اعدّل: -w 4 إلى -w 8 في /etc/systemd/system/el-akeil.service

sudo systemctl daemon-reload
sudo systemctl restart el-akeil
```

### استهلاك الذاكرة مرتفع
```bash
# اعرض التفاصيل
ps aux | grep gunicorn

# إعادة تشغيل
sudo systemctl restart el-akeil
```

---

## 📈 المراقبة

### استخدام htop
```bash
sudo apt install -y htop
htop
```

### استخدام Uptime Robot (خارجي)
1. اذهب إلى [uptimerobot.com](https://uptimerobot.com)
2. أنشئ monitor جديد
3. أضف: `https://el-akeil.com`

### استخدم Healthchecks.io
```bash
# قم بإضافة ping URL إلى cron jobs
curl https://hc-ping.com/your-unique-id
```

---

## 📝 الصيانة الدورية

### أسبوعياً
- ✅ تحقق من استهلاك الموارد
- ✅ راجع السجلات بحثاً عن الأخطاء
- ✅ تحقق من المساحة المتاحة

### شهرياً
- ✅ حدّث النظام
- ✅ راجع النسخ الاحتياطية
- ✅ اختبر استعادة النسخة الاحتياطية

### سنوياً
- ✅ أعد تقييم استراتيجية الأمان
- ✅ اختبر خطة الكوارث
- ✅ راجع التوثيق

---

## 📞 الدعم

- **الموقع**: https://el-akeil.com
- **البريد**: support@el-akeil.com
- **WhatsApp**: 01001144459

---

## 📚 الموارد الإضافية

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - دليل شامل
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - دليل الإعداد المحلي
- [.env.production](.env.production) - إعدادات الإنتاج

---

**آخر تحديث**: 22 يناير 2026
