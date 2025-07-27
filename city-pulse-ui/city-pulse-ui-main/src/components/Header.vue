<template>
  <header class="fixed top-0 left-0 right-0 bg-customBackground text-customText p-4 flex items-start justify-between z-30">
    <div class="flex flex-col items-start relative">
      <h1 class="text-xs pl-1 mb-0">City Pulse</h1>
      <div class="flex flex-col items-start">
        <h2 class="text-2xl font-bold mt-0">{{ displayPageTitle }}</h2>
        <button @click="toggleMenu('city')" class="mt-1 px-2 py-1 rounded-full bg-customText text-customBackground text-sm font-semibold">
          Bangalore
        </button>
      </div>
      <CityMenu v-if="activeMenu === 'city'" @close-menu="closeAllMenus" class="absolute top-full left-0 mt-2" />
    </div>
    <div class="flex items-center space-x-2 relative">
      <button @click="toggleMenu('profile')" class="w-10 h-10 rounded-full bg-black flex items-center justify-center focus:outline-none">
        <span class="material-icons text-xl">account_circle</span>
      </button>
      <button @click="toggleMenu('notifications')" class="w-10 h-10 rounded-full bg-black flex items-center justify-center focus:outline-none">
        <span class="material-icons text-xl">notifications</span>
      </button>
      <button @click="toggleMenu('navigation')" class="w-10 h-10 rounded-full bg-black flex items-center justify-center focus:outline-none">
        <span class="material-icons text-xl">more_vert</span>
      </button>
      
      <NavigationMenu v-if="activeMenu === 'navigation'" @close-menu="closeAllMenus" class="absolute top-full right-0 mt-2" />
      <ProfileMenu v-if="activeMenu === 'profile'" @close-menu="closeAllMenus" class="absolute top-full right-0 mt-2" />
      <NotificationsMenu v-if="activeMenu === 'notifications'" @close-menu="closeAllMenus" class="absolute top-full right-0 mt-2" />
    </div>
  </header>
</template>

<script setup>
import { ref, computed, defineProps } from 'vue'
import NavigationMenu from './NavigationMenu.vue'
import ProfileMenu from './ProfileMenu.vue'
import NotificationsMenu from './NotificationsMenu.vue'
import CityMenu from './CityMenu.vue'

const props = defineProps({
  pageTitle: {
    type: String,
    default: 'dashboard' // Default to 'dashboard' route name
  }
})

const displayTitles = {
  dashboard: 'Dashboard',
  map: 'Map',
  chat: 'Chat',
  report: 'Submit Report',
  profile: 'Profile' // Assuming a profile route will be added later
}

const displayPageTitle = computed(() => {
  return displayTitles[props.pageTitle] || props.pageTitle.charAt(0).toUpperCase() + props.pageTitle.slice(1)
})

const activeMenu = ref(null) // 'navigation', 'profile', 'notifications', 'city', or null

const activeMenuComponent = computed(() => {
  switch (activeMenu.value) {
    case 'navigation':
      return NavigationMenu
    case 'profile':
      return ProfileMenu
    case 'notifications':
      return NotificationsMenu
    case 'city':
      return CityMenu
    default:
      return null
  }
})

const toggleMenu = (menuName) => {
  if (activeMenu.value === menuName) {
    activeMenu.value = null // Close if already open
  } else {
    activeMenu.value = menuName // Open the clicked menu
  }
}

const closeAllMenus = () => {
  activeMenu.value = null
}

// Expose closeAllMenus to parent component (App.vue)
import { defineExpose } from 'vue'
defineExpose({ closeAllMenus })
</script>