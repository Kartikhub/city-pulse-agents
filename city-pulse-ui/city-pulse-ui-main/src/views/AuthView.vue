<template>
  <div class="flex flex-col items-center justify-center min-h-screen bg-customBackground text-customText p-4">
    <h1 class="text-3xl font-bold mb-8">{{ isLogin ? 'Login' : 'Sign Up' }}</h1>

    <form @submit.prevent="handleSubmit" class="w-full max-w-sm">
      <div class="mb-4">
        <label for="email" class="block text-customText text-sm font-bold mb-2">Email</label>
        <input type="email" id="email" v-model="email" required
               class="shadow appearance-none border rounded w-full py-2 px-3 bg-black text-customText leading-tight focus:outline-none focus:shadow-outline">
      </div>

      <div class="mb-4" v-if="!isLogin">
        <label for="name" class="block text-customText text-sm font-bold mb-2">Name</label>
        <input type="text" id="name" v-model="name" required
               class="shadow appearance-none border rounded w-full py-2 px-3 bg-black text-customText leading-tight focus:outline-none focus:shadow-outline">
      </div>

      <div class="mb-4" v-if="!isLogin">
        <label for="dob" class="block text-customText text-sm font-bold mb-2">Date of Birth</label>
        <input type="date" id="dob" v-model="dob" required
               class="shadow appearance-none border rounded w-full py-2 px-3 bg-black text-customText leading-tight focus:outline-none focus:shadow-outline">
      </div>

      <div class="mb-6">
        <label for="password" class="block text-customText text-sm font-bold mb-2">Password</label>
        <input type="password" id="password" v-model="password" required
               class="shadow appearance-none border rounded w-full py-2 px-3 bg-black text-customText leading-tight focus:outline-none focus:shadow-outline">
      </div>

      <div class="flex items-center justify-between mb-4">
        <button type="submit" :disabled="authStore.loading" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          {{ authStore.loading ? 'Loading...' : (isLogin ? 'Login' : 'Sign Up') }}
        </button>
        <a @click.prevent="isLogin = !isLogin" class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800 cursor-pointer">
          {{ isLogin ? 'Need an account? Sign Up' : 'Already have an account? Login' }}
        </a>
      </div>

      <p v-if="authStore.error" class="text-red-500 text-xs italic">{{ authStore.error }}</p>
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const name = ref('') // New ref for name
const dob = ref('') // New ref for DOB
const isLogin = ref(false) // Default to Sign Up

const handleSubmit = async () => {
  if (isLogin.value) {
    await authStore.signIn(email.value, password.value)
  } else {
    await authStore.signUp(email.value, password.value, name.value, dob.value) // Pass new fields
  }
  if (authStore.isAuthenticated) {
    // Redirect based on whether interests are selected
    if (authStore.hasSelectedInterests) {
      router.push('/') // Go to dashboard
    } else {
      router.push('/interests') // Go to interests selection
    }
  }
}
</script>

<style scoped>
/* Add any specific styles for AuthView if needed */
</style>