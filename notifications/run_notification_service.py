#!/usr/bin/env python3
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
import logging
import os
import sys
from pathlib import Path

# Add the notification_agent directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "notification_agent"))

from notification_agent.agent import notification_agent
from notification_agent.pubsub_trigger import PubSubNotificationTrigger


async def start_notification_service():
    """Start the notification agent service with PubSub triggers."""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('notification_agent.log'),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Starting City Pulse Notification Agent Service...")
    
    # Configuration from environment variables or defaults
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "expanded-aria-209314")
    
    subscription_patterns = {
        "user-reports": "user-reports-topic",
        "environmental-data": "environmental-data-topic", 
        "events": "events-topic",
        "emergencies": "emergencies-topic"
    }
    
    try:
        # Start PubSub trigger service
        logger.info("Initializing PubSub notification trigger service...")
        trigger_service = PubSubNotificationTrigger(project_id, subscription_patterns)
        
        # Start the service (this will run indefinitely)
        logger.info("Notification Agent Service is now running...")
        logger.info("Listening for patterns, triggers, and events...")
        logger.info("Press Ctrl+C to stop the service")
        
        await trigger_service.start_listening()
        
    except KeyboardInterrupt:
        logger.info("Received shutdown signal. Stopping Notification Agent Service...")
    except Exception as e:
        logger.error(f"Error starting notification service: {e}")
        raise
    finally:
        logger.info("Notification Agent Service stopped.")


async def test_notification_agent():
    """Test the notification agent functionality."""
    
    print("🧪 Testing Notification Agent...")
    
    # Test 1: Pattern analysis
    print("\n1. Testing pattern analysis and notification triggers...")
    from notification_agent.agent import analyze_patterns_and_trigger_notifications
    
    result = await analyze_patterns_and_trigger_notifications(trigger_type="auto")
    print(f"✅ Pattern analysis completed: {len(result)} characters of results")
    
    # Test 2: User preferences
    print("\n2. Testing user location preferences...")
    from notification_agent.agent import get_user_location_preferences
    
    user_prefs = await get_user_location_preferences("all")
    print(f"✅ Retrieved user preferences: {len(user_prefs)} characters")
    
    # Test 3: Personalized notification
    print("\n3. Testing personalized notification sending...")
    from notification_agent.agent import send_personalized_notification
    
    notification_result = await send_personalized_notification(
        user_ids="user1,user2",
        notification_type="info",
        location="Test Location",
        custom_message="This is a test notification from the City Pulse system."
    )
    print(f"✅ Sent personalized notification: {len(notification_result)} characters")
    
    print("\n🎉 All tests completed successfully!")
    print("The Notification Agent is ready for deployment.")


def main():
    """Main entry point for the notification service."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="City Pulse Notification Agent")
    parser.add_argument(
        "--mode", 
        choices=["service", "test"], 
        default="service",
        help="Run mode: 'service' for production, 'test' for testing"
    )
    
    args = parser.parse_args()
    
    if args.mode == "test":
        print("🚀 Running Notification Agent in TEST mode...")
        asyncio.run(test_notification_agent())
    else:
        print("🚀 Running Notification Agent in SERVICE mode...")
        asyncio.run(start_notification_service())


if __name__ == "__main__":
    main()
