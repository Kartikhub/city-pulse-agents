# Firebase Configuration for Notification Agent
# Copy this file to config.py and update with your actual Firebase credentials

import os

# Firebase Configuration
FIREBASE_CONFIG = {
    "service_account_path": os.getenv("FIREBASE_SERVICE_ACCOUNT_PATH", "path/to/firebase-service-account.json"),
    "project_id": os.getenv("FIREBASE_PROJECT_ID", "your-firebase-project-id"),
    "database_url": os.getenv("FIREBASE_DATABASE_URL", "https://your-project.firebaseio.com/"),
    "enabled": os.getenv("FIREBASE_ENABLED", "false").lower() == "true"  # Enable/disable Firebase
}

# Google Cloud PubSub Configuration
PUBSUB_CONFIG = {
    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT_ID", "your-gcp-project-id"),
    "credentials_path": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "path/to/gcp-service-account.json"),
    "enabled": os.getenv("PUBSUB_ENABLED", "false").lower() == "true",  # Enable/disable PubSub
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
    "confidence_threshold": float(os.getenv("AI_CONFIDENCE_THRESHOLD", "0.7")),
    "learning_enabled": os.getenv("AI_LEARNING_ENABLED", "true").lower() == "true",
    "explanation_required": os.getenv("AI_EXPLANATION_REQUIRED", "true").lower() == "true",
    "fallback_to_simulation": os.getenv("AI_FALLBACK_ENABLED", "true").lower() == "true",
    "response_timeout": float(os.getenv("AI_RESPONSE_TIMEOUT", "5.0"))
}

# Notification Settings
NOTIFICATION_SETTINGS = {
    "default_radius_km": 5.0,  # Default notification radius in kilometers
    "max_radius_km": 15.0,     # Maximum notification radius
    "cluster_threshold": 3,     # Minimum events to form a cluster
    "anomaly_threshold": 2.0,   # Standard deviations for anomaly detection
    "time_window_minutes": 20,  # Time window for cluster detection
    "max_notifications_per_user_per_hour": 5,  # Rate limiting
}

# Pattern Detection Settings
PATTERN_DETECTION = {
    "min_historical_data_points": 5,  # Minimum data points for pattern analysis
    "prediction_confidence_threshold": 0.6,  # Minimum confidence for predictions
    "severity_thresholds": {
        "emergency": {"critical": 3, "high": 2},
        "flooding": {"critical": 5, "high": 3},
        "infrastructure": {"critical": 8, "high": 5},
        "maintenance": {"critical": 10, "high": 7}
    }
}

# User Location Data (Mock - in production, this would come from a database)
MOCK_USER_LOCATIONS = {
    "HSR Layout": ["user1", "user2"],
    "Whitefield": ["user3", "user4"],
    "Koramangala": ["user5", "user6"],
    "Indiranagar": ["user7", "user8"],
    "BTM Layout": ["user9", "user10"]
}

# Bangalore Area Coordinates (for distance calculations)
BANGALORE_AREAS = {
    "HSR Layout": {"lat": 12.9081, "lng": 77.6476},
    "Whitefield": {"lat": 12.9698, "lng": 77.7500},
    "Koramangala": {"lat": 12.9279, "lng": 77.6271},
    "Indiranagar": {"lat": 12.9716, "lng": 77.6412},
    "BTM Layout": {"lat": 12.9165, "lng": 77.6101},
    "Electronic City": {"lat": 12.8456, "lng": 77.6603},
    "Marathahalli": {"lat": 12.9591, "lng": 77.6974},
    "JP Nagar": {"lat": 12.9089, "lng": 77.5833}
}
