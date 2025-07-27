let mapPromise;

export function loadGoogleMaps(apiKey) {
  if (mapPromise) {
    return mapPromise;
  }

  mapPromise = new Promise((resolve, reject) => {
    // Check if the script is already loaded (e.g., by another component)
    if (window.google && window.google.maps && window.google.maps.visualization) {
      console.log('Google Maps and Visualization library already loaded.');
      resolve(window.google.maps);
      return;
    }

    const script = document.createElement('script');
    script.src = `https://maps.googleapis.com/maps/api/js?key=${apiKey}&libraries=visualization`;
    script.async = true;
    script.defer = true;
    
    script.onload = () => {
      if (window.google && window.google.maps && window.google.maps.visualization) {
        console.log('Google Maps API with Visualization library loaded and verified.');
        resolve(window.google.maps);
      } else {
        console.error('Google Maps API loaded, but Visualization library is missing.');
        reject(new Error('Google Maps Visualization library failed to load.'));
      }
    };
    
    script.onerror = (error) => {
      console.error('Failed to load the Google Maps script.', error);
      reject(error);
    };

    document.head.appendChild(script);
  });

  return mapPromise;
}

export function initializeMap(mapElement, options) {
  return new google.maps.Map(mapElement, options);
}