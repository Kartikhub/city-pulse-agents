# City Pulse Notification Agent 📱

An intelligent notification agent that provides predictive and personalized push notifications based on patterns, triggers, and user location data. The agent analyzes city data streams and automatically sends relevant alerts to keep citizens informed and safe.

## 🌟 Features

### 1. Cross-Agent Pattern Detection 🔗
- **Multi-Agent Data Correlation**: Analyzes data from multiple city agents simultaneously
- **Infrastructure-Environment Correlation**: Detects when infrastructure events coincide with environmental changes
- **User Report Validation**: Validates citizen reports against official event data
- **Systemic Stress Detection**: Identifies city-wide system stress patterns
- **Cascading Failure Analysis**: Predicts potential cascading failures across systems

### 2. AI-Powered Pattern Recognition 🤖
- **Intelligent Clustering**: Uses AI to determine concerning event clusters
- **Contextual Analysis**: Considers multiple factors beyond simple thresholds
- **Adaptive Thresholds**: Adjusts sensitivity based on event type and location
- **Anomaly Detection**: Statistical and AI-based anomaly identification
- **Predictive Modeling**: Risk prediction with confidence scoring

### 3. Smart Notification Generation 📬
- **Pattern-Specific Templates**: Different notification styles for different patterns
- **Severity-Based Prioritization**: CRITICAL > HIGH > MEDIUM > LOW
- **Location-Aware Targeting**: Notifications sent to users in affected areas
- **Cross-Agent Alerts**: Special notifications for multi-system events
- **Actionable Recommendations**: AI-generated recommended actions

### 4. Firebase Push Notification System 📲
- **Real-time Delivery**: Instant push notifications via Firebase FCM
- **Device Token Management**: Secure device registration and targeting
- **Rich Notifications**: Support for custom data, actions, and rich media
- **Delivery Tracking**: Monitor notification success and failure rates
- **Mock Mode**: Development-friendly mock notifications for testing

### 5. Multi-Agent Integration 🤝
- **Event Agent**: Monitors city events and activities
- **Environment Agent**: Tracks weather and environmental conditions  
- **User Report Agent**: Analyzes citizen reports and incidents
- **Real-time Data Streams**: Continuous monitoring and analysis
- **Agent-to-Agent Communication**: Seamless data sharing between agents

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Event Agent   │    │Environment Agent│    │User Report Agent│
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                    ┌─────────────▼─────────────┐
                    │   Notification Agent     │
                    │                          │
                    │  ┌─────────────────────┐ │
                    │  │ Pattern Detector    │ │ ← AI-powered analysis
                    │  │ - Event Clustering  │ │
                    │  │ - Cross-Agent AI    │ │
                    │  │ - Anomaly Detection │ │
                    │  │ - Risk Prediction   │ │
                    │  └─────────────────────┘ │
                    │  ┌─────────────────────┐ │
                    │  │ Notification Gen.   │ │ ← Smart templates
                    │  │ - Context-aware     │ │
                    │  │ - Multi-pattern     │ │
                    │  │ - Personalized     │ │
                    │  └─────────────────────┘ │
                    │  ┌─────────────────────┐ │
                    │  │ Firebase Service    │ │ ← Push delivery
                    │  │ - FCM Integration   │ │
                    │  │ - Device Management │ │
                    │  │ - Delivery Tracking │ │
                    │  └─────────────────────┘ │
                    └─────────────┬───────────┘
                                  │
                         ┌─────────▼─────────┐
                         │  Citizens' Mobile │
                         │     Devices       │
                         └───────────────────┘
```

## 🔄 Cross-Agent Notification Flow

### 1. Data Collection Phase
```
Event Agent ────┐
                ├─→ Pattern Detector ─→ AI Analysis ─→ Cross-Agent Patterns
Environment ────┤
Agent           │
                │
User Reports ───┘
```

### 2. Pattern Detection Types

#### Infrastructure-Environment Correlation
- **Trigger**: Infrastructure events + Environmental stress
- **Example**: Power outages during extreme heat
- **Action**: Enhanced monitoring, emergency cooling centers

#### User Report Validation  
- **Trigger**: Citizen reports + Official event data alignment
- **Example**: User flooding reports confirmed by sensors
- **Action**: Prioritize similar user reports, validate crowd-sourced data

#### Systemic Stress Detection
- **Trigger**: Multiple systems showing high activity
- **Example**: Power + Traffic + Emergency all spiking
- **Action**: City-wide emergency protocol activation

#### Power Grid Instability
- **Trigger**: Multiple power-related incidents across city
- **Example**: Rolling blackouts in different areas
- **Action**: Grid stability checks, backup system activation

### 3. Notification Delivery Process
```
Pattern Detection → Severity Assessment → User Targeting → Firebase → Mobile Device
      ↓                     ↓                   ↓            ↓         ↓
   AI Analysis      CRITICAL/HIGH/MEDIUM    Location-based   FCM     Push Alert
                         ↓                      ↓                       ↓
                  Notification Template    Device Tokens          User Action
```
                    │  └─────────────────────┘ │
                    └─────────────┬───────────┘
                                  │
                         ┌────────▼────────┐
                         │  Push Notifications │
                         │  📱 📱 📱 📱 📱  │
                         └─────────────────┘
```

## 📦 Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Firebase**:
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com)
   - Enable Cloud Messaging (FCM)
   - Download service account key JSON file
   - Update `config_template.py` with your Firebase credentials

3. **Configure Google Cloud PubSub** (Optional):
   - Enable PubSub API in Google Cloud Console
   - Create topics and subscriptions for data streams
   - Update project ID in configuration

## ⚙️ Configuration

1. **Copy and customize configuration**:
   ```bash
   cp config_template.py config.py
   ```

2. **Update Firebase settings** in `config.py`:
   ```python
   FIREBASE_CONFIG = {
       "service_account_path": "path/to/your/firebase-key.json",
       "project_id": "your-firebase-project-id",
       "database_url": "https://your-project.firebaseio.com/"
   }
   ```

3. **Customize notification settings**:
   ```python
   NOTIFICATION_SETTINGS = {
       "default_radius_km": 5.0,
       "cluster_threshold": 3,
       "time_window_minutes": 20,
       "max_notifications_per_user_per_hour": 5
   }
   ```

## 🚀 Usage

### As a Standalone Agent

```python
from notification_agent.agent import notification_agent

# The agent can be used directly for queries
response = await notification_agent.generate_content(
    "Analyze current patterns and send notifications if needed"
)
```

### With PubSub Triggers

```python
from notification_agent.pubsub_trigger import PubSubNotificationTrigger

# Setup PubSub listener
project_id = "your-google-cloud-project"
subscriptions = {
    "user-reports": "user-reports-topic",
    "environmental-data": "environmental-data-topic",
    "events": "events-topic",
    "emergencies": "emergencies-topic"
}

trigger_service = PubSubNotificationTrigger(project_id, subscriptions)
await trigger_service.start_listening()
```

### Manual Notification Triggers

```python
from notification_agent.agent import analyze_patterns_and_trigger_notifications

# Analyze patterns and trigger notifications
result = await analyze_patterns_and_trigger_notifications(
    trigger_type="auto",
    events_data="all",
    user_reports_data="all"
)
```

## 📊 Notification Types

### 1. Cluster Alerts
**Triggered when**: Multiple similar incidents occur in the same area
```
🚨 Infrastructure Alert - HSR Layout
Multiple power cut reports (5) detected in HSR Layout within 20 minutes. 
Exercise caution in the area.
```

### 2. Predictive Alerts
**Triggered when**: Historical patterns indicate increased risk
```
🔮 High Risk Alert - Koramangala
Based on recent patterns, there's a 82% chance of incidents in 
Koramangala within next 3-6 hours. Stay alert.
```

### 3. Environmental Alerts
**Triggered when**: Environmental conditions exceed thresholds
```
⚠️ Air Quality Alert - Whitefield
Air quality in Whitefield is unhealthy (AQI: 165). 
Limit outdoor activities.
```

### 4. Event Notifications
**Triggered when**: Events happening near user location
```
🎉 Upcoming Event - Convention Center
Tech Conference happening tomorrow at 9:00 AM. Check it out!
```

### 5. Emergency Alerts
**Triggered when**: Critical situations require immediate attention
```
🚨 EMERGENCY ALERT - Downtown
URGENT: Gas leak reported in Downtown. Please avoid the area 
and follow official guidance.
```

## 🛠️ API Functions

### `analyze_patterns_and_trigger_notifications()`
Analyzes city data patterns and triggers intelligent notifications.

**Parameters**:
- `events_data`: Events data to analyze (default: "all")
- `environment_data`: Environmental data (default: "all")
- `user_reports_data`: User reports data (default: "all")
- `trigger_type`: "auto", "threshold", "prediction", or "emergency"

### `get_user_location_preferences()`
Retrieves user location preferences and notification settings.

**Parameters**:
- `user_id`: Specific user ID or "all" for all users

### `send_personalized_notification()`
Sends personalized notifications to specific users.

**Parameters**:
- `user_ids`: Comma-separated user IDs or "all"
- `notification_type`: "emergency", "info", "event", or "prediction"
- `location`: Location context
- `custom_message`: Custom message content

## 🔧 Customization

### Pattern Detection Thresholds
Customize in `config.py`:
```python
PATTERN_DETECTION = {
    "severity_thresholds": {
        "emergency": {"critical": 3, "high": 2},
        "flooding": {"critical": 5, "high": 3},
        "infrastructure": {"critical": 8, "high": 5}
    }
}
```

### Notification Templates
Modify in `agent.py` - `NotificationGenerator` class:
```python
def generate_cluster_notification(self, cluster):
    # Customize notification content here
    title = f"{emoji} {cluster.event_type.title()} Alert - {cluster.location}"
    # ...
```

### User Targeting
Customize radius and targeting logic:
```python
def _calculate_affected_radius(self, event_type: str, count: int) -> float:
    # Customize affected radius calculation
    base_radius = {"flooding": 5.0, "infrastructure": 3.0}
    # ...
```

## 📈 Monitoring & Metrics

### Logging
The agent provides comprehensive logging:
- Pattern detection events
- Notification triggers
- User targeting metrics
- Firebase delivery status

### Metrics to Track
- **Notification Accuracy**: False positive/negative rates
- **User Engagement**: Notification open rates
- **Response Time**: Time from event to notification
- **Coverage**: Percentage of affected users reached

## 🔒 Security & Privacy

### Data Privacy
- User location data is anonymized
- Notification preferences are respected
- Device tokens are securely stored

### Rate Limiting
- Maximum notifications per user per hour
- Cooldown periods for similar alerts
- Emergency override capabilities

### Authentication
- Firebase service account authentication
- Google Cloud IAM for PubSub access
- Secure token management

## 🧪 Testing

### Unit Tests
```bash
pytest tests/test_pattern_detector.py
pytest tests/test_notification_generator.py
pytest tests/test_firebase_service.py
```

### Integration Tests
```bash
pytest tests/test_pubsub_integration.py
pytest tests/test_agent_integration.py
```

### Load Testing
```bash
# Test notification throughput
python tests/load_test_notifications.py
```

## 🚀 Deployment

### Local Development
```bash
python -m notification_agent.agent
```

### Production Deployment
1. **Docker Container**:
   ```bash
   docker build -t notification-agent .
   docker run -p 8004:8004 notification-agent
   ```

2. **Google Cloud Run**:
   ```bash
   gcloud run deploy notification-agent --source .
   ```

3. **Kubernetes**:
   ```bash
   kubectl apply -f k8s/deployment.yaml
   ```

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting guide
- Review logs for error details

## 🔮 Future Enhancements

- **Machine Learning Models**: Advanced prediction algorithms
- **Multi-modal Notifications**: SMS, email, voice calls
- **Geofencing**: More precise location targeting
- **A/B Testing**: Optimize notification content
- **Analytics Dashboard**: Real-time monitoring interface
