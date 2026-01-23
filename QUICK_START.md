# El Akeil Frontend - Quick Start Guide

## 📂 Project Structure

```
Frontend/
├── index.html                    # Main landing page (UPDATED)
├── auth.html                     # Customer auth
├── customer.html                 # Customer dashboard
├── chef.html                     # Chef dashboard
├── chef_register.html            # Chef registration (NEW)
├── chef_login.html               # Chef login (NEW)
├── driver.html                   # Driver dashboard
├── driver_register.html          # Driver registration (NEW)
├── driver_login.html             # Driver login (NEW)
├── assets/
│   ├── css/
│   │   └── styles.css            # Main stylesheet (UPDATED)
│   ├── js/
│   │   ├── main.js               # Main functions (UPDATED)
│   │   ├── auth.js               # Authentication
│   │   ├── common.js             # Common utilities
│   │   └── i18n.js               # i18n system
│   ├── lang/
│   │   ├── ar.json               # Arabic translations (UPDATED)
│   │   ├── en.json               # English translations (UPDATED)
│   │   ├── fr.json               # French
│   │   ├── de.json               # German
│   │   ├── es.json               # Spanish
│   │   ├── it.json               # Italian
│   │   ├── tr.json               # Turkish
│   │   ├── ru.json               # Russian
│   │   └── zh.json               # Chinese
│   └── images/
│       └── splash_logo.png
└── README.md
```

---

## 🚀 Getting Started (5 Minutes)

### Step 1: Clone/Setup
```bash
cd src/Frontend
```

### Step 2: Serve Locally
```bash
# Python 3
python -m http.server 8000

# Or Node/npm
npx http-server

# Or any local web server
```

### Step 3: Open Browser
```
http://localhost:8000
```

### Step 4: Test Navigation
- ✅ Home page loads with splash screen
- ✅ 5 sections visible (hero, levels, categories, occasions, join)
- ✅ Click "انضم لشركتنا" opens modal
- ✅ Select Chef → opens chef_register.html
- ✅ Select Driver → opens driver_register.html

---

## 🎯 Key Pages Overview

### 1. **index.html** - Main Landing Page
- **Sections:**
  - Hero with search
  - Food levels browser (horizontal scroll)
  - Food categories grid
  - Occasions & holidays
  - Join Our Company CTA
- **Modal:** Role selection for join flow
- **Features:** 5 food filtering functions, smooth animations

### 2. **chef_register.html** - Chef Signup
- **Fields:** Name, Email, Password, Kitchen Name, Address, National ID
- **Validation:** Client-side form validation
- **API:** POST `/api/auth/chef-register`
- **Success:** Stores token, redirects to chef.html

### 3. **chef_login.html** - Chef Login
- **Fields:** Email, Password
- **API:** POST `/api/auth/chef-login`
- **Links:** Back to home, sign up link

### 4. **driver_register.html** - Driver Signup
- **Fields:** Name, Email, Password, Vehicle Type, License, National ID, Phone
- **Validation:** Client-side form validation
- **API:** POST `/api/auth/driver-register`
- **Success:** Stores token, redirects to driver.html

### 5. **driver_login.html** - Driver Login
- **Fields:** Email, Password
- **API:** POST `/api/auth/driver-login`
- **Links:** Back to home, sign up link

---

## 💻 Development Quick Reference

### Add New Food Level
```javascript
// 1. Add to HTML (index.html, SECTION 2)
<div class="level-card" onclick="filterByLevel('luxury')">
  <div class="level-card-header">👑</div>
  <h3>أكلات فاخرة</h3>
</div>

// 2. Add mock data (main.js)
mockFoods.levels.luxury = [
  { id: 50, name: 'وجبة فاخرة', ... }
];

// 3. Add translation (ar.json)
"level_luxury": "أكلات فاخرة"
```

### Add New Category
```javascript
// 1. Add to HTML (index.html, SECTION 3)
<div class="category-card" onclick="filterByCategory('pizza')">
  <div class="category-icon">🍕</div>
  <h3>بيتزا</h3>
</div>

// 2. Add mock data
mockFoods.categories.pizza = [ ... ];

// 3. Add translation
"cat_pizza": "بيتزا"
```

### Add New Occasion
```javascript
// 1. Add to HTML (index.html, SECTION 4)
<div class="occasion-card" onclick="filterByOccasion('weddings')">
  <div class="occasion-badge">حفلات أعراس</div>
</div>

// 2. Add mock data
mockFoods.occasions.push({ occasion: 'weddings', ... });

// 3. Add translation
"occasion_weddings": "حفلات أعراس"
```

---

## 🔌 API Integration

### Current: Mock Data
```javascript
filterByLevel('fast') // Uses mockFoods.levels.fast
```

### Production: Real API
```javascript
async function filterByLevel(level) {
    try {
        const result = await apiFetch(`/api/foods?level=${level}`);
        if (result.ok) {
            renderDishCards(result.data, 'levelFoodsContainer');
        }
    } catch (e) {
        console.error('Failed to load foods:', e);
    }
}
```

---

## 🌐 Language Support

### Current Languages
- 🇸🇦 Arabic (ar) - Default
- 🇺🇸 English (en)
- 🇫🇷 French (fr)
- 🇩🇪 German (de)
- 🇪🇸 Spanish (es)
- 🇮🇹 Italian (it)
- 🇹🇷 Turkish (tr)
- 🇷🇺 Russian (ru)
- 🇨🇳 Chinese (zh)

### Add Translation
```json
// In assets/lang/ar.json
{
  "new_key": "النص العربي"
}
```

### Use Translation
```html
<h1 data-i18n="new_key">Default Text</h1>
```

---

## 🎨 Customization

### Colors
Edit `/assets/css/styles.css`:
```css
:root {
    --primary: #5E2129;              /* Main maroon */
    --primary-hover: #4a1a20;        /* Hover darker */
    --bg-dark: #FFF5F5;              /* Light pink */
    --bg-card: #FFFFFF;              /* White */
}
```

### Fonts
```css
--font-ar: 'Cairo', sans-serif;
--font-en: 'Inter', sans-serif;
```

### Spacing
Search for `padding`, `margin`, `gap` in styles.css

---

## 🧪 Testing Checklist

### Homepage
- [ ] Splash screen shows (5 seconds)
- [ ] Navbar loads with logo and language selector
- [ ] Hero section displays headline and search box
- [ ] 4 level cards display and scroll horizontally
- [ ] Clicking level shows food cards below
- [ ] 5 category cards display
- [ ] Clicking category shows food cards
- [ ] Occasions section highlights in orange
- [ ] Join button opens modal
- [ ] Modal shows chef and driver options

### Chef Register
- [ ] Form displays all fields
- [ ] Email validation works
- [ ] Password mismatch shows error
- [ ] Submit button works
- [ ] Link to chef login works
- [ ] Form responsive on mobile

### Driver Register
- [ ] Form displays all fields
- [ ] Vehicle type dropdown works
- [ ] National ID validation (14 digits)
- [ ] Phone validation (10-11 digits)
- [ ] Submit button works
- [ ] Form responsive on mobile

### Mobile (480px)
- [ ] Menu is accessible
- [ ] Text readable
- [ ] Buttons easy to tap
- [ ] Forms fit screen
- [ ] Scroll works smoothly

---

## 🔗 Important Functions Reference

### Food Filtering
```javascript
filterByLevel(level)        // Args: 'fast'|'home'|'special'|'diet'
filterByCategory(category)  // Args: 'meat'|'chicken'|'seafood'|'sweets'|'drinks'
filterByOccasion(occasion)  // Args: 'ramadan'|'eid'|'events'|'gatherings'
renderDishCards(foods, id)  // Internal rendering function
```

### Modal Management
```javascript
openJoinModal()              // Opens role selection modal
closeJoinModal()             // Closes modal
selectRole(role)             // Args: 'chef'|'driver', redirects
```

### Authentication
```javascript
logout()                     // Clears token and redirects
checkAuth(role)              // Verify logged in and role
apiFetch(endpoint, method)   // Make API calls with auth
```

### Language
```javascript
loadLanguage(lang)           // Args: 'ar'|'en'|'fr'|etc
initLanguage()               // Initialize on page load
applyTranslations(lang)      // Update all data-i18n elements
```

---

## 📱 Responsive Breakpoints

```css
Desktop:     1200px+
Tablet:      768px - 1200px
Mobile:      480px - 768px
Small Mobile: < 480px
```

Each breakpoint has CSS media queries for optimal display.

---

## 🐛 Common Issues & Fixes

### Issue: Splash screen stuck
**Fix:** Check CSS animation in index.html, ensure it completes after 5 seconds

### Issue: Food cards not showing
**Fix:** Check console for errors, verify mockFoods structure

### Issue: Modal won't close
**Fix:** Check JavaScript in main.js, ensure closeJoinModal() called

### Issue: Language not changing
**Fix:** Check lang files exist in assets/lang/, verify JSON format

### Issue: Mobile layout broken
**Fix:** Check viewport meta tag, verify CSS media queries

---

## 📊 Performance Tips

1. **Lazy Loading**
   - Load images only when visible
   - Use Intersection Observer API

2. **Caching**
   - Cache language files
   - Cache user preferences in localStorage

3. **Minification**
   - Minify CSS before production
   - Minify JavaScript before production

4. **Compression**
   - Enable gzip on server
   - Compress images

---

## 🔐 Security Tips

1. **Never** store sensitive data in localStorage
2. **Always** validate on server
3. **Use HTTPS** in production
4. **Never** commit API keys/secrets
5. **Sanitize** user input before display

---

## 📚 Additional Resources

- **Bootstrap Classes** - Custom classes in styles.css
- **Cairo Font** - Google Fonts, no download needed
- **Leaflet Maps** - Already included for location (see index.html)
- **Socket.io** - Already included for real-time features

---

## 🚀 Deployment Steps

### 1. Test Locally
```bash
npm run test
# or manually test in browser
```

### 2. Build (if using build tool)
```bash
npm run build
```

### 3. Deploy to Server
```bash
# Copy all files to /var/www/html/elakeil
scp -r src/Frontend/* user@server:/var/www/html/elakeil/
```

### 4. Configure Web Server
```nginx
server {
    listen 80;
    server_name elakeil.example.com;
    
    root /var/www/html/elakeil;
    index index.html;
    
    # Fallback for SPA routing
    try_files $uri $uri/ /index.html;
}
```

### 5. Enable HTTPS
```bash
sudo certbot --nginx -d elakeil.example.com
```

---

## 📞 Support

For issues or questions:
1. Check console for errors
2. Review IMPLEMENTATION_GUIDE.md
3. Check API_SPECIFICATIONS.md
4. Test in different browsers
5. Check mobile responsiveness

---

## ✅ Deployment Checklist

- [ ] All files copied to server
- [ ] HTTPS enabled
- [ ] Domain configured
- [ ] Backend APIs working
- [ ] Language files loading
- [ ] Images loading
- [ ] Console no errors
- [ ] Mobile responsive
- [ ] Forms submitting
- [ ] Redirects working
- [ ] All links functional
- [ ] Performance acceptable

---

**Ready to launch! 🎉**

Last Updated: January 21, 2026
Version: 2.0
