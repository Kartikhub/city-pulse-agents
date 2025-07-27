import { defineStore } from 'pinia'
import { getChatResponse } from '../services/ConciergeAgentAPI'

export const useChatStore = defineStore('chat', {
  state: () => ({
    messageInput: '',
    messages: []
  }),
  actions: {
    setInitialMessage(text) {
      this.messageInput = text
    },
    addMessage(message) {
      this.messages.push(message)
    },
    async sendMessage(userMessage) {
      if (userMessage.trim() === '') return

      this.addMessage({ text: userMessage, sender: 'user' })

      // Prepare chat context
      const chatContext = JSON.stringify(this.messages.map(msg => ({ role: msg.sender === 'user' ? 'user' : 'model', content: msg.text }))) // Map to role/content for LLM

      // Simulate bot response using API, sending context
      const response = await getChatResponse(userMessage, chatContext)
      this.addMessage({ text: response.response, sender: 'bot' })
    },
    clearChat() {
      this.messages = []
      this.messageInput = ''
    }
  }
})