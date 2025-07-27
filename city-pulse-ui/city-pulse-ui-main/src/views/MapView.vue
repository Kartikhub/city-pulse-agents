<template>
  <div class="relative flex flex-col h-full">
    <div ref="mapContainer" class="flex-grow bg-gray-700 flex items-center justify-center text-customText text-2xl"></div>

    <div class="absolute bottom-0 left-0 right-0 z-10">
      <div v-if="selectedOverlay === 'Traffic'" class="bg-black bg-opacity-50 p-2 flex items-center justify-center space-x-4">
        <label for="time-slider" class="text-white font-medium">Time:</label>
        <input id="time-slider" type="range" min="0" max="24" step="1" v-model.number="timeSliderValue" class="w-64">
        <span class="text-white w-24 text-center">{{ formattedTime }}</span>
      </div>

      <div class="flex-shrink-0 bg-transparent p-4 overflow-x-auto whitespace-nowrap flex justify-center">
        <button @click="handleButtonClick('Traffic')"
                @mousedown="startLongPressTimer($event, 'Traffic Overlay')" @mouseup="clearLongPressTimer" @mouseleave="clearLongPressTimer"
                @touchstart="startLongPressTimer($event, 'Traffic Overlay')" @touchend="clearLongPressTimer"
                :class="{ 'bg-blue-500': selectedOverlay === 'Traffic', 'bg-black': selectedOverlay !== 'Traffic' }"
                class="text-customText w-12 h-12 rounded-full mr-2 flex items-center justify-center">
          <span class="material-icons">traffic</span>
        </button>
        <button @click="handleButtonClick('Incidents')"
                @mousedown="startLongPressTimer($event, 'Incidents Overlay')" @mouseup="clearLongPressTimer" @mouseleave="clearLongPressTimer"
                @touchstart="startLongPressTimer($event, 'Incidents Overlay')" @touchend="clearLongPressTimer"
                :class="{ 'bg-blue-500': selectedOverlay === 'Incidents', 'bg-black': selectedOveay !== 'Incidents' }"
                class="text-customText w-12 h-12 rounded-full mr-2 flex items-center justify-center">
          <span class="material-icons">warning</span>
        </button>
        <button @click="handleButtonClick('Events')"
                @mousedown="startLongPressTimer($event, 'Events Overlay')" @mouseup="clearLongPressTimer" @mouseleave="clearLongPressTimer"
                @touchstart="startLongPressTimer($event, 'Events Overlay')" @touchend="clearLongPressTimer"
                :class="{ 'bg-blue-500': selectedOverlay === 'Events', 'bg-black': selectedOverlay !== 'Events' }"
                class="text-customText w-12 h-12 rounded-full mr-2 flex items-center justify-center">
          <span class="material-icons">event</span>
        </button>
        <button @click="handleButtonClick('Food & Drink')"
                @mousedown="startLongPressTimer($event, 'Food & Drink Overlay')" @mouseup="clearLongPressTimer" @mouseleave="clearLongPressTimer"
                @touchstart="startLongPressTimer($event, 'Food & Drink Overlay')" @touchend="clearLongPressTimer"
                :class="{ 'bg-blue-500': selectedOverlay === 'Food & Drink', 'bg-black': selectedOverlay !== 'Food & Drink' }"
                class="text-customText w-12 h-12 rounded-full mr-2 flex items-center justify-center">
          <span class="material-icons">restaurant</span>
        </button>
        <button @click="handleButtonClick('Weather')"
                @mousedown="startLongPressTimer($event, 'Weather Overlay')" @mouseup="clearLongPressTimer" @mouseleave="clearLongPressTimer"
                @touchstart="startLongPressTimer($event, 'Weather Overlay')" @touchend="clearLongPressTimer"
                :class="{ 'bg-blue-500': selectedOverlay === 'Weather', 'bg-black': selectedOverlay !== 'Weather' }"
                class="text-customText w-12 h-12 rounded-full mr-2 flex items-center justify-center">
          <span class="material-icons">cloud</span>
        </button>
      </div>
    </div>

    <div v-if="showSnackbar"
         :style="{ left: snackbarX, bottom: snackbarY }"
         class="absolute bg-black bg-opacity-60 text-customText px-4 py-2 rounded-md z-20 transition-opacity duration-300 transform -translate-x-1/2">
      {{ snackbarText }}
    </div>

    <div v-if="selectedOverlay === 'Weather'" class="absolute right-4 top-1/2 transform -translate-y-1/2 flex flex-col space-y-2 z-10">
      <div class="flex flex-col rounded-full bg-gray-800 p-1 space-y-1">
        <button @click="handleWeatherSubOverlayClick('Temperature')"
                :class="{ 'bg-blue-500 text-white': weatherSubOverlay === 'Temperature', 'text-gray-400': weatherSubOverlay !== 'Temperature' }"
                class="w-12 h-12 rounded-full text-sm font-medium transition-colors duration-200 flex items-center justify-center">
          <span class="material-icons">thermostat</span>
        </button>
        <button @click="handleWeatherSubOverlayClick('AQI')"
                :class="{ 'bg-blue-500 text-white': weatherSubOverlay === 'AQI', 'text-gray-400': weatherSubOverlay !== 'AQI' }"
                class="w-12 h-12 rounded-full text-sm font-medium transition-colors duration-200 flex items-center justify-center">
          <span class="material-icons">air</span>
        </button>
        <button @click="handleWeatherSubOverlayClick('Clouds')"
                :class="{ 'bg-blue-500 text-white': weatherSubOverlay === 'Clouds', 'text-gray-400': weatherSubOverlay !== 'Clouds' }"
                class="w-12 h-12 rounded-full text-sm font-medium transition-colors duration-200 flex items-center justify-center">
          <span class="material-icons">cloudy_snowing</span>
        </button>
      </div>
    </div>

    <div v-if="showLegend" class="legend-container">
      <h4 class="legend-title">{{ legendTitle }}</h4>
      <div class="legend-gradient" :style="{ background: legendGradient }"></div>
      <div class="legend-labels">
        <span>{{ legendMinLabel }}</span>
        <span>{{ legendMaxLabel }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useEventsStore } from '../stores/events'
import { useChatStore } from '../stores/chat'
import { useAuthStore } from '../stores/auth'
import { getInitialEvents, getTrafficPredictions, getIncidents, getWeatherData, getAQIData } from '../services/ConciergeAgentAPI'
import { storeToRefs } from 'pinia'
import { loadGoogleMaps, initializeMap } from '../utils/mapLoader'

// Import the new icons
import floodIcon from '../assets/flood.png';
import potholeIcon from '../assets/pothole.png';
import trafficAccidentIcon from '../assets/traffic.png';

const selectedOverlay = ref(null)
const weatherSubOverlay = ref(null)

const snackbarText = ref('')
const showSnackbar = ref(false)
const snackbarX = ref('0px')
const snackbarY = ref('0px')
const timeSliderValue = ref(0)
let map = null;
let heatmap = null;
let trafficLayer = null;

const eventMarkers = ref([]);
const incidentMarkers = ref([]);
let longPressTimer = null
let snackbarVisibleTimer = null
let isLongPressing = false

// --- State for Legend ---
const showLegend = ref(false);
const legendTitle = ref('');
const legendGradient = ref('');
const legendMinLabel = ref('');
const legendMaxLabel = ref('');

const authStore = useAuthStore()
const eventsStore = useEventsStore()
const { events } = storeToRefs(eventsStore)
const router = useRouter()
const chatStore = useChatStore()
const mapContainer = ref(null)

// --- HELPER FUNCTIONS ---
const formattedTime = computed(() => {
  if (timeSliderValue.value === 0) return 'Now';
  const minutes = timeSliderValue.value * 15;
  const hours = Math.floor(minutes / 60);
  const mins = minutes % 60;
  let timeString = '+';
  if (hours > 0) timeString += `${hours}h `;
  if (mins > 0) timeString += `${mins}m`;
  return timeString.trim();
});

const getIconForIncidentType = (type) => {
  const common = { scaledSize: new google.maps.Size(32, 32), anchor: new google.maps.Point(16, 16) };
  switch (type) {
    case 'Traffic Accident': return { ...common, url: trafficAccidentIcon };
    case 'Pothole': return { ...common, url: potholeIcon };
    case 'Flooding': return { ...common, url: floodIcon };
    default: return { path: google.maps.SymbolPath.CIRCLE, fillColor: '#FFFFFF', fillOpacity: 1, strokeWeight: 1, scale: 7 };
  }
};

const createMarker = (item, infoWindow, icon = null) => {
  if (!item.coords) return null;
  const marker = new google.maps.Marker({ position: item.coords, map: map, title: item.name || item.type, icon: icon });
  marker.addListener('click', () => {
    const content = `<div style="color: black;"><h3 style="font-weight: bold;">${item.name || item.type}</h3><p>${item.description}</p><button id="know-more-btn" style="background-color: #4285F4; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Know More</button></div>`;
    infoWindow.setContent(content);
    infoWindow.open(map, marker);
    google.maps.event.addListenerOnce(infoWindow, 'domready', () => {
      document.getElementById('know-more-btn').addEventListener('click', () => {
        chatStore.setInitialMessage(`Tell me more about ${item.name || item.type} at ${item.location}`);
        router.push({ name: 'chat' });
      });
    });
  });
  return marker;
};

const clearMarkers = (markers) => {
    markers.value.forEach(marker => marker.setMap(null));
    markers.value.length = 0;
};

const updateMapLayers = async () => {
  const overlay = selectedOverlay.value;
  const timeValue = timeSliderValue.value;
  
  if (overlay === null) {
    eventMarkers.value.forEach(m => m.setVisible(true));
    trafficLayer = new google.maps.TrafficLayer({ map });
    const incidents = await getIncidents();
    const infoWindow = new google.maps.InfoWindow();
    incidents.forEach(incident => {
      const marker = createMarker(incident, infoWindow, getIconForIncidentType(incident.type));
      if (marker) incidentMarkers.value.push(marker);
    });
    return;
  }
  
  if (overlay === 'Traffic') {
    if (timeValue === 0) {
      trafficLayer = new google.maps.TrafficLayer({ map });
    } else {
      const predictions = await getTrafficPredictions(timeValue);
      const heatmapData = new google.maps.MVCArray(predictions.map(p => ({ location: new google.maps.LatLng(p.location.lat, p.location.lng), weight: p.weight })));
      heatmap = new google.maps.visualization.HeatmapLayer({ data: heatmapData, map, radius: 60, opacity: 0.9, maxIntensity: 1, gradient: ['rgba(0, 255, 255, 0)', 'rgba(0, 255, 255, 1)', 'rgba(0, 191, 255, 1)', 'rgba(0, 127, 255, 1)', 'rgba(0, 63, 255, 1)', 'rgba(0, 0, 255, 1)', 'rgba(0, 0, 223, 1)', 'rgba(0, 0, 191, 1)', 'rgba(0, 0, 159, 1)', 'rgba(0, 0, 127, 1)', 'rgba(63, 0, 91, 1)', 'rgba(127, 0, 63, 1)', 'rgba(191, 0, 31, 1)', 'rgba(255, 0, 0, 1)'] });
    }
    return;
  }
  
  if (overlay === 'Incidents') {
    const incidents = await getIncidents();
    const infoWindow = new google.maps.InfoWindow();
    incidents.forEach(incident => {
      const marker = createMarker(incident, infoWindow, getIconForIncidentType(incident.type));
      if (marker) incidentMarkers.value.push(marker);
    });
    return;
  }

  if (overlay === 'Events') {
    eventMarkers.value.forEach(m => m.setVisible(true));
    return;
  }
  
  if (overlay === 'Weather') {
    const weatherData = await getWeatherData();
    const aqiData = await getAQIData();
    const initialRadius = { 10: 120, 11: 70, 12: 50, 13: 30, 14: 20 }[map.getZoom()] || 15;

    if (weatherSubOverlay.value === 'Temperature') {
      const temps = weatherData.map(p => p.temperature);
      const minTemp = Math.min(...temps);
      const maxTemp = Math.max(...temps);
      const tempRange = maxTemp - minTemp;
      const heatmapData = new google.maps.MVCArray(weatherData.map(p => ({ location: new google.maps.LatLng(p.lat, p.lng), weight: tempRange > 0 ? (p.temperature - minTemp) / tempRange : 0.5 })));
      const gradient = ['rgba(0, 0, 255, 0)', 'rgba(0, 0, 255, 1)', 'rgba(0, 255, 255, 1)', 'rgba(0, 255, 0, 1)', 'rgba(255, 255, 0, 1)', 'rgba(255, 0, 0, 1)'];
      
      heatmap = new google.maps.visualization.HeatmapLayer({ data: heatmapData, map, radius: initialRadius, dissipating: false, opacity: 0.7, maxIntensity: 1.0, gradient });
      
      showLegend.value = true;
      legendTitle.value = 'Temperature (°C)';
      legendMinLabel.value = minTemp;
      legendMaxLabel.value = maxTemp;
      legendGradient.value = `linear-gradient(to right, ${gradient.join(', ')})`;

    } else if (weatherSubOverlay.value === 'AQI') {
      const aqiHeatmapData = new google.maps.MVCArray(aqiData.map(p => ({ location: new google.maps.LatLng(p.lat, p.lng), weight: p.aqiValue })));
      const gradient = ['rgba(0, 255, 0, 0)', 'rgba(0, 255, 0, 1)', 'rgba(255, 255, 0, 1)', 'rgba(255, 165, 0, 1)', 'rgba(255, 0, 0, 1)', 'rgba(128, 0, 128, 1)'];
      
      heatmap = new google.maps.visualization.HeatmapLayer({ data: aqiHeatmapData, map, radius: initialRadius, dissipating: false, opacity: 0.7, maxIntensity: 200, gradient });

      showLegend.value = true;
      legendTitle.value = 'Air Quality Index (AQI)';
      legendMinLabel.value = 'Good';
      legendMaxLabel.value = 'Hazardous';
      legendGradient.value = `linear-gradient(to right, ${gradient.join(', ')})`;

    } else if (weatherSubOverlay.value === 'Clouds') {
      const cloudData = weatherData.map(item => ({ location: new google.maps.LatLng(item.lat, item.lng), weight: item.cloudCover }));
      const gradient = ['rgba(200, 200, 200, 0)', 'rgba(200, 200, 200, 1)'];
      
      heatmap = new google.maps.visualization.HeatmapLayer({ data: cloudData, map, radius: initialRadius, dissipating: false, opacity: 0.7, maxIntensity: 100, gradient });

      showLegend.value = true;
      legendTitle.value = 'Cloud Cover (%)';
      legendMinLabel.value = '0%';
      legendMaxLabel.value = '100%';
      legendGradient.value = `linear-gradient(to right, ${gradient.join(', ')})`;
    }
    return;
  }
};

const getBoundsForRadiusKm = (lat, lng, radiusKm) => {
  const R = 6371; // Earth's radius in kilometers
  const latRad = (lat * Math.PI) / 180;
  const degLatKm = 110.574; // 1 degree of latitude in km
  const degLngKm = 111.32 * Math.cos(latRad); // 1 degree of longitude in km

  const deltaLat = radiusKm / degLatKm;
  const deltaLng = radiusKm / degLngKm;

  const north = lat + deltaLat;
  const south = lat - deltaLat;
  const east = lng + deltaLng;
  const west = lng - deltaLng;

  return {
    north: Math.min(90, north),
    south: Math.max(-90, south),
    east: Math.min(180, east),
    west: Math.max(-180, west),
  };
};

const getUserLocationAndInitializeMap = async () => {
  return new Promise((resolve) => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const userLat = position.coords.latitude;
          const userLng = position.coords.longitude;
          const bounds = getBoundsForRadiusKm(userLat, userLng, 5); // 5km radius
          resolve({ center: { lat: userLat, lng: userLng }, bounds: bounds });
        },
        (error) => {
          console.error("Error getting user location:", error);
          // Fallback to Bangalore if geolocation fails
          resolve({ center: { lat: 12.9716, lng: 77.5946 }, bounds: { north: 13.15, south: 12.75, east: 77.85, west: 77.35 } });
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
      );
    } else {
      console.warn("Geolocation is not supported by this browser.");
      // Fallback to Bangalore if geolocation not supported
      resolve({ center: { lat: 12.9716, lng: 77.5946 }, bounds: { north: 13.15, south: 12.75, east: 77.85, west: 77.35 } });
    }
  });
};

const reloadMap = async () => {
  if (!mapContainer.value) return;

  if (map) {
    if (heatmap) heatmap.setMap(null);
    if (trafficLayer) trafficLayer.setMap(null);
    clearMarkers(incidentMarkers);
    clearMarkers(eventMarkers);
  }
  showLegend.value = false;
  mapContainer.value.innerHTML = '';

  try {
    await loadGoogleMaps(import.meta.env.VITE_Maps_API_KEY);

    const { center, bounds } = await getUserLocationAndInitializeMap();

    const mapOptions = {
      center: center,
      zoom: 14, // A good zoom level for a 5km radius
      minZoom: 10, // Allow zooming out to see the whole city
      restriction: {
        latLngBounds: { north: 13.15, south: 12.75, east: 77.85, west: 77.35 }, // Full Bangalore bounds
      },
    };
    map = initializeMap(mapContainer.value, mapOptions);

    map.addListener('zoom_changed', () => {
      if (!heatmap) return;
      const zoom = map.getZoom();
      const radiusMap = { 10: 120, 11: 70, 12: 50, 13: 30, 14: 20 };
      const newRadius = radiusMap[zoom] || 15;
      heatmap.set('radius', newRadius);
    });

    const infoWindow = new google.maps.InfoWindow();
    events.value.forEach((event) => {
      const marker = createMarker(event, infoWindow);
      if (marker) eventMarkers.value.push(marker);
    });

    eventMarkers.value.forEach((m) => m.setVisible(false));

    await updateMapLayers();
  } catch (error) {
    console.error("Error during map reload:", error);
  }
};

let debounceTimer = null;

watch([selectedOverlay, timeSliderValue, weatherSubOverlay], () => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(reloadMap, 100);
});

onMounted(async () => {
  eventsStore.clearEvents();
  const initialEvents = await getInitialEvents();
  eventsStore.setEvents(initialEvents);
  reloadMap();
});

onUnmounted(() => {
});

// --- UI HANDLERS ---
const handleButtonClick = (overlayName) => {
  if (isLongPressing) { isLongPressing = false; return; }
  selectedOverlay.value = selectedOverlay.value === overlayName ? null : overlayName;
  if (overlayName !== 'Traffic') { timeSliderValue.value = 0; }
  if (overlayName !== 'Weather') { weatherSubOverlay.value = null; } 
  else if (overlayName === 'Weather' && weatherSubOverlay.value === null) { weatherSubOverlay.value = 'Temperature'; }
  hideSnackbar();
};

const startLongPressTimer = (event, text) => {
  snackbarText.value = text;
  const buttonRect = event.currentTarget.getBoundingClientRect();
  snackbarX.value = `${buttonRect.left + buttonRect.width / 2}px`;
  snackbarY.value = `${buttonRect.height + 20}px`;
  longPressTimer = setTimeout(() => {
    showSnackbar.value = true;
    isLongPressing = true;
    snackbarVisibleTimer = setTimeout(hideSnackbar, 1500);
  }, 375);
};

const clearLongPressTimer = () => { clearTimeout(longPressTimer); };
const hideSnackbar = () => { clearTimeout(longPressTimer); clearTimeout(snackbarVisibleTimer); showSnackbar.value = false; snackbarText.value = ''; isLongPressing = false; };

const handleWeatherSubOverlayClick = (subOverlayType) => {
  weatherSubOverlay.value = subOverlayType;
  hideSnackbar();
};
</script>

<style scoped>
.legend-container {
  position: absolute;
  bottom: 8rem; /* Adjust to sit above the bottom controls */
  left: 1rem;
  background-color: rgba(31, 41, 55, 0.8); /* bg-gray-800 with opacity */
  padding: 0.75rem;
  border-radius: 0.5rem;
  z-index: 10;
  color: white;
  width: 200px;
  backdrop-filter: blur(4px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.legend-title {
  margin: 0 0 0.5rem 0;
  font-weight: 600;
  font-size: 0.875rem;
  text-align: center;
}

.legend-gradient {
  height: 1.25rem;
  width: 100%;
  border-radius: 0.25rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
}

.legend-labels {
  display: flex;
  justify-content: space-between;
  margin-top: 0.25rem;
  font-size: 0.75rem;
}
</style>