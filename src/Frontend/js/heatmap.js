/**
 * Heatmap Visualization Module
 * Displays demand intensity and order hotspots on interactive map
 */

class HeatmapManager {
    constructor() {
        this.socket = null;
        this.map = null;
        this.heatmapLayer = null;
        this.token = null;
        this.userRole = null;
        this.userId = null;
        this.currentZones = [];
        this.timeRange = 'daily';
        this.updateInterval = null;
    }

    /**
     * Initialize heatmap system
     * @param {Object} options - Configuration options
     */
    async init(options = {}) {
        this.socket = options.socket || window.io();
        this.token = options.token;
        this.userRole = options.userRole || 'customer';
        this.userId = options.userId;
        this.timeRange = options.timeRange || 'daily';

        // Initialize map
        if (window.google && window.google.maps) {
            this.initializeGoogleMapsHeatmap();
        } else if (window.L) {
            this.initializeLeafletHeatmap();
        }

        // Setup listeners
        this.setupSocketListeners();

        // Load initial heatmap data
        await this.loadHeatmapData();

        // Set up auto-refresh (every 5 minutes)
        this.updateInterval = setInterval(() => {
            this.loadHeatmapData();
        }, 300000);
    }

    /**
     * Initialize Google Maps heatmap
     */
    initializeGoogleMapsHeatmap() {
        const mapElement = document.getElementById('heatmap-map');
        if (!mapElement) return;

        this.map = new google.maps.Map(mapElement, {
            zoom: 13,
            center: { lat: 30.0444, lng: 31.2357 }, // Cairo
            mapTypeControl: true,
            fullscreenControl: true,
            styles: [
                {
                    featureType: 'water',
                    stylers: [{ color: '#046fd0' }]
                },
                {
                    featureType: 'land',
                    stylers: [{ color: '#f3f3f3' }]
                },
                {
                    featureType: 'road',
                    stylers: [{ color: '#ffffff' }]
                }
            ]
        });

        // Add control for time range selection
        this.addTimeRangeControl();
    }

    /**
     * Initialize Leaflet heatmap
     */
    initializeLeafletHeatmap() {
        const mapElement = document.getElementById('heatmap-map');
        if (!mapElement) return;

        this.map = window.L.map(mapElement).setView([30.0444, 31.2357], 13);

        window.L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© OpenStreetMap contributors',
            maxZoom: 19
        }).addTo(this.map);

        // Create heatmap layer using Leaflet.heat plugin
        if (!window.L.heatLayer) {
            console.warn('Leaflet.heat not loaded - heatmap functionality limited');
        }

        this.addTimeRangeControl();
    }

    /**
     * Add time range selection control
     */
    addTimeRangeControl() {
        const controlElement = document.createElement('div');
        controlElement.className = 'heatmap-time-control';
        controlElement.innerHTML = `
            <div class="control-group">
                <label>Time Range:</label>
                <select onchange="heatmapManager.setTimeRange(this.value)">
                    <option value="daily">Daily</option>
                    <option value="weekly">Weekly</option>
                    <option value="monthly">Monthly</option>
                </select>
                <button class="btn-refresh" onclick="heatmapManager.loadHeatmapData()">🔄 Refresh</button>
            </div>
            <div class="heatmap-legend">
                <div class="legend-item">
                    <div class="legend-color" style="background: linear-gradient(to right, #4575b4, #91bfdb, #e0f3f8, #ffffbf, #fee090, #fc8d59, #e34a33, #b30000)"></div>
                    <span>Low Demand ← → High Demand</span>
                </div>
            </div>
        `;

        if (this.map && this.map.controls) {
            this.map.controls[google.maps.ControlPosition.TOP_RIGHT].push(controlElement);
        } else {
            const container = document.getElementById('heatmap-controls');
            if (container) container.appendChild(controlElement);
        }
    }

    /**
     * Set time range filter
     * @param {string} range - Time range (daily, weekly, monthly)
     */
    setTimeRange(range) {
        this.timeRange = range;
        this.loadHeatmapData();
    }

    /**
     * Load heatmap data from backend
     */
    async loadHeatmapData() {
        try {
            const response = await fetch(
                `/api/heatmap/zones?time_range=${this.timeRange}`,
                {
                    headers: {
                        'Authorization': `Bearer ${this.token}`
                    }
                }
            );

            if (response.ok) {
                const data = await response.json();
                this.currentZones = data.zones;
                this.renderHeatmap(data.zones);
                this.updateHeatmapStats(data);
            } else {
                console.error('Failed to load heatmap data:', response.status);
            }
        } catch (error) {
            console.error('Error loading heatmap data:', error);
        }
    }

    /**
     * Render heatmap on map
     * @param {Array} zones - Array of heatmap zones
     */
    renderHeatmap(zones) {
        if (!zones || zones.length === 0) {
            this.showMessage('No heatmap data available');
            return;
        }

        if (window.google && window.google.maps && this.map.data) {
            this.renderGoogleMapsHeatmap(zones);
        } else if (window.L && this.map) {
            this.renderLeafletHeatmap(zones);
        }

        // Add info window to each zone
        zones.forEach((zone, index) => {
            this.addZoneMarker(zone, index);
        });
    }

    /**
     * Render heatmap using Google Maps
     * @param {Array} zones - Heatmap zones
     */
    renderGoogleMapsHeatmap(zones) {
        // Convert zones to heatmap points
        const heatmapPoints = zones.map(zone => {
            const weight = zone.demand_intensity / 100; // Normalize to 0-1
            return new google.maps.LatLng(zone.center.lat, zone.center.long);
        });

        // Create heatmap layer
        if (this.heatmapLayer) {
            this.heatmapLayer.setData(heatmapPoints);
        } else {
            this.heatmapLayer = new google.maps.visualization.HeatmapLayer({
                data: heatmapPoints,
                map: this.map,
                radius: 50,
                maxIntensity: 100,
                dissipating: true,
                gradient: [
                    'rgba(0, 255, 255, 0)',      // Cyan
                    'rgba(0, 255, 0, 1)',        // Green (low)
                    'rgba(255, 255, 0, 1)',      // Yellow (medium)
                    'rgba(255, 128, 0, 1)',      // Orange
                    'rgba(255, 0, 0, 1)',        // Red (high)
                    'rgba(128, 0, 0, 1)'         // Dark red (very high)
                ]
            });
        }
    }

    /**
     * Render heatmap using Leaflet
     * @param {Array} zones - Heatmap zones
     */
    renderLeafletHeatmap(zones) {
        // Remove existing heatmap layer
        if (this.heatmapLayer) {
            this.map.removeLayer(this.heatmapLayer);
        }

        // Prepare data for Leaflet.heat
        const heatmapData = zones.map(zone => [
            zone.center.lat,
            zone.center.long,
            zone.demand_intensity / 100 // Intensity as weight (0-1)
        ]);

        // Create heatmap layer
        if (window.L.heatLayer) {
            this.heatmapLayer = window.L.heatLayer(heatmapData, {
                radius: 50,
                blur: 15,
                maxZoom: 18,
                gradient: {
                    0.0: '#4575b4',  // Blue (low)
                    0.2: '#91bfdb',
                    0.4: '#e0f3f8',
                    0.5: '#ffffbf',  // Yellow (medium)
                    0.6: '#fee090',
                    0.8: '#fc8d59',
                    1.0: '#b30000'   // Red (high)
                }
            }).addTo(this.map);
        } else {
            // Fallback: render circles for each zone
            zones.forEach(zone => {
                const intensity = zone.demand_intensity;
                const color = this.getIntensityColor(intensity);
                const radius = (intensity / 100) * 1000; // Convert intensity to radius

                window.L.circle([zone.center.lat, zone.center.long], {
                    color: color,
                    fill: true,
                    fillColor: color,
                    fillOpacity: 0.5,
                    radius: radius
                }).addTo(this.map).bindPopup(`
                    <b>Demand: ${intensity}%</b><br/>
                    Orders today: ${zone.order_count.daily}<br/>
                    Average price: ${zone.average_price.toFixed(2)} LE
                `);
            });
        }
    }

    /**
     * Get color based on demand intensity
     * @param {number} intensity - Intensity (0-100)
     */
    getIntensityColor(intensity) {
        if (intensity < 20) return '#4575b4';  // Blue
        if (intensity < 40) return '#91bfdb';  // Light blue
        if (intensity < 50) return '#e0f3f8';  // Very light blue
        if (intensity < 60) return '#ffffbf';  // Yellow
        if (intensity < 70) return '#fee090';  // Light orange
        if (intensity < 85) return '#fc8d59';  // Orange
        return '#b30000';                      // Dark red
    }

    /**
     * Add zone marker to map
     * @param {Object} zone - Zone data
     * @param {number} index - Zone index
     */
    addZoneMarker(zone, index) {
        const intensity = zone.demand_intensity;
        const color = this.getIntensityColor(intensity);
        const icon = this.getIntensityIcon(intensity);

        const infoContent = `
            <div class="zone-info-window">
                <h3>${icon} Demand Zone</h3>
                <p><strong>Intensity:</strong> ${intensity}%</p>
                <p><strong>Orders Today:</strong> ${zone.order_count.daily}</p>
                <p><strong>Orders This Week:</strong> ${zone.order_count.weekly}</p>
                <p><strong>Average Price:</strong> ${zone.average_price.toFixed(2)} LE</p>
                <p><small>Last Updated: ${new Date(zone.last_updated).toLocaleTimeString()}</small></p>
            </div>
        `;

        if (window.L && this.map && this.map.setView) {
            // Leaflet marker
            const marker = window.L.marker([zone.center.lat, zone.center.long], {
                title: `Zone ${intensity}% Demand`
            }).addTo(this.map);

            marker.bindPopup(infoContent);
            marker.setIcon(window.L.divIcon({
                className: `zone-marker intensity-${Math.round(intensity / 20) * 20}`,
                html: icon,
                iconSize: [32, 32],
                iconAnchor: [16, 16],
                popupAnchor: [0, -16]
            }));
        } else if (window.google && window.google.maps && this.map) {
            // Google Maps marker
            new google.maps.Marker({
                position: { lat: zone.center.lat, lng: zone.center.long },
                map: this.map,
                title: `Zone ${intensity}% Demand`,
                icon: {
                    path: google.maps.SymbolPath.CIRCLE,
                    scale: intensity / 10,
                    fillColor: color,
                    fillOpacity: 0.7,
                    strokeColor: '#ffffff',
                    strokeWeight: 2
                }
            }).addListener('click', () => {
                this.showZoneInfo(zone, infoContent);
            });
        }
    }

    /**
     * Get intensity emoji icon
     * @param {number} intensity - Intensity (0-100)
     */
    getIntensityIcon(intensity) {
        if (intensity < 30) return '🟢';      // Green - low
        if (intensity < 60) return '🟡';      // Yellow - medium
        if (intensity < 80) return '🟠';      // Orange - high
        return '🔴';                          // Red - very high
    }

    /**
     * Show zone information
     * @param {Object} zone - Zone data
     * @param {string} infoContent - HTML content
     */
    showZoneInfo(zone, infoContent) {
        const modal = document.createElement('div');
        modal.className = 'modal zone-info-modal';
        modal.innerHTML = `
            <div class="modal-content">
                <button class="modal-close" onclick="this.parentElement.parentElement.remove()">×</button>
                ${infoContent}
                <div class="zone-actions">
                    <button class="btn btn-primary" onclick="heatmapManager.focusZone(${zone.center.lat}, ${zone.center.long})">
                        📍 Focus Map
                    </button>
                </div>
            </div>
        `;
        document.body.appendChild(modal);
    }

    /**
     * Focus map on a specific zone
     * @param {number} lat - Latitude
     * @param {number} long - Longitude
     */
    focusZone(lat, long) {
        if (this.map && this.map.panTo) {
            this.map.panTo([lat, long]);
        } else if (this.map && this.map.setCenter) {
            this.map.setCenter({ lat: lat, lng: long });
        }
    }

    /**
     * Update heatmap statistics display
     * @param {Object} data - Heatmap data
     */
    updateHeatmapStats(data) {
        const statsContainer = document.getElementById('heatmap-stats');
        if (!statsContainer) return;

        const highDemand = data.zones.filter(z => z.demand_intensity >= 75).length;
        const mediumDemand = data.zones.filter(z => z.demand_intensity >= 50 && z.demand_intensity < 75).length;
        const lowDemand = data.zones.filter(z => z.demand_intensity < 50).length;

        statsContainer.innerHTML = `
            <div class="stats-grid">
                <div class="stat-card high-demand">
                    <h4>🔴 High Demand</h4>
                    <p>${highDemand} zones</p>
                </div>
                <div class="stat-card medium-demand">
                    <h4>🟡 Medium Demand</h4>
                    <p>${mediumDemand} zones</p>
                </div>
                <div class="stat-card low-demand">
                    <h4>🟢 Low Demand</h4>
                    <p>${lowDemand} zones</p>
                </div>
                <div class="stat-card total-zones">
                    <h4>📊 Total Zones</h4>
                    <p>${data.zones.length} zones</p>
                </div>
            </div>
        `;
    }

    /**
     * Set up Socket.IO listeners
     */
    setupSocketListeners() {
        this.socket.on('heatmap_updated', () => {
            this.loadHeatmapData();
        });

        this.socket.on('heatmap_data', (data) => {
            this.currentZones = data.zones;
            this.renderHeatmap(data.zones);
        });

        this.socket.on('heatmap_error', (data) => {
            console.error('Heatmap error:', data);
            this.showMessage('Error loading heatmap data', 'error');
        });
    }

    /**
     * Show message
     * @param {string} message - Message text
     * @param {string} type - Message type (info, error, success)
     */
    showMessage(message, type = 'info') {
        const container = document.getElementById('heatmap-message');
        if (container) {
            container.textContent = message;
            container.className = `heatmap-message ${type}`;
            container.style.display = 'block';
            setTimeout(() => container.style.display = 'none', 3000);
        }
    }

    /**
     * Export heatmap data
     */
    exportHeatmapData() {
        const csvContent = 'data:text/csv;charset=utf-8,' +
            ['Latitude,Longitude,Intensity,Orders Today,Average Price']
            .concat(this.currentZones.map(z =>
                `${z.center.lat},${z.center.long},${z.demand_intensity},${z.order_count.daily},${z.average_price}`
            ))
            .join('\n');

        const link = document.createElement('a');
        link.setAttribute('href', encodeURI(csvContent));
        link.setAttribute('download', `heatmap_${this.timeRange}_${new Date().toISOString().split('T')[0]}.csv`);
        link.click();
    }

    /**
     * Cleanup
     */
    destroy() {
        if (this.updateInterval) {
            clearInterval(this.updateInterval);
        }
    }
}

// Global instance
const heatmapManager = new HeatmapManager();

// Initialize when page loads
document.addEventListener('DOMContentLoaded', () => {
    const heatmapElement = document.getElementById('heatmap-map');
    if (heatmapElement) {
        heatmapManager.init({
            userRole: document.body.dataset.userRole || 'customer',
            userId: document.body.dataset.userId,
            token: localStorage.getItem('auth_token')
        });
    }
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    heatmapManager.destroy();
});
