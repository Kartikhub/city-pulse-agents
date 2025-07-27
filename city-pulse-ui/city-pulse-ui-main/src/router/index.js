import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import AuthView from '../views/AuthView.vue'
import InterestsView from '../views/InterestsView.vue'
import ProfileView from '../views/ProfileView.vue' // Import ProfileView
import { useAuthStore } from '../stores/auth'
import { useEventsStore } from '../stores/events'
import { getInitialEvents } from '../services/ConciergeAgentAPI'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'dashboard',
      component: DashboardView,
      meta: { requiresAuth: true }
    },
    {
      path: '/map',
      name: 'map',
      component: () => import('../views/MapView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/chat',
      name: 'chat',
      component: () => import('../views/ChatView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/report',
      name: 'report',
      component: () => import('../views/SubmitReportView.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/auth',
      name: 'auth',
      component: AuthView,
      meta: { requiresGuest: true } // Only accessible to unauthenticated users
    },
    {
      path: '/interests',
      name: 'interests',
      component: InterestsView,
      meta: { requiresAuth: true, requiresInterestsSelection: false } // Requires auth, but specifically for selecting interests
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView,
      meta: { requiresAuth: true } // Requires authentication
    },
    {
      path: '/help',
      name: 'help',
      component: () => import('../views/HelpView.vue'),
      meta: { requiresAuth: false } // Help page does not require authentication
    }
  ]
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()
  const eventsStore = useEventsStore()
  
  // Ensure auth state is initialized before proceeding
  if (!authStore._authInitialized) {
    await authStore.initAuth()
  }

  const isAuthenticated = authStore.isAuthenticated
  const hasSelectedInterests = authStore.hasSelectedInterests

  if (to.meta.requiresAuth && !isAuthenticated) {
    // If route requires auth and user is not authenticated, redirect to login
    next({ name: 'auth' })
  } else if (to.meta.requiresGuest && isAuthenticated) {
    // If route requires guest and user is authenticated, redirect to dashboard
    next({ name: 'dashboard' })
  } else if (to.meta.requiresAuth && !hasSelectedInterests && to.name !== 'interests') {
    // If route requires auth, user is authenticated but hasn't selected interests, and not already on interests page
    next({ name: 'interests' })
  } else {
    // Fetch events on every route change (except for auth and interests pages)
    if (to.name !== 'auth' && to.name !== 'interests') {
      const initialEvents = await getInitialEvents()
      eventsStore.setEvents(initialEvents)
    }
    next()
  }
})

export default router