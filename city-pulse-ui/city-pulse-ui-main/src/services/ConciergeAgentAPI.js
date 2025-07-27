import { useEventsStore } from '../stores/events'

// Combined Mock Data for Bengaluru Application

// Mock data for weather (areawise) with temperature and cloud cover
const mockWeatherData = [
  { lat: 12.9716, lng: 77.5946, temperature: 28, cloudCover: 40 },   // MG Road
  { lat: 12.9352, lng: 77.6245, temperature: 30, cloudCover: 60 },   // Koramangala
  { lat: 12.9719, lng: 77.6412, temperature: 27, cloudCover: 55 },   // Indiranagar
  { lat: 12.9177, lng: 77.6238, temperature: 29, cloudCover: 70 },   // Silk Board
  { lat: 12.9784, lng: 77.5918, temperature: 26, cloudCover: 30 },   // Cubbon Park
  { lat: 12.9698, lng: 77.7499, temperature: 31, cloudCover: 75 },   // Whitefield
  { lat: 12.9569, lng: 77.7011, temperature: 30, cloudCover: 65 },   // Marathahalli
  { lat: 13.0355, lng: 77.5971, temperature: 29, cloudCover: 50 },   // Hebbal
  { lat: 12.9254, lng: 77.5828, temperature: 28, cloudCover: 45 },   // Jayanagar
  { lat: 13.0475, lng: 77.6212, temperature: 32, cloudCover: 80 },   // Manyata Tech Park
  { lat: 13.1007, lng: 77.5963, temperature: 29, cloudCover: 60 },   // Yelahanka
  { lat: 12.9304, lng: 77.6784, temperature: 31, cloudCover: 70 },   // Bellandur
  { lat: 12.9902, lng: 77.5529, temperature: 27, cloudCover: 35 },   // Rajajinagar
  { lat: 12.8906, lng: 77.5977, temperature: 28, cloudCover: 50 },   // Bannerghatta Road
  { lat: 12.9767, lng: 77.5713, temperature: 29, cloudCover: 65 },   // Majestic
  // --- New Data Points ---
  { lat: 13.0178, lng: 77.6826, temperature: 31, cloudCover: 70 },   // K R Puram
  { lat: 12.9952, lng: 77.6961, temperature: 32, cloudCover: 75 },   // Mahadevapura
  { lat: 12.9926, lng: 77.7153, temperature: 31, cloudCover: 65 },   // Hoodi
  { lat: 13.0134, lng: 77.6603, temperature: 30, cloudCover: 60 },   // Ramamurthy Nagar
  { lat: 12.9859, lng: 77.6568, temperature: 29, cloudCover: 55 }    // CV Raman Nagar
];

// Mock data for AQI (areawise)
const mockAQIData = [
  { lat: 12.9716, lng: 77.5946, aqiValue: 85 },    // MG Road
  { lat: 12.9352, lng: 77.6245, aqiValue: 120 },   // Koramangala
  { lat: 12.9719, lng: 77.6412, aqiValue: 70 },    // Indiranagar
  { lat: 12.9177, lng: 77.6238, aqiValue: 165 },   // Silk Board
  { lat: 12.9784, lng: 77.5918, aqiValue: 60 },    // Cubbon Park
  { lat: 12.9698, lng: 77.7499, aqiValue: 140 },   // Whitefield
  { lat: 12.9569, lng: 77.7011, aqiValue: 155 },   // Marathahalli
  { lat: 13.0355, lng: 77.5971, aqiValue: 95 },    // Hebbal
  { lat: 12.9254, lng: 77.5828, aqiValue: 80 },    // Jayanagar
  { lat: 13.0475, lng: 77.6212, aqiValue: 130 },   // Manyata Tech Park
  { lat: 13.1007, lng: 77.5963, aqiValue: 75 },    // Yelahanka
  { lat: 12.9304, lng: 77.6784, aqiValue: 145 },   // Bellandur
  { lat: 12.9902, lng: 77.5529, aqiValue: 90 },    // Rajajinagar
  { lat: 12.8906, lng: 77.5977, aqiValue: 110 },   // Bannerghatta Road
  { lat: 12.9767, lng: 77.5713, aqiValue: 170 },   // Majestic
  // --- New Data Points ---
  { lat: 13.0178, lng: 77.6826, aqiValue: 155 },   // K R Puram
  { lat: 12.9952, lng: 77.6961, aqiValue: 160 },   // Mahadevapura
  { lat: 12.9926, lng: 77.7153, aqiValue: 145 },   // Hoodi
  { lat: 13.0134, lng: 77.6603, aqiValue: 135 },   // Ramamurthy Nagar
  { lat: 12.9859, lng: 77.6568, aqiValue: 115 }    // CV Raman Nagar
];

// Mock data for incidents
const mockIncidents = [
  {
    id: 'inc1',
    type: 'Traffic Accident',
    location: 'MG Road',
    description: 'Minor fender bender, traffic slowing down.',
    timestamp: Date.now() - 3600000, // 1 hour ago
    coords: { lat: 12.9716, lng: 77.5946 }
  },
  {
    id: 'inc2',
    type: 'Pothole',
    location: 'Koramangala 4th Block',
    description: 'Large pothole near the main signal.',
    timestamp: Date.now() - 7200000, // 2 hours ago
    coords: { lat: 12.9352, lng: 77.6245 }
  },
  {
    id: 'inc3',
    type: 'Flooding',
    location: 'Indiranagar 100 Feet Road',
    description: 'Water logging near the metro station.',
    timestamp: Date.now() - 10800000, // 3 hours ago
    coords: { lat: 12.9719, lng: 77.6412 }
  },
  {
    id: 'inc4',
    type: 'Tree Fall',
    location: 'Jayanagar 4th Block',
    description: 'A large tree has fallen, blocking one lane.',
    timestamp: Date.now() - 1800000, // 30 minutes ago
    coords: { lat: 12.9254, lng: 77.5828 }
  },
  {
    id: 'inc5',
    type: 'Power Outage',
    location: 'Whitefield',
    description: 'Unscheduled power cut reported in the EPIP zone.',
    timestamp: Date.now() - 5400000, // 1.5 hours ago
    coords: { lat: 12.9698, lng: 77.7499 }
  },
  {
    id: 'inc6',
    type: 'Road Blockage',
    location: 'Hebbal Flyover',
    description: 'Protest march causing heavy traffic blockage.',
    timestamp: Date.now() - 9000000, // 2.5 hours ago
    coords: { lat: 13.0355, lng: 77.5971 }
  },
  {
    id: 'inc7',
    type: 'Waterlogging',
    location: 'Bellandur Outer Ring Road',
    description: 'Severe waterlogging under the flyover due to heavy rain.',
    timestamp: Date.now() - 14400000, // 4 hours ago
    coords: { lat: 12.9304, lng: 77.6784 }
  },
  {
    id: 'inc8',
    type: 'Traffic Jam',
    location: 'Silk Board Junction',
    description: 'Gridlock traffic, avoid this route if possible.',
    timestamp: Date.now() - 600000, // 10 minutes ago
    coords: { lat: 12.9177, lng: 77.6238 }
  }
];

// Mock data for events
const mockEvents = [
  {
    id: 'evt1',
    type: 'Concert',
    name: 'Rock Fest',
    location: 'Palace Grounds',
    description: 'Annual rock music festival.',
    timestamp: Date.now() + 86400000, // Tomorrow
    coords: { lat: 13.0082, lng: 77.5946 }
  },
  {
    id: 'evt2',
    type: 'Food Festival',
    name: 'Taste of Bangalore',
    location: 'Lalbagh Botanical Garden',
    description: 'Local food vendors and culinary delights.',
    timestamp: Date.now() + 172800000, // 2 days from now
    coords: { lat: 12.9507, lng: 77.5848 }
  },
  {
    id: 'evt3',
    type: 'Art Exhibition',
    name: 'Modern Art Show',
    location: 'National Gallery of Modern Art',
    description: 'Exhibition of contemporary Indian artists.',
    timestamp: Date.now() + 259200000, // 3 days from now
    coords: { lat: 12.9821, lng: 77.5928 }
  },
  {
    id: 'evt4',
    type: 'Workshop',
    name: 'Pottery Workshop',
    location: 'Claytopia',
    description: 'Learn the basics of pottery.',
    timestamp: Date.now() + 345600000, // 4 days from now
    coords: { lat: 12.9345, lng: 77.6265 }
  },
  {
    id: 'evt5',
    type: 'Marathon',
    name: 'Bengaluru 10K Run',
    location: 'Kanteerava Stadium',
    description: 'City-wide 10K marathon starting from Kanteerava Stadium.',
    timestamp: Date.now() + 518400000, // 6 days from now
    coords: { lat: 12.9696, lng: 77.5891 }
  },
  {
    id: 'evt6',
    type: 'Tech Conference',
    name: 'Future of AI Summit',
    location: 'Bangalore International Exhibition Centre (BIEC)',
    description: 'A global conference on Artificial Intelligence and Machine Learning.',
    timestamp: Date.now() + 1209600000, // 2 weeks from now
    coords: { lat: 13.0691, lng: 77.4815 }
  },
  {
    id: 'evt7',
    type: 'Theater Play',
    name: 'A Midsummer Night\'s Dream',
    location: 'Ranga Shankara',
    description: 'A classic Shakespearean play directed by a renowned artist.',
    timestamp: Date.now() + 691200000, // 8 days from now
    coords: { lat: 12.9113, lng: 77.5704 }
  },
  {
    id: 'evt8',
    type: 'Farmers Market',
    name: 'Organic Farmers Market',
    location: 'Indiranagar Club',
    description: 'Weekly market for fresh, organic produce direct from farms.',
    timestamp: Date.now() + 432000000, // 5 days from now
    coords: { lat: 12.9734, lng: 77.6405 }
  }
];

// Simulate a POST request for submitting a report
export const submitReport = async (reportData) => {
  console.log('Mock API: Submitting report:', reportData)
  return new Promise(resolve => {
    setTimeout(() => {
      console.log('Mock API: Report submitted successfully.')
      resolve({ success: true, message: 'Report submitted successfully.' })
    }, 1000)
  })
}

// Simulate a GET request for chat response
export const getChatResponse = async (message, context) => {
  console.log('Mock API: Getting chat response for message:', message)
  console.log('Mock API: Chat context:', context)
  return new Promise(resolve => {
    setTimeout(() => {
      let response = 'I am your Bangalore buddy. How can I help you today?'
      if (message.toLowerCase().includes('traffic')) {
        response = 'Traffic is moderate on Outer Ring Road. Expect delays near Marathahalli.'
      } else if (message.toLowerCase().includes('friends')) {
        response = 'There are many pubs in Koramangala and Indiranagar. You could also check out a live music venue.'
      } else if (message.toLowerCase().includes('nature')) {
        response = 'Lalbagh Botanical Garden and Cubbon Park are great for a nature retreat.'
      }
      console.log('Mock API: Sending chat response:', response)
      resolve({ response })
    }, 1500)
  })
}

// Initial data fetch (simulated)
export const getInitialEvents = async () => {
  return new Promise(resolve => {
    setTimeout(() => {
      console.log('Mock API: Providing initial events.')
      resolve(mockEvents)
    }, 500)
  })
}

// Mock data for overlays
const mockTrafficData = [
  { id: 'traf1', type: 'Heavy Traffic', location: 'Silk Board Junction', description: 'Heavy congestion due to peak hours.', coords: { lat: 12.9177, lng: 77.6238 } },
  { id: 'traf2', type: 'Road Closure', location: 'Koramangala 80 Feet Road', description: 'Road closed for maintenance.', coords: { lat: 12.9352, lng: 77.6245 } }
];

const mockSafetyData = [
  { id: 'safe1', type: 'Low Light Area', location: 'Cubbon Park', description: 'Poorly lit area, exercise caution at night.', coords: { lat: 12.9757, lng: 77.5929 } },
  { id: 'safe2', type: 'Reported Theft', location: 'Majestic Bus Stand', description: 'Recent reports of pickpocketing.', coords: { lat: 12.9764, lng: 77.5719 } }
];

// Simulate a GET request for overlay data
export const getOverlayData = async (overlayType) => {
  return new Promise(resolve => {
    setTimeout(() => {
      console.log(`Mock API: Providing data for ${overlayType} overlay.`);
      switch (overlayType) {
        case 'Traffic':
          resolve(mockTrafficData);
          break;
        case 'Safety':
          resolve(mockSafetyData);
          break;
        case 'Incidents':
          resolve(mockIncidents);
          break;
        case 'Events':
          resolve(mockEvents);
          break;
        default:
          resolve([]);
      }
    }, 500);
  });
};

// Simulate a GET request for traffic predictions
export const getTrafficPredictions = async (timeOffset) => {
  return new Promise(resolve => {
    setTimeout(() => {
      console.log(`Mock API: Providing traffic predictions for time offset: ${timeOffset}`);
      // Simple mock: return different data based on the time offset
      const intensity = 1 + (timeOffset / 24) * 4; // Intensity increases with time
      console.log(intensity)
      const predictions = [
        { location: { lat: 12.9177, lng: 77.6238 }, weight: intensity * 2 }, // Silk Board
        { location: { lat: 12.9716, lng: 77.5946 }, weight: intensity * 1.5 }, // MG Road
        { location: { lat: 12.9352, lng: 77.6245 }, weight: intensity }, // Koramangala
        { location: { lat: 12.9279, lng: 77.6271 }, weight: intensity * 1.2 }, // HSR Layout
        { location: { lat: 12.9784, lng: 77.5918 }, weight: intensity * 0.8 }, // Cubbon Park Area
        { location: { lat: 13.0082, lng: 77.5946 }, weight: intensity ^ 0.5 }, // Palace Grounds
      ];
      resolve(predictions);
    }, 500);
  });
};

// Simulate a GET request for incidents
export const getIncidents = async () => {
  return new Promise(resolve => {
    setTimeout(() => {
      console.log('Mock API: Providing incidents.');
      resolve(mockIncidents);
    }, 500);
  });
};

export const getWeatherData = async () => {
  return new Promise(resolve => {
    setTimeout(() => {
      console.log('Mock API: Providing weather data.');
      resolve(mockWeatherData);
    }, 500);
  });
};

export const getAQIData = async () => {
  return new Promise(resolve => {
    setTimeout(() => {
      console.log('Mock API: Providing AQI data.');
      resolve(mockAQIData);
    }, 500);
  });
};

