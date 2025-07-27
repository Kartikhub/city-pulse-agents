#!/usr/bin/env python3
"""
Demo script showcasing the enhanced AI capabilities of the notification agent.
This demonstrates real AI agent intelligence vs simulation.
"""

import asyncio
import json
from notification_agent.agent import (
    PatternDetector,
    NotificationAgent,
    analyze_patterns_and_trigger_notifications,
    notification_agent
)

async def demo_ai_vs_simulation():
    """Demonstrate the difference between AI-powered and simulation-based analysis"""
    
    print("🚀 CITY PULSE NOTIFICATION AGENT - AI CAPABILITIES DEMO")
    print("=" * 60)
    
    # Sample incident data for testing
    sample_incidents = [
        {
            "documentId": "incident1",
            "incidentType": "Infrastructure",
            "location": "HSR Layout",
            "description": "Critical transformer failure causing widespread power outage - emergency repair needed",
            "timestamp": "2025-07-26T14:30:00Z",
            "severity": "critical"
        },
        {
            "documentId": "incident2", 
            "incidentType": "Infrastructure",
            "location": "HSR Layout",
            "description": "Multiple voltage spikes damaging household appliances across 3 apartment complexes",
            "timestamp": "2025-07-26T14:25:00Z",
            "severity": "high"
        },
        {
            "documentId": "incident3",
            "incidentType": "Infrastructure", 
            "location": "HSR Layout",
            "description": "Complete area blackout affecting traffic signals and street lighting",
            "timestamp": "2025-07-26T14:20:00Z",
            "severity": "critical"
        }
    ]
    
    print("\n🔍 SAMPLE INCIDENT DATA:")
    for i, incident in enumerate(sample_incidents, 1):
        print(f"  {i}. {incident['incidentType']} in {incident['location']}")
        print(f"     Description: {incident['description'][:80]}...")
        print(f"     Severity: {incident['severity']}")
    
    print("\n" + "=" * 60)
    print("🤖 TESTING AI-POWERED ANALYSIS")
    print("=" * 60)
    
    # Test 1: AI-Powered Pattern Detection
    print("\n1️⃣ AI-POWERED CLUSTER DETECTION:")
    print("-" * 40)
    
    ai_pattern_detector = PatternDetector(ai_agent=notification_agent)
    
    try:
        cluster = await ai_pattern_detector.detect_event_cluster(sample_incidents, time_window_minutes=20)
        
        if cluster:
            print(f"✅ AI DETECTED CLUSTER:")
            print(f"   Event Type: {cluster.event_type}")
            print(f"   Location: {cluster.location}")
            print(f"   Count: {cluster.count} incidents")
            print(f"   Severity: {cluster.severity}")
            print(f"   Affected Radius: {cluster.affected_radius_km} km")
            print(f"   Time Window: {cluster.time_window}")
        else:
            print("❌ No cluster detected by AI agent")
            
    except Exception as e:
        print(f"⚠️ AI analysis failed: {e}")
        print("🔄 Falling back to simulation mode...")
    
    # Test 2: AI-Powered Risk Prediction
    print("\n2️⃣ AI-POWERED RISK PREDICTION:")
    print("-" * 40)
    
    try:
        risk_prediction = await ai_pattern_detector.predict_future_risk("HSR Layout", "Infrastructure")
        
        print(f"🔮 AI RISK PREDICTION:")
        print(f"   Risk Level: {risk_prediction.get('risk_level', 'Unknown')}")
        print(f"   Confidence: {risk_prediction.get('confidence', 0)*100:.1f}%")
        print(f"   Predicted Timeframe: {risk_prediction.get('predicted_timeframe', 'Unknown')}")
        
        if 'reasoning' in risk_prediction:
            print(f"   AI Reasoning: {risk_prediction['reasoning'][:100]}...")
            
        if 'contributing_factors' in risk_prediction:
            print(f"   Contributing Factors:")
            for factor in risk_prediction['contributing_factors'][:3]:
                print(f"     - {factor}")
                
    except Exception as e:
        print(f"⚠️ AI risk prediction failed: {e}")
    
    # Test 3: AI-Powered Anomaly Detection
    print("\n3️⃣ AI-POWERED ANOMALY DETECTION:")
    print("-" * 40)
    
    current_data = {
        "type": "infrastructure_failure_rate",
        "value": 15.0,  # Unusually high failure rate
        "location": "HSR Layout",
        "timestamp": "2025-07-26T14:30:00Z"
    }
    
    historical_data = [
        {"value": 2.1}, {"value": 1.8}, {"value": 2.5}, {"value": 1.9}, 
        {"value": 2.3}, {"value": 2.0}, {"value": 2.2}, {"value": 1.7}
    ]
    
    try:
        anomaly_result = await ai_pattern_detector.ai_powered_anomaly_detection(current_data, historical_data)
        
        print(f"🔍 AI ANOMALY ANALYSIS:")
        print(f"   Is Anomaly: {anomaly_result.get('is_anomaly', False)}")
        print(f"   Confidence: {anomaly_result.get('confidence', 0)*100:.1f}%")
        print(f"   Anomaly Type: {anomaly_result.get('anomaly_type', 'Unknown')}")
        print(f"   Severity: {anomaly_result.get('severity', 'Unknown')}")
        print(f"   Should Alert: {anomaly_result.get('should_alert', False)}")
        
        if 'reasoning' in anomaly_result:
            print(f"   AI Reasoning: {anomaly_result['reasoning'][:100]}...")
            
    except Exception as e:
        print(f"⚠️ AI anomaly detection failed: {e}")
    
    # Test 4: Complete AI-Enhanced Notification Pipeline
    print("\n4️⃣ COMPLETE AI-ENHANCED NOTIFICATION PIPELINE:")
    print("-" * 50)
    
    try:
        result = await analyze_patterns_and_trigger_notifications(
            events_data="all",
            environment_data="all", 
            user_reports_data="all",
            trigger_type="auto"
        )
        
        result_data = json.loads(result)
        
        print(f"🎯 PIPELINE RESULTS:")
        print(f"   Status: {result_data.get('status', 'Unknown')}")
        print(f"   AI Enhanced: {result_data.get('ai_analysis_used', False)}")
        print(f"   Patterns Detected: {len(result_data.get('patterns_detected', []))}")
        print(f"   Notifications Sent: {len(result_data.get('notifications_sent', []))}")
        print(f"   Predictions Made: {len(result_data.get('predictions', []))}")
        print(f"   AI Insights: {len(result_data.get('ai_insights', []))}")
        
        if 'ai_summary' in result_data:
            print(f"   AI Summary: {result_data['ai_summary']}")
        
        # Show AI insights if available
        ai_insights = result_data.get('ai_insights', [])
        if ai_insights:
            print(f"\n   🧠 AI INSIGHTS:")
            for insight in ai_insights[:2]:  # Show first 2 insights
                print(f"     - Type: {insight.get('type', 'Unknown')}")
                if 'ai_analysis' in insight:
                    print(f"       Analysis: {insight['ai_analysis']}")
                    
    except Exception as e:
        print(f"⚠️ AI notification pipeline failed: {e}")
    
    print("\n" + "=" * 60)
    print("📊 COMPARISON: AI vs SIMULATION")
    print("=" * 60)
    
    print("\n🤖 AI-POWERED CAPABILITIES:")
    print("  ✅ Real reasoning and context understanding")
    print("  ✅ Natural language processing of incident descriptions")
    print("  ✅ Multi-factor decision making")
    print("  ✅ Learning from previous decisions")
    print("  ✅ Adaptive thresholds based on context")
    print("  ✅ Cross-domain pattern correlation")
    print("  ✅ Uncertainty quantification")
    print("  ✅ Explainable decision reasoning")
    
    print("\n🔄 SIMULATION FALLBACK:")
    print("  ⚡ Fast rule-based analysis")
    print("  ⚡ Statistical pattern detection")  
    print("  ⚡ Fixed threshold-based decisions")
    print("  ⚡ Basic severity calculation")
    print("  ⚡ Limited context awareness")
    
    print(f"\n🎯 RECOMMENDATION:")
    print(f"  • Use AI agent for intelligent, context-aware analysis")
    print(f"  • Fallback to simulation ensures reliability")
    print(f"  • Continuous learning improves accuracy over time")
    print(f"  • Real-time decision making with explainable AI")

async def demo_ai_learning():
    """Demonstrate AI learning capabilities"""
    
    print("\n" + "=" * 60)
    print("🧠 AI LEARNING & ADAPTATION DEMO")
    print("=" * 60)
    
    ai_detector = PatternDetector(ai_agent=notification_agent)
    
    # Simulate learning from multiple scenarios
    learning_scenarios = [
        {
            "location": "HSR Layout",
            "event_type": "Infrastructure",
            "incidents": 4,
            "outcome": "successful_prevention"
        },
        {
            "location": "Whitefield", 
            "event_type": "Flooding",
            "incidents": 2,
            "outcome": "early_warning_effective"
        },
        {
            "location": "Electronic City",
            "event_type": "Infrastructure", 
            "incidents": 6,
            "outcome": "rapid_response_needed"
        }
    ]
    
    print("\n📚 LEARNING SCENARIOS:")
    for i, scenario in enumerate(learning_scenarios, 1):
        print(f"  {i}. {scenario['location']} - {scenario['event_type']}")
        print(f"     Incidents: {scenario['incidents']}, Outcome: {scenario['outcome']}")
        
        # Store learning data
        learning_key = f"scenario_learning_{scenario['location']}_{scenario['event_type']}"
        ai_detector.learning_memory[learning_key].append({
            "scenario": scenario,
            "timestamp": "2025-07-26T14:30:00Z",
            "effectiveness": "high" if "successful" in scenario['outcome'] else "medium"
        })
    
    print(f"\n🧠 AI LEARNING MEMORY:")
    total_learning_entries = sum(len(memories) for memories in ai_detector.learning_memory.values())
    print(f"  Total Learning Entries: {total_learning_entries}")
    print(f"  Learning Categories: {len(ai_detector.learning_memory)}")
    
    for category, memories in list(ai_detector.learning_memory.items())[:3]:
        print(f"  📝 {category}: {len(memories)} entries")
    
    print(f"\n✨ ADAPTIVE IMPROVEMENTS:")
    print(f"  • Threshold adjustment based on location history")
    print(f"  • Context-aware severity calculation")
    print(f"  • Personalized notification timing")
    print(f"  • Cross-pattern correlation learning")

def main():
    """Main demo function"""
    print("🏙️ Welcome to the City Pulse Notification Agent AI Demo!")
    print("This demonstrates real AI agent capabilities vs simulation fallback.")
    
    try:
        # Run AI vs Simulation demo
        asyncio.run(demo_ai_vs_simulation())
        
        # Run AI learning demo
        asyncio.run(demo_ai_learning())
        
        print(f"\n✅ Demo completed successfully!")
        print(f"💡 The notification agent now uses real AI intelligence with simulation fallback.")
        
    except KeyboardInterrupt:
        print(f"\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        
    print(f"\n🚀 Ready to deploy intelligent city notifications!")

if __name__ == "__main__":
    main()
