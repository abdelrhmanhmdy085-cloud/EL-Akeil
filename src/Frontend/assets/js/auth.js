function checkAuth(role = null) {
    const token = localStorage.getItem('token');
    if (!token) {
        // Allow public pages
        const path = location.pathname;
        if (!path.endsWith('index.html') && !path.endsWith('auth.html') && path !== '/') {
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
