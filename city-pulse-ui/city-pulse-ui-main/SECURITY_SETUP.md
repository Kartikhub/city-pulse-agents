# City Pulse UI Security Setup

## Environment Variables Setup

This project uses environment variables to keep sensitive API keys secure. Follow these steps to set up your local development environment:

### 1. Create Environment File

Copy the template file and rename it:
```bash
cp .env.template .env
```

### 2. Get Your API Keys

#### Google Maps API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Maps JavaScript API
4. Create an API key in the Credentials section
5. Restrict the API key to your domain for security

#### Firebase Configuration
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project or select an existing one
3. Go to Project Settings > General
4. In the "Your apps" section, find or create a web app
5. Copy the configuration values

### 3. Update .env File

Edit the `.env` file and replace the placeholder values with your actual API keys:

```env
VITE_GOOGLE_MAPS_API_KEY=your_actual_google_maps_api_key
VITE_FIREBASE_API_KEY=your_actual_firebase_api_key
VITE_FIREBASE_AUTH_DOMAIN=your_project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your_actual_project_id
VITE_FIREBASE_STORAGE_BUCKET=your_project.firebasestorage.app
VITE_FIREBASE_MESSAGING_SENDER_ID=your_actual_sender_id
VITE_FIREBASE_APP_ID=your_actual_app_id
VITE_FIREBASE_MEASUREMENT_ID=your_actual_measurement_id
```

### 4. Security Notes

- Never commit the `.env` file to version control
- The `.env.template` file should not contain actual API keys
- In production, use your hosting platform's environment variable settings
- Regularly rotate your API keys for security

### 5. Development

After setting up the environment variables, you can run the development server:

```bash
npm install
npm run dev
```

The application will automatically use the environment variables from your `.env` file.
