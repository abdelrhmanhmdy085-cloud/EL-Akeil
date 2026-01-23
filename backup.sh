#!/bin/bash

# ======================================
# El-Akeil Database Backup Script
# ======================================

PROJECT_PATH="/var/www/el-akeil"
DB_FILE="$PROJECT_PATH/src/backend/data.db"
BACKUP_DIR="/var/backups/el-akeil"
RETENTION_DAYS=30
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/el-akeil-$DATE.db"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Create backup directory
if [ ! -d "$BACKUP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    echo "✅ Backup directory created: $BACKUP_DIR"
fi

# Check if database exists
if [ ! -f "$DB_FILE" ]; then
    echo -e "${RED}❌ Database file not found: $DB_FILE${NC}"
    exit 1
fi

echo "🔄 Starting database backup..."
echo "   Source: $DB_FILE"
echo "   Destination: $BACKUP_FILE"

# Create backup
if cp "$DB_FILE" "$BACKUP_FILE"; then
    echo -e "${GREEN}✅ Backup completed successfully${NC}"
    
    # Get file size
    SIZE=$(du -h "$BACKUP_FILE" | awk '{print $1}')
    echo "   Size: $SIZE"
    
    # Create checksum
    CHECKSUM=$(sha256sum "$BACKUP_FILE" | awk '{print $1}')
    echo "$CHECKSUM" > "$BACKUP_FILE.sha256"
    echo "   Checksum: $CHECKSUM"
else
    echo -e "${RED}❌ Backup failed${NC}"
    exit 1
fi

# Clean up old backups
echo ""
echo "🧹 Cleaning up old backups (keeping last $RETENTION_DAYS days)..."
OLD_BACKUPS=$(find "$BACKUP_DIR" -name "el-akeil-*.db" -mtime +$RETENTION_DAYS)

if [ -z "$OLD_BACKUPS" ]; then
    echo "   ℹ️  No old backups to remove"
else
    echo "$OLD_BACKUPS" | while read file; do
        echo "   🗑️  Removing: $(basename $file)"
        rm -f "$file" "$file.sha256"
    done
fi

# Summary
echo ""
echo "📊 Backup Summary:"
echo "   Total backups: $(ls -1 $BACKUP_DIR/*.db 2>/dev/null | wc -l)"
echo "   Backup size: $(du -sh $BACKUP_DIR | awk '{print $1}')"
echo "   Latest backup: $(date -r $BACKUP_FILE '+%Y-%m-%d %H:%M:%S')"

# Optional: Upload to cloud storage
# Uncomment to enable cloud backup

# echo ""
# echo "☁️  Uploading to cloud storage..."
# 
# # AWS S3
# aws s3 cp "$BACKUP_FILE" "s3://el-akeil-backups/" --region us-east-1
# 
# # Or Google Cloud Storage
# gsutil cp "$BACKUP_FILE" "gs://el-akeil-backups/"
# 
# # Or DigitalOcean Spaces
# aws s3 cp "$BACKUP_FILE" "s3://el-akeil/" --endpoint-url https://nyc3.digitaloceanspaces.com

echo ""
echo -e "${GREEN}✅ Backup process completed${NC}"
