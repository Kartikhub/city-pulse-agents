<template>
  <div class="flex flex-col flex-grow p-4 overflow-y-auto">
    <template v-if="isLoading">
      <div class="flex flex-col items-center justify-center flex-grow">
        <LoadingSpinner />
        <p class="mt-4 text-customText">Loading updates...</p>
      </div>
    </template>
    <template v-else>
      <div class="p-4 pt-4">
        <h2 class="text-2xl font-bold mb-4">Your Updates</h2>
        <ExpandableList v-model:isExpanded="isUpdatesExpanded">
          <li v-for="event in events" :key="event.id" class="mb-1">
            <span class="font-semibold">{{ event.type }}</span>: {{ event.description }} ({{ event.location }})
          </li>
        </ExpandableList>
      </div>
      <div ref="mapContainer" class="w-full bg-green-500 flex items-center justify-center text-black font-bold rounded-lg mb-4 h-[40vh] flex-shrink-0"></div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import ExpandableList from '../components/ExpandableList.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import { useEventsStore } from '../stores/events'
import { useChatStore } from '../stores/chat'
import { useAuthStore } from '../stores/auth'
import { getInitialEvents } from '../services/ConciergeAgentAPI'
import { storeToRefs } from 'pinia'
import { loadGoogleMaps, initializeMap } from '../utils/mapLoader'

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

const isLoading = ref(true) // Initial state is loading
const isUpdatesExpanded = ref(false)
const eventsStore = useEventsStore()
const { events } = storeToRefs(eventsStore) // Ensure reactivity
const router = useRouter()
const chatStore = useChatStore()
const authStore = useAuthStore()

const mapContainer = ref(null)

onMounted(async () => {
  console.log('DashboardView: onMounted fired.')
  console.log('DashboardView: Events in store before fetch:', eventsStore.events.length)
  
  isLoading.value = true // Set loading to true
  eventsStore.clearEvents() // Clear existing events
  const initialEvents = await getInitialEvents()
  console.log('DashboardView: Fetched initial events:', initialEvents.length)
  eventsStore.setEvents(initialEvents) // Use setEvents to replace the array reactively
  console.log('DashboardView: Events in store after fetch:', eventsStore.events.length)
  isLoading.value = false // Set loading to false after fetch

  // Initialize Google Map
  try {
    await loadGoogleMaps(import.meta.env.VITE_GOOGLE_MAPS_API_KEY);
    if (mapContainer.value) {
      let mapCenter = { lat: 12.9716, lng: 77.5946 }; // Default to Bangalore
      let mapBounds = { north: 13.15, south: 12.75, east: 77.85, west: 77.35 };
      
      if (authStore.user && authStore.user.lastKnownLocation) {
        const userLat = authStore.user.lastKnownLocation.latitude;
        const userLng = authStore.user.lastKnownLocation.longitude;
        mapCenter = { lat: userLat, lng: userLng };
        mapBounds = getBoundsForRadiusKm(userLat, userLng, 5); // 5km radius
      }

      const mapOptions = {
        center: mapCenter,
        zoom: 14, // Zoom level for a 5km radius
        minZoom: 10, // Allow zooming out to see the whole city
        restriction: {
          latLngBounds: { north: 13.15, south: 12.75, east: 77.85, west: 77.35 }, // Full Bangalore bounds
        },
      };
      const map = initializeMap(mapContainer.value, mapOptions);
      const infoWindow = new google.maps.InfoWindow();

      // Add markers for each event
      events.value.forEach(event => {
        if (event.coords) {
          const marker = new google.maps.Marker({
            position: event.coords,
            map: map,
            title: event.name || event.type,
          });

          marker.addListener('click', () => {
            const content = `
              <div style="color: black;">
                <h3 style="font-weight: bold;">${event.name || event.type}</h3>
                <p>${event.description}</p>
                <button id="know-more-btn" style="background-color: #4285F4; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer;">Know More</button>
              </div>
            `;
            infoWindow.setContent(content);
            infoWindow.open(map, marker);

            google.maps.event.addListenerOnce(infoWindow, 'domready', () => {
              document.getElementById('know-more-btn').addEventListener('click', () => {
                chatStore.setInitialMessage(`Tell me more about ${event.name || event.type} at ${event.location}`);
                router.push({ name: 'chat' });
              });
            });
          });
        }
      });
    }
  } catch (error) {
    console.error("Error loading Google Maps in DashboardView:", error);
  }
})
</script>