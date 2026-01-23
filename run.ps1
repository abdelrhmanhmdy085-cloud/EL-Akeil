# ================================
# El Akeil - Quick Start
# ================================

# للتشغيل السريع بدون setup مرة أخرى
cd "D:\3abdo\El Akeil"

# تفعيل البيئة الافتراضية
.\.venv\Scripts\Activate.ps1

# تعيين المتغيرات
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = "1"
$env:SECRET_KEY = "change_this_secret_key_in_production"

# تشغيل السيرفر
Write-Host "🚀 Starting El Akeil Server..." -ForegroundColor Green
Write-Host "📱 Access at: http://localhost:5000" -ForegroundColor Cyan
Write-Host "🛑 Press Ctrl+C to stop`n" -ForegroundColor Yellow

cd "src\backend"
python app.py
