/**
 * Push Notifications Manager
 * Handles Firebase Cloud Messaging and Web Push notifications
 */

class NotificationManager {
    constructor() {
        this.socket = null;
        this.serviceWorkerRegistration = null;
        this.token = null;
        this.userRole = null;
        this.userId = null;
        this.notificationQueue = [];
        this.isServiceWorkerReady = false;
    }

    /**
     * Initialize notification system
     * @param {Object} options - Configuration options
     */
    async init(options = {}) {
        this.socket = options.socket || window.io();
        this.token = options.token;
        this.userRole = options.userRole || 'customer';
        this.userId = options.userId;

        // Register service worker for web push
        if ('serviceWorker' in navigator) {
            try {
                this.serviceWorkerRegistration = await navigator.serviceWorker.register('js/service-worker.js');
                this.isServiceWorkerReady = true;
                console.log('Service worker registered');
            } catch (error) {
                console.error('Service worker registration failed:', error);
            }
        }

        // Request notification permission
        if ('Notification' in window) {
            if (Notification.permission === 'default') {
                this.requestNotificationPermission();
            }
        }

        // Initialize FCM if available
        if (typeof firebase !== 'undefined' && firebase.messaging) {
            this.initializeFirebaseMessaging();
        }

        // Setup socket listeners
        this.setupSocketListeners();

        // Load existing notifications
        this.loadNotifications();
    }

    /**
     * Request browser notification permission
     */
    async requestNotificationPermission() {
        if (!('Notification' in window)) {
            console.log('Notifications not supported');
            return;
        }

        try {
            const permission = await Notification.requestPermission();
            if (permission === 'granted') {
                console.log('Notification permission granted');
                this.registerDeviceToken();
            }
        } catch (error) {
            console.error('Notification permission error:', error);
        }
    }

    /**
     * Initialize Firebase Cloud Messaging
     */
    initializeFirebaseMessaging() {
        try {
            const messaging = firebase.messaging();

            messaging.onMessage((payload) => {
                console.log('Foreground message received:', payload);
                this.handleForegroundMessage(payload);
            });

            // Get FCM token and register
            messaging.getToken()
                .then((token) => {
                    if (token) {
                        this.registerDeviceToken(token, 'web');
                    }
                })
                .catch((error) => {
                    console.error('Error getting FCM token:', error);
                });

            // Listen for token refresh
            messaging.onTokenRefresh(() => {
                messaging.getToken()
                    .then((token) => {
                        this.registerDeviceToken(token, 'web');
                    });
            });

        } catch (error) {
            console.error('Firebase messaging init error:', error);
        }
    }

    /**
     * Register device token with backend
     * @param {string} deviceToken - The device token (FCM or push token)
     * @param {string} platform - Platform type (android, ios, web)
     */
    async registerDeviceToken(deviceToken = null, platform = 'web') {
        try {
            if (!deviceToken) {
                // Try to get from service worker
                if (this.serviceWorkerRegistration) {
                    const subscription = await this.serviceWorkerRegistration.pushManager.getSubscription();
                    if (subscription) {
                        deviceToken = JSON.stringify(subscription.toJSON());
                    }
                }
            }

            if (!deviceToken) {
                console.warn('No device token available');
                return;
            }

            const response = await fetch('/api/notifications/device-token/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({
                    device_token: deviceToken,
                    platform: platform
                })
            });

            if (response.ok) {
                console.log('Device token registered');
                this.showNotification('Notifications Enabled', '📱 You will now receive push notifications', 'info');
            }
        } catch (error) {
            console.error('Error registering device token:', error);
        }
    }

    /**
     * Set up Socket.IO listeners
     */
    setupSocketListeners() {
        // Listen for real-time notifications
        this.socket.on('notification_received', (data) => {
            this.handleNotification(data);
        });

        this.socket.on('order_status_update', (data) => {
            this.handleOrderStatusUpdate(data);
        });

        this.socket.on('driver_nearby', (data) => {
            this.handleDriverNearby(data);
        });

        this.socket.on('notification_error', (data) => {
            console.error('Notification error:', data);
        });
    }

    /**
     * Handle foreground FCM message
     * @param {Object} payload - Firebase message payload
     */
    handleForegroundMessage(payload) {
        const notification = payload.notification;
        const data = payload.data;

        this.showNotification(
            notification.title || 'Notification',
            notification.body || 'You have a new notification',
            'info',
            data
        );

        // Add to notification center
        this.addToNotificationCenter({
            title: notification.title,
            message: notification.body,
            type: data.type || 'general',
            data: data,
            timestamp: new Date()
        });
    }

    /**
     * Handle incoming notification
     * @param {Object} data - Notification data
     */
    handleNotification(data) {
        const icon = this.getNotificationIcon(data.type);
        const title = `${icon} ${data.title || 'Notification'}`;
        
        this.showNotification(title, data.message, 'info', data);
        
        // Show toast
        this.showToast(title, data.message);

        // Add to center
        this.addToNotificationCenter({
            title: data.title,
            message: data.message,
            type: data.notification_type || data.type,
            order_id: data.order_id,
            data: data,
            timestamp: new Date()
        });
    }

    /**
     * Handle order status update notification
     * @param {Object} data - Update data
     */
    handleOrderStatusUpdate(data) {
        let message = '';
        let icon = '📦';

        switch (data.status) {
            case 'pending':
                message = 'Your order has been received';
                icon = '📋';
                break;
            case 'cooking':
                message = 'Your food is being prepared';
                icon = '👨‍🍳';
                break;
            case 'ready':
                message = 'Your food is ready for pickup';
                icon = '✅';
                break;
            case 'delivering':
                message = `${data.driver_name || 'Driver'} is on the way`;
                icon = '🚗';
                break;
            case 'delivered':
                message = 'Your order has been delivered!';
                icon = '🎉';
                break;
            default:
                message = 'Order status updated';
        }

        this.showNotification(`${icon} Order Update`, message, 'info', data);
        this.showToast(`${icon} Order #${data.order_id}`, message);
    }

    /**
     * Handle driver nearby notification
     * @param {Object} data - Driver location data
     */
    handleDriverNearby(data) {
        const message = `${data.driver_name || 'Driver'} is ${data.distance_km.toFixed(1)} km away`;
        this.showNotification('🚗 Driver Nearby', message, 'info', data);
        this.showToast('📍 Driver Location', message);
    }

    /**
     * Get notification icon based on type
     * @param {string} type - Notification type
     */
    getNotificationIcon(type) {
        const icons = {
            'order_accepted': '✅',
            'order_cooking': '👨‍🍳',
            'order_ready': '📦',
            'driver_started': '🚗',
            'driver_nearby': '📍',
            'order_delivered': '🎉',
            'order_cancelled': '❌',
            'payment_received': '💰',
            'review_received': '⭐',
            'system': 'ℹ️'
        };
        return icons[type] || '🔔';
    }

    /**
     * Show desktop/browser notification
     * @param {string} title - Notification title
     * @param {string} message - Notification message
     * @param {string} type - Notification type (info, success, warning, error)
     * @param {Object} data - Additional data
     */
    showNotification(title, message, type = 'info', data = {}) {
        if (!('Notification' in window)) return;

        if (Notification.permission === 'granted') {
            const notification = new Notification(title, {
                body: message,
                icon: this.getNotificationIconUrl(type),
                tag: `notif-${Date.now()}`,
                requireInteraction: type === 'warning' || type === 'error',
                data: data
            });

            // Handle notification click
            notification.onclick = () => {
                window.focus();
                if (data.order_id) {
                    window.location.href = `/order/${data.order_id}`;
                }
                notification.close();
            };

            // Auto-close after 4 seconds for non-critical
            if (type === 'info' || type === 'success') {
                setTimeout(() => notification.close(), 4000);
            }
        }
    }

    /**
     * Get notification icon URL
     * @param {string} type - Notification type
     */
    getNotificationIconUrl(type) {
        const icons = {
            'success': 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="green"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>',
            'error': 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="red"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12 19 6.41z"/></svg>',
            'warning': 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="orange"><path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/></svg>',
            'info': 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="blue"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>'
        };
        return icons[type] || icons['info'];
    }

    /**
     * Show toast notification
     * @param {string} title - Toast title
     * @param {string} message - Toast message
     */
    showToast(title, message) {
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.innerHTML = `
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">×</button>
        `;
        
        const container = document.getElementById('toast-container') || this.createToastContainer();
        container.appendChild(toast);

        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 10);

        // Auto-remove after 4 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    /**
     * Create toast container if it doesn't exist
     */
    createToastContainer() {
        const container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'toast-container';
        document.body.appendChild(container);
        return container;
    }

    /**
     * Add notification to notification center
     * @param {Object} notif - Notification object
     */
    addToNotificationCenter(notif) {
        this.notificationQueue.push(notif);

        // Keep only last 50 notifications
        if (this.notificationQueue.length > 50) {
            this.notificationQueue.shift();
        }

        // Update UI if notification center exists
        this.updateNotificationCenterUI();
    }

    /**
     * Load notifications from backend
     */
    async loadNotifications() {
        try {
            const response = await fetch('/api/notifications/list?unread_only=true&limit=20', {
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (response.ok) {
                const data = await response.json();
                data.notifications.forEach(notif => {
                    this.addToNotificationCenter(notif);
                });
                this.updateNotificationBadge(data.count);
            }
        } catch (error) {
            console.error('Error loading notifications:', error);
        }
    }

    /**
     * Update notification center UI
     */
    updateNotificationCenterUI() {
        const centerPanel = document.querySelector('.notification-center-panel');
        if (!centerPanel) return;

        const list = centerPanel.querySelector('.notification-list');
        if (!list) return;

        list.innerHTML = this.notificationQueue.map((notif, index) => `
            <div class="notification-item" data-index="${index}">
                <div class="notif-icon">${this.getNotificationIcon(notif.type)}</div>
                <div class="notif-content">
                    <div class="notif-title">${notif.title || 'Notification'}</div>
                    <div class="notif-message">${notif.message || ''}</div>
                    <div class="notif-time">${new Date(notif.timestamp).toLocaleTimeString()}</div>
                </div>
                <button class="btn-close-notif" onclick="notificationManager.removeNotification(${index})">×</button>
            </div>
        `).join('');
    }

    /**
     * Update notification badge count
     * @param {number} count - Number of unread notifications
     */
    updateNotificationBadge(count) {
        const badge = document.querySelector('.notification-badge');
        if (badge) {
            badge.textContent = count > 99 ? '99+' : count;
            badge.style.display = count > 0 ? 'inline-block' : 'none';
        }
    }

    /**
     * Remove notification from queue
     * @param {number} index - Notification index
     */
    removeNotification(index) {
        this.notificationQueue.splice(index, 1);
        this.updateNotificationCenterUI();
    }

    /**
     * Mark all notifications as read
     */
    async markAllAsRead() {
        try {
            // Backend call to mark all as read
            await fetch('/api/notifications/mark-all-read', {
                method: 'PUT',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            this.notificationQueue.forEach(notif => notif.is_read = true);
            this.updateNotificationBadge(0);
            this.updateNotificationCenterUI();
        } catch (error) {
            console.error('Error marking notifications as read:', error);
        }
    }

    /**
     * Get notification count
     */
    getNotificationCount() {
        return this.notificationQueue.length;
    }

    /**
     * Clear all notifications
     */
    clearAllNotifications() {
        if (confirm('Clear all notifications?')) {
            this.notificationQueue = [];
            this.updateNotificationCenterUI();
            this.updateNotificationBadge(0);
        }
    }
}

// Global instance
const notificationManager = new NotificationManager();

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    notificationManager.init({
        userRole: document.body.dataset.userRole || 'customer',
        userId: document.body.dataset.userId,
        token: localStorage.getItem('auth_token')
    });
});

// Handle app visibility - reload notifications when returning to app
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        notificationManager.loadNotifications();
    }
});
