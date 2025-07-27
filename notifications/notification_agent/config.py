# Simple Configuration for Testing Without External Services
# This config file allows you to test the notification agent locally

import os

# Test Mode Configuration
TEST_MODE = True  # Set to False when using real Firebase/PubSub

# Firebase Configuration (for testing - disabled by default)
FIREBASE_CONFIG = {
    "service_account_path": os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", ""),
    "project_id": os.getenv("FIREBASE_PROJECT_ID", "test-project"),
    "database_url": os.getenv("FIREBASE_DATABASE_URL", ""),
    "enabled": os.getenv("FIREBASE_ENABLED", "false").lower() == "true"
}

# Google Cloud PubSub Configuration (for testing - disabled by default)
PUBSUB_CONFIG = {
    "enabled": False,
    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID", "test-project"),
    "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""),
    "enabled": os.getenv("PUBSUB_ENABLED", "false").lower() == "true",
    "subscription_patterns": {
        "user-reports": "user-reports-topic",
        "environmental-data": "environmental-data-topic", 
        "events": "events-topic",
        "emergencies": "emergencies-topic"
    }
}

# AI Agent Configuration
AI_AGENT_CONFIG = {
    "use_real_ai": os.getenv("USE_REAL_AI", "true").lower() == "true",
    "model": os.getenv("AI_MODEL", "gemini-2.0-flash"),
    "api_key": os.getenv("GOOGLE_API_KEY", ""),  # Add your API key here or in .env
    "confidence_threshold": float(os.getenv("AI_CONFIDENCE_THRESHOLD", "0.7")),
    "learning_enabled": os.getenv("AI_LEARNING_ENABLED", "true").lower() == "true",
    "explanation_required": os.getenv("AI_EXPLANATION_REQUIRED", "true").lower() == "true",
    "fallback_to_simulation": os.getenv("AI_FALLBACK_ENABLED", "true").lower() == "true",
    "response_timeout": float(os.getenv("AI_RESPONSE_TIMEOUT", "5.0"))
}

# Notification Settings
NOTIFICATION_SETTINGS = {
    "default_radius_km": 5.0,
    "max_radius_km": 15.0,
    "cluster_threshold": 3,
    "anomaly_threshold": 2.0,
    "time_window_minutes": 20,
    "max_notifications_per_user_per_hour": 5,
}

# Pattern Detection Settings
PATTERN_DETECTION = {
    "min_historical_data_points": 5,
    "prediction_confidence_threshold": 0.6,
    "severity_thresholds": {
        "emergency": {"critical": 3, "high": 2},
        "flooding": {"critical": 5, "high": 3},
        "infrastructure": {"critical": 8, "high": 5},
        "maintenance": {"critical": 10, "high": 7}
    }
}

# Mock User Locations for Testing
MOCK_USER_LOCATIONS = {
    "HSR Layout": ["user1@test.com", "user2@test.com"],
    "Whitefield": ["user3@test.com", "user4@test.com"],
    "Koramangala": ["user5@test.com", "user6@test.com"],
    "Indiranagar": ["user7@test.com", "user8@test.com"],
    "BTM Layout": ["user9@test.com", "user10@test.com"]
}

# Bangalore Area Coordinates
BANGALORE_AREAS = {
    "HSR Layout": {"lat": 12.9081, "lng": 77.6476},
    "Whitefield": {"lat": 12.9698, "lng": 77.7500},
    "Koramangala": {"lat": 12.9279, "lng": 77.6271},
    "Indiranagar": {"lat": 12.9716, "lng": 77.6412},
    "BTM Layout": {"lat": 12.9165, "lng": 77.6101},
    "Electronic City": {"lat": 12.8456, "lng": 77.6603},
    "Marathahalli": {"lat": 12.9591, "lng": 77.6974},
    "JP Nagar": {"lat": 12.9089, "lng": 77.5833},
    "MG Road": {"lat": 12.9716, "lng": 77.6412},
    "Outer Ring Road": {"lat": 12.9352, "lng": 77.6245}
}
