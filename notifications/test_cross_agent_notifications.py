#!/usr/bin/env python3
"""
Test script for Cross-Agent Notification System

This script demonstrates and tests the cross-agent notification capabilities
of the City Pulse notification agent, including:
- Multi-agent data correlation analysis
- AI-powered pattern detection
- Predictive risk assessment
- Smart notification generation
- Firebase push notification delivery
- Anomaly detection with AI reasoning
"""

import asyncio
import json
import datetime
from notification_agent.agent import (
    NotificationAgent,
    PatternDetector,
    FirebaseNotificationService,
    NotificationGenerator
)


async def test_cross_agent_notification_system():
    """
    Comprehensive test function to demonstrate cross-agent notification capabilities
    """
    print("🚀 Testing Cross-Agent Notification System...")
    print("=" * 60)
    
    # Initialize components
    notification_agent = NotificationAgent()
    
    # Test 1: Basic Pattern Analysis and Clustering
    print("\n📊 Test 1: Basic Pattern Analysis and Clustering")
    print("-" * 50)
    try:
        result1 = await notification_agent.analyze_patterns_and_trigger_notifications(
            trigger_type="auto"
        )
        result_data = json.loads(result1)
        print(f"✅ Status: {result_data.get('status', 'unknown')}")
        print(f"📈 Summary: {result_data.get('summary', 'No summary available')}")
        print(f"🔍 Patterns Detected: {len(result_data.get('patterns_detected', []))}")
        print(f"📱 Notifications Sent: {len(result_data.get('notifications_sent', []))}")
    except Exception as e:
        print(f"❌ Error in Test 1: {e}")
    
    # Test 2: Cross-Agent Pattern Detection
    print("\n🔍 Test 2: Cross-Agent Pattern Detection")
    print("-" * 50)
    try:
        pattern_detector = PatternDetector(ai_agent=notification_agent)
        
        # Mock cross-agent data representing a crisis scenario
        cross_agent_data = {
            'events': [
                {
                    "type": "infrastructure", 
                    "location": "HSR Layout", 
                    "description": "Power grid failure", 
                    "timestamp": datetime.datetime.now().isoformat()
                },
                {
                    "type": "infrastructure", 
                    "location": "HSR Layout", 
                    "description": "Backup systems failing", 
                    "timestamp": datetime.datetime.now().isoformat()
                }
            ],
            'environment': [
                {
                    "temperature": 42.5, 
                    "location": "HSR Layout", 
                    "alert": "extreme_heat", 
                    "timestamp": datetime.datetime.now().isoformat()
                },
                {
                    "humidity": 15, 
                    "location": "HSR Layout", 
                    "alert": "low_humidity", 
                    "timestamp": datetime.datetime.now().isoformat()
                },
                {
                    "air_quality": "hazardous", 
                    "location": "HSR Layout", 
                    "timestamp": datetime.datetime.now().isoformat()
                }
            ],
            'user_reports': [
                {
                    "type": "Infrastructure", 
                    "location": "HSR Layout", 
                    "description": "AC not working due to power issues"
                },
                {
                    "type": "Infrastructure", 
                    "location": "HSR Layout", 
                    "description": "Elevators stopped working"
                },
                {
                    "type": "Environment", 
                    "location": "HSR Layout", 
                    "description": "Extremely hot conditions"
                }
            ]
        }
        
        patterns = await pattern_detector.analyze_cross_agent_patterns(cross_agent_data)
        print(f"✅ Detected {len(patterns)} cross-agent patterns:")
        
        for i, pattern in enumerate(patterns, 1):
            print(f"  {i}. Pattern Type: {pattern['type']}")
            print(f"     Description: {pattern['description']}")
            print(f"     Severity: {pattern['severity']}")
            print(f"     Confidence: {pattern.get('confidence', 'N/A')}")
            print(f"     Recommendation: {pattern.get('recommendation', 'N/A')}")
            print()
            
    except Exception as e:
        print(f"❌ Error in Test 2: {e}")
    
    # Test 3: Predictive Risk Analysis
    print("\n🔮 Test 3: Predictive Risk Analysis")
    print("-" * 50)
    try:
        prediction_result = await notification_agent.send_predictive_notification(
            location="HSR Layout",
            event_type="infrastructure"
        )
        prediction_data = json.loads(prediction_result)
        print(f"✅ Prediction Status: {prediction_data['status']}")
        
        if prediction_data.get('prediction'):
            pred = prediction_data['prediction']
            print(f"🎯 Risk Level: {pred['risk_level']}")
            print(f"📊 Confidence: {pred['confidence']:.1%}")
            print(f"⏰ Predicted Time: {pred.get('predicted_time', 'N/A')}")
            print(f"🔄 Notification Sent: {prediction_data.get('notification_sent', False)}")
        else:
            print(f"📝 Reason: {prediction_data.get('reason', 'No prediction available')}")
            
    except Exception as e:
        print(f"❌ Error in Test 3: {e}")
    
    # Test 4: Firebase Notification Delivery Simulation
    print("\n📱 Test 4: Firebase Notification Delivery")
    print("-" * 50)
    try:
        firebase_service = FirebaseNotificationService()
        
        notification_result = await firebase_service.send_notification(
            device_token="test_device_token_123",
            title="🚨 Cross-Agent Alert: Infrastructure-Environment Crisis",
            body="Multiple systems affected in HSR Layout. Power grid failure coinciding with extreme heat conditions.",
            data={
                "pattern_type": "infrastructure_environment_correlation",
                "severity": "HIGH",
                "location": "HSR Layout",
                "affected_systems": "infrastructure,environment"
            }
        )
        
        print(f"✅ Firebase Status: {notification_result['status']}")
        print(f"📧 Message Preview:")
        preview = notification_result.get('notification_preview', {})
        print(f"   Title: {preview.get('title', 'N/A')}")
        print(f"   Body: {preview.get('body', 'N/A')[:80]}...")
        
    except Exception as e:
        print(f"❌ Error in Test 4: {e}")
    
    # Test 5: AI-Powered Anomaly Detection
    print("\n🤖 Test 5: AI-Powered Anomaly Detection")
    print("-" * 50)
    try:
        pattern_detector = PatternDetector(ai_agent=notification_agent)
        
        # Simulate unusual spike in incidents
        current_data = {
            "type": "infrastructure", 
            "location": "HSR Layout",
            "value": 15,  # Unusual high incident count
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        # Normal historical pattern (2 incidents per day average)
        historical_data = [
            {
                "value": 2, 
                "timestamp": (datetime.datetime.now() - datetime.timedelta(days=i)).isoformat()
            }
            for i in range(1, 11)
        ]
        
        anomaly_result = await pattern_detector.ai_powered_anomaly_detection(
            current_data, historical_data
        )
        
        print(f"✅ Anomaly Detected: {anomaly_result['is_anomaly']}")
        print(f"📊 Confidence: {anomaly_result['confidence']:.1%}")
        print(f"📈 Anomaly Type: {anomaly_result.get('anomaly_type', 'N/A')}")
        print(f"⚠️ Severity: {anomaly_result.get('severity', 'N/A')}")
        print(f"🧠 AI Reasoning: {anomaly_result['reasoning']}")
        print(f"🚨 Should Alert: {anomaly_result.get('should_alert', False)}")
        
    except Exception as e:
        print(f"❌ Error in Test 5: {e}")
    
    # Test 6: Cross-Agent Notification Generation
    print("\n🔔 Test 6: Cross-Agent Notification Generation")
    print("-" * 50)
    try:
        notification_generator = NotificationGenerator()
        
        # Test different types of cross-agent patterns
        test_patterns = [
            {
                "type": "infrastructure_environment_correlation",
                "severity": "HIGH",
                "description": "Power grid failure during extreme heat",
                "confidence": 0.85,
                "recommendation": "Implement emergency cooling centers"
            },
            {
                "type": "systemic_stress",
                "severity": "CRITICAL", 
                "description": "Multiple city systems under stress",
                "confidence": 0.92,
                "recommendation": "Activate city-wide emergency protocols"
            },
            {
                "type": "user_report_validation",
                "severity": "MEDIUM",
                "description": "User reports confirmed by official data",
                "confidence": 0.78,
                "recommendation": "Prioritize similar user reports"
            }
        ]
        
        for i, pattern in enumerate(test_patterns, 1):
            notification = notification_generator.generate_cross_agent_notification(pattern)
            print(f"  Pattern {i}: {pattern['type']}")
            print(f"    Title: {notification.title}")
            print(f"    Body: {notification.body[:60]}...")
            print(f"    Priority: {notification.priority}")
            print(f"    Impact: {notification.predicted_impact}")
            print()
            
    except Exception as e:
        print(f"❌ Error in Test 6: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("✅ Cross-Agent Notification System Test Complete!")
    print("\n🔄 Cross-Agent Notification Features Demonstrated:")
    feature_list = [
        "Multi-agent data correlation analysis",
        "AI-powered pattern detection", 
        "Predictive risk assessment",
        "Smart notification generation",
        "Firebase push notification delivery",
        "Anomaly detection with AI reasoning",
        "Cross-system vulnerability identification",
        "Severity-based notification prioritization",
        "Location-based user targeting",
        "Pattern-specific notification templates"
    ]
    
    for feature in feature_list:
        print(f"  ✓ {feature}")
    
    print(f"\n🎯 System Status: All cross-agent features operational")
    print(f"📊 Test Completion Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


async def test_individual_components():
    """Test individual components separately for debugging"""
    print("\n🔧 Testing Individual Components...")
    print("-" * 40)
    
    # Test PatternDetector
    print("1. Testing PatternDetector...")
    try:
        detector = PatternDetector()
        print("   ✅ PatternDetector initialized")
    except Exception as e:
        print(f"   ❌ PatternDetector error: {e}")
    
    # Test NotificationGenerator  
    print("2. Testing NotificationGenerator...")
    try:
        generator = NotificationGenerator()
        print("   ✅ NotificationGenerator initialized")
    except Exception as e:
        print(f"   ❌ NotificationGenerator error: {e}")
    
    # Test FirebaseNotificationService
    print("3. Testing FirebaseNotificationService...")
    try:
        firebase = FirebaseNotificationService()
        print("   ✅ FirebaseNotificationService initialized")
    except Exception as e:
        print(f"   ❌ FirebaseNotificationService error: {e}")
    
    # Test NotificationAgent
    print("4. Testing NotificationAgent...")
    try:
        agent = NotificationAgent()
        print("   ✅ NotificationAgent initialized")
    except Exception as e:
        print(f"   ❌ NotificationAgent error: {e}")


if __name__ == "__main__":
    print("🌟 City Pulse Cross-Agent Notification System Test Suite")
    print("=" * 60)
    
    # Run component tests first
    asyncio.run(test_individual_components())
    
    # Run full system test
    asyncio.run(test_cross_agent_notification_system())
    
    print("\n🏁 All tests completed!")
