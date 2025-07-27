<template>
  <div class="absolute top-full left-0 mt-2 w-48 bg-black rounded-md shadow-lg py-1 z-50">
    <router-link to="/" @click="closeMenu" class="block px-4 py-2 text-sm text-customText hover:bg-gray-700">Dashboard</router-link>
    <router-link to="/map" @click="closeMenu" class="block px-4 py-2 text-sm text-customText hover:bg-gray-700">Map</router-link>
    <router-link to="/chat" @click="closeMenu" class="block px-4 py-2 text-sm text-customText hover:bg-gray-700">Chat</router-link>
    <router-link to="/report" @click="closeMenu" class="block px-4 py-2 text-sm text-customText hover:bg-gray-700">Submit Report</router-link>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue'

const emit = defineEmits(['close-menu'])

const closeMenu = () => {
  emit('close-menu')
}
</script>
