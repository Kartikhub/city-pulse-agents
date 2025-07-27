<template>
  <div class="absolute top-full left-0 mt-2 w-48 bg-black rounded-md shadow-lg py-1 z-50">
    <button class="block w-full text-left px-4 py-2 text-sm text-customText hover:bg-gray-700 focus:outline-none" @click="selectCity('Bangalore')">
      Bangalore
    </button>
    <button disabled class="block w-full text-left px-4 py-2 text-sm text-gray-500 cursor-not-allowed">
      Delhi (Coming soon...)
    </button>
    <button disabled class="block w-full text-left px-4 py-2 text-sm text-gray-500 cursor-not-allowed">
      Mumbai (Coming soon...)
    </button>
    <button disabled class="block w-full text-left px-4 py-2 text-sm text-gray-500 cursor-not-allowed">
      Kolkata (Coming soon...)
    </button>
  </div>
</template>

<script setup>
import { defineEmits } from 'vue'

const emit = defineEmits(['close-menu', 'select-city'])

const selectCity = (city) => {
  // In a real app, you'd update a store or emit a more complex event
  console.log('Selected city:', city)
  emit('select-city', city)
  emit('close-menu')
}
</script>