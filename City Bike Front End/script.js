// Add weather functionality
async function fetchWeather(lat, lng) {
    const apiUrl = `http://127.0.0.1:5000/weather?lat=${lat}&lon=${lng}`;
    
    try {
        const response = await fetch(apiUrl);
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        const data = await response.json();
        console.log("API Response Data:", data);  // For debugging

        if (data.main && data.weather && data.weather.length > 0) {
            // Main weather information
            let temp = Math.round(data.main.temp);
            let description = data.weather[0].description;
            let weatherIcon = getWeatherIcon(data.weather[0].icon);
            
            // Detailed weather information
            let feelsLike = Math.round(data.main.feels_like);
            let humidity = data.main.humidity;
            let windSpeed = data.wind.speed;
            
            // Combine all information into a single display line
            document.getElementById("weather").innerHTML = 
                `<span class="weather-city">Dublin</span> ${weatherIcon} 
                <span class="weather-temp">${temp}°C</span> |
                <span class="weather-feels-like">Feels like: ${feelsLike}°C</span> |
                <span class="weather-humidity">Humidity: ${humidity}%</span> |
                <span class="weather-wind">Wind: ${windSpeed} m/s</span>`;
        
        } else {
            document.getElementById("weather").innerText = "⚠️ Weather unavailable";
        }
    } catch (error) {
        console.error("Weather fetch failed:", error);
        document.getElementById("weather").innerText = "⚠️ Weather unavailable";
    }
}

// Return the corresponding icon based on the weather code
function getWeatherIcon(iconCode) {
    const iconMap = {
        "01d": "☀️", "01n": "🌙", "02d": "⛅", "02n": "☁️", 
        "03d": "☁️", "03n": "☁️", "04d": "☁️", "04n": "☁️", 
        "09d": "🌧️", "09n": "🌧️", "10d": "🌦️", "10n": "🌧️", 
        "11d": "⛈️", "11n": "⛈️", "13d": "❄️", "13n": "❄️", 
        "50d": "🌫️", "50n": "🌫️"
    };
    return iconMap[iconCode] || "🌤️"; // Default icon
}

// Display weather information when clicking on the map
async function addWeatherClickListener(map) {
    google.maps.event.addListener(map, 'click', async (event) => {
        const lat = event.latLng.lat();
        const lng = event.latLng.lng();
        // Fetch and display the weather information for the clicked location
        await fetchWeather(lat, lng);
    });
}

// Initialize and add the map
async function initMap() {
    // The location of Dublin
    const position = { lat: 53.3498, lng: -6.2603 };
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 14,
        center: position,
        mapId: "ebb6cf6a252364a4",
        fullscreenControl: false,
        mapTypeControl: false,
        streetViewControl: false,
        zoomControl: false,
        disableDefaultUI: true,
    });


    // Add magnification buttons
    addMagnificationControls(map);

    // Fetch station info and availability
    await fetchStationInfo();
    await fetchAvailability();

    // Place markers on the map
    placeMarkers(map);

    const groupedStationsWithTotalsAndAverages = groupStations(stations);
    addGroupMarkers(map, groupedStationsWithTotalsAndAverages);
    groupMarkers.forEach(marker => marker.setMap(null)); // When the map is initialized, group markers should not be visible

    // Add click event to display weather information
    addWeatherClickListener(map);
}

// Fetch weather data when the page loads
document.addEventListener('DOMContentLoaded', () => {
    fetchWeather(53.3498, -6.2603);  // Default: display Dublin's weather
});


// Function to add magnification controls
function addMagnificationControls(map) {
    // Creating a container for both buttons
    const magControlDiv = document.createElement("div");
    magControlDiv.style.display = "flex";
    magControlDiv.style.flexDirection = "column"; 
    magControlDiv.style.gap = "10px"; 

    // Create the first magnification button
    const magControl = createMagControl(map);
    magControlDiv.appendChild(magControl);

    // Create the second magnification button
    const zoomMagControl = createZoomMagControl(map);
    magControlDiv.appendChild(zoomMagControl);

    // Adding the container to the map
    map.controls[google.maps.ControlPosition.RIGHT_BOTTOM].push(magControlDiv);
}

// Function to create the first magnification button (zoomed in)
function createMagControl(map) {
    const magButton = document.createElement("button");
    magButton.className = "magButton defMag";
    magButton.innerHTML = '<img src="Media/magnificationIn.png">';

    magButton.addEventListener("click", () => {
        map.setCenter({ lat: 53.345430, lng: -6.263867 }); // Reset map center to Dublin
        map.setZoom(15); // Reset zoom to default
        showMarkers(map); // Show station markers
        hideGroupMarkers(); // Hide group markers
    });

    return magButton;
}

// Function to create the second magnification button (zoomed out)
function createZoomMagControl(map) {
    const zoomMagButton = document.createElement("button");
    zoomMagButton.className = "magButton zoomMag";
    zoomMagButton.innerHTML = '<img src="Media/magnificationOut.png">';

    zoomMagButton.addEventListener("click", () => {
        map.setZoom(14); 
        map.setCenter({ lat: 53.345430, lng: -6.263867 });
        hideMarkers(); // Hide station markers
        showGroupMarkers(map); // Show group markers
    });

    return zoomMagButton;
}

// Function to hide group markers
function hideGroupMarkers() {
    groupMarkers.forEach(marker => marker.setMap(null));
}

// Function to show group markers
function showGroupMarkers(map) {
    groupMarkers.forEach(marker => marker.setMap(map));
}

// Making initMap globally accessible
window.initMap = initMap;

// Function to fetch station data
let stations = [];
async function fetchStationInfo() {
    try {
        const response = await fetch("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=eeb44b00e16a123704765d0077479e41fe503728");
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();

        stations = data.map(station => ({
            name: station.name,
            address: station.address,
            latitude: station.position.lat,
            longitude: station.position.lng,
            number: station.number
        }));
        
        console.log("Stations data:", stations);
    } catch (error) {
        console.error("Error fetching station data:", error);
    }
}

// Testing group markers
function groupStations(stations) {
    // Sorting by Lat and Long
    stations.sort((a, b) => {
        if (a.latitude === b.latitude) {
            return a.longitude - b.longitude;
        }
        return a.latitude - b.latitude;
    });

    // Grouping stations into arrays of 20 (I calculated 115 total stations so roughly 5 equal groups)
    const groupedStations = [];
    for (let i = 0; i < stations.length; i += 20) {
        const group = stations.slice(i, i + 20); // Get a group of 20 stations
        groupedStations.push(group);
    }

    // Calculating the average Lat and Long and also the total bikes available 
    const groupedStationsWithTotalsAndAverages = groupedStations.map((group, index) => {
        // Calculate total available_bikes
        const totalAvailableBikes = group.reduce((sum, station) => sum + station.available_bikes, 0);

        // Calculate average Lat and Long
        const totalLatitude = group.reduce((sum, station) => sum + station.latitude, 0);
        const totalLongitude = group.reduce((sum, station) => sum + station.longitude, 0);
        const averageLatitude = totalLatitude / group.length;
        const averageLongitude = totalLongitude / group.length;

        return {
            groupId: index + 1, // Unique ID for the group
            stations: group,
            totalAvailableBikes: totalAvailableBikes,
            averageLatitude: averageLatitude,
            averageLongitude: averageLongitude
        };
    });

    return groupedStationsWithTotalsAndAverages;
}

// Array to store group markers
let groupMarkers = [];

function addGroupMarkers(map, groupedStationsWithTotalsAndAverages) {
    groupedStationsWithTotalsAndAverages.forEach(group => {
        const groupMarker = new google.maps.Marker({
            position: { lat: group.averageLatitude, lng: group.averageLongitude },
            map: map,
            title: `Group ${group.groupId} - Total Bikes: ${group.totalAvailableBikes}`,
            label: {
                text: group.totalAvailableBikes.toString(),
                color: "#000000",
                fontWeight: "bold"
            },
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 20,
                fillColor: "white",
                fillOpacity: 1,
                strokeColor: "rgba(0, 121, 252, 0.897)",
                strokeWeight: 1,
            }
        });

        // Adding on click event for hiding group markers and showing station markers
        google.maps.event.addListener(groupMarker, 'click', () => {
            map.panTo({ lat: group.averageLatitude, lng: group.averageLongitude });
            map.setZoom(15);
            showMarkers(map); // Show station markers
            hideGroupMarkers(); // Hide group markers
        });

        groupMarkers.push(groupMarker); 
    });
}

// Function to fetch bike availability
async function fetchAvailability() {
    try {
        const response = await fetch("https://api.jcdecaux.com/vls/v1/stations?contract=dublin&apiKey=eeb44b00e16a123704765d0077479e41fe503728");
        if (!response.ok) throw new Error("Network response was not ok");
        const data = await response.json();

        data.forEach(availability => {
            const station = stations.find(station => station.number === availability.number);
            if (station) {
                station.available_bikes = availability.available_bikes;
                station.available_parking = availability.available_bike_stands;
            }
        });
        
        console.log("Stations data:", stations);
    } catch (error) {
        console.error("Error fetching station data:", error);
    }
}

// Array to store markers
let markers = [];

// Function to place markers
function placeMarkers(map) {
    for (const station of stations) {
        const position = { lat: station.latitude, lng: station.longitude };
        
        const circleMarker = new google.maps.Marker({
            map: map,
            position: position,
            icon: {
                path: google.maps.SymbolPath.CIRCLE,
                scale: 20, // Circle size
                fillColor: "white",
                fillOpacity: 1,
                strokeColor: "rgba(0, 121, 252, 0.897)",
                strokeWeight: 1,
            },
            zIndex: 1
        });
        
        const iconUrl = getBikeIcon(station.available_bikes);

        const bikeMarker = new google.maps.Marker({
            map: map,
            position: position,  
            icon: {
                url: iconUrl,  
                scaledSize: new google.maps.Size(25, 25),  // Set size of icon
                anchor: new google.maps.Point(14, 14)  // Center bottom alignment
            },
            zIndex: 2 // Put bike icon in the foreground
        });

        // Store markers in the array
        markers.push(circleMarker, bikeMarker);

        // Show availability when hovering over the station
        const infoWindow = new google.maps.InfoWindow({
            content: `<div class="info-box">
                <h3>${station.name} </h3>
                <div class="station-info">
                    <p>Station Nr. ${station.number} | ${station.address}</p>
                </div>
                <div class="availability">
                    <p>Total Bikes available: ${station.available_bikes}</br>
                    Available Parking stands:  ${station.available_parking}</p>
                </div>
            </div>`,
            disableAutoPan: true
        });

        // Add hover to show the info box
        bikeMarker.addListener('mouseover', () => infoWindow.open(map, bikeMarker));
        bikeMarker.addListener('mouseout', () => infoWindow.close());
        bikeMarker.addListener('click', () => {

            stationDetail(station); 
            infoWindow.close(); //remove the infobox once one station is clicked 
        
            map.panTo({ lat: station.latitude, lng: station.longitude });
        
        });
    }
}

// Function to hide markers
function hideMarkers() {
    markers.forEach(marker => marker.setMap(null)); // Hide station markers
    groupMarkers.forEach(marker => marker.setMap(null)); // Hide group markers
}

// Function to show markers
function showMarkers(map) {
    markers.forEach(marker => marker.setMap(map)); // Show station markers
    groupMarkers.forEach(marker => marker.setMap(map)); // Show group markers
}

// Function to display bike icon based on availability
function getBikeIcon(availableBikes) {
    if (availableBikes < 5) {
        return "Media/bikeRed.png";
    } else if (availableBikes >= 5 && availableBikes < 10) {
        return "Media/bikeOrange.png";
    } else {
        return "Media/bikeGreen.png";
    }
}

// Function for station detail when clicking a station (open sidebar)
function stationDetail(station) {
    let stationSidebar = document.getElementById("station-detail");
    // Create sidebar if it doesn't exist
    if (!stationSidebar) {
        stationSidebar = document.createElement("div");
        stationSidebar.id = "station-detail";
        document.body.appendChild(stationSidebar);
    }

    stationSidebar.innerHTML = `
        <h2>
            ${station.name}
            <img src="Media/starWhite.png" alt="favorise" class="favorite-button-sidebar"/>
        </h2>
        <p>Station Nr. ${station.number}</p>
        <p> Total bikes available: ${station.available_bikes}</br>
            Available Parking stands:  ${station.available_parking}</p>
    `;
    stationSidebar.style.display = 'block';

    const favoriteButton = document.querySelector('.favorite-button-sidebar');
    // Add click event directly to the button
    favoriteButton.addEventListener('click', () => favoriteStation(station, favoriteButton));


    // Adding a close button
    const close_button = document.createElement("button");
    close_button.classList.add("close-button");
    close_button.innerHTML = "&times;";
    close_button.onclick = () => {
        stationSidebar.style.display = 'none';
    };

    // Adding the close button to the sidebar
    stationSidebar.appendChild(close_button);
}

const favorites = [];

// Function to change favorite button to starFilled.png and add station to a list 
function favoriteStation(station, buttonElement){
    if (!favorites.some(fav => fav.number === station.number)) {
        favorites.push(station);
        buttonElement.src = "Media/starFilled.png"; // Change to filled star
    } else {
        const index = favorites.findIndex(fav => fav.number === station.number);
        favorites.splice(index, 1);
        buttonElement.src = "Media/starWhite.png"; // Change back to unfilled
    }
}

// display list once menu option is clicked
window.addEventListener("DOMContentLoaded", () => {
document.getElementById("menu-bar").addEventListener("click", () =>{
    let favoriteSidebar = document.getElementById("favorite-list");

    // If it doesn't exist, create it
    if (!favoriteSidebar) {
        favoriteSidebar = document.createElement("div");
        favoriteSidebar.id = "favorite-list";
        document.body.appendChild(favoriteSidebar);
    }

    // Toggle visibility
    favoriteSidebar.style.display = 
        favoriteSidebar.style.display === "none" || favoriteSidebar.style.display === ""
        ? "block"
        : "none";

    // Populate the list
    favoriteSidebar.innerHTML = `<h2>Favorite Stations</h2>`;

    if (favorites.length === 0) {
        favoriteSidebar.innerHTML += `<p>No favorite Stations added</p>`;
    } else {
        favorites.forEach(station => {
            favoriteSidebar.innerHTML += `
            <div class="favorite-item">
            <p>${station.name} | ${station.available_bikes} Bikes </p>
            </div>`;
        });
    }
});
});