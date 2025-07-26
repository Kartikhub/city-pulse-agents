# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import json
import pytest
from unittest.mock import Mock, patch
from notification_agent.agent import (
    PatternDetector,
    NotificationGenerator,
    FirebaseNotificationService,
    EventCluster,
    NotificationData,
    analyze_patterns_and_trigger_notifications
)


class TestPatternDetector:
    """Test cases for pattern detection functionality."""
    
    def setup_method(self):
        self.detector = PatternDetector()
    
    def test_detect_event_cluster_with_sufficient_events(self):
        """Test cluster detection with enough events."""
        events = [
            {"incidentType": "Infrastructure", "location": "HSR Layout"},
            {"incidentType": "Infrastructure", "location": "HSR Layout"},
            {"incidentType": "Infrastructure", "location": "HSR Layout"},
            {"incidentType": "Infrastructure", "location": "HSR Layout"}
        ]
        
        cluster = self.detector.detect_event_cluster(events)
        
        assert cluster is not None
        assert cluster.event_type == "Infrastructure"
        assert cluster.location == "HSR Layout"
        assert cluster.count == 4
        assert cluster.severity in ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    
    def test_detect_event_cluster_insufficient_events(self):
        """Test cluster detection with insufficient events."""
        events = [
            {"incidentType": "Infrastructure", "location": "HSR Layout"},
            {"incidentType": "Infrastructure", "location": "HSR Layout"}
        ]
        
        cluster = self.detector.detect_event_cluster(events)
        assert cluster is None
    
    def test_calculate_severity_emergency(self):
        """Test severity calculation for emergency events."""
        severity = self.detector._calculate_severity(3, "Emergency")
        assert severity == "HIGH"
        
        severity = self.detector._calculate_severity(5, "Emergency")
        assert severity == "CRITICAL"
    
    def test_calculate_affected_radius(self):
        """Test affected radius calculation."""
        radius = self.detector._calculate_affected_radius("flooding", 3)
        assert radius > 5.0
        assert radius <= 15.0
    
    def test_anomaly_detection(self):
        """Test anomaly detection algorithm."""
        historical_values = [10, 12, 11, 9, 10, 11, 12]
        
        # Normal value should not be anomalous
        assert not self.detector.detect_anomaly(10.5, historical_values)
        
        # Extreme value should be anomalous
        assert self.detector.detect_anomaly(25, historical_values)
    
    def test_predict_future_risk(self):
        """Test future risk prediction."""
        prediction = self.detector.predict_future_risk("HSR Layout", "Infrastructure")
        
        assert "risk_level" in prediction
        assert "confidence" in prediction
        assert prediction["risk_level"] in ["LOW", "MEDIUM", "HIGH", "UNKNOWN"]


class TestNotificationGenerator:
    """Test cases for notification generation."""
    
    def setup_method(self):
        self.generator = NotificationGenerator()
    
    def test_generate_cluster_notification_critical(self):
        """Test cluster notification generation for critical severity."""
        cluster = EventCluster(
            event_type="Emergency",
            location="Downtown",
            count=5,
            severity="CRITICAL",
            time_window="15 minutes",
            affected_radius_km=10.0
        )
        
        notification = self.generator.generate_cluster_notification(cluster)
        
        assert "🚨" in notification.title
        assert "URGENT" in notification.body
        assert notification.priority == "high"
        assert notification.event_type == "Emergency"
        assert notification.location == "Downtown"
    
    def test_generate_cluster_notification_low(self):
        """Test cluster notification generation for low severity."""
        cluster = EventCluster(
            event_type="Maintenance",
            location="Koramangala",
            count=3,
            severity="LOW",
            time_window="30 minutes",
            affected_radius_km=2.0
        )
        
        notification = self.generator.generate_cluster_notification(cluster)
        
        assert notification.priority == "normal"
        assert "Authorities have been notified" in notification.body
    
    def test_generate_predictive_notification_high_risk(self):
        """Test predictive notification for high risk."""
        prediction = {
            "risk_level": "HIGH",
            "confidence": 0.85,
            "predicted_time": "next 3-6 hours"
        }
        
        notification = self.generator.generate_predictive_notification("Whitefield", prediction)
        
        assert notification is not None
        assert "🔮" in notification.title
        assert "85%" in notification.body
        assert notification.event_type == "prediction"
    
    def test_generate_predictive_notification_low_risk(self):
        """Test that low risk predictions don't generate notifications."""
        prediction = {
            "risk_level": "LOW",
            "confidence": 0.3,
            "predicted_time": "next 24-48 hours"
        }
        
        notification = self.generator.generate_predictive_notification("BTM Layout", prediction)
        assert notification is None
    
    def test_generate_event_notification(self):
        """Test event notification generation."""
        event_data = {
            "name": "Summer Music Festival",
            "location": "Central Park",
            "time": "Saturday 7 PM"
        }
        
        notification = self.generator.generate_event_notification(event_data)
        
        assert "🎉" in notification.title
        assert "Summer Music Festival" in notification.body
        assert notification.event_type == "event"
        assert notification.location == "Central Park"


class TestFirebaseNotificationService:
    """Test cases for Firebase notification service."""
    
    def setup_method(self):
        self.service = FirebaseNotificationService()
    
    @pytest.mark.asyncio
    async def test_send_notification_mock(self):
        """Test notification sending with mock Firebase."""
        notification = NotificationData(
            title="Test Notification",
            body="This is a test notification",
            priority="normal",
            target_users=["device_token_1", "device_token_2"],
            event_type="test",
            location="Test Location",
            predicted_impact="No impact"
        )
        
        # Since Firebase is not initialized, this should return mock response
        result = await self.service.send_notification(notification)
        
        assert result["status"] == "success"
        assert "Mock notification sent" in result["message"]
        assert result["notification_preview"]["title"] == "Test Notification"


class TestIntegration:
    """Integration tests for the notification agent."""
    
    @pytest.mark.asyncio
    async def test_analyze_patterns_and_trigger_notifications(self):
        """Test the main pattern analysis and notification function."""
        result_json = await analyze_patterns_and_trigger_notifications(
            trigger_type="auto"
        )
        
        result = json.loads(result_json)
        
        assert result["status"] == "success"
        assert "analysis_timestamp" in result
        assert "patterns_detected" in result
        assert "notifications_sent" in result
        assert "predictions" in result
        assert len(result["notifications_sent"]) > 0
    
    @pytest.mark.asyncio
    async def test_analyze_patterns_emergency_trigger(self):
        """Test emergency trigger analysis."""
        result_json = await analyze_patterns_and_trigger_notifications(
            trigger_type="emergency"
        )
        
        result = json.loads(result_json)
        assert result["trigger_type"] == "emergency"
    
    @pytest.mark.asyncio
    async def test_analyze_patterns_prediction_trigger(self):
        """Test prediction trigger analysis."""
        result_json = await analyze_patterns_and_trigger_notifications(
            trigger_type="prediction"
        )
        
        result = json.loads(result_json)
        assert result["trigger_type"] == "prediction"


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
