#!/bin/bash

# ======================================
# El-Akeil Domain Deployment Script
# Domain: el-akeil.com
# ======================================
# This script automates the deployment of El-Akeil on Ubuntu/Linux servers

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
DOMAIN="el-akeil.com"
PROJECT_PATH="/var/www/el-akeil"
VENV_PATH="$PROJECT_PATH/.venv"
APP_USER="el-akeil"
APP_GROUP="www-data"
WORKERS=4
PORT=8000

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   log_error "هذا السكريبت يجب أن يعمل كـ root"
   log_info "شغّل: sudo bash deploy.sh"
   exit 1
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   El-Akeil Deployment Script          ║"
echo "║   Domain: $DOMAIN                   ║"
echo "╚════════════════════════════════════════╝"
echo ""

# ============================================
# 1️⃣ Update System
# ============================================
log_info "1️⃣ تحديث النظام..."
apt update
apt upgrade -y
log_success "النظام تم تحديثه"

# ============================================
# 2️⃣ Install Dependencies
# ============================================
log_info "2️⃣ تثبيت المتطلبات..."

PACKAGES=(
    "python3"
    "python3-venv"
    "python3-pip"
    "python3-dev"
    "nginx"
    "certbot"
    "python3-certbot-nginx"
    "git"
    "curl"
    "wget"
    "supervisor"
)

for package in "${PACKAGES[@]}"; do
    if ! dpkg -l | grep -q "^ii  $package"; then
        log_info "تثبيت $package..."
        apt install -y "$package"
    else
        log_success "$package مثبت بالفعل"
    fi
done

log_success "جميع المتطلبات مثبتة"

# ============================================
# 3️⃣ Create Project Directory
# ============================================
log_info "3️⃣ إعداد مجلد المشروع..."

if [ ! -d "$PROJECT_PATH" ]; then
    log_info "إنشاء مجلد المشروع: $PROJECT_PATH"
    mkdir -p "$PROJECT_PATH"
    chown -R "$APP_USER:$APP_GROUP" "$PROJECT_PATH"
else
    log_success "مجلد المشروع موجود بالفعل"
fi

cd "$PROJECT_PATH"
log_success "مجلد المشروع جاهز"

# ============================================
# 4️⃣ Create Virtual Environment
# ============================================
log_info "4️⃣ إنشاء البيئة الافتراضية..."

if [ ! -d "$VENV_PATH" ]; then
    python3 -m venv "$VENV_PATH"
    log_success "البيئة الافتراضية تم إنشاؤها"
else
    log_success "البيئة الافتراضية موجودة بالفعل"
fi

# Activate virtual environment
source "$VENV_PATH/bin/activate"
log_success "البيئة الافتراضية تم تفعيلها"

# ============================================
# 5️⃣ Install Python Packages
# ============================================
log_info "5️⃣ تثبيت الحزم الـ Python..."

pip install --upgrade pip setuptools wheel
log_success "pip تم تحديثه"

if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    log_success "الحزم من requirements.txt تم تثبيتها"
else
    log_warning "requirements.txt لم يُعثر عليه"
fi

# Install Gunicorn
pip install gunicorn
log_success "Gunicorn تم تثبيته"

# ============================================
# 6️⃣ Setup Database
# ============================================
log_info "6️⃣ إعداد قاعدة البيانات..."

python3 << EOF
try:
    from src.backend.app import create_app, db
    app = create_app()
    with app.app_context():
        db.create_all()
    print("✅ قاعدة البيانات تم إنشاؤها بنجاح")
except Exception as e:
    print(f"⚠️  خطأ في إنشاء قاعدة البيانات: {e}")
EOF

log_success "قاعدة البيانات جاهزة"

# ============================================
# 7️⃣ Create Systemd Service
# ============================================
log_info "7️⃣ إنشاء خدمة Systemd..."

cat > /etc/systemd/system/el-akeil.service << EOF
[Unit]
Description=El-Akeil Flask Application
After=network.target

[Service]
User=$APP_USER
Group=$APP_GROUP
WorkingDirectory=$PROJECT_PATH/src/backend
Environment="PATH=$VENV_PATH/bin"
ExecStart=$VENV_PATH/bin/gunicorn -w $WORKERS -b 127.0.0.1:$PORT app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable el-akeil.service
systemctl start el-akeil.service
log_success "خدمة Systemd تم إنشاؤها وتفعيلها"

# ============================================
# 8️⃣ Configure Nginx
# ============================================
log_info "8️⃣ إعداد Nginx..."

cat > /etc/nginx/sites-available/el-akeil << EOF
upstream el_akeil {
    server 127.0.0.1:$PORT;
}

server {
    server_name $DOMAIN www.$DOMAIN;
    client_max_body_size 20M;

    # Static files
    location /assets/ {
        alias $PROJECT_PATH/src/Frontend/assets/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # API endpoints
    location /api/ {
        proxy_pass http://el_akeil;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Socket.IO
    location /socket.io {
        proxy_pass http://el_akeil/socket.io;
        proxy_http_version 1.1;
        proxy_buffering off;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "Upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }

    # Frontend pages
    location / {
        proxy_pass http://el_akeil;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Deny access to sensitive files
    location ~ /\.ht {
        deny all;
    }

    location ~ \.db$ {
        deny all;
    }

    # Gzip compression
    gzip on;
    gzip_types text/plain text/css text/xml application/json application/javascript;
    gzip_min_length 1024;
}
EOF

# Enable site
if [ ! -L /etc/nginx/sites-enabled/el-akeil ]; then
    ln -s /etc/nginx/sites-available/el-akeil /etc/nginx/sites-enabled/
    log_success "الموقع تم تفعيله في Nginx"
fi

# Disable default site
if [ -L /etc/nginx/sites-enabled/default ]; then
    rm /etc/nginx/sites-enabled/default
fi

# Test Nginx configuration
nginx -t
systemctl restart nginx
log_success "Nginx تم إعادة تشغيله"

# ============================================
# 9️⃣ Setup SSL Certificate
# ============================================
log_info "9️⃣ إعداد شهادة SSL..."

if certbot certonly --nginx -d "$DOMAIN" -d "www.$DOMAIN" --non-interactive --agree-tos -m admin@$DOMAIN --register-unsafely-without-email 2>/dev/null; then
    log_success "شهادة SSL تم إنشاؤها"
else
    log_warning "لم يتمكن من إنشاء شهادة SSL. ستحتاج لإنشاءها يدويًا:"
    log_info "certbot --nginx -d $DOMAIN -d www.$DOMAIN"
fi

# ============================================
# 🔟 Setup Firewall
# ============================================
log_info "🔟 إعداد Firewall..."

if command -v ufw &> /dev/null; then
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    log_success "Firewall تم إعداده"
else
    log_warning "ufw لم يتم العثور عليه"
fi

# ============================================
# 1️⃣1️⃣ Setup Log Rotation
# ============================================
log_info "1️⃣1️⃣ إعداد تدوير السجلات..."

cat > /etc/logrotate.d/el-akeil << EOF
$PROJECT_PATH/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    create 0640 $APP_USER $APP_GROUP
    sharedscripts
}
EOF

log_success "تدوير السجلات تم إعداده"

# ============================================
# Final Status
# ============================================
echo ""
echo "╔════════════════════════════════════════╗"
echo "║    النشر اكتمل بنجاح! 🎉             ║"
echo "╚════════════════════════════════════════╝"
echo ""

log_success "الموقع متاح على: https://$DOMAIN"
log_success "الخادم يعمل على: http://127.0.0.1:$PORT"

echo ""
log_info "الأوامر المفيدة:"
echo "  - عرض حالة التطبيق: systemctl status el-akeil"
echo "  - إعادة تشغيل التطبيق: systemctl restart el-akeil"
echo "  - عرض السجلات: journalctl -u el-akeil -f"
echo "  - عرض حالة Nginx: systemctl status nginx"
echo "  - إعادة تشغيل Nginx: systemctl restart nginx"
echo ""

log_success "تم إنشاء المستخدم 'el-akeil'. يمكنك تسجيل الدخول بـ:"
log_info "ssh $APP_USER@your-server-ip"

echo ""
log_warning "⚠️  تذكرات أمان:"
echo "  1. غيّر SECRET_KEY في ملف البيئة"
echo "  2. عطّل DEBUG mode في الإنتاج"
echo "  3. استخدم قاعدة بيانات احترافية (PostgreSQL)"
echo "  4. قم بإعداد نسخ احتياطية يومية"
echo "  5. راقب استهلاك الموارد"
echo ""
