/**
 * Navigation Module - Real-time driver navigation and tracking
 * Handles turn-by-turn directions, ETA, and customer tracking view
 */

class NavigationManager {
    constructor() {
        this.socket = null;
        this.currentOrder = null;
        this.currentRoute = null;
        this.map = null;
        this.directionsRenderer = null;
        this.isDriver = false;
        this.isCustomer = false;
        this.locationInterval = null;
        this.watchId = null;
    }

    /**
     * Initialize navigation system
     * @param {Object} options - Configuration options
     */
    async init(options = {}) {
        this.socket = options.socket || window.io();
        this.userRole = options.userRole || 'customer';
        this.userId = options.userId;
        this.token = options.token;
        
        this.isDriver = this.userRole === 'driver';
        this.isCustomer = this.userRole === 'customer';
        
        // Listen for socket events
        this.setupSocketListeners();
        
        // Load Google Maps or use OpenStreetMap
        if (window.google && window.google.maps) {
            this.initializeGoogleMaps();
        } else {
            this.initializeOpenStreetMap();
        }
    }

    /**
     * Set up Socket.IO event listeners
     */
    setupSocketListeners() {
        // Driver location updates
        this.socket.on('driver_location_update', (data) => {
            this.updateDriverLocationOnMap(data);
        });

        // Navigation started
        this.socket.on('navigation_started', (data) => {
            this.handleNavigationStarted(data);
        });

        // Leg completed
        this.socket.on('leg_update', (data) => {
            this.handleLegUpdate(data);
        });

        // Order completed
        this.socket.on('order_completed', (data) => {
            this.handleOrderCompleted(data);
        });

        // Route information
        this.socket.on('route_info', (data) => {
            this.currentRoute = data;
            this.displayRoute(data);
        });

        // Error handling
        this.socket.on('nav_error', (data) => {
            this.showError(data.message);
        });
    }

    /**
     * Initialize Google Maps for navigation
     */
    initializeGoogleMaps() {
        const mapElement = document.getElementById('navigation-map');
        if (!mapElement) return;

        this.map = new google.maps.Map(mapElement, {
            zoom: 15,
            center: { lat: 30.0444, lng: 31.2357 }, // Default to Cairo
            mapTypeControl: true,
            fullscreenControl: true,
            trafficLayer: true
        });

        this.directionsRenderer = new google.maps.DirectionsRenderer({
            map: this.map,
            suppressMarkers: false,
            suppressPolylines: false
        });

        // Watch for drag/pan and update bounds
        this.map.addListener('bounds_changed', () => {
            this.updateMapBounds();
        });
    }

    /**
     * Initialize OpenStreetMap (Leaflet) for navigation
     */
    initializeOpenStreetMap() {
        const mapElement = document.getElementById('navigation-map');
        if (!mapElement) return;

        // Requires leaflet.js loaded
        if (!window.L) {
            console.error('Leaflet.js not loaded');
            return;
        }

        this.map = window.L.map(mapElement).setView([30.0444, 31.2357], 15);
        
        window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Add markers
        this.driverMarker = window.L.marker([30.0444, 31.2357], {
            title: 'Driver Location',
            icon: window.L.icon({
                iconUrl: '🚗',
                iconSize: [32, 32]
            })
        }).addTo(this.map);

        this.chefMarker = window.L.marker([30.0444, 31.2357], {
            title: 'Chef Location (Pickup)',
            icon: window.L.icon({
                iconUrl: '🍽️',
                iconSize: [32, 32]
            })
        }).addTo(this.map);

        this.customerMarker = window.L.marker([30.0444, 31.2357], {
            title: 'Delivery Location',
            icon: window.L.icon({
                iconUrl: '📍',
                iconSize: [32, 32]
            })
        }).addTo(this.map);
    }

    /**
     * Start navigation for driver
     * @param {number} orderId - Order ID
     */
    async startNavigation(orderId) {
        if (!this.isDriver) {
            this.showError('Only drivers can start navigation');
            return;
        }

        this.currentOrder = orderId;

        // Emit socket event
        this.socket.emit('start_navigation', {
            token: this.token,
            order_id: orderId
        });

        // Request route from backend
        try {
            const response = await fetch(`/api/navigation/route/create`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                },
                body: JSON.stringify({ order_id: orderId })
            });

            const data = await response.json();
            if (response.ok) {
                this.currentRoute = data.route;
                this.displayRoute(data.route);
                
                // Start tracking location
                this.startLocationTracking();
                
                // Show driver controls
                this.showDriverControls();
            } else {
                this.showError(data.error || 'Failed to create route');
            }
        } catch (error) {
            console.error('Error creating route:', error);
            this.showError('Failed to create route');
        }
    }

    /**
     * Display route on map
     * @param {Object} route - Route data
     */
    displayRoute(route) {
        if (!route) return;

        const mapContainer = document.getElementById('navigation-map');
        if (!mapContainer) return;

        // Clear previous route
        if (this.directionsRenderer) {
            this.directionsRenderer.setDirections({ routes: [] });
        }

        // Create route info panel
        const infoPanel = this.createRouteInfoPanel(route);
        this.updateRouteInfo(route);

        // If using OpenStreetMap
        if (this.map && this.map.setView) {
            // Parse route data and draw polyline
            if (route.pickup && route.pickup.distance_km) {
                const pickupEta = new Date(route.pickup.eta);
                const deliveryEta = new Date(route.delivery.eta);

                // Update markers
                if (this.driverMarker) {
                    this.driverMarker.setLatLng([
                        route.current_location.lat,
                        route.current_location.long
                    ]);
                }

                // Fit all markers in view
                const group = window.L.featureGroup([
                    this.driverMarker,
                    this.chefMarker,
                    this.customerMarker
                ]);
                this.map.fitBounds(group.getBounds().pad(0.1));
            }
        }
    }

    /**
     * Create route information panel
     * @param {Object} route - Route data
     */
    createRouteInfoPanel(route) {
        const panel = document.createElement('div');
        panel.className = 'route-info-panel';
        panel.innerHTML = `
            <div class="route-info-container">
                <div class="route-header">
                    <h3>🗺️ Navigation</h3>
                    <button class="btn-minimize" onclick="this.parentElement.parentElement.classList.toggle('minimized')">−</button>
                </div>

                <div class="route-content">
                    <!-- Current Leg -->
                    <div class="current-leg">
                        <div class="leg-status">
                            <span class="leg-label">${route.current_leg === 'pickup' ? '📍 Pickup' : '🚚 Delivery'}</span>
                            <span class="leg-progress"></span>
                        </div>
                    </div>

                    <!-- Leg Details -->
                    <div class="leg-details">
                        <div class="leg-item pickup-leg">
                            <h4>🏪 Pickup from Restaurant</h4>
                            <p class="distance">${route.pickup?.distance_km.toFixed(1)} km</p>
                            <p class="duration">${route.pickup?.duration_mins} min</p>
                            <p class="eta">ETA: ${new Date(route.pickup?.eta).toLocaleTimeString()}</p>
                        </div>

                        <div class="leg-item delivery-leg">
                            <h4>📦 Deliver to Customer</h4>
                            <p class="distance">${route.delivery?.distance_km.toFixed(1)} km</p>
                            <p class="duration">${route.delivery?.duration_mins} min</p>
                            <p class="eta">ETA: ${new Date(route.delivery?.eta).toLocaleTimeString()}</p>
                        </div>

                        <div class="leg-item total-leg">
                            <h4>⏱️ Total Duration</h4>
                            <p class="total-time">${(route.pickup?.duration_mins || 0) + (route.delivery?.duration_mins || 0)} min</p>
                        </div>
                    </div>

                    <!-- Driver Controls (only for drivers) -->
                    <div class="driver-controls" id="driver-controls" style="display: none;">
                        <button class="btn btn-primary" onclick="navigationManager.markLegCompleted()">
                            ✓ Leg Complete
                        </button>
                        <button class="btn btn-secondary" onclick="navigationManager.requestSupport()">
                            ⚠️ Request Support
                        </button>
                    </div>
                </div>
            </div>
        `;

        const mapContainer = document.getElementById('navigation-map');
        if (mapContainer) {
            mapContainer.parentElement.appendChild(panel);
        }

        return panel;
    }

    /**
     * Update route information display
     * @param {Object} route - Route data
     */
    updateRouteInfo(route) {
        const panel = document.querySelector('.route-info-panel');
        if (!panel || !route) return;

        // Update pickup leg
        const pickupLeg = panel.querySelector('.pickup-leg');
        if (pickupLeg && route.pickup) {
            pickupLeg.querySelector('.distance').textContent = `${route.pickup.distance_km.toFixed(1)} km`;
            pickupLeg.querySelector('.duration').textContent = `${route.pickup.duration_mins} min`;
            if (route.pickup.eta) {
                pickupLeg.querySelector('.eta').textContent = `ETA: ${new Date(route.pickup.eta).toLocaleTimeString()}`;
            }
        }

        // Update delivery leg
        const deliveryLeg = panel.querySelector('.delivery-leg');
        if (deliveryLeg && route.delivery) {
            deliveryLeg.querySelector('.distance').textContent = `${route.delivery.distance_km.toFixed(1)} km`;
            deliveryLeg.querySelector('.duration').textContent = `${route.delivery.duration_mins} min`;
            if (route.delivery.eta) {
                deliveryLeg.querySelector('.eta').textContent = `ETA: ${new Date(route.delivery.eta).toLocaleTimeString()}`;
            }
        }

        // Update current leg indicator
        const legStatus = panel.querySelector('.leg-status .leg-label');
        if (legStatus) {
            legStatus.textContent = route.current_leg === 'pickup' ? '📍 Heading to Pickup' : '🚚 Delivering Order';
        }
    }

    /**
     * Start tracking driver location
     */
    startLocationTracking() {
        if (!this.isDriver) return;

        if (!navigator.geolocation) {
            this.showError('Geolocation not supported');
            return;
        }

        // Request permission and start tracking
        this.watchId = navigator.geolocation.watchPosition(
            (position) => {
                this.sendLocationUpdate(position.coords.latitude, position.coords.longitude);
            },
            (error) => {
                console.error('Geolocation error:', error);
                this.showError('Failed to access location');
            },
            {
                enableHighAccuracy: true,
                maximumAge: 10000, // 10 seconds
                timeout: 5000
            }
        );

        console.log('Location tracking started');
    }

    /**
     * Send location update to server
     * @param {number} lat - Latitude
     * @param {number} long - Longitude
     */
    sendLocationUpdate(lat, long) {
        if (!this.currentOrder) return;

        // Emit via socket for real-time
        this.socket.emit('update_location', {
            token: this.token,
            order_id: this.currentOrder,
            lat: lat,
            long: long
        });

        // Update local marker
        if (this.driverMarker && this.driverMarker.setLatLng) {
            this.driverMarker.setLatLng([lat, long]);
        }
    }

    /**
     * Mark current leg as completed
     */
    markLegCompleted() {
        if (!this.currentOrder) return;

        if (!confirm('Mark this leg as completed?')) return;

        this.socket.emit('leg_completed', {
            token: this.token,
            order_id: this.currentOrder
        });
    }

    /**
     * Handle navigation started event
     * @param {Object} data - Event data
     */
    handleNavigationStarted(data) {
        this.showNotification(
            '🚗 Navigation Started',
            `Driver ${data.driver_id} started navigation`
        );
    }

    /**
     * Handle leg update event
     * @param {Object} data - Event data
     */
    handleLegUpdate(data) {
        this.showNotification(
            '📍 Leg Update',
            data.message || 'Leg information updated'
        );
        this.displayRoute(this.currentRoute);
    }

    /**
     * Handle order completed event
     * @param {Object} data - Event data
     */
    handleOrderCompleted(data) {
        this.showNotification(
            '✅ Order Delivered',
            data.message || 'Order has been successfully delivered'
        );
        this.stopLocationTracking();
        this.hideDriverControls();
    }

    /**
     * Update driver location on customer's map
     * @param {Object} data - Location data
     */
    updateDriverLocationOnMap(data) {
        if (!this.isCustomer) return;

        if (this.driverMarker && this.driverMarker.setLatLng) {
            this.driverMarker.setLatLng([data.latitude, data.longitude]);
            
            // Pan map to driver if they're close
            if (this.map && this.map.panTo) {
                this.map.panTo([data.latitude, data.longitude]);
            }
        }

        // Update time
        const timeEl = document.querySelector('.driver-tracking-time');
        if (timeEl) {
            const time = new Date(data.timestamp);
            timeEl.textContent = `Last update: ${time.toLocaleTimeString()}`;
        }
    }

    /**
     * Show driver control buttons
     */
    showDriverControls() {
        const controls = document.getElementById('driver-controls');
        if (controls) {
            controls.style.display = 'flex';
        }
    }

    /**
     * Hide driver control buttons
     */
    hideDriverControls() {
        const controls = document.getElementById('driver-controls');
        if (controls) {
            controls.style.display = 'none';
        }
    }

    /**
     * Stop location tracking
     */
    stopLocationTracking() {
        if (this.watchId !== null) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
            console.log('Location tracking stopped');
        }
    }

    /**
     * Request support during delivery
     */
    requestSupport() {
        const message = prompt('Describe the issue:');
        if (message) {
            this.socket.emit('request_support', {
                token: this.token,
                order_id: this.currentOrder,
                message: message
            });
            this.showNotification('📞 Support Requested', 'Our team will contact you shortly');
        }
    }

    /**
     * Show error message
     * @param {string} message - Error message
     */
    showError(message) {
        const toast = document.createElement('div');
        toast.className = 'toast toast-error';
        toast.textContent = `❌ ${message}`;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
    }

    /**
     * Show notification
     * @param {string} title - Notification title
     * @param {string} message - Notification message
     */
    showNotification(title, message) {
        const notif = document.createElement('div');
        notif.className = 'notification';
        notif.innerHTML = `
            <div class="notif-content">
                <h4>${title}</h4>
                <p>${message}</p>
            </div>
        `;
        document.body.appendChild(notif);
        
        // Trigger animation
        setTimeout(() => notif.classList.add('show'), 10);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            notif.classList.remove('show');
            setTimeout(() => notif.remove(), 300);
        }, 3000);
    }

    /**
     * Update map bounds
     */
    updateMapBounds() {
        // Trigger custom event for bounds update
        window.dispatchEvent(new Event('mapBoundsChanged'));
    }
}

// Global instance
const navigationManager = new NavigationManager();

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    navigationManager.init({
        userRole: document.body.dataset.userRole || 'customer',
        userId: document.body.dataset.userId,
        token: localStorage.getItem('auth_token')
    });
});
