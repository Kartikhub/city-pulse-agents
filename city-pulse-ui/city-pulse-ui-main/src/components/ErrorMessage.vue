<template>
  <div class="bg-red-500 text-white p-4 rounded-md shadow-md">
    <p class="font-bold">Error:</p>
    <p>{{ message }}</p>
  </div>
</template>

<script setup>
import { defineProps } from 'vue'

defineProps({
  message: {
    type: String,
    required: true
  }
})
</script>
