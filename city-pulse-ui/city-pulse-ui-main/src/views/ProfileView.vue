<template>
  <div class="flex flex-col h-full p-4">
    <template v-if="isLoading">
      <div class="flex flex-col items-center justify-center flex-grow">
        <LoadingSpinner />
        <p class="mt-4 text-customText">Loading profile...</p>
      </div>
    </template>
    <template v-else-if="error">
      <div class="flex flex-col items-center justify-center flex-grow">
        <ErrorMessage :message="error" />
      </div>
    </template>
    <template v-else-if="profileData">
      <h1 class="text-3xl font-bold mb-6">User Profile</h1>

      <div class="bg-black p-6 rounded-lg shadow-lg mb-4">
        <div class="mb-4">
          <p class="text-gray-400 text-sm">Email:</p>
          <p class="text-customText text-lg font-semibold">{{ profileData.email }}</p>
        </div>
        <div class="mb-4">
          <p class="text-gray-400 text-sm">Name:</p>
          <p class="text-customText text-lg font-semibold">{{ profileData.name || 'N/A' }}</p>
        </div>
        <div class="mb-4">
          <p class="text-gray-400 text-sm">Date of Birth:</p>
          <p class="text-customText text-lg font-semibold">{{ profileData.dob || 'N/A' }}</p>
        </div>
        <div>
          <p class="text-gray-400 text-sm">Interests:</p>
          <div class="flex flex-wrap gap-2 mt-2">
            <span v-for="interest in profileData.interests" :key="interest"
                  class="bg-gray-700 text-customText px-3 py-1 rounded-full text-sm">
              {{ interest }}
            </span>
            <span v-if="!profileData.interests || profileData.interests.length === 0" class="text-gray-500 text-sm">None selected</span>
          </div>
        </div>
        <div class="mt-4">
          <p class="text-gray-400 text-sm">Last Known Location:</p>
          <p v-if="profileData.lastKnownLocation" class="text-customText text-lg font-semibold">
            Lat: {{ profileData.lastKnownLocation.latitude?.toFixed(4) }}, Lng: {{ profileData.lastKnownLocation.longitude?.toFixed(4) }}
            <br>
            <span class="text-gray-500 text-sm">({{ formatTimestamp(profileData.lastKnownLocation.timestamp) }})</span>
          </p>
          <p v-else class="text-gray-500 text-sm">Location data not available.</p>
        </div>
      </div>
    </template>
    <template v-else>
      <div class="flex flex-col items-center justify-center flex-grow">
        <p class="text-customText">No profile data found.</p>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import { doc, getDoc } from 'firebase/firestore'
import { db } from '../firebase'
import LoadingSpinner from '../components/LoadingSpinner.vue'
import ErrorMessage from '../components/ErrorMessage.vue'

const authStore = useAuthStore()
const profileData = ref(null)
const isLoading = ref(true)
const error = ref(null)

const formatTimestamp = (timestamp) => {
  if (!timestamp) return 'N/A';
  const date = new Date(timestamp);
  return date.toLocaleString();
};

onMounted(async () => {
  if (!authStore.user) {
    error.value = 'User not logged in.'
    isLoading.value = false
    return
  }

  try {
    const userDocRef = doc(db, 'city-pulse-ui-users', authStore.user.uid)
    const userDocSnap = await getDoc(userDocRef)

    if (userDocSnap.exists()) {
      profileData.value = userDocSnap.data()
    } else {
      error.value = 'No profile data found for this user.'
    }
  } catch (e) {
    console.error('Error fetching profile data:', e)
    error.value = 'Failed to load profile data.'
  } finally {
    isLoading.value = false
  }
})
</script>

<style scoped>
/* Add any specific styles for ProfileView if needed */
</style>
