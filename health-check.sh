#!/bin/bash

# ======================================
# El-Akeil Server Health Monitoring
# ======================================
# This script monitors the health of the El-Akeil server

DOMAIN="el-akeil.com"
APP_URL="https://$DOMAIN"
ALERT_EMAIL="admin@$DOMAIN"
LOG_FILE="/var/log/el-akeil-health.log"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Logging function
log_status() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Check if application is running
check_app_status() {
    if systemctl is-active --quiet el-akeil; then
        echo -e "${GREEN}✅ Application is running${NC}"
        log_status "✅ Application is running"
        return 0
    else
        echo -e "${RED}❌ Application is NOT running${NC}"
        log_status "❌ Application is NOT running - Restarting..."
        sudo systemctl restart el-akeil
        return 1
    fi
}

# Check if website is responding
check_website_status() {
    HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$APP_URL")
    
    if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "301" ] || [ "$HTTP_CODE" = "302" ]; then
        echo -e "${GREEN}✅ Website is responding (HTTP $HTTP_CODE)${NC}"
        log_status "✅ Website responding with HTTP $HTTP_CODE"
        return 0
    else
        echo -e "${RED}❌ Website returned HTTP $HTTP_CODE${NC}"
        log_status "❌ Website returned HTTP $HTTP_CODE"
        return 1
    fi
}

# Check API health
check_api_status() {
    API_RESPONSE=$(curl -s "$APP_URL/api/browse/categories" | jq '.' 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ API is responding${NC}"
        log_status "✅ API is responding"
        return 0
    else
        echo -e "${RED}❌ API is NOT responding${NC}"
        log_status "❌ API is NOT responding"
        return 1
    fi
}

# Check disk space
check_disk_space() {
    DISK_USAGE=$(df /var/www/el-akeil | awk 'NR==2 {print $5}' | sed 's/%//')
    
    if [ "$DISK_USAGE" -lt 80 ]; then
        echo -e "${GREEN}✅ Disk space OK ($DISK_USAGE% used)${NC}"
        log_status "✅ Disk space OK ($DISK_USAGE% used)"
        return 0
    else
        echo -e "${RED}❌ Disk space LOW ($DISK_USAGE% used)${NC}"
        log_status "❌ Disk space LOW ($DISK_USAGE% used)"
        return 1
    fi
}

# Check memory usage
check_memory_usage() {
    MEM_USAGE=$(free | grep Mem | awk '{printf("%.0f", $3/$2 * 100.0)}')
    
    if [ "$MEM_USAGE" -lt 80 ]; then
        echo -e "${GREEN}✅ Memory OK ($MEM_USAGE% used)${NC}"
        log_status "✅ Memory OK ($MEM_USAGE% used)"
        return 0
    else
        echo -e "${YELLOW}⚠️  Memory HIGH ($MEM_USAGE% used)${NC}"
        log_status "⚠️  Memory HIGH ($MEM_USAGE% used)"
        return 1
    fi
}

# Check CPU usage
check_cpu_usage() {
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{printf("%.0f", 100 - $1)}')
    
    if [ "$CPU_USAGE" -lt 80 ]; then
        echo -e "${GREEN}✅ CPU OK ($CPU_USAGE% used)${NC}"
        log_status "✅ CPU OK ($CPU_USAGE% used)"
        return 0
    else
        echo -e "${YELLOW}⚠️  CPU HIGH ($CPU_USAGE% used)${NC}"
        log_status "⚠️  CPU HIGH ($CPU_USAGE% used)"
        return 1
    fi
}

# Check database connectivity
check_database_status() {
    DB_FILE="/var/www/el-akeil/src/backend/data.db"
    
    if [ -f "$DB_FILE" ]; then
        DB_SIZE=$(du -h "$DB_FILE" | awk '{print $1}')
        echo -e "${GREEN}✅ Database exists ($DB_SIZE)${NC}"
        log_status "✅ Database exists ($DB_SIZE)"
        return 0
    else
        echo -e "${RED}❌ Database file NOT found${NC}"
        log_status "❌ Database file NOT found"
        return 1
    fi
}

# Generate health report
generate_report() {
    echo ""
    echo "╔════════════════════════════════════════╗"
    echo "║   El-Akeil Health Check Report        ║"
    echo "║   $(date '+%Y-%m-%d %H:%M:%S')           ║"
    echo "╚════════════════════════════════════════╝"
    echo ""
    
    echo "🔍 Checking Services..."
    check_app_status
    check_website_status
    check_api_status
    
    echo ""
    echo "💾 Checking Resources..."
    check_disk_space
    check_memory_usage
    check_cpu_usage
    check_database_status
    
    echo ""
    echo "📊 System Information:"
    echo "  - Hostname: $(hostname)"
    echo "  - Uptime: $(uptime | awk -F'up' '{print $2}' | cut -d',' -f1)"
    echo "  - Load Average: $(uptime | awk -F'load average:' '{print $2}')"
    
    echo ""
}

# Main execution
case "${1:-full}" in
    app)
        check_app_status
        ;;
    website)
        check_website_status
        ;;
    api)
        check_api_status
        ;;
    disk)
        check_disk_space
        ;;
    memory)
        check_memory_usage
        ;;
    cpu)
        check_cpu_usage
        ;;
    database)
        check_database_status
        ;;
    full)
        generate_report
        ;;
    *)
        echo "Usage: $0 {app|website|api|disk|memory|cpu|database|full}"
        exit 1
        ;;
esac
