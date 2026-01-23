# El Akeil Food Browsing System - Deployment Checklist

**Date:** January 21, 2026  
**System:** El Akeil - Category & Food Level Navigation  
**Status:** Ready for Deployment ✅

---

## Pre-Deployment Verification

### 1. Backend Setup
- [ ] Django/Flask app running without errors
- [ ] Database connection established
- [ ] `src/backend/routes/browse.py` all functions implemented
- [ ] Models.py has Category and Level classes
- [ ] Dish model has category_id and level_id fields

**Verification Commands:**
```bash
# Check backend runs
cd src/backend
python app.py

# Test API endpoints
curl http://localhost:5000/api/browse/categories
curl http://localhost:5000/api/browse/levels
```

### 2. Database Setup
- [ ] SQLite database initialized
- [ ] `seed_categories_levels.py` script accessible
- [ ] Database has write permissions
- [ ] No existing data conflicts

**Verification Commands:**
```bash
# Run seed script
python seed_categories_levels.py

# Verify data
# Check database shows 5 categories and 5 levels
```

### 3. Frontend Files
- [ ] `categories.html` copied to `src/Frontend/`
- [ ] `category.html` copied to `src/Frontend/`
- [ ] `levels.html` copied to `src/Frontend/`
- [ ] `level.html` copied to `src/Frontend/`
- [ ] All HTML files readable and valid

**File Checklist:**
```
src/Frontend/
├── index.html ✓ (updated)
├── categories.html ✓ (new)
├── category.html ✓ (new)
├── levels.html ✓ (updated)
├── level.html ✓ (new)
```

### 4. Language Files
- [ ] `ar.json` updated with new keys
- [ ] `en.json` updated with new keys
- [ ] Both files valid JSON
- [ ] All translation keys present

**Translation Key Verification:**
```json
Required keys:
✓ categories_title
✓ categories_subtitle
✓ levels_title
✓ levels_subtitle
✓ category_detail_title
✓ level_detail_title
✓ all_categories
✓ all_levels
✓ home_button
✓ no_categories
✓ no_levels
✓ no_dishes
✓ error_loading
✓ try_again
✓ view_all
✓ dishes_count
```

### 5. API Endpoints
Test each endpoint manually or with scripts:

```bash
# Test categories endpoint
curl "http://localhost:5000/api/browse/categories?lang=en"
# Expected: Array of 5 categories

# Test category detail
curl "http://localhost:5000/api/browse/category/1?lang=en"
# Expected: Category with grouped_by_level

# Test levels endpoint
curl "http://localhost:5000/api/browse/levels?lang=en"
# Expected: Array of 5 levels

# Test level detail
curl "http://localhost:5000/api/browse/level/1?lang=en"
# Expected: Level with grouped_by_category

# Test search
curl "http://localhost:5000/api/browse/dishes/search?lang=en"
# Expected: Array of dishes
```

**Checklist:**
- [ ] GET /api/browse/categories returns 200
- [ ] GET /api/browse/category/{id} returns 200
- [ ] GET /api/browse/levels returns 200
- [ ] GET /api/browse/level/{id} returns 200
- [ ] All endpoints have proper error handling
- [ ] Language parameter works correctly

---

## Feature Verification

### Pages Load Correctly
- [ ] http://localhost:5000/categories loads
- [ ] http://localhost:5000/levels loads
- [ ] http://localhost:5000/category.html?id=1 loads
- [ ] http://localhost:5000/level.html?id=1 loads

### Data Display
- [ ] Categories page shows all 5 categories
- [ ] Levels page shows all 5 levels (1 highlighted as special)
- [ ] Category detail shows dishes grouped by level
- [ ] Level detail shows dishes grouped by category

### Navigation
- [ ] Click category card → opens category detail
- [ ] Click level card → opens level detail
- [ ] Back button works
- [ ] "View All" buttons work from home page

### Language Support
- [ ] Page loads in Arabic by default
- [ ] Language selector works
- [ ] Switching to English displays English text
- [ ] RTL/LTR layout switches correctly
- [ ] localStorage persists language preference

### Mobile Responsiveness
- [ ] Test on 375px width (mobile)
- [ ] Test on 768px width (tablet)
- [ ] Test on 1440px width (desktop)
- [ ] All elements visible and clickable
- [ ] Grid adjusts properly

### Error States
- [ ] Try accessing category/level that doesn't exist
- [ ] Check error message displays
- [ ] Try with API down
- [ ] Check loading spinner works

---

## Browser Testing

### Desktop Browsers
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Mobile Browsers
- [ ] Chrome Mobile
- [ ] Safari iOS
- [ ] Firefox Mobile

### Testing Matrix
| Browser | Desktop | Tablet | Mobile |
|---------|---------|--------|--------|
| Chrome | ✓ | ✓ | ✓ |
| Firefox | ✓ | ✓ | ✓ |
| Safari | ✓ | ✓ | ✓ |
| Edge | ✓ | ✓ | ✓ |

---

## Performance Verification

### Load Times
- [ ] Categories page: < 2 seconds
- [ ] Category detail: < 2 seconds
- [ ] Levels page: < 2 seconds
- [ ] Level detail: < 2 seconds

### API Response Times
- [ ] GET /api/browse/categories: < 500ms
- [ ] GET /api/browse/category/{id}: < 500ms
- [ ] GET /api/browse/levels: < 500ms
- [ ] GET /api/browse/level/{id}: < 500ms

### Lighthouse Scores
- [ ] Performance: > 80
- [ ] Accessibility: > 80
- [ ] Best Practices: > 80
- [ ] SEO: > 80

---

## Security Checklist

### Code Security
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] Input validation on all endpoints
- [ ] CORS properly configured
- [ ] No sensitive data in logs

### Database
- [ ] Database backups working
- [ ] Proper user permissions
- [ ] Connection secured
- [ ] No default credentials

### API
- [ ] Public endpoints clearly documented
- [ ] Admin endpoints protected
- [ ] Rate limiting considered
- [ ] Error messages don't leak info

---

## Deployment Steps

### Step 1: Database
```bash
cd d:\3abdo\El Akeil
python seed_categories_levels.py
# Output should show:
# ✓ Created 5 categories
# ✓ Created 5 levels
```

**Verify:**
- [ ] Script runs without errors
- [ ] Shows all 5 categories created
- [ ] Shows all 5 levels created

### Step 2: Backend
```bash
cd src/backend
python app.py
# Should show: Running on http://127.0.0.1:5000/
```

**Verify:**
- [ ] App starts without errors
- [ ] Listening on correct port
- [ ] No database connection errors
- [ ] Routes properly registered

### Step 3: Frontend
Ensure all HTML files are in place:
```
src/Frontend/
├── categories.html
├── category.html
├── levels.html
├── level.html
```

**Verify:**
- [ ] Files exist
- [ ] Files are readable
- [ ] No syntax errors in HTML

### Step 4: Testing
1. Open http://localhost:5000/categories
2. Open http://localhost:5000/levels
3. Click category → see details
4. Click level → see details
5. Toggle language
6. Test mobile view

---

## Post-Deployment Verification

### 24-Hour Checks
- [ ] No error logs
- [ ] All pages loading
- [ ] API response times normal
- [ ] Language switching works
- [ ] Database not corrupted

### Weekly Checks
- [ ] Monitor user engagement
- [ ] Check error rates
- [ ] Verify performance metrics
- [ ] Check mobile responsiveness

### Monthly Checks
- [ ] Database backup verified
- [ ] Update dependencies
- [ ] Review analytics
- [ ] Plan improvements

---

## Rollback Plan

If issues occur:

### Quick Rollback
```bash
# Stop the application
# Restore database backup
# Restore previous HTML files
# Restart application
```

### Version Control
```bash
# If using git
git revert <commit-hash>
```

### Data Recovery
```bash
# Restore from backup
# Verify data integrity
# Check API responses
```

---

## Documentation

### User Documentation
- [ ] Users know about new browse pages
- [ ] Help text available
- [ ] FAQ prepared

### Developer Documentation
- [ ] API documentation complete
- [ ] Code comments present
- [ ] Architecture documented
- [ ] Deployment guide written

### Admin Documentation
- [ ] How to add categories
- [ ] How to add levels
- [ ] How to manage dishes
- [ ] Troubleshooting guide

---

## Monitoring

### Set Up Monitoring For
- [ ] API response times
- [ ] Error rates
- [ ] Database performance
- [ ] Page load times
- [ ] User engagement

### Tools
- [ ] Application logs
- [ ] Database logs
- [ ] Web server logs
- [ ] Error tracking (Sentry, etc.)

---

## Sign-Off

### Development Team
- **Developer Name:** ____________________
- **Date:** ____________________
- **Sign:** ____________________

### QA Team
- **QA Lead Name:** ____________________
- **Date:** ____________________
- **Sign:** ____________________

### Project Manager
- **PM Name:** ____________________
- **Date:** ____________________
- **Sign:** ____________________

### Deployment Authorized
- **Authorization:** ✅ YES / ❌ NO
- **Date:** ____________________
- **Notes:** ____________________

---

## Deployment Log

**Deployment Date:** ____________________  
**Deployed By:** ____________________  
**Start Time:** ____________________  
**End Time:** ____________________  
**Status:** ✅ SUCCESS / ❌ FAILED  

### Issues Encountered
```
(None expected if checklist completed)
```

### Resolution
```
N/A
```

### Post-Deployment Status
```
All systems operational
✓ Categories page working
✓ Levels page working
✓ API endpoints responding
✓ Language switching functional
✓ Mobile responsive
```

---

## Contact & Support

**Issues or Questions?**
- Check: `FOOD_BROWSING_SYSTEM_GUIDE.md`
- Check: `IMPLEMENTATION_COMPLETION_REPORT.md`
- Review: `src/backend/routes/browse.py`
- Review: Frontend HTML files

---

**Deployment Checklist Version:** 1.0  
**Last Updated:** January 21, 2026  
**Status:** Ready for Deployment ✅
