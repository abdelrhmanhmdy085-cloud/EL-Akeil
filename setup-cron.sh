#!/bin/bash

# ======================================
# El-Akeil Cron Jobs Setup
# ======================================
# This script sets up automated tasks for El-Akeil

CRON_FILE="/etc/cron.d/el-akeil"
PROJECT_PATH="/var/www/el-akeil"
HEALTH_CHECK_SCRIPT="$PROJECT_PATH/health-check.sh"
BACKUP_SCRIPT="$PROJECT_PATH/backup.sh"
LOG_DIR="/var/log/el-akeil"

# Create log directory
sudo mkdir -p "$LOG_DIR"
sudo chmod 755 "$LOG_DIR"

# Remove old cron file if exists
sudo rm -f "$CRON_FILE"

# Create new cron file
sudo tee "$CRON_FILE" > /dev/null << 'EOF'
# ======================================
# El-Akeil Automated Tasks
# ======================================

SHELL=/bin/bash
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# Health check every 5 minutes
*/5 * * * * root bash /var/www/el-akeil/health-check.sh full >> /var/log/el-akeil/health-check.log 2>&1

# Database backup daily at 2 AM
0 2 * * * el-akeil bash /var/www/el-akeil/backup.sh >> /var/log/el-akeil/backup.log 2>&1

# Clean old backups weekly (keep last 30 days)
0 3 * * 0 root find /var/backups/el-akeil -name "*.db" -mtime +30 -delete

# SSL certificate renewal check (Let's Encrypt)
0 3 * * * root certbot renew --quiet

# Clear application logs older than 30 days
0 4 * * * root find /var/log/el-akeil -name "*.log" -mtime +30 -delete

# Restart application if needed (check every hour)
0 * * * * root systemctl is-active el-akeil || systemctl restart el-akeil

# Update system packages weekly
0 5 * * 0 root apt update && apt upgrade -y

# Restart application daily at 3 AM for cleanup
0 3 * * * root systemctl restart el-akeil

# Compress logs older than 7 days
0 1 * * * root find /var/log/el-akeil -name "*.log" -mtime +7 | xargs -r gzip
EOF

echo "✅ Cron jobs installed at $CRON_FILE"

# List cron jobs
echo ""
echo "Installed Cron Jobs:"
sudo cat "$CRON_FILE"
