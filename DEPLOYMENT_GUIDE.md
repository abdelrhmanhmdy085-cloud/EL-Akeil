# 🚀 دليل نشر El-Akeil على Domain

## النشر الأول - الخطوات الكاملة 🔧

### المتطلبات:
- ✅ سيرفر Linux (Ubuntu 20.04+)
- ✅ Domain تم إشارته (el-akeil.com)
- ✅ SSH access بصلاحيات root

---

## الطريقة 1: الطريقة السريعة (الأسهل) ⚡

```bash
# 1. اتصل بالسيرفر
ssh root@your-server-ip

# 2. انسخ السكريبت
cd /root
wget https://your-repo-url/deploy.sh
chmod +x deploy.sh

# 3. شغّل السكريبت (سيستغرق 5-10 دقائق)
sudo bash deploy.sh
```

---

## الطريقة 2: الخطوات اليدوية 📝

### 1️⃣ تحديث النظام
```bash
sudo apt update && sudo apt upgrade -y
```

### 2️⃣ تثبيت المتطلبات
```bash
sudo apt install -y \
  python3 python3-venv python3-pip python3-dev \
  nginx certbot python3-certbot-nginx \
  git curl wget supervisor
```

### 3️⃣ إنشاء مستخدم التطبيق
```bash
sudo useradd -m -s /bin/bash el-akeil
sudo usermod -aG sudo el-akeil
```

### 4️⃣ إنشاء مجلد المشروع
```bash
sudo mkdir -p /var/www/el-akeil
sudo chown -R el-akeil:www-data /var/www/el-akeil
cd /var/www/el-akeil
```

### 5️⃣ استنساخ المشروع (أو رفع الملفات)
```bash
# استخدم git (إذا كان المشروع على GitHub)
sudo -u el-akeil git clone https://github.com/your-repo/el-akeil.git .

# أو استخدم SCP لرفع الملفات من جهازك المحلي:
# scp -r ./src root@your-server-ip:/var/www/el-akeil/
# scp requirements.txt root@your-server-ip:/var/www/el-akeil/
```

### 6️⃣ إعداد البيئة الافتراضية
```bash
sudo -u el-akeil python3 -m venv /var/www/el-akeil/.venv
sudo -u el-akeil /var/www/el-akeil/.venv/bin/pip install --upgrade pip
sudo -u el-akeil /var/www/el-akeil/.venv/bin/pip install -r /var/www/el-akeil/requirements.txt
sudo -u el-akeil /var/www/el-akeil/.venv/bin/pip install gunicorn
```

### 7️⃣ إعداد قاعدة البيانات
```bash
cd /var/www/el-akeil
sudo -u el-akeil /var/www/el-akeil/.venv/bin/python3 << EOF
from src.backend.app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
print("Database created successfully!")
EOF
```

### 8️⃣ إنشاء خدمة Systemd
```bash
sudo tee /etc/systemd/system/el-akeil.service > /dev/null << EOF
[Unit]
Description=El-Akeil Flask Application
After=network.target

[Service]
User=el-akeil
Group=www-data
WorkingDirectory=/var/www/el-akeil/src/backend
Environment="PATH=/var/www/el-akeil/.venv/bin"
ExecStart=/var/www/el-akeil/.venv/bin/gunicorn -w 4 -b 127.0.0.1:8000 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable el-akeil.service
sudo systemctl start el-akeil.service
```

### 9️⃣ إعداد Nginx
```bash
sudo tee /etc/nginx/sites-available/el-akeil > /dev/null << EOF
upstream el_akeil {
    server 127.0.0.1:8000;
}

server {
    server_name el-akeil.com www.el-akeil.com;
    client_max_body_size 20M;

    location /assets/ {
        alias /var/www/el-akeil/src/Frontend/assets/;
        expires 30d;
    }

    location /api/ {
        proxy_pass http://el_akeil;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location /socket.io {
        proxy_pass http://el_akeil/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
    }

    location / {
        proxy_pass http://el_akeil;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    location ~ /\.ht {
        deny all;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/el-akeil /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 🔟 تفعيل SSL (HTTPS)
```bash
sudo certbot --nginx -d el-akeil.com -d www.el-akeil.com
```

**اختر المسار الأول لإعادة التوجيه من HTTP إلى HTTPS**

---

## التحقق من الحالة 🔍

```bash
# تحقق من حالة التطبيق
sudo systemctl status el-akeil

# تحقق من حالة Nginx
sudo systemctl status nginx

# عرض السجلات
sudo journalctl -u el-akeil -f

# اختبر الاتصال
curl -I https://el-akeil.com
```

---

## الأوامر المهمة 📋

### إعادة تشغيل التطبيق
```bash
sudo systemctl restart el-akeil
```

### عرض السجلات الحية
```bash
sudo journalctl -u el-akeil -f
```

### إعادة تشغيل Nginx
```bash
sudo systemctl restart nginx
sudo nginx -s reload
```

### التحقق من إعدادات Nginx
```bash
sudo nginx -t
```

### إدارة شهادات SSL
```bash
# تجديد الشهادات
sudo certbot renew

# عرض الشهادات
sudo certbot certificates
```

---

## التحديثات المستقبلية 🔄

### سحب أحدث نسخة من المشروع
```bash
cd /var/www/el-akeil
sudo -u el-akeil git pull origin main
```

### إعادة تشغيل التطبيق بعد التحديث
```bash
sudo systemctl restart el-akeil
```

---

## حل المشاكل 🔧

### المشكلة: الموقع لا يفتح

```bash
# 1. تحقق من حالة التطبيق
sudo systemctl status el-akeil

# 2. اعرض السجلات
sudo journalctl -u el-akeil -n 50

# 3. تحقق من Nginx
sudo nginx -t
sudo systemctl status nginx

# 4. اختبر الاتصال مباشرة
curl http://127.0.0.1:8000
```

### المشكلة: الأداء بطيء

```bash
# زد عدد العمال
# عدّل /etc/systemd/system/el-akeil.service
# غيّر: -w 4 إلى -w 8 (أو أكثر حسب عدد CPU)

sudo systemctl daemon-reload
sudo systemctl restart el-akeil
```

### المشكلة: استهلاك الذاكرة مرتفع

```bash
# اعرض استهلاك الموارد
ps aux | grep gunicorn

# قلل عدد العمال مؤقتاً
sudo systemctl restart el-akeil
```

### المشكلة: SSL Certificate منتهي الصلاحية

```bash
# جدد الشهادة يدويًا
sudo certbot renew --force-renewal
```

---

## النسخ الاحتياطية 💾

### عمل نسخة احتياطية من قاعدة البيانات
```bash
# يومياً في 2 صباحاً
sudo crontab -e

# أضف السطر:
0 2 * * * sudo cp /var/www/el-akeil/src/backend/data.db /var/backups/el-akeil-$(date +\%Y\%m\%d).db
```

### استعادة من النسخة الاحتياطية
```bash
sudo cp /var/backups/el-akeil-20260122.db /var/www/el-akeil/src/backend/data.db
sudo chown el-akeil:www-data /var/www/el-akeil/src/backend/data.db
sudo systemctl restart el-akeil
```

---

## الأمان 🔐

### تحقق من Firewall
```bash
sudo ufw status
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### غيّر SECRET_KEY
```bash
# على السيرفر، عدّل:
nano /var/www/el-akeil/.env

# وأضف:
# SECRET_KEY=your_new_secret_key_here
```

### عطّل DEBUG Mode
```bash
# تأكد من أن FLASK_DEBUG=0 في .env
```

---

## المراقبة المستمرة 👁️

### استخدم `htop` لمراقبة الموارد
```bash
sudo apt install -y htop
htop
```

### اجعل السيرفر يرسل تنبيهات على Slack/Discord
```bash
# ستحتاج لأداة مراقبة مثل:
# - Uptime Robot
# - Healthchecks.io
# - New Relic
```

---

## المتطلبات الإضافية 📦

### استخدام PostgreSQL بدلاً من SQLite
```bash
sudo apt install -y postgresql postgresql-contrib
sudo -u postgres createdb el_akeil
sudo -u postgres createuser el_akeil
```

### استخدام Redis للـ Caching
```bash
sudo apt install -y redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

---

## الدعم والمساعدة 📞

- **الموقع**: https://el-akeil.com
- **البريد الإلكتروني**: support@el-akeil.com
- **WhatsApp**: 01001144459

---

**آخر تحديث**: 22 يناير 2026
