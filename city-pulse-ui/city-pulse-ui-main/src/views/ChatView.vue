<template>
  <div class="flex flex-col h-full p-4">
    <!-- Scrollable Chat Messages Area -->
    <div class="flex-grow overflow-y-auto flex flex-col"> <!-- flex-col here -->
      <div class="flex-grow"></div> <!-- Spacer to push content to bottom -->

      <!-- Dynamic Chat Messages -->
      <div v-for="(msg, index) in messages" :key="index" class="mb-2"
           :class="{ 'text-right': msg.sender === 'user' }">
        <p class="p-2 rounded-xl block break-words max-w-[80%]"
           :class="{ 'bg-black ml-auto': msg.sender === 'user', 'bg-gray-700 mr-auto': msg.sender === 'bot' }">
          {{ msg.text }}
        </p>
      </div>

      <!-- Welcome Headers and Recommendation Buttons (Conditional, will appear above messages due to spacer) -->
      <template v-if="messages.length === 0">
        <h1 class="text-3xl font-bold mb-2">Hello User...</h1>
        <h2 class="text-lg text-gray-300 mb-4">Welcome to the chat, I am your Bangalore buddy. You can ask me anything the city!</h2>
        <div class="flex flex-wrap justify-end gap-2 mb-2">
          <button v-for="(rec, index) in recommendations" :key="index"
                  @click="selectRecommendation(rec)"
                  class="bg-black p-2 rounded-lg text-customText text-sm focus:outline-none hover:bg-gray-600">
            {{ rec }}
          </button>
        </div>
      </template>
    </div>

    <!-- Chat input area (fixed at bottom) -->
    <div class="flex items-end mt-4">
      <textarea ref="textareaRef" placeholder="Chat here..." class="flex-grow bg-black text-customText p-3 rounded-lg focus:outline-none resize-none overflow-hidden break-words whitespace-pre-wrap"
                v-model="messageInput" @input="adjustTextareaHeight" @keyup.enter.prevent="sendMessage"
                :style="{ 'max-height': textareaMaxHeight }"></textarea>
      <button @click="sendMessage" class="ml-2 w-10 h-10 rounded-full bg-black flex items-center justify-center">
        <span class="material-icons text-customText">send</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, watch } from 'vue'
import { useChatStore } from '../stores/chat'
import { storeToRefs } from 'pinia'

const chatStore = useChatStore()
const { messageInput, messages } = storeToRefs(chatStore)
const textareaRef = ref(null)
const textareaMaxHeight = ref('33vh') // 1/3rd of viewport height

const recommendations = ref([
  "How's traffic today?",
  "What can I do with friends tonight?",
  "Help me plan a nature retreat style outing this weekend"
])

const selectRecommendation = (rec) => {
  messageInput.value = rec
  sendMessage() // Simulate sending the message
}

const sendMessage = async () => {
  if (messageInput.value.trim() === '') return

  const userMessage = messageInput.value // Store message before clearing input
  await chatStore.sendMessage(userMessage) // Use the store's sendMessage action
  messageInput.value = '' // Clear input after sending
  nextTick(() => {
    adjustTextareaHeight() // Reset textarea height after sending
  })

  // Scroll to bottom after new messages
  nextTick(() => {
    const chatMessagesArea = document.querySelector('.overflow-y-auto')
    if (chatMessagesArea) {
      chatMessagesArea.scrollTop = chatMessagesArea.scrollHeight
    }
  })
}

const adjustTextareaHeight = () => {
  if (textareaRef.value) {
    textareaRef.value.style.height = 'auto' // Reset height to calculate scrollHeight correctly
    if (messageInput.value === '') {
      textareaRef.value.style.height = '48px' // Explicitly set to single line height when empty
    } else {
      textareaRef.value.style.height = `${textareaRef.value.scrollHeight}px`
    }
  }
}

onMounted(() => {
  // Set initial height to a single line
  if (textareaRef.value) {
    textareaRef.value.style.height = '48px'
  }
  // Adjust height if messageInput is pre-filled on mount
  if (messageInput.value) {
    nextTick(() => {
      adjustTextareaHeight()
      sendMessage() // Automatically send the message if pre-filled
    })
  }
})

watch(messageInput, () => {
  nextTick(() => {
    adjustTextareaHeight()
  })
})

</script>

<style scoped>
/* Add any specific styles for chat messages if needed */
</style>
