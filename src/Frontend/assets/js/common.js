const API_BASE = '/api';
let socket = null;

async function apiFetch(endpoint, method = 'GET', body = null) {
    const headers = { 'Content-Type': 'application/json' };
    const token = localStorage.getItem('token');
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const opts = { method, headers };
    if (body) opts.body = JSON.stringify(body);

    try {
        const res = await fetch(API_BASE + endpoint, opts);
        const data = await res.json();
        return { ok: res.ok, status: res.status, data };
    } catch (e) {
        console.error(e);
        return { ok: false, error: 'Network Error' };
    }
}

function initSocket() {
    if (typeof io === 'undefined') return;
    socket = io();

    socket.on('connect', () => {
        const token = localStorage.getItem('token');
        if (token) {
            socket.emit('auth_join', { token });
        }
    });

    // Global Notification Handlers
    socket.on('order_update', (data) => {
        showNotification(`Order #${data.id} is now ${data.status}`);
        if (window.location.hash === '#orders') loadOrders(); // Refresh if on orders page
    });

    socket.on('new_order', (data) => {
        showNotification(`New Order #${data.id} received!`);
        // If on chef page, refresh
        if (typeof loadData === 'function') loadData();
    });

    socket.on('job_available', (data) => {
        showNotification(`New Job: Order #${data.id} from ${data.chef}`);
        if (typeof loadPool === 'function') loadPool();
    });
}

function showNotification(msg) {
    // Update Badge
    const badge = document.getElementById('notiBadge');
    const container = document.getElementById('notiContainer');
    if (badge && container) {
        container.classList.remove('hidden');
        badge.style.display = 'block';
        let count = parseInt(badge.innerText) || 0;
        badge.innerText = count + 1;

        // Add to dropdown
        const drop = document.getElementById('notiDropdown');
        const item = document.createElement('div');
        item.style.padding = '10px';
        item.style.borderBottom = '1px solid #333';
        item.style.fontSize = '0.9rem';
        item.innerText = msg;
        drop.prepend(item);
    }

    // Toast (optional, verify if user wants toast but req says "red badge... dropdown")
    // Let's add simple toast sound if possible? "Include sound alert (optional)"
    try {
        const audio = new Audio('assets/sounds/alert.mp3'); // path might not exist yet
        audio.play().catch(e => { });
    } catch (e) { }
}

function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}

// Init socket on load if token exists
window.addEventListener('load', () => {
    initSocket();

    // Toggle Dropdown
    const cont = document.getElementById('notiContainer');
    const drop = document.getElementById('notiDropdown');
    if (cont && drop) {
        const toggleNoti = (e) => {
            // reset badge
            document.getElementById('notiBadge').innerText = '0';
            document.getElementById('notiBadge').style.display = 'none';
            drop.style.display = drop.style.display === 'none' ? 'flex' : 'none';
            e.stopPropagation();
        };
        cont.onclick = toggleNoti;
        cont.onkeydown = (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleNoti(e);
            }
        };
        document.addEventListener('click', () => {
            drop.style.display = 'none';
        });
    }
});
