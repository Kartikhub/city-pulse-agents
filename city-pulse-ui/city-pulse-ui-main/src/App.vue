<template>
  <div class="min-h-screen bg-customBackground text-customText flex flex-col" @click="handleGlobalClick">
    <Header v-if="$route.name !== 'auth'" ref="headerRef" :pageTitle="$route.name" />
    <main class="flex-grow pt-24 flex flex-col">
      <router-view class="flex-grow" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRoute } from 'vue-router'
import Header from './components/Header.vue'

const headerRef = ref(null)
const route = useRoute()

const handleGlobalClick = (event) => {
  // Check if the click originated from within the header or any of its children
  if (headerRef.value && !headerRef.value.$el.contains(event.target)) {
    // If the click is outside the header, close all menus
    headerRef.value.closeAllMenus()
  }
}
</script>

<style>
/* Global styles can go here */
body {
  margin: 0;
}
</style>