/**
 * Advanced Chef Tracking & Live Map
 * Includes real-time tracking, heatmap, and analytics
 */

let advancedMap = null;
let heatmapData = [];
let trackingMarkers = {};
let socket = null;

// Initialize advanced tracking map
function initAdvancedChefMap(mapElementId = 'advancedMap') {
    const mapElement = document.getElementById(mapElementId);
    if (!mapElement) return;

    // Default to Cairo
    const defaultLat = 30.0444;
    const defaultLng = 31.2357;

    advancedMap = L.map(mapElementId).setView([defaultLat, defaultLng], 12);
    
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(advancedMap);

    // Initialize socket for real-time updates
    if (typeof io !== 'undefined' && socket === null) {
        socket = io();
        setupRealtimeTracking();
    }

    loadHeatmapData();
}

// Setup real-time tracking via WebSocket
function setupRealtimeTracking() {
    if (!socket) return;

    // Track driver location
    socket.on('driver_location_update', (data) => {
        updateDriverMarker(data.driver_id, data.lat, data.lng, data.order_id);
    });

    // Track chef activity
    socket.on('chef_status_update', (data) => {
        updateChefMarker(data.chef_id, data.status, data.lat, data.lng);
    });

    // Update heatmap
    socket.on('order_completed', (data) => {
        addHeatmapPoint(data.lat, data.lng);
    });
}

// Update driver marker on map
function updateDriverMarker(driverId, lat, lng, orderId) {
    const markerId = `driver_${driverId}`;
    
    if (trackingMarkers[markerId]) {
        trackingMarkers[markerId].setLatLng([lat, lng]);
    } else {
        const marker = L.marker([lat, lng], {
            icon: L.icon({
                iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-green.png',
                shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                iconSize: [25, 41],
                iconAnchor: [12, 41],
                popupAnchor: [1, -34],
                shadowSize: [41, 41]
            })
        }).addTo(advancedMap)
         .bindPopup(`<b>🚗 Driver #${driverId}</b><br>Order: #${orderId}<br>Live Tracking`);
        
        trackingMarkers[markerId] = marker;
    }
}

// Update chef marker status
function updateChefMarker(chefId, status, lat, lng) {
    const markerId = `chef_${chefId}`;
    let color = 'gray';
    
    if (status === 'preparing') color = 'orange';
    if (status === 'ready') color = 'green';
    if (status === 'closed') color = 'red';
    
    if (trackingMarkers[markerId]) {
        trackingMarkers[markerId].setLatLng([lat, lng]);
        // Update color based on status
        const newIcon = L.icon({
            iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${color}.png`,
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });
        trackingMarkers[markerId].setIcon(newIcon);
    }
}

// Load heatmap data from server
async function loadHeatmapData() {
    try {
        const response = await apiFetch('/customer/heatmap-data');
        if (response.ok) {
            heatmapData = response.data.map(point => [point.lat, point.lng, point.intensity || 1]);
            displayHeatmap();
        }
    } catch (error) {
        console.error('Error loading heatmap data:', error);
    }
}

// Display heatmap on map
function displayHeatmap() {
    if (!advancedMap || heatmapData.length === 0) return;

    // Remove old heatmap if exists
    if (window.heatmapLayer) {
        advancedMap.removeLayer(window.heatmapLayer);
    }

    // Note: Requires leaflet-heat plugin
    // <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-heat/0.2.0/leaflet-heat.js"></script>
    if (typeof L.heatLayer !== 'undefined') {
        window.heatmapLayer = L.heatLayer(heatmapData, {
            radius: 25,
            blur: 15,
            maxZoom: 17,
            minOpacity: 0.2,
            gradient: {
                0.0: '#0000ff',      // Blue (cold)
                0.25: '#00ffff',     // Cyan
                0.5: '#00ff00',      // Green
                0.75: '#ffff00',     // Yellow
                1.0: '#ff0000'       // Red (hot)
            }
        }).addTo(advancedMap);
    }
}

// Add point to heatmap
function addHeatmapPoint(lat, lng, intensity = 1) {
    heatmapData.push([lat, lng, intensity]);
    displayHeatmap();
}

// Get analytics data
async function getChefAnalytics() {
    try {
        const response = await apiFetch('/customer/chef-analytics');
        if (response.ok) {
            return response.data;
        }
    } catch (error) {
        console.error('Error loading analytics:', error);
    }
    return null;
}

// Display chef statistics
function displayChefStats(analytics) {
    if (!analytics) return;

    const statsHtml = `
        <div style="background: white; padding: 15px; border-radius: 8px; margin: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
            <h3 style="margin: 0 0 10px 0; color: #FF5A00;">📊 Platform Analytics</h3>
            
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px;">
                <div style="background: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 0.8rem; color: #666;">Total Chefs</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #FF5A00;">${analytics.total_chefs || 0}</div>
                </div>
                <div style="background: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 0.8rem; color: #666;">Active Now</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #4CAF50;">${analytics.active_chefs || 0}</div>
                </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                <div style="background: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 0.8rem; color: #666;">Today's Orders</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #2196F3;">${analytics.orders_today || 0}</div>
                </div>
                <div style="background: #f0f0f0; padding: 10px; border-radius: 5px; text-align: center;">
                    <div style="font-size: 0.8rem; color: #666;">Avg Rating</div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #FFA500;">⭐ ${analytics.avg_rating || 4.5}</div>
                </div>
            </div>
        </div>
    `;

    const statsContainer = document.getElementById('chefStatsContainer');
    if (statsContainer) {
        statsContainer.innerHTML = statsHtml;
    }
}

// Real-time delivery tracking
function trackDelivery(orderId, startLat, startLng) {
    const deliveryMarker = L.marker([startLat, startLng], {
        icon: L.icon({
            iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        })
    }).addTo(advancedMap)
     .bindPopup(`<b>🎯 Order #${orderId}</b><br>Tracking Delivery...`);

    return deliveryMarker;
}

// Get busy areas (high demand zones)
async function getBusyAreas() {
    try {
        const response = await apiFetch('/customer/busy-areas');
        if (response.ok) {
            return response.data;
        }
    } catch (error) {
        console.error('Error loading busy areas:', error);
    }
    return [];
}

// Display busy areas on map
async function displayBusyAreas() {
    const busyAreas = await getBusyAreas();
    
    busyAreas.forEach(area => {
        const intensity = area.intensity || 0.5;
        
        L.circleMarker([area.lat, area.lng], {
            radius: Math.max(5, intensity * 30),
            fillColor: area.status === 'critical' ? '#ff0000' : area.status === 'high' ? '#ffa500' : '#ffff00',
            color: '#000',
            weight: 2,
            opacity: 0.8,
            fillOpacity: 0.6
        }).addTo(advancedMap)
         .bindPopup(`
            <b>🔥 Busy Area</b><br>
            Status: ${area.status}<br>
            Demand: ${Math.round(intensity * 100)}%<br>
            Active Chefs: ${area.active_chefs}
         `);
    });
}

// Export heatmap as image
function exportHeatmapImage() {
    if (!advancedMap) return;
    
    const canvas = document.querySelector('.leaflet-container canvas');
    if (canvas) {
        const link = document.createElement('a');
        link.href = canvas.toDataURL();
        link.download = `heatmap-${new Date().toISOString()}.png`;
        link.click();
    }
}

// Initialize stats on load
window.addEventListener('load', () => {
    getChefAnalytics().then(analytics => {
        displayChefStats(analytics);
    });
});
