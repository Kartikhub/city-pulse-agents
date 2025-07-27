import { defineStore } from 'pinia'
import { auth, db } from '../firebase'
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  updateProfile
} from 'firebase/auth'
import { doc, setDoc, getDoc } from 'firebase/firestore'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    isAuthenticated: false,
    loading: false,
    error: null,
    hasSelectedInterests: false,
    _authInitialized: false, // Internal flag to track if initAuth has completed
    locationUpdateInterval: null // To store the interval ID for location tracking
  }),
  actions: {
    async signUp(email, password, name, dob) {
      this.loading = true
      this.error = null
      try {
        const userCredential = await createUserWithEmailAndPassword(auth, email, password)
        this.user = userCredential.user
        this.isAuthenticated = true
        this.hasSelectedInterests = false // Interests not selected yet

        // Update Firebase Auth profile
        if (this.user && name) {
          await updateProfile(this.user, { displayName: name })
          this.user.displayName = name // Manually update the user object in store
        }

        // Create user document in Firestore
        await setDoc(doc(db, 'city-pulse-ui-users', this.user.uid), {
          name: name,
          email: email,
          dob: dob,
          hasSelectedInterests: false,
          interests: []
        })

      } catch (error) {
        this.error = error.message
        this.isAuthenticated = false
      } finally {
        this.loading = false
      }
    },
    async signIn(email, password) {
      this.loading = true
      this.error = null
      try {
        const userCredential = await signInWithEmailAndPassword(auth, email, password)
        this.user = userCredential.user
        this.isAuthenticated = true

        // Fetch user profile from Firestore
        const userDoc = await getDoc(doc(db, 'city-pulse-ui-users', this.user.uid))
        if (userDoc.exists()) {
          this.hasSelectedInterests = userDoc.data().hasSelectedInterests || false
        } else {
          // This case should ideally not happen if user signed up via our app
          this.hasSelectedInterests = false
        }

      } catch (error) {
        this.error = error.message
        this.isAuthenticated = false
      } finally {
        this.loading = false
      }
    },
    async signOut() {
      this.loading = true
      this.error = null
      try {
        await signOut(auth)
        this.user = null
        this.isAuthenticated = false
        this.hasSelectedInterests = false
      } catch (error) {
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    initAuth() {
      if (this._authInitialized) {
        return Promise.resolve(); // Already initialized
      }
      this.loading = true;
      return new Promise(resolve => {
        onAuthStateChanged(auth, async (user) => {
          if (user) {
            this.user = user;
            this.isAuthenticated = true;
            // Fetch user profile from Firestore
            const userDoc = await getDoc(doc(db, 'city-pulse-ui-users', this.user.uid))
            if (userDoc.exists()) {
              const userData = userDoc.data();
              this.hasSelectedInterests = userData.hasSelectedInterests || false;
              this.user.lastKnownLocation = userData.lastKnownLocation || null; // Populate lastKnownLocation
            } else {
              // This case should ideally not happen if user signed up via our app
              this.hasSelectedInterests = false;
              this.user.lastKnownLocation = null;
            }
            this.startLocationTracking(); // Start tracking location on successful login
          } else {
            this.user = null;
            this.isAuthenticated = false;
            this.hasSelectedInterests = false;
            this.stopLocationTracking(); // Stop tracking if user logs out or is not authenticated
          }
          this.loading = false;
          this._authInitialized = true; // Mark as initialized
          resolve();
        });
      });
    },
    async setInterestsSelected(value, interests = []) {
      this.hasSelectedInterests = value
      if (this.user) {
        await setDoc(doc(db, 'city-pulse-ui-users', this.user.uid), {
          hasSelectedInterests: value,
          interests: interests
        }, { merge: true }) // Use merge to update without overwriting other fields
      }
    },
    async updateUserLocation(latitude, longitude) {
      if (this.user) {
        try {
          await setDoc(doc(db, 'city-pulse-ui-users', this.user.uid), {
            lastKnownLocation: {
              latitude: latitude,
              longitude: longitude,
              timestamp: Date.now()
            }
          }, { merge: true });
          console.log("User location updated in Firestore.");
        } catch (error) {
          console.error("Error updating user location:", error);
        }
      }
    },
    startLocationTracking() {
      if (navigator.geolocation) {
        this.locationUpdateInterval = setInterval(() => {
          navigator.geolocation.getCurrentPosition(
            (position) => {
              this.updateUserLocation(position.coords.latitude, position.coords.longitude);
            },
            (error) => {
              console.error("Error tracking user location:", error);
            },
            { enableHighAccuracy: true, timeout: 15000, maximumAge: 0 }
          );
        }, 5000); // Update every 5 seconds
      } else {
        console.warn("Geolocation is not supported by this browser. Cannot track location.");
      }
    },
    stopLocationTracking() {
      if (this.locationUpdateInterval) {
        clearInterval(this.locationUpdateInterval);
        this.locationUpdateInterval = null;
      }
    }
  }
})