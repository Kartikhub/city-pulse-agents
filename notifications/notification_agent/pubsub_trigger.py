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
import logging
from typing import Dict, Any, Callable
from concurrent.futures import ThreadPoolExecutor
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.subscriber.message import Message

from .agent import (
    PatternDetector, 
    FirebaseNotificationService, 
    NotificationGenerator,
    analyze_patterns_and_trigger_notifications
)


class PubSubNotificationTrigger:
    """
    PubSub listener that triggers notifications based on incoming city data.
    
    This service listens to various PubSub topics for:
    - User report submissions
    - Environmental sensor data
    - Event updates
    - Emergency alerts
    
    When patterns or thresholds are detected, it automatically triggers notifications.
    """
    
    def __init__(self, project_id: str, subscription_patterns: Dict[str, str]):
        """
        Initialize PubSub notification trigger.
        
        Args:
            project_id: Google Cloud project ID
            subscription_patterns: Dict mapping subscription names to topic patterns
        """
        self.project_id = project_id
        self.subscription_patterns = subscription_patterns
        self.subscriber = pubsub_v1.SubscriberClient()
        self.pattern_detector = PatternDetector()
        self.notification_generator = NotificationGenerator()
        self.firebase_service = FirebaseNotificationService()
        self.executor = ThreadPoolExecutor(max_workers=10)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Message buffers for pattern analysis
        self.message_buffers = {
            "user_reports": [],
            "environmental_data": [],
            "events": [],
            "emergencies": []
        }
        
        # Callback mapping
        self.message_handlers = {
            "user-reports": self._handle_user_report,
            "environmental-data": self._handle_environmental_data,
            "events": self._handle_event_data,
            "emergencies": self._handle_emergency_data
        }
    
    async def start_listening(self):
        """Start listening to all configured PubSub subscriptions."""
        self.logger.info("Starting PubSub notification trigger service...")
        
        tasks = []
        for subscription_name, topic_pattern in self.subscription_patterns.items():
            subscription_path = self.subscriber.subscription_path(
                self.project_id, subscription_name
            )
            
            # Create subscription if it doesn't exist
            try:
                self.subscriber.create_subscription(
                    request={"name": subscription_path, "topic": f"projects/{self.project_id}/topics/{topic_pattern}"}
                )
                self.logger.info(f"Created subscription: {subscription_name}")
            except Exception as e:
                self.logger.info(f"Subscription {subscription_name} already exists or couldn't be created: {e}")
            
            # Start listening
            task = asyncio.create_task(
                self._listen_to_subscription(subscription_path, subscription_name)
            )
            tasks.append(task)
        
        # Start pattern analysis task
        tasks.append(asyncio.create_task(self._periodic_pattern_analysis()))
        
        # Wait for all tasks
        await asyncio.gather(*tasks)
    
    async def _listen_to_subscription(self, subscription_path: str, subscription_name: str):
        """Listen to a specific PubSub subscription."""
        self.logger.info(f"Listening to subscription: {subscription_name}")
        
        def callback(message: Message):
            """Handle incoming PubSub message."""
            try:
                # Decode message
                data = json.loads(message.data.decode('utf-8'))
                
                # Route to appropriate handler
                handler = self.message_handlers.get(subscription_name)
                if handler:
                    asyncio.run_coroutine_threadsafe(
                        handler(data), 
                        asyncio.get_event_loop()
                    )
                
                # Acknowledge message
                message.ack()
                
            except Exception as e:
                self.logger.error(f"Error processing message from {subscription_name}: {e}")
                message.nack()
        
        # Start pulling messages
        flow_control = pubsub_v1.types.FlowControl(max_messages=100)
        streaming_pull_future = self.subscriber.subscribe(
            subscription_path, 
            callback=callback,
            flow_control=flow_control
        )
        
        try:
            # Keep the subscription alive
            streaming_pull_future.result()
        except KeyboardInterrupt:
            streaming_pull_future.cancel()
            self.logger.info(f"Stopped listening to {subscription_name}")
    
    async def _handle_user_report(self, data: Dict[str, Any]):
        """Handle incoming user report data."""
        self.logger.info(f"Received user report: {data.get('incidentType')} in {data.get('location')}")
        
        # Add to buffer for pattern analysis
        self.message_buffers["user_reports"].append(data)
        
        # Check for immediate triggers (emergency situations)
        if data.get("incidentType", "").lower() == "emergency":
            await self._trigger_emergency_notification(data)
        
        # Check for cluster formation
        await self._check_incident_cluster(data)
    
    async def _handle_environmental_data(self, data: Dict[str, Any]):
        """Handle incoming environmental sensor data."""
        self.logger.info(f"Received environmental data for {data.get('location')}")
        
        # Add to buffer
        self.message_buffers["environmental_data"].append(data)
        
        # Check for environmental anomalies
        await self._check_environmental_anomaly(data)
    
    async def _handle_event_data(self, data: Dict[str, Any]):
        """Handle incoming event data."""
        self.logger.info(f"Received event data: {data.get('name')} in {data.get('location')}")
        
        # Add to buffer
        self.message_buffers["events"].append(data)
        
        # Check for event-based notifications
        await self._check_event_notifications(data)
    
    async def _handle_emergency_data(self, data: Dict[str, Any]):
        """Handle incoming emergency data."""
        self.logger.critical(f"EMERGENCY: {data.get('description')} in {data.get('location')}")
        
        # Immediate emergency notification
        await self._trigger_emergency_notification(data)
    
    async def _check_incident_cluster(self, new_report: Dict[str, Any]):
        """Check if new report forms a cluster with recent reports."""
        location = new_report.get("location")
        incident_type = new_report.get("incidentType")
        
        # Get recent reports for same location and type
        recent_reports = [
            report for report in self.message_buffers["user_reports"][-20:]  # Last 20 reports
            if (report.get("location") == location and 
                report.get("incidentType") == incident_type)
        ]
        
        # Check for cluster
        cluster = self.pattern_detector.detect_event_cluster(recent_reports)
        
        if cluster and cluster.count >= 3:
            notification = self.notification_generator.generate_cluster_notification(cluster)
            
            # Send notification to users in the area
            await self._send_location_based_notification(notification, location, cluster.affected_radius_km)
            
            self.logger.warning(f"Cluster detected: {cluster.count} {cluster.event_type} incidents in {cluster.location}")
    
    async def _check_environmental_anomaly(self, env_data: Dict[str, Any]):
        """Check for environmental anomalies that require notifications."""
        location = env_data.get("location")
        
        # Example: Air quality anomaly
        if "air_quality_index" in env_data:
            aqi = env_data["air_quality_index"]
            if aqi > 150:  # Unhealthy level
                notification_data = {
                    "title": f"⚠️ Air Quality Alert - {location}",
                    "body": f"Air quality in {location} is unhealthy (AQI: {aqi}). Limit outdoor activities.",
                    "priority": "high",
                    "event_type": "environmental",
                    "location": location,
                    "predicted_impact": "Health impact for sensitive individuals"
                }
                
                await self._send_location_based_notification(notification_data, location, 5.0)
        
        # Example: Temperature anomaly
        if "temperature" in env_data:
            temp = env_data["temperature"]
            if temp > 40:  # Extreme heat
                notification_data = {
                    "title": f"🌡️ Heat Wave Alert - {location}",
                    "body": f"Extreme heat detected in {location} ({temp}°C). Stay hydrated and avoid outdoor activities.",
                    "priority": "high",
                    "event_type": "environmental",
                    "location": location,
                    "predicted_impact": "Heat-related health risks"
                }
                
                await self._send_location_based_notification(notification_data, location, 10.0)
    
    async def _check_event_notifications(self, event_data: Dict[str, Any]):
        """Check if users should be notified about nearby events."""
        location = event_data.get("location")
        event_time = event_data.get("time")
        
        # Notify users about events happening within 24 hours
        notification = self.notification_generator.generate_event_notification(event_data)
        
        await self._send_location_based_notification(notification.__dict__, location, 10.0)
        
        self.logger.info(f"Event notification sent for {event_data.get('name')} in {location}")
    
    async def _trigger_emergency_notification(self, emergency_data: Dict[str, Any]):
        """Trigger immediate emergency notification."""
        location = emergency_data.get("location", "Unknown")
        description = emergency_data.get("description", "Emergency situation")
        
        notification_data = {
            "title": f"🚨 EMERGENCY ALERT - {location}",
            "body": f"URGENT: {description} in {location}. Please follow official guidance and stay safe.",
            "priority": "high",
            "event_type": "emergency",
            "location": location,
            "predicted_impact": "Immediate safety concern"
        }
        
        # Send to all users within 15km radius
        await self._send_location_based_notification(notification_data, location, 15.0)
        
        self.logger.critical(f"Emergency notification sent for {location}: {description}")
    
    async def _send_location_based_notification(self, notification_data: Dict[str, Any], location: str, radius_km: float):
        """Send notification to users within specified radius of location."""
        # Mock implementation - in real scenario, query user database by location
        affected_users = self._get_users_in_radius(location, radius_km)
        
        if affected_users:
            # Create notification object
            from .agent import NotificationData
            notification = NotificationData(
                title=notification_data.get("title", "City Alert"),
                body=notification_data.get("body", "City notification"),
                priority=notification_data.get("priority", "normal"),
                target_users=[f"device_token_{user}" for user in affected_users],
                event_type=notification_data.get("event_type", "info"),
                location=location,
                predicted_impact=notification_data.get("predicted_impact", "General information")
            )
            
            # Send via Firebase
            result = await self.firebase_service.send_notification(notification)
            
            self.logger.info(f"Notification sent to {len(affected_users)} users in {location} (radius: {radius_km}km)")
            return result
        
        return {"status": "no_users_found"}
    
    def _get_users_in_radius(self, location: str, radius_km: float) -> list:
        """Get users within specified radius of location (mock implementation)."""
        # In real implementation, this would query a user location database
        # using geospatial queries with latitude/longitude coordinates
        
        from .config_template import MOCK_USER_LOCATIONS
        
        # Simple mock: return users if location matches exactly or within major areas
        nearby_areas = {
            "HSR Layout": ["Koramangala", "BTM Layout"],
            "Whitefield": ["Marathahalli"],
            "Koramangala": ["HSR Layout", "Indiranagar"],
            "Indiranagar": ["Koramangala"],
            "BTM Layout": ["HSR Layout", "JP Nagar"]
        }
        
        users = MOCK_USER_LOCATIONS.get(location, [])
        
        # Add users from nearby areas if radius is large enough
        if radius_km > 8.0:
            for nearby_area in nearby_areas.get(location, []):
                users.extend(MOCK_USER_LOCATIONS.get(nearby_area, []))
        
        return list(set(users))  # Remove duplicates
    
    async def _periodic_pattern_analysis(self):
        """Periodically analyze patterns and send predictive notifications."""
        while True:
            try:
                await asyncio.sleep(300)  # Run every 5 minutes
                
                # Analyze patterns in buffered data
                self.logger.info("Running periodic pattern analysis...")
                
                # Analyze user reports for patterns
                if len(self.message_buffers["user_reports"]) > 10:
                    await self._analyze_report_patterns()
                
                # Clear old data from buffers (keep last 100 messages)
                for buffer_name in self.message_buffers:
                    if len(self.message_buffers[buffer_name]) > 100:
                        self.message_buffers[buffer_name] = self.message_buffers[buffer_name][-100:]
                
            except Exception as e:
                self.logger.error(f"Error in periodic pattern analysis: {e}")
    
    async def _analyze_report_patterns(self):
        """Analyze patterns in user reports and generate predictive notifications."""
        reports = self.message_buffers["user_reports"]
        
        # Group by location
        location_patterns = {}
        for report in reports:
            location = report.get("location", "unknown")
            if location not in location_patterns:
                location_patterns[location] = []
            location_patterns[location].append(report)
        
        # Analyze each location for prediction opportunities
        for location, loc_reports in location_patterns.items():
            if len(loc_reports) >= 5:  # Need sufficient data for prediction
                
                # Get prediction for this location
                prediction = self.pattern_detector.predict_future_risk(
                    location, 
                    loc_reports[0].get("incidentType", "general")
                )
                
                # Send predictive notification if risk is significant
                if prediction["risk_level"] in ["HIGH", "MEDIUM"] and prediction["confidence"] > 0.6:
                    pred_notification = self.notification_generator.generate_predictive_notification(
                        location, prediction
                    )
                    
                    if pred_notification:
                        await self._send_location_based_notification(
                            pred_notification.__dict__, 
                            location, 
                            8.0
                        )
                        
                        self.logger.info(f"Predictive notification sent for {location}: {prediction['risk_level']} risk")


# Example usage and configuration
async def main():
    """Main function to start the PubSub notification trigger service."""
    
    # Configuration
    project_id = "your-google-cloud-project-id"
    subscription_patterns = {
        "user-reports": "user-reports-topic",
        "environmental-data": "environmental-data-topic", 
        "events": "events-topic",
        "emergencies": "emergencies-topic"
    }
    
    # Create and start the service
    trigger_service = PubSubNotificationTrigger(project_id, subscription_patterns)
    
    try:
        await trigger_service.start_listening()
    except KeyboardInterrupt:
        print("Shutting down PubSub notification trigger service...")


if __name__ == "__main__":
    asyncio.run(main())
