<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-customBackground text-customText p-4">
    <h1 class="text-3xl font-bold mb-8">Choose Your Interests</h1>

    <div class="flex flex-wrap justify-center gap-4 mb-8">
      <button v-for="interest in availableInterests" :key="interest"
              @click="toggleInterest(interest)"
              :class="{ 'bg-blue-600': selectedInterests.includes(interest), 'bg-gray-700': !selectedInterests.includes(interest) }"
              class="px-6 py-3 rounded-full text-lg font-semibold focus:outline-none hover:bg-gray-600 transition-colors duration-200">
        {{ interest }}
      </button>
    </div>

    <button @click="continueToApp" class="bg-green-500 hover:bg-green-700 text-white font-bold py-3 px-8 rounded-full focus:outline-none focus:shadow-outline">
      Continue to App
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const availableInterests = ref([
  'Traffic',
  'Events',
  'Food & Drink',
  'Nature & Outdoors',
  'Public Transport',
  'Safety',
  'Attractions',
  'Shopping'
])

const selectedInterests = ref([])

const toggleInterest = (interest) => {
  const index = selectedInterests.value.indexOf(interest)
  if (index > -1) {
    selectedInterests.value.splice(index, 1) // Remove if already selected
  } else {
    selectedInterests.value.push(interest) // Add if not selected
  }
}

const continueToApp = async () => {
  console.log('Selected Interests:', selectedInterests.value)
  await authStore.setInterestsSelected(true, selectedInterests.value)
  router.push('/') // Redirect to dashboard
}
</script>

<style scoped>
/* Add any specific styles for InterestsView if needed */
</style>