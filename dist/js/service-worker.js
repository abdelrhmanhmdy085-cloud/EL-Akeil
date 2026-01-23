/**
 * Service Worker for Push Notifications
 * Handles background notifications and offline queue
 */

const CACHE_NAME = 'el-akeil-v1';
const NOTIFICATION_QUEUE_DB = 'notification-queue';

// Install service worker
self.addEventListener('install', (event) => {
    console.log('Service Worker installed');
    self.skipWaiting();
});

// Activate service worker
self.addEventListener('activate', (event) => {
    console.log('Service Worker activated');
    event.waitUntil(self.clients.claim());
});

// Handle push notifications
self.addEventListener('push', (event) => {
    console.log('Push notification received:', event);

    if (!event.data) {
        console.log('No data in push notification');
        return;
    }

    let notificationData = {};
    try {
        notificationData = event.data.json();
    } catch (e) {
        notificationData = {
            title: 'El Akeil Notification',
            body: event.data.text()
        };
    }

    const title = notificationData.title || 'El Akeil';
    const options = {
        body: notificationData.body || 'You have a new notification',
        icon: '/assets/images/logo-icon.png',
        badge: '/assets/images/badge-icon.png',
        tag: `notif-${Date.now()}`,
        requireInteraction: notificationData.requireInteraction || false,
        data: notificationData.data || {}
    };

    // Add vibration pattern
    if (notificationData.requireInteraction) {
        options.vibrate = [200, 100, 200];
    }

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

// Handle notification click
self.addEventListener('notificationclick', (event) => {
    console.log('Notification clicked:', event);

    event.notification.close();

    const data = event.notification.data;
    const urlToOpen = data.url || '/';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then((clientList) => {
                // Check if app is already open
                for (let i = 0; i < clientList.length; i++) {
                    const client = clientList[i];
                    if (client.url === urlToOpen && 'focus' in client) {
                        return client.focus();
                    }
                }
                // Open new window if not already open
                if (clients.openWindow) {
                    return clients.openWindow(urlToOpen);
                }
            })
    );
});

// Handle notification close
self.addEventListener('notificationclose', (event) => {
    console.log('Notification dismissed');
    // Could track dismissed notifications here
});

// Fetch event handler for offline support
self.addEventListener('fetch', (event) => {
    // Skip non-GET requests
    if (event.request.method !== 'GET') {
        return;
    }

    // Handle API requests
    if (event.request.url.includes('/api/')) {
        event.respondWith(
            fetch(event.request)
                .then((response) => {
                    if (response.status === 200) {
                        // Cache successful responses
                        const responseClone = response.clone();
                        caches.open(CACHE_NAME)
                            .then((cache) => cache.put(event.request, responseClone));
                    }
                    return response;
                })
                .catch(() => {
                    // Return cached response if offline
                    return caches.match(event.request)
                        .then((cached) => cached || createOfflineResponse());
                })
        );
    } else {
        // Cache-first strategy for static assets
        event.respondWith(
            caches.match(event.request)
                .then((cached) => cached || fetch(event.request))
                .catch(() => createOfflineResponse())
        );
    }
});

/**
 * Create offline response
 */
function createOfflineResponse() {
    return new Response(
        JSON.stringify({
            error: 'Offline',
            message: 'You are currently offline. Please check your internet connection.'
        }),
        {
            status: 503,
            statusText: 'Service Unavailable',
            headers: new Headers({
                'Content-Type': 'application/json'
            })
        }
    );
}

/**
 * Message handler for communication with main thread
 */
self.addEventListener('message', (event) => {
    console.log('Service Worker message:', event.data);

    if (event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data.type === 'QUEUE_NOTIFICATION') {
        queueNotificationOffline(event.data.notification);
    }

    if (event.data.type === 'GET_NOTIFICATION_QUEUE') {
        getNotificationQueue().then((queue) => {
            event.ports[0].postMessage({
                type: 'NOTIFICATION_QUEUE',
                data: queue
            });
        });
    }

    if (event.data.type === 'CLEAR_NOTIFICATION_QUEUE') {
        clearNotificationQueue();
    }
});

/**
 * Queue notification for offline
 * @param {Object} notification - Notification data
 */
function queueNotificationOffline(notification) {
    // Store in IndexedDB or localStorage
    if ('indexedDB' in self) {
        const request = indexedDB.open('el-akeil', 1);
        
        request.onsuccess = (event) => {
            const db = event.target.result;
            const transaction = db.transaction(['notifications'], 'readwrite');
            const store = transaction.objectStore('notifications');
            store.add({
                ...notification,
                timestamp: Date.now(),
                synced: false
            });
        };

        request.onerror = () => {
            console.error('IndexedDB error');
        };
    }
}

/**
 * Get notification queue from storage
 */
async function getNotificationQueue() {
    return new Promise((resolve) => {
        if ('indexedDB' in self) {
            const request = indexedDB.open('el-akeil', 1);
            
            request.onsuccess = (event) => {
                const db = event.target.result;
                const transaction = db.transaction(['notifications'], 'readonly');
                const store = transaction.objectStore('notifications');
                const query = store.getAll();
                
                query.onsuccess = () => {
                    resolve(query.result);
                };
                
                query.onerror = () => {
                    resolve([]);
                };
            };

            request.onerror = () => {
                resolve([]);
            };
        } else {
            resolve([]);
        }
    });
}

/**
 * Clear notification queue
 */
function clearNotificationQueue() {
    if ('indexedDB' in self) {
        const request = indexedDB.open('el-akeil', 1);
        
        request.onsuccess = (event) => {
            const db = event.target.result;
            const transaction = db.transaction(['notifications'], 'readwrite');
            const store = transaction.objectStore('notifications');
            store.clear();
        };
    }
}

/**
 * Periodic background sync for notifications
 * (requires permission and browser support)
 */
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-notifications') {
        event.waitUntil(syncNotifications());
    }
});

/**
 * Sync queued notifications
 */
async function syncNotifications() {
    const queue = await getNotificationQueue();
    
    for (const notification of queue) {
        if (!notification.synced) {
            try {
                // Send to server
                const response = await fetch('/api/notifications/sync', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(notification)
                });

                if (response.ok) {
                    // Mark as synced
                    updateNotificationSync(notification.id, true);
                }
            } catch (error) {
                console.error('Sync error:', error);
            }
        }
    }
}

/**
 * Update notification sync status
 * @param {number} id - Notification ID
 * @param {boolean} synced - Sync status
 */
function updateNotificationSync(id, synced) {
    if ('indexedDB' in self) {
        const request = indexedDB.open('el-akeil', 1);
        
        request.onsuccess = (event) => {
            const db = event.target.result;
            const transaction = db.transaction(['notifications'], 'readwrite');
            const store = transaction.objectStore('notifications');
            const query = store.get(id);
            
            query.onsuccess = () => {
                const data = query.result;
                if (data) {
                    data.synced = synced;
                    store.put(data);
                }
            };
        };
    }
}

console.log('Service Worker loaded and ready');
