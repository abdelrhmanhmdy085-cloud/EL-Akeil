/**
 * Chef Location Map Module
 * Handles displaying chefs on a map and filtering by location
 */

let chefMap = null;
let chefsMarkers = {};
let userLocation = null;

// Initialize the chef location map
function initChefMap(mapElementId = 'map') {
    const mapElement = document.getElementById(mapElementId);
    if (!mapElement) return;

    // Default to Cairo
    const defaultLat = 30.0444;
    const defaultLng = 31.2357;
    const defaultZoom = 13;

    chefMap = L.map(mapElementId).setView([defaultLat, defaultLng], defaultZoom);
    
    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(chefMap);

    // Get user location if available
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                userLocation = {
                    lat: position.coords.latitude,
                    lng: position.coords.longitude
                };
                // Update map view to user location
                chefMap.setView([userLocation.lat, userLocation.lng], 13);
                
                // Add user marker
                L.marker([userLocation.lat, userLocation.lng], {
                    icon: L.icon({
                        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-blue.png',
                        shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
                        iconSize: [25, 41],
                        iconAnchor: [12, 41],
                        popupAnchor: [1, -34],
                        shadowSize: [41, 41]
                    })
                }).addTo(chefMap)
                 .bindPopup('<b>📍 Your Location</b>');
                
                // Load and display chefs
                loadChefsOnMap();
            },
            (error) => {
                console.warn('Geolocation error:', error);
                // Load chefs with default location anyway
                loadChefsOnMap();
            }
        );
    } else {
        loadChefsOnMap();
    }
}

// Load chefs and display them on map
async function loadChefsOnMap() {
    try {
        // Build query params
        const params = new URLSearchParams();
        if (userLocation) {
            params.append('lat', userLocation.lat);
            params.append('long', userLocation.lng);
            params.append('max_distance', 50); // 50 km radius
        }

        const response = await apiFetch(`/customer/chefs?${params.toString()}`);
        
        if (!response.ok) {
            console.error('Failed to load chefs:', response.data);
            return;
        }

        const chefs = response.data;
        
        // Clear existing markers
        Object.values(chefsMarkers).forEach(marker => {
            chefMap.removeLayer(marker);
        });
        chefsMarkers = {};

        // Add markers for each chef
        chefs.forEach(chef => {
            if (chef.lat && chef.long) {
                addChefMarker(chef);
            }
        });

        // Fit map bounds to show all markers
        if (chefs.length > 0) {
            fitMapToBounds();
        }

    } catch (error) {
        console.error('Error loading chefs on map:', error);
    }
}

// Add a chef marker to the map
function addChefMarker(chef) {
    const ratingColor = chef.rating >= 4.5 ? 'gold' : chef.rating >= 4 ? 'orange' : 'red';
    
    const popupContent = `
        <div style="width: 200px; font-family: Cairo, sans-serif;">
            <h3 style="margin: 5px 0; color: #FF5A00; font-size: 1.1rem;">👨‍🍳 ${chef.name}</h3>
            <p style="margin: 5px 0; font-size: 0.85rem;">📍 ${chef.address}</p>
            <p style="margin: 5px 0;">
                <span style="color: ${ratingColor};">⭐ ${chef.rating}</span>
                <span style="color: #999; font-size: 0.8rem;">(${chef.review_count} reviews)</span>
            </p>
            <p style="margin: 5px 0; color: #666; font-size: 0.85rem;">
                ⏱️ Prep Time: ${chef.prep_time} min
            </p>
            ${chef.distance ? `<p style="margin: 5px 0; color: #0066cc; font-size: 0.85rem;">📏 ${chef.distance} km away</p>` : ''}
            <button onclick="selectChef(${chef.user_id})" style="
                width: 100%;
                padding: 8px;
                background: #FF5A00;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                margin-top: 10px;
            ">View Dishes</button>
        </div>
    `;

    const marker = L.marker([chef.lat, chef.long], {
        icon: L.icon({
            iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-${ratingColor}.png`,
            shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.7/images/marker-shadow.png',
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        })
    })
    .bindPopup(popupContent)
    .addTo(chefMap);

    chefsMarkers[chef.user_id] = marker;
}

// Fit map bounds to show all markers
function fitMapToBounds() {
    const group = new L.featureGroup(Object.values(chefsMarkers));
    if (userLocation) {
        const userMarker = L.marker([userLocation.lat, userLocation.lng]);
        group.addLayer(userMarker);
    }
    chefMap.fitBounds(group.getBounds().pad(0.1));
}

// Select a chef and filter dishes
function selectChef(chefId) {
    if (typeof filterByChef === 'function') {
        filterByChef(chefId);
    }
    // Close popup
    if (chefMap) {
        chefMap.closePopup();
    }
}

// Update map when filters change
function updateMapDisplay(chefIds = null) {
    Object.entries(chefsMarkers).forEach(([chefId, marker]) => {
        if (chefIds && !chefIds.includes(parseInt(chefId))) {
            marker.setOpacity(0.3);
        } else {
            marker.setOpacity(1);
        }
    });
}

// Re-center map on user location
function recenterMapOnUser() {
    if (userLocation && chefMap) {
        chefMap.setView([userLocation.lat, userLocation.lng], 13);
    }
}
