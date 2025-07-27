#!/usr/bin/env python3
"""
Quick Test Script for Notification Agent
Tests the agent without requiring Firebase/PubSub setup
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from notification_agent.agent import NotificationAgent, PatternDetector
    print("✅ Successfully imported notification agent")
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the notifications directory")
    sys.exit(1)

class TestLogger:
    """Simple logger for test output"""
    def __init__(self):
        self.logs = []
    
    def log(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        print(log_entry)
        self.logs.append(log_entry)

async def test_pattern_detection():
    """Test AI-powered pattern detection"""
    logger = TestLogger()
    logger.log("🧠 Testing AI Pattern Detection...")
    
    detector = PatternDetector()
    
    # Test data - multiple flooding events in HSR Layout
    events = [
        {
            "type": "flooding",
            "severity": "medium",
            "location": "HSR Layout Sector 1",
            "coordinates": {"lat": 12.9081, "lng": 77.6476},
            "timestamp": "2025-01-26T09:00:00Z"
        },
        {
            "type": "flooding", 
            "severity": "high",
            "location": "HSR Layout Sector 2",
            "coordinates": {"lat": 12.9085, "lng": 77.6480},
            "timestamp": "2025-01-26T09:15:00Z"
        },
        {
            "type": "flooding",
            "severity": "high", 
            "location": "HSR Layout Sector 3",
            "coordinates": {"lat": 12.9090, "lng": 77.6485},
            "timestamp": "2025-01-26T09:30:00Z"
        }
    ]
    
    try:
        # Test cluster detection
        clusters = await detector.detect_clusters(events)
        logger.log(f"🎯 Found {len(clusters)} clusters")
        
        for i, cluster in enumerate(clusters):
            logger.log(f"   Cluster {i+1}: {cluster.get('severity', 'unknown')} severity")
            logger.log(f"   Events: {len(cluster.get('events', []))}")
            if 'ai_analysis' in cluster:
                logger.log(f"   AI Analysis: {cluster['ai_analysis'][:100]}...")
        
        # Test anomaly detection
        anomalies = await detector.detect_anomalies(events)
        logger.log(f"⚠️  Found {len(anomalies)} anomalies")
        
        # Test risk prediction
        risk = await detector.predict_risk(events[0])
        logger.log(f"📊 Risk Level: {risk.get('level', 'unknown')}")
        logger.log(f"   Confidence: {risk.get('confidence', 0):.2f}")
        
        return True
        
    except Exception as e:
        logger.log(f"❌ Pattern detection failed: {e}", "ERROR")
        return False

async def test_notification_generation():
    """Test notification generation"""
    logger = TestLogger()
    logger.log("📱 Testing Notification Generation...")
    
    try:
        # Create agent without external services
        agent = NotificationAgent(use_firebase=False, use_pubsub=False)
        
        # Test emergency event
        emergency_event = {
            "type": "emergency",
            "severity": "critical",
            "location": "MG Road Metro Station", 
            "description": "Gas leak detected, immediate evacuation required",
            "coordinates": {"lat": 12.9716, "lng": 77.6412},
            "timestamp": "2025-01-26T14:30:00Z"
        }
        
        # Process event
        result = await agent.process_event(emergency_event)
        
        logger.log("📋 Generated Notification:")
        logger.log(f"   Title: {result.get('notification', {}).get('title', 'N/A')}")
        logger.log(f"   Body: {result.get('notification', {}).get('body', 'N/A')}")
        logger.log(f"   Priority: {result.get('notification', {}).get('priority', 'N/A')}")
        logger.log(f"   Affected Users: {len(result.get('affected_users', []))}")
        
        if result.get('ai_reasoning'):
            logger.log(f"🤖 AI Reasoning: {result['ai_reasoning'][:100]}...")
        
        return True
        
    except Exception as e:
        logger.log(f"❌ Notification generation failed: {e}", "ERROR")
        return False

async def test_multiple_scenarios():
    """Test multiple event scenarios"""
    logger = TestLogger()
    logger.log("🎭 Testing Multiple Scenarios...")
    
    scenarios = [
        {
            "name": "Weather Alert",
            "event": {
                "type": "weather",
                "severity": "high",
                "location": "Whitefield",
                "description": "Heavy rainfall warning - 80mm expected in next 2 hours",
                "coordinates": {"lat": 12.9698, "lng": 77.7500}
            }
        },
        {
            "name": "Traffic Jam",
            "event": {
                "type": "traffic",
                "severity": "medium", 
                "location": "Electronic City Flyover",
                "description": "Major accident causing 45-minute delays",
                "coordinates": {"lat": 12.8456, "lng": 77.6603}
            }
        },
        {
            "name": "Infrastructure Issue",
            "event": {
                "type": "infrastructure",
                "severity": "low",
                "location": "Koramangala Water Plant",
                "description": "Scheduled maintenance - water supply affected",
                "coordinates": {"lat": 12.9279, "lng": 77.6271}
            }
        }
    ]
    
    agent = NotificationAgent(use_firebase=False, use_pubsub=False)
    success_count = 0
    
    for scenario in scenarios:
        try:
            logger.log(f"Testing: {scenario['name']}")
            result = await agent.process_event(scenario['event'])
            
            if result and result.get('notification'):
                logger.log(f"   ✅ {scenario['name']} - Success")
                success_count += 1
            else:
                logger.log(f"   ❌ {scenario['name']} - No notification generated")
                
        except Exception as e:
            logger.log(f"   ❌ {scenario['name']} - Error: {e}")
    
    logger.log(f"📊 Scenario Results: {success_count}/{len(scenarios)} passed")
    return success_count == len(scenarios)

async def main():
    """Main test function"""
    print("🚀 City Pulse Notification Agent - Quick Test")
    print("=" * 50)
    
    tests = [
        ("Pattern Detection", test_pattern_detection),
        ("Notification Generation", test_notification_generation), 
        ("Multiple Scenarios", test_multiple_scenarios)
    ]
    
    passed_tests = 0
    total_tests = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running: {test_name}")
        print("-" * 30)
        
        try:
            success = await test_func()
            if success:
                print(f"✅ {test_name} - PASSED")
                passed_tests += 1
            else:
                print(f"❌ {test_name} - FAILED")
        except Exception as e:
            print(f"💥 {test_name} - CRASHED: {e}")
    
    print("\n" + "=" * 50)
    print(f"🏁 Test Summary: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All tests passed! Your notification agent is working correctly.")
        print("\n📋 Next Steps:")
        print("1. Review SETUP_GUIDE.md for Firebase/PubSub configuration")
        print("2. Run 'python demo_ai_capabilities.py' to see AI vs simulation")
        print("3. Configure real services for production deployment")
    else:
        print("⚠️  Some tests failed. Check the error messages above.")
        print("💡 Make sure all dependencies are installed: pip install -r requirements.txt")
    
    return passed_tests == total_tests

if __name__ == "__main__":
    # Run the tests
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        print("🔧 Try running from the notifications directory")
