# 🚀 Complete Setup Guide for City Pulse Notification Agent

This guide will help you set up Firebase, Google Cloud PubSub, and AI components to test your notification agent.

## 📋 Prerequisites

- Python 3.8+
- Google account
- Credit card (for Google Cloud - free tier available)

## 🔥 Firebase Setup (30 minutes)

### Step 1: Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Create a project"
3. Enter project name: `city-pulse-notifications`
4. Enable Google Analytics (optional)
5. Click "Create project"

### Step 2: Enable Cloud Messaging
1. In Firebase Console, go to "Project settings" (gear icon)
2. Click "Cloud Messaging" tab
3. Note your "Server key" and "Sender ID"

### Step 3: Generate Service Account Key
1. Go to "Project settings" > "Service accounts"
2. Click "Generate new private key"
3. Download the JSON file
4. Save as `firebase-service-account.json` in your project

### Step 4: Get Project Configuration
```json
{
  "project_id": "city-pulse-notifications-xxxxx",
  "database_url": "https://city-pulse-notifications-xxxxx-default-rtdb.firebaseio.com/"
}
```

## ☁️ Google Cloud PubSub Setup (20 minutes)

### Step 1: Enable Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create new project or use existing Firebase project
3. Enable billing (required for PubSub)

### Step 2: Enable PubSub API
1. Go to "APIs & Services" > "Library"
2. Search for "Cloud Pub/Sub API"
3. Click "Enable"

### Step 3: Create Service Account
1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Name: `city-pulse-pubsub`
4. Add roles: "Pub/Sub Editor" and "Pub/Sub Subscriber"
5. Create and download JSON key
6. Save as `gcp-service-account.json`

### Step 4: Create Topics and Subscriptions
```bash
# Install Google Cloud CLI first
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Create topics
gcloud pubsub topics create user-reports-topic
gcloud pubsub topics create environmental-data-topic
gcloud pubsub topics create events-topic
gcloud pubsub topics create emergencies-topic

# Create subscriptions
gcloud pubsub subscriptions create user-reports-sub --topic=user-reports-topic
gcloud pubsub subscriptions create environmental-data-sub --topic=environmental-data-topic
gcloud pubsub subscriptions create events-sub --topic=events-topic
gcloud pubsub subscriptions create emergencies-sub --topic=emergencies-topic
```

## 🤖 AI Configuration Setup (10 minutes)

### Step 1: Get Google AI API Key
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Click "Get API key"
3. Create new API key
4. Copy the key

### Step 2: Set Environment Variables
Create a `.env` file in your notifications folder:

```bash
# Firebase Configuration
FIREBASE_ENABLED=true
FIREBASE_PROJECT_ID=city-pulse-notifications-xxxxx
FIREBASE_SERVICE_ACCOUNT_PATH=./firebase-service-account.json
FIREBASE_DATABASE_URL=https://city-pulse-notifications-xxxxx-default-rtdb.firebaseio.com/

# Google Cloud PubSub
PUBSUB_ENABLED=true
GOOGLE_CLOUD_PROJECT_ID=city-pulse-notifications-xxxxx
GOOGLE_APPLICATION_CREDENTIALS=./gcp-service-account.json

# AI Configuration
USE_REAL_AI=true
GOOGLE_API_KEY=your-google-ai-api-key-here
AI_MODEL=gemini-2.0-flash
AI_CONFIDENCE_THRESHOLD=0.7
AI_LEARNING_ENABLED=true
AI_EXPLANATION_REQUIRED=true
AI_FALLBACK_ENABLED=true
```

## 📱 Testing Without Real Mobile App (Quick Start)

### Option 1: Console Testing (Recommended for beginners)
```python
# Create test_simple_notifications.py
import asyncio
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from notification_agent.agent import NotificationAgent

async def test_basic_notification():
    """Test basic notification without Firebase/PubSub"""
    agent = NotificationAgent(
        use_firebase=False,  # Disable Firebase for testing
        use_pubsub=False     # Disable PubSub for testing
    )
    
    # Test data
    test_event = {
        "type": "flooding",
        "severity": "high",
        "location": "HSR Layout",
        "description": "Heavy waterlogging reported",
        "coordinates": {"lat": 12.9081, "lng": 77.6476}
    }
    
    # Generate notification
    result = await agent.process_event(test_event)
    print(f"📱 Notification Generated: {result}")

if __name__ == "__main__":
    asyncio.run(test_basic_notification())
```

### Option 2: Mock Firebase Testing
```python
# Create test_mock_firebase.py
import asyncio
from notification_agent.agent import NotificationAgent

class MockFirebaseService:
    """Mock Firebase for testing"""
    async def send_notification(self, tokens, title, body, data=None):
        print(f"🔥 MOCK FIREBASE NOTIFICATION:")
        print(f"   Title: {title}")
        print(f"   Body: {body}")
        print(f"   Tokens: {tokens}")
        print(f"   Data: {data}")
        return {"success": len(tokens), "failure": 0}

async def test_with_mock_firebase():
    agent = NotificationAgent(use_firebase=False)
    agent.firebase_service = MockFirebaseService()  # Inject mock
    
    test_event = {
        "type": "emergency",
        "severity": "critical",
        "location": "Whitefield",
        "description": "Building collapse reported"
    }
    
    result = await agent.process_event(test_event)
    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test_with_mock_firebase())
```

## 🧪 Full Integration Testing

### Step 1: Install Dependencies
```bash
cd notifications
pip install -r requirements.txt
pip install python-dotenv  # For .env file support
```

### Step 2: Copy Configuration
```bash
cp notification_agent/config_template.py notification_agent/config.py
# Edit config.py with your actual values
```

### Step 3: Run Tests
```bash
# Test AI capabilities
python demo_ai_capabilities.py

# Test notification processing
python test_notification_agent.py

# Test cross-agent communication
python test_cross_agent_notifications.py

# Test PubSub integration
python run_notification_service.py
```

## 🔧 Troubleshooting

### Common Issues:

**1. Firebase Authentication Error**
```bash
Error: DefaultCredentialsError
Solution: Set GOOGLE_APPLICATION_CREDENTIALS environment variable
```

**2. PubSub Permission Denied**
```bash
Error: 403 Permission denied
Solution: Check service account has Pub/Sub Editor role
```

**3. AI API Quota Exceeded**
```bash
Error: Quota exceeded
Solution: Check Google AI Studio quota limits
```

**4. Import Errors**
```bash
Error: ModuleNotFoundError
Solution: Run from notifications directory and check sys.path
```

## 📊 Testing Scenarios

### Scenario 1: Emergency Alert
```python
emergency_event = {
    "type": "emergency",
    "severity": "critical",
    "location": "MG Road",
    "description": "Gas leak detected near metro station",
    "coordinates": {"lat": 12.9716, "lng": 77.6412},
    "timestamp": "2025-01-26T10:30:00Z"
}
```

### Scenario 2: Weather Alert
```python
weather_event = {
    "type": "weather",
    "severity": "high", 
    "location": "Electronic City",
    "description": "Heavy rainfall warning - 50mm expected",
    "coordinates": {"lat": 12.8456, "lng": 77.6603}
}
```

### Scenario 3: Traffic Alert
```python
traffic_event = {
    "type": "traffic",
    "severity": "medium",
    "location": "Outer Ring Road",
    "description": "Major accident causing 2-hour delays"
}
```

## 🎯 Success Indicators

✅ **Firebase Working**: Notifications appear in Firebase Console
✅ **PubSub Working**: Messages received in subscriptions  
✅ **AI Working**: Intelligent pattern detection with explanations
✅ **Integration Working**: Real-time processing of multi-agent data

## 🚀 Next Steps

1. **Start Simple**: Use console testing first
2. **Add Firebase**: Configure real notifications
3. **Enable PubSub**: Connect to other agents
4. **Scale Up**: Add real user devices and mobile app

## 📞 Getting Help

- Firebase Issues: [Firebase Support](https://firebase.google.com/support)
- Google Cloud Issues: [GCP Support](https://cloud.google.com/support)
- AI API Issues: [Google AI Support](https://aistudio.google.com/)

## 💡 Pro Tips

- Use Firebase Emulator for local testing
- Monitor PubSub metrics in Google Cloud Console
- Check AI API usage in Google AI Studio
- Enable logging for better debugging
- Start with mock services before real integration
