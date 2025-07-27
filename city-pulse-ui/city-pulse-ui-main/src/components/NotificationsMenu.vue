<template>
  <div class="absolute top-full right-0 mt-2 w-64 bg-black rounded-md shadow-lg py-1 z-50">
    <div class="px-4 py-2 text-lg font-bold text-gray-300">Your recent events</div>
    <template v-if="recentEvents.length > 0">
      <a v-for="event in recentEvents" :key="event.id" href="#" @click.prevent="handleEventClick(event)" class="block px-4 py-2 text-sm text-customText hover:bg-gray-700">
        <span class="font-semibold">{{ event.type }}</span>: {{ event.description }}
      </a>
    </template>
    <template v-else>
      <p class="px-4 py-2 text-sm text-gray-500">No recent events.</p>
    </template>
  </div>
</template>

<script setup>
import { defineEmits, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useEventsStore } from '../stores/events'
import { useChatStore } from '../stores/chat'
import { storeToRefs } from 'pinia'

const emit = defineEmits(['close-menu'])
const router = useRouter()
const eventsStore = useEventsStore()
const chatStore = useChatStore()
const { events } = storeToRefs(eventsStore)

console.log('NotificationsMenu: events from store', events.value)

const recentEvents = computed(() => {
  console.log('NotificationsMenu: Computing recentEvents', events.value.length)
  // Sort by timestamp (newest first) and take the top 3
  return [...events.value]
    .sort((a, b) => b.timestamp - a.timestamp)
    .slice(0, 3)
})

const handleEventClick = (event) => {
  chatStore.setInitialMessage(`Tell me more about this event: ${event.description}`)
  router.push('/chat')
  closeMenu()
}

const closeMenu = () => {
  emit('close-menu')
}
</script>