<template>
  <div class="absolute top-full right-0 mt-2 w-48 bg-black rounded-md shadow-lg py-1 z-50">
    <router-link to="/profile" @click="closeMenu" class="block px-4 py-2 text-sm text-customText hover:bg-gray-700">View Profile</router-link>
    <a href="#" @click.prevent="handleSignOut" class="block px-4 py-2 text-sm text-customText hover:bg-gray-700">
      Log Out
    </a>
    <a class="block px-4 py-2 text-sm text-gray-500 cursor-not-allowed">My Subscription (Coming soon...)</a>
    <router-link to="/help" @click="closeMenu" class="block px-4 py-2 text-sm text-customText hover:bg-gray-700">Help</router-link>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const emit = defineEmits(['close-menu'])
const router = useRouter()
const authStore = useAuthStore()

const handleSignOut = async () => {
  await authStore.signOut()
  emit('close-menu') // Close the menu
  router.push('/auth') // Redirect to login page
}

const closeMenu = () => {
  emit('close-menu')
}
</script>
