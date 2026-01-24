
// Note: LANG_KEY, DEFAULT_LANG, SUPPORTED_LANGS, and translations are defined in i18n.js
// Note: loadLanguage, applyTranslations, initLanguage, toggleLanguage are defined in i18n.js
// Note: API_BASE and apiFetch are defined in common.js

// Auth & Utils
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

function checkAuth(role = null) {
    const token = localStorage.getItem('token');
    if (!token) {
        if (!location.pathname.endsWith('index.html') && !location.pathname.endsWith('auth.html')) {
            window.location.href = 'auth.html';
        }
        return;
    }
    if (role) {
        const user = JSON.parse(localStorage.getItem('user') || '{}');
        if (user.role !== role) {
            alert('Access Denied');
            window.location.href = 'index.html';
        }
    }
}

// ============================================
// FOOD BROWSING & FILTERING FUNCTIONS
// ============================================

// Mock food data (replace with API call in production)
const mockFoods = {
    levels: {
        fast: [
            { id: 1, name: 'برجر سريع', category: 'meat', level: 'fast', chef: 'أم أحمد', price: 50, rating: 4.5, emoji: '🍔' },
            { id: 2, name: 'شاورما دجاج', category: 'chicken', level: 'fast', chef: 'العم محمود', price: 45, rating: 4.3, emoji: '🌯' },
            { id: 3, name: 'بيتزا سريعة', category: 'meat', level: 'fast', chef: 'فاطمة', price: 55, rating: 4.6, emoji: '🍕' }
        ],
        home: [
            { id: 4, name: 'كشري بيتي', category: 'meat', level: 'home', chef: 'أم علي', price: 35, rating: 4.8, emoji: '🍲' },
            { id: 5, name: 'فتة الدجاج', category: 'chicken', level: 'home', chef: 'الحاجة فاطمة', price: 60, rating: 4.9, emoji: '🍗' },
            { id: 6, name: 'فسيخ وفتة', category: 'seafood', level: 'home', chef: 'بيت الفسيخ', price: 75, rating: 4.7, emoji: '🐟' }
        ],
        special: [
            { id: 7, name: 'لحم ستيك فاخر', category: 'meat', level: 'special', chef: 'الشيف أحمد', price: 200, rating: 4.9, emoji: '🥩' },
            { id: 8, name: 'دجاج بالعسل والجوز', category: 'chicken', level: 'special', chef: 'مطبخ السلام', price: 150, rating: 4.8, emoji: '🍯' },
            { id: 9, name: 'سمك فيليه مشوي', category: 'seafood', level: 'special', chef: 'أسطى محمود', price: 180, rating: 4.9, emoji: '🐠' }
        ],
        diet: [
            { id: 10, name: 'صدور دجاج مشوية', category: 'chicken', level: 'diet', chef: 'مطبخ صحي', price: 55, rating: 4.6, emoji: '🍗' },
            { id: 11, name: 'سلطة خضراء فاخرة', category: 'drinks', level: 'diet', chef: 'مطبخ النبات', price: 40, rating: 4.5, emoji: '🥗' },
            { id: 12, name: 'أسماك مشوية بالعشبة', category: 'seafood', level: 'diet', chef: 'صحي وطيب', price: 120, rating: 4.7, emoji: '🐟' }
        ]
    },
    categories: {
        meat: [
            { id: 1, name: 'برجر سريع', category: 'meat', level: 'fast', chef: 'أم أحمد', price: 50, rating: 4.5, emoji: '🍔' },
            { id: 3, name: 'بيتزا سريعة', category: 'meat', level: 'fast', chef: 'فاطمة', price: 55, rating: 4.6, emoji: '🍕' },
            { id: 7, name: 'لحم ستيك فاخر', category: 'meat', level: 'special', chef: 'الشيف أحمد', price: 200, rating: 4.9, emoji: '🥩' }
        ],
        chicken: [
            { id: 2, name: 'شاورما دجاج', category: 'chicken', level: 'fast', chef: 'العم محمود', price: 45, rating: 4.3, emoji: '🌯' },
            { id: 5, name: 'فتة الدجاج', category: 'chicken', level: 'home', chef: 'الحاجة فاطمة', price: 60, rating: 4.9, emoji: '🍗' },
            { id: 8, name: 'دجاج بالعسل والجوز', category: 'chicken', level: 'special', chef: 'مطبخ السلام', price: 150, rating: 4.8, emoji: '🍯' }
        ],
        seafood: [
            { id: 6, name: 'فسيخ وفتة', category: 'seafood', level: 'home', chef: 'بيت الفسيخ', price: 75, rating: 4.7, emoji: '🐟' },
            { id: 9, name: 'سمك فيليه مشوي', category: 'seafood', level: 'special', chef: 'أسطى محمود', price: 180, rating: 4.9, emoji: '🐠' },
            { id: 12, name: 'أسماك مشوية بالعشبة', category: 'seafood', level: 'diet', chef: 'صحي وطيب', price: 120, rating: 4.7, emoji: '🐟' }
        ],
        sweets: [
            { id: 13, name: 'كنافة نابلسية', category: 'sweets', level: 'special', chef: 'أم محمود', price: 80, rating: 4.8, emoji: '🍰' },
            { id: 14, name: 'حلويات تمر', category: 'sweets', level: 'home', chef: 'الحاجة عائشة', price: 50, rating: 4.7, emoji: '🍪' }
        ],
        drinks: [
            { id: 15, name: 'عصير برتقال طازج', category: 'drinks', level: 'diet', chef: 'مطبخ العصائر', price: 30, rating: 4.6, emoji: '🥤' },
            { id: 16, name: 'قمح بلبن', category: 'drinks', level: 'home', chef: 'أم فاطمة', price: 25, rating: 4.5, emoji: '🥛' }
        ]
    },
    occasions: [
        { id: 20, name: 'مائدة رمضانية فاخرة', occasion: 'ramadan', level: 'special', chef: 'الشيف أحمد', price: 500, rating: 4.9, emoji: '🍲' },
        { id: 21, name: 'أكلات عيد مميزة', occasion: 'eid', level: 'special', chef: 'مطبخ العيد', price: 450, rating: 4.8, emoji: '🍗' },
        { id: 22, name: 'وجبة عزومة كاملة', occasion: 'gatherings', level: 'special', chef: 'فاطمة وأخواتها', price: 600, rating: 4.9, emoji: '🍽️' },
        { id: 23, name: 'طبخة مناسبات', occasion: 'events', level: 'special', chef: 'مطبخ المناسبات', price: 550, rating: 4.8, emoji: '🎉' }
    ]
};

function renderDishCards(dishes, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    if (!dishes || dishes.length === 0) {
        container.innerHTML = '<p style="text-align: center; color: var(--text-secondary); grid-column: 1/-1;">لا توجد أطعمة متاحة</p>';
        return;
    }

    container.innerHTML = dishes.map(food => `
        <div class="dish-card">
            <div class="dish-image">${food.emoji}</div>
            <div class="dish-info">
                <div class="dish-name">${food.name}</div>
                <div class="dish-chef">👨‍🍳 ${food.chef}</div>
                <div class="dish-meta">
                    <span class="dish-price">${food.price} ج.م</span>
                    <span class="dish-rating">⭐ ${food.rating}</span>
                </div>
            </div>
        </div>
    `).join('');
}

function filterByLevel(level) {
    const foods = mockFoods.levels[level] || [];
    renderDishCards(foods, 'levelFoodsContainer');
    // Smooth scroll to results
    document.getElementById('levelFoodsContainer').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function filterByCategory(category) {
    const foods = mockFoods.categories[category] || [];
    renderDishCards(foods, 'categoryFoodsContainer');
    // Smooth scroll to results
    document.getElementById('categoryFoodsContainer').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function filterByOccasion(occasion) {
    const foods = mockFoods.occasions.filter(f => f.occasion === occasion);
    renderDishCards(foods, 'occasionFoodsContainer');
    // Smooth scroll to results
    document.getElementById('occasionFoodsContainer').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// ============================================
// JOIN COMPANY MODAL FUNCTIONS
// ============================================

function openJoinModal() {
    const modal = document.getElementById('joinCompanyModal');
    if (modal) modal.classList.remove('hidden');
}

function closeJoinModal() {
    const modal = document.getElementById('joinCompanyModal');
    if (modal) modal.classList.add('hidden');
}

function selectRole(role) {
    closeJoinModal();
    if (role === 'chef') {
        window.location.href = 'chef_register.html';
    } else if (role === 'driver') {
        window.location.href = 'driver_register.html';
    }
}

// Close modal when clicking outside
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('joinCompanyModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeJoinModal();
            }
        });
    }
    initLanguage();
});

// Run init
document.addEventListener('DOMContentLoaded', () => {
    initLanguage();
});
