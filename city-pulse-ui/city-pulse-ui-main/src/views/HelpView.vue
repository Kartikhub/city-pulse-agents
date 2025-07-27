<template>
  <div class="flex flex-col flex-grow p-4 overflow-y-auto text-customText">
    <h1 class="text-3xl font-bold mb-4">City Pulse - App Overview</h1>

    <section class="mb-6">
      <h2 class="text-2xl font-semibold mb-2">Core UI Screens & Features</h2>
      
      <div class="mb-4">
        <h3 class="text-xl font-medium mb-1">Dashboard ("Your Updates")</h3>
        <ul class="list-disc list-inside ml-4">
          <li>Displays a personalized feed of recent updates (events).</li>
          <li>**Functionality:** Events are fetched dynamically on page load.</li>
          <li>**Functionality:** Expandable list for event details (maintains map size).</li>
          <li>**Mocked:** The map is a Google Maps instance centered on Bangalore, but currently does not display dynamic event markers or overlays.</li>
        </ul>
      </div>

      <div class="mb-4">
        <h3 class="text-xl font-medium mb-1">Map View</h3>
        <ul class="list-disc list-inside ml-4">
          <li>Full-screen interactive Google Map centered on Bangalore.</li>
          <li>**Functionality:** Overlay options (Traffic, Incidents, Events, Safety, Public Transport, Food & Drink, Attractions) are clickable buttons with long-press tooltips.</li>
          <li>**Mocked:** Overlays do not currently filter or display data on the map.</li>
          <li>**Mocked:** Map does not display dynamic event markers.</li>
        </ul>
      </div>

      <div class="mb-4">
        <h3 class="text-xl font-medium mb-1">Chat View</h3>
        <ul class="list-disc list-inside ml-4">
          <li>Conversational interface for interacting with the Concierge Agent.</li>
          <li>**Functionality:** Send and receive messages.</li>
          <li>**Functionality:** Textarea auto-adjusts height.</li>
          <li>**Functionality:** Clicking a recent event from the Notifications menu (top right) will pre-fill the chat input and automatically send the message.</li>
          <li>**Mocked:** Backend responses are simulated; actual Concierge Agent integration is pending.</li>
        </ul>
      </div>

      <div class="mb-4">
        <h3 class="text-xl font-medium mb-1">Submit Report Flow</h3>
        <ul class="list-disc list-inside ml-4">
          <li>Multi-step user flow for citizen reporting.</li>
          <li>**Mocked:** This is a UI mockup. No backend integration for report submission is currently implemented.</li>
        </ul>
      </div>

      <div class="mb-4">
        <h3 class="text-xl font-medium mb-1">Authentication & Profile</h3>
        <ul class="list-disc list-inside ml-4">
          <li>**Functionality:** User authentication (login/logout).</li>
          <li>**Functionality:** Interests selection page.</li>
          <li>**Mocked:** Profile view is a UI mockup.</li>
        </ul>
      </div>
    </section>

    <section class="mb-6">
      <h2 class="text-2xl font-semibold mb-2">Key Agent Interactions (Supported by UI)</h2>
      <ul class="list-disc list-inside ml-4">
        <li>**Concierge Agent:** The UI is built to interact with a single Concierge Agent endpoint for all data fetching and user interactions.</li>
        <li>**Real-time Updates:** The UI is designed to receive real-time event pushes (though currently mocked data).</li>
        <li>**Continuous Learning:** The UI can display toast notifications for profile updates (e.g., "I've updated your profile with your new interest in handicrafts!"), demonstrating the continuous learning loop.</li>
      </ul>
    </section>

    <section class="mb-6">
      <h2 class="text-2xl font-semibold mb-2">Current Development Status</h2>
      <ul class="list-disc list-inside ml-4">
        <li>**Working:** Core navigation, responsive layout, dynamic event fetching on page load, Google Maps integration (display only), chat input and auto-send from notifications.</li>
        <li>**Mocked/Not Yet Functional:** Dynamic map markers/overlays, actual backend integration for chat responses, report submission, profile updates.</li>
      </ul>
    </section>
  </div>
</template>

<script setup>
// No specific script logic needed for this static help page
</script>

<style scoped>
/* Add any specific styles for HelpView if needed */
</style>