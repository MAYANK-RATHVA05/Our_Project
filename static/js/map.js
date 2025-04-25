/**
 * Weather App Map Functionality
 * Initializes a Leaflet map on the home page and handles location selection
 */

// Initialize map when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check if map container exists
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // Initialize the map
    const map = L.map('map', {
        scrollWheelZoom: false,  // Disable scroll wheel zoom for embedded map
        zoomControl: true
    }).setView([20, 0], 2);  // Default to world view

    // Add OpenStreetMap tiles
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    // Add control to go to full map view
    const fullMapButton = L.control({ position: 'topright' });
    fullMapButton.onAdd = function() {
        const div = L.DomUtil.create('div', 'leaflet-bar leaflet-control');
        div.innerHTML = '<a href="/weather/map/" title="Open Full Map" class="leaflet-control-fullmap" style="font-size: 18px; display: flex; align-items: center; justify-content: center; text-decoration: none; height: 30px; width: 30px;"><i class="fas fa-expand-alt"></i></a>';
        return div;
    };
    fullMapButton.addTo(map);

    // Variables for storing selected location
    let marker = null;
    let selectedLat = null;
    let selectedLng = null;

    // Handle map clicks
    map.on('click', function(e) {
        // Get coordinates
        selectedLat = e.latlng.lat.toFixed(6);
        selectedLng = e.latlng.lng.toFixed(6);

        // Add or move marker
        if (marker) {
            marker.setLatLng(e.latlng);
        } else {
            marker = L.marker(e.latlng).addTo(map);
        }

        // Show info and submit button
        showLocationInfo(selectedLat, selectedLng);
    });

    // Function to show location info and get weather button
    function showLocationInfo(lat, lng) {
        const locationInfoElement = document.getElementById('location-info');
        if (!locationInfoElement) return;

        // Show the location info container
        locationInfoElement.style.display = 'block';

        // Update coordinates display
        document.getElementById('selected-coordinates').textContent = `${lat}, ${lng}`;

        // Set form input values
        document.getElementById('lat-input').value = lat;
        document.getElementById('lng-input').value = lng;

        // Try to get location name through reverse geocoding
        reverseGeocode(lat, lng);
    }

    // Function to perform reverse geocoding
    function reverseGeocode(lat, lng) {
        // Use OpenStreetMap Nominatim API for reverse geocoding
        fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}`)
            .then(response => response.json())
            .then(data => {
                if (data && data.display_name) {
                    document.getElementById('selected-location-name').textContent = data.display_name;
                } else {
                    document.getElementById('selected-location-name').textContent = 'Unknown location';
                }
            })
            .catch(error => {
                console.error('Error reverse geocoding:', error);
                document.getElementById('selected-location-name').textContent = 'Unknown location';
            });
    }

    // Try to get user's location
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                // Center map on user's location
                const userLat = position.coords.latitude;
                const userLng = position.coords.longitude;
                map.setView([userLat, userLng], 10);

                // Add a marker for the user's location
                L.circle([userLat, userLng], {
                    color: 'blue',
                    fillColor: '#3388ff',
                    fillOpacity: 0.2,
                    radius: 1000
                }).addTo(map).bindPopup("Your approximate location").openPopup();
            },
            function(error) {
                console.log('Error getting location:', error.message);
            }
        );
    }

    // Handle location search if search box exists
    const searchBox = document.getElementById('map-search-input');
    const searchButton = document.getElementById('map-search-button');
    
    if (searchBox && searchButton) {
        // Search on button click
        searchButton.addEventListener('click', function() {
            searchLocation();
        });
        
        // Search on Enter key
        searchBox.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                searchLocation();
            }
        });
        
        // Function to search for a location
        function searchLocation() {
            const query = searchBox.value.trim();
            if (!query) return;
            
            // Use OpenStreetMap Nominatim API for geocoding
            fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data && data.length > 0) {
                        // Get first result
                        const result = data[0];
                        const lat = parseFloat(result.lat);
                        const lng = parseFloat(result.lon);
                        
                        // Move map to location
                        map.setView([lat, lng], 12);
                        
                        // Add or move marker
                        if (marker) {
                            marker.setLatLng([lat, lng]);
                        } else {
                            marker = L.marker([lat, lng]).addTo(map);
                        }
                        
                        // Show location info
                        selectedLat = lat.toFixed(6);
                        selectedLng = lng.toFixed(6);
                        showLocationInfo(selectedLat, selectedLng);
                    } else {
                        alert('Location not found. Please try a different search term.');
                    }
                })
                .catch(error => {
                    console.error('Error searching for location:', error);
                    alert('Error searching for location. Please try again.');
                });
        }
    }
});

