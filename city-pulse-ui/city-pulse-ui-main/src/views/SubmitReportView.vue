<template>
  <div class="flex flex-col h-full p-4">
    <!-- Step 1: Report Details -->
    <template v-if="currentStep === 1">
      <div class="flex-grow flex flex-col-reverse min-h-full">
        <div class="mb-4">
          <label for="description" class="block text-customText text-lg font-bold mb-2">Detailed description</label>
          <textarea id="description" v-model="report.description" placeholder="Describe the incident in your own words... A more detailed description helps us better help the community!"
                    rows="5" class="shadow appearance-none border rounded w-full py-2 px-3 bg-black text-customText leading-tight focus:outline-none focus:shadow-outline resize-none"></textarea>
        </div>

        <div class="mb-4">
          <label for="incidentType" class="block text-customText text-lg font-bold mb-2">Type of Incident</label>
          <div class="relative">
            <select id="incidentType" v-model="report.incidentType"
                    class="block appearance-none w-full bg-black border border-gray-700 text-customText py-2 px-3 pr-8 rounded leading-tight focus:outline-none focus:bg-gray-800 focus:border-gray-500">
              <option value="">Type of incident</option>
              <option value="Traffic Accident">Traffic Accident</option>
              <option value="Flooding">Flooding</option>
              <option value="Potholes">Potholes</option>
              <option value="Bad streetlight">Bad streetlight</option>
            </select>
            <div class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-customText">
              <svg class="fill-current h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M9.293 12.95l.707.707L15.657 8l-1.414-1.414L10 10.828 5.757 6.586 4.343 8z"/></svg>
            </div>
          </div>
        </div>

        <div class="mb-4">
          <label for="location" class="block text-customText text-lg font-bold mb-2">Location</label>
          <input type="text" id="location" v-model="report.location" placeholder="e.g. Indiranagar"
                 class="shadow appearance-none border rounded w-full py-2 px-3 bg-black text-customText leading-tight focus:outline-none focus:shadow-outline">
        </div>
      </div>

      <div class="flex justify-end">
        <button @click="nextStep" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Next
        </button>
      </div>
    </template>

    <!-- Step 2: Upload Reference -->
    <template v-if="currentStep === 2">
      <div class="flex-grow flex flex-col">
        <h2 class="text-xl font-bold mb-4">Upload reference (optional)</h2>
        <div class="flex-grow flex flex-col items-center justify-center p-4 rounded-lg mb-4 border-2 border-dashed border-gray-600">
          <input type="file" id="mediaUpload" multiple accept="image/*,video/*" @change="handleFileChange" class="hidden" />
          <label for="mediaUpload" class="cursor-pointer bg-gray-700 hover:bg-gray-600 text-customText font-bold py-2 px-4 rounded-lg">
            Select Files
          </label>
          <p class="text-gray-400 text-sm mt-2">Images or Videos (Max 5 files)</p>

          <div v-if="mediaPreviews.length > 0" class="mt-4 grid grid-cols-3 gap-2">
            <div v-for="(preview, index) in mediaPreviews" :key="index" class="relative w-24 h-24 bg-gray-800 rounded-lg overflow-hidden">
              <img v-if="preview.type.startsWith('image')" :src="preview.url" class="w-full h-full object-cover" />
              <video v-else-if="preview.type.startsWith('video')" :src="preview.url" class="w-full h-full object-cover"></video>
              <div v-else class="w-full h-full flex items-center justify-center text-customText text-xs">File</div>
              <button @click="removeMedia(index)" class="absolute top-1 right-1 bg-red-500 rounded-full p-1 text-white text-xs leading-none">
                &times;
              </button>
            </div>
          </div>

          <div v-if="isUploading" class="mt-4 text-customText">
            Uploading: {{ uploadProgress.toFixed(0) }}%
          </div>
        </div>
      </div>

      <div class="flex justify-between">
        <button @click="currentStep--" class="bg-gray-600 hover:bg-gray-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          Back
        </button>
        <button @click="submitReport" :disabled="isSubmitting || isUploading" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline">
          {{ isSubmitting ? 'Submitting...' : 'Submit' }}
        </button>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { submitReport as submitReportAPI } from '../services/ConciergeAgentAPI'
import { getStorage, ref as storageRef, uploadBytesResumable, getDownloadURL } from "firebase/storage";
import { getFirestore, collection, addDoc, serverTimestamp } from "firebase/firestore";
import { db } from '../firebase'; // Assuming firebase.js exports db
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();
const storage = getStorage();

const currentStep = ref(1)

const report = ref({
  location: '',
  incidentType: '',
  description: '',
  media: [] // To store uploaded media URLs
})

const mediaFiles = ref([]);
const mediaPreviews = ref([]);
const isUploading = ref(false);
const uploadProgress = ref(0);
const isSubmitting = ref(false);

const handleFileChange = (event) => {
  const files = Array.from(event.target.files);
  if (mediaFiles.value.length + files.length > 5) {
    alert("You can upload a maximum of 5 files.");
    return;
  }

  files.forEach(file => {
    mediaFiles.value.push(file);
    const reader = new FileReader();
    reader.onload = (e) => {
      mediaPreviews.value.push({ url: e.target.result, type: file.type });
    };
    reader.readAsDataURL(file);
  });
};

const removeMedia = (index) => {
  mediaFiles.value.splice(index, 1);
  mediaPreviews.value.splice(index, 1);
};

const uploadMedia = async () => {
  const downloadURLs = [];
  if (mediaFiles.value.length === 0) return downloadURLs;

  isUploading.value = true;
  let uploadedCount = 0;

  for (const file of mediaFiles.value) {
    const uniqueFileName = `${authStore.user.uid}/${Date.now()}_${file.name}`;
    const fileRef = storageRef(storage, uniqueFileName);
    const uploadTask = uploadBytesResumable(fileRef, file);

    await new Promise((resolve, reject) => {
      uploadTask.on('state_changed',
        (snapshot) => {
          uploadProgress.value = (snapshot.bytesTransferred / snapshot.totalBytes) * 100;
        },
        (error) => {
          console.error("Upload failed:", error);
          alert("Media upload failed. Please try again.");
          isUploading.value = false;
          reject(error);
        },
        async () => {
          const downloadURL = await getDownloadURL(uploadTask.snapshot.ref);
          downloadURLs.push(downloadURL);
          uploadedCount++;
          if (uploadedCount === mediaFiles.value.length) {
            isUploading.value = false;
            uploadProgress.value = 0;
            resolve();
          }
        }
      );
    });
  }
  return downloadURLs;
};

const nextStep = () => {
  currentStep.value++
  console.log('Moving to next step. Current step:', currentStep.value)
}

const submitReport = async () => {
  isSubmitting.value = true;
  try {
    const mediaUrls = await uploadMedia();
    report.value.media = mediaUrls;

    const reportToSave = {
      ...report.value,
      userId: authStore.user.uid, // Associate report with user
      timestamp: serverTimestamp(), // Firestore server timestamp
    };

    await addDoc(collection(db, "city-pulse-ui-reports"), reportToSave);

    alert("Report submitted successfully!");
    // Clear form and reset step
    report.value = {
      location: '',
      incidentType: '',
      description: '',
      media: []
    };
    mediaFiles.value = [];
    mediaPreviews.value = [];
    currentStep.value = 1;
  } catch (error) {
    console.error("Error submitting report:", error);
    alert("Error submitting report. Please try again.");
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* Add any specific styles for SubmitReportView if needed */
</style>