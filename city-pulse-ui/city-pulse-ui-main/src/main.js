import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './index.css'
import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'
import { loadGoogleMaps } from './utils/mapLoader'

const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

// Initialize auth store
const authStore = useAuthStore()
authStore.initAuth()

// Load Google Maps API
loadGoogleMaps(import.meta.env.VITE_GOOGLE_MAPS_API_KEY)
  .catch(error => {
    console.error("Failed to load Google Maps API:", error);
  });

app.mount('#app')