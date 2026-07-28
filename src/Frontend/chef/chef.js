// Chef Dashboard JavaScript

let chefId = null;
let dashboardData = {};
let allDishes = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    chefId = localStorage.getItem('chef_id');
    
    if (!chefId) {
        window.location.href = '/chef_login.html';
        return;
    }

    initializeDashboard();
    setupEventListeners();
    loadDashboardData();
});

// Initialize Dashboard
function initializeDashboard() {
    // Load section navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            switchSection(item.dataset.section);
        });
    });

    // Load initial data
    loadCategories();
    loadLevels();
}

// Setup Event Listeners
function setupEventListeners() {
    // Add dish form
    document.getElementById('add-dish-form').addEventListener('submit', handleAddDish);

    // Settings form
    document.getElementById('settings-form').addEventListener('submit', handleSaveSettings);
}

// Switch Sections
function switchSection(sectionName) {
    // Hide all sections
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

    // Show active section
    document.getElementById(`${sectionName}-section`).classList.add('active');
    event.target.classList.add('active');

    // Update title
    const titles = {
        'overview': 'نظرة عامة',
        'dishes': 'أطباقي',
        'orders': 'الطلبات',
        'reviews': 'التقييمات',
        'analytics': 'الإحصائيات',
        'settings': 'الإعدادات'
    };
    document.getElementById('section-title').textContent = titles[sectionName] || 'لوحة التحكم';

    // Load section-specific data
    if (sectionName === 'dishes') loadDishes();
    if (sectionName === 'orders') loadOrders();
    if (sectionName === 'reviews') loadReviews();
    if (sectionName === 'analytics') loadAnalytics();
}

// Load Dashboard Data
async function loadDashboardData() {
    try {
        const response = await fetch('/api/chef/dashboard', {
            headers: { 'Chef-ID': chefId }
        });

        if (!response.ok) throw new Error('Failed to load dashboard data');

        const data = await response.json();
        dashboardData = data.dashboard;

        updateDashboardUI();
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showNotification('خطأ في تحميل البيانات', 'error');
    }
}

// Update Dashboard UI
function updateDashboardUI() {
    const { statistics, revenue, recent_orders } = dashboardData;

    // Update stats
    document.getElementById('total-dishes').textContent = statistics.total_dishes;
    document.getElementById('weekly-orders').textContent = statistics.total_orders;
    document.getElementById('avg-rating').textContent = statistics.average_rating;

    // Calculate today's revenue
    const today = new Date().toISOString().split('T')[0];
    const todayRevenue = revenue[today] || 0;
    document.getElementById('daily-revenue').textContent = `${todayRevenue.toFixed(2)} ر.س`;

    // Update chef info
    document.getElementById('chef-name').textContent = dashboardData.chef_info.name;
}

// Load Categories
async function loadCategories() {
    try {
        const response = await fetch('/api/browse/categories');
        const data = await response.json();

        const select = document.getElementById('dish-category');
        select.innerHTML = '<option value="">اختر الفئة</option>';

        if (data.status === 'success') {
            data.categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat.id;
                option.textContent = cat.name;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load Levels
async function loadLevels() {
    try {
        const response = await fetch('/api/browse/levels');
        const data = await response.json();

        const select = document.getElementById('dish-level');
        select.innerHTML = '<option value="">اختر المستوى</option>';

        if (data.status === 'success') {
            data.levels.forEach(level => {
                const option = document.createElement('option');
                option.value = level.id;
                option.textContent = level.name;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading levels:', error);
    }
}

// Load Dishes
async function loadDishes() {
    try {
        const response = await fetch(`/api/chef/dishes?chef_id=${chefId}`);
        const data = await response.json();

        if (data.status === 'success') {
            allDishes = data.dishes;
            renderDishes();
        }
    } catch (error) {
        console.error('Error loading dishes:', error);
        showNotification('خطأ في تحميل الأطباق', 'error');
    }
}

// Render Dishes
function renderDishes() {
    const container = document.getElementById('dishes-container');
    container.innerHTML = '';

    if (allDishes.length === 0) {
        container.innerHTML = '<div class="empty-state">لا توجد أطباق حالياً</div>';
        return;
    }

    allDishes.forEach(dish => {
        const dishCard = createDishCard(dish);
        container.appendChild(dishCard);
    });
}

// Create Dish Card
function createDishCard(dish) {
    const card = document.createElement('div');
    card.className = 'dish-card';
    card.innerHTML = `
        <div class="dish-image">
            ${dish.image_path ? `<img src="${dish.image_path}" alt="${dish.name}">` : '🍽️'}
        </div>
        <div class="dish-info">
            <div class="dish-name">${dish.name}</div>
            <div class="dish-description">${dish.description || 'بدون وصف'}</div>
            <div class="dish-price" style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <span>${dish.price.toFixed(2)} ر.س</span>
                <span class="status-badge ${dish.available ? 'status-completed' : 'status-pending'}">
                    ${dish.available ? 'متوفر' : 'غير متوفر'}
                </span>
            </div>
            <div class="dish-actions">
                <button class="dish-edit" onclick="editDish(${dish.id})">✏️ تعديل</button>
                <button class="dish-toggle" onclick="toggleAvailability(${dish.id})" title="${dish.available ? 'تعطيل توفر الطبق' : 'تفعيل توفر الطبق'}" aria-label="${dish.available ? 'تعطيل توفر الطبق' : 'تفعيل توفر الطبق'}">
                    ${dish.available ? '⏸️ تعطيل' : '▶️ تفعيل'}
                </button>
                <button class="dish-delete" onclick="deleteDish(${dish.id})">🗑️ حذف</button>
            </div>
        </div>
    `;
    return card;
}

// Add Dish
async function handleAddDish(e) {
    e.preventDefault();

    const formData = new FormData();
    formData.append('chef_id', chefId);
    formData.append('name', document.getElementById('dish-name').value);
    formData.append('description', document.getElementById('dish-description').value);
    formData.append('price', document.getElementById('dish-price').value);
    formData.append('category_id', document.getElementById('dish-category').value);
    formData.append('level_id', document.getElementById('dish-level').value);

    if (document.getElementById('dish-image').files.length > 0) {
        formData.append('image', document.getElementById('dish-image').files[0]);
    }

    try {
        const response = await fetch('/api/chef/dishes', {
            method: 'POST',
            headers: { 'Chef-ID': chefId },
            body: formData
        });

        const data = await response.json();

        if (data.status === 'success') {
            showNotification('تم إضافة الطبق بنجاح', 'success');
            closeAddDishModal();
            document.getElementById('add-dish-form').reset();
            loadDishes();
        } else {
            showNotification(data.error || 'حدث خطأ', 'error');
        }
    } catch (error) {
        console.error('Error adding dish:', error);
        showNotification('خطأ في إضافة الطبق', 'error');
    }
}

// Delete Dish
async function deleteDish(dishId) {
    if (!confirm('هل تريد حذف هذا الطبق؟')) return;

    try {
        const response = await fetch(`/api/chef/dishes/${dishId}`, {
            method: 'DELETE',
            headers: { 'Chef-ID': chefId }
        });

        const data = await response.json();

        if (data.status === 'success') {
            showNotification('تم حذف الطبق بنجاح', 'success');
            loadDishes();
        } else {
            showNotification(data.error || 'حدث خطأ', 'error');
        }
    } catch (error) {
        console.error('Error deleting dish:', error);
        showNotification('خطأ في حذف الطبق', 'error');
    }
}

// Toggle Availability
async function toggleAvailability(dishId) {
    try {
        const response = await fetch(`/api/chef/dishes/${dishId}/toggle-availability`, {
            method: 'POST',
            headers: { 'Chef-ID': chefId }
        });

        const data = await response.json();

        if (data.status === 'success') {
            showNotification('تم تحديث حالة الطبق', 'success');
            loadDishes();
        } else {
            showNotification(data.error || 'حدث خطأ', 'error');
        }
    } catch (error) {
        console.error('Error toggling availability:', error);
        showNotification('خطأ في تحديث الحالة', 'error');
    }
}

// Load Orders
async function loadOrders() {
    try {
        const response = await fetch(`/api/browse/orders?chef_id=${chefId}`);
        const data = await response.json();

        if (data.status === 'success') {
            renderOrders(data.orders);
        }
    } catch (error) {
        console.error('Error loading orders:', error);
    }
}

// Render Orders
function renderOrders(orders) {
    const tbody = document.getElementById('orders-tbody');
    tbody.innerHTML = '';

    if (orders.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">لا توجد طلبات</td></tr>';
        return;
    }

    orders.forEach(order => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>#${order.id}</td>
            <td>${order.customer_name}</td>
            <td>${order.total.toFixed(2)} ر.س</td>
            <td><span class="status-badge status-${order.status.toLowerCase()}">${order.status}</span></td>
            <td>${new Date(order.created_at).toLocaleDateString('ar-SA')}</td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="viewOrder(${order.id})">عرض</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Load Reviews
async function loadReviews() {
    try {
        const response = await fetch(`/api/chef/reviews?chef_id=${chefId}`);
        const data = await response.json();

        if (data.status === 'success') {
            renderReviews(data.reviews);
        }
    } catch (error) {
        console.error('Error loading reviews:', error);
    }
}

// Render Reviews
function renderReviews(reviews) {
    const container = document.getElementById('reviews-container');
    container.innerHTML = '';

    if (reviews.length === 0) {
        container.innerHTML = '<div class="empty-state">لا توجد تقييمات حالياً</div>';
        return;
    }

    reviews.forEach(review => {
        const reviewCard = document.createElement('div');
        reviewCard.className = 'review-card';
        reviewCard.innerHTML = `
            <div class="review-header">
                <div class="review-author">${review.customer_name}</div>
                <div class="review-rating">${'⭐'.repeat(review.rating)}</div>
            </div>
            <div class="review-text">${review.comment}</div>
            ${review.chef_response ? `
                <div class="review-response">
                    <strong>ردك:</strong> ${review.chef_response}
                </div>
            ` : `
                <button class="btn btn-sm btn-primary" onclick="respondToReview(${review.id})">
                    الرد على التقييم
                </button>
            `}
        `;
        container.appendChild(reviewCard);
    });
}

// Load Analytics
async function loadAnalytics() {
    try {
        const response = await fetch(`/api/chef/stats/top-dishes?chef_id=${chefId}&limit=10`);
        const data = await response.json();

        if (data.status === 'success') {
            renderTopDishes(data.dishes);
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
}

// Render Top Dishes
function renderTopDishes(dishes) {
    const container = document.getElementById('top-dishes-list');
    container.innerHTML = '';

    if (dishes.length === 0) {
        container.innerHTML = '<div class="empty-state">لا توجد بيانات</div>';
        return;
    }

    const list = document.createElement('ol');
    dishes.forEach((dish, index) => {
        const item = document.createElement('li');
        item.innerHTML = `
            <strong>${dish.name}</strong>
            <br/>
            <small>الطلبات: ${dish.orders} | السعر: ${dish.price.toFixed(2)} ر.س</small>
        `;
        list.appendChild(item);
    });

    container.appendChild(list);
}

// Save Settings
async function handleSaveSettings(e) {
    e.preventDefault();

    const phone = document.getElementById('chef-phone').value;
    const bio = document.getElementById('chef-bio').value;

    try {
        const response = await fetch('/api/chef/profile', {
            method: 'PUT',
            headers: {
                'Chef-ID': chefId,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ phone, bio })
        });

        const data = await response.json();

        if (data.status === 'success') {
            showNotification('تم حفظ التغييرات بنجاح', 'success');
        } else {
            showNotification(data.error || 'حدث خطأ', 'error');
        }
    } catch (error) {
        console.error('Error saving settings:', error);
        showNotification('خطأ في حفظ التغييرات', 'error');
    }
}

// Modal Functions
function openAddDishModal() {
    document.getElementById('add-dish-modal').classList.add('active');
}

function closeAddDishModal() {
    document.getElementById('add-dish-modal').classList.remove('active');
}

// Notification Helper
function showNotification(message, type = 'info') {
    // This can be enhanced with a proper toast library
    alert(message);
}

// Logout
function logout() {
    if (confirm('هل تريد تسجيل الخروج؟')) {
        localStorage.removeItem('chef_id');
        localStorage.removeItem('chef_token');
        window.location.href = '/chef_login.html';
    }
}
