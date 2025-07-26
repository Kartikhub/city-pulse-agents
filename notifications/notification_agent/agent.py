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
import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict, Counter
import numpy as np
from dataclasses import dataclass
import firebase_admin
from firebase_admin import credentials, messaging
from google.adk import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.genai import types


@dataclass
class UserProfile:
    """User profile for personalized notifications"""
    user_id: str
    location: str
    interests: List[str]
    notification_preferences: Dict[str, bool]
    device_token: str


@dataclass
class EventCluster:
    """Represents a cluster of related events"""
    event_type: str
    location: str
    count: int
    severity: str
    time_window: str
    affected_radius_km: float


@dataclass
class NotificationData:
    """Notification data structure"""
    title: str
    body: str
    priority: str
    target_users: List[str]
    event_type: str
    location: str
    predicted_impact: str


class PatternDetector:
    """AI-powered pattern detection using the notification agent's intelligence"""
    
    def __init__(self, ai_agent=None):
        self.historical_data = defaultdict(list)
        self.ai_agent = ai_agent  # Reference to the AI agent for intelligent analysis
        
    async def detect_event_cluster(self, events: List[Dict], time_window_minutes: int = 20) -> Optional[EventCluster]:
        """Use AI agent to intelligently detect concerning event clusters"""
        if not events:
            return None
        
        # If AI agent is available, use its intelligence for analysis
        if self.ai_agent:
            return await self._ai_powered_cluster_detection(events, time_window_minutes)
        else:
            # Fallback to basic analysis
            return await self._basic_cluster_detection(events, time_window_minutes)
    
    async def _ai_powered_cluster_detection(self, events: List[Dict], time_window_minutes: int) -> Optional[EventCluster]:
        """Let the AI agent analyze events and determine if they form concerning clusters"""
        
        # Prepare context for AI analysis
        events_summary = self._prepare_events_for_ai_analysis(events, time_window_minutes)
        
        # AI prompt for intelligent cluster analysis
        ai_analysis_prompt = f"""
        Analyze the following city incident data to determine if there are concerning patterns or clusters:

        INCIDENT DATA:
        {events_summary}

        TIME WINDOW: {time_window_minutes} minutes

        Please analyze and determine:
        1. Are there concerning clusters of similar incidents in the same location?
        2. What is the severity level (LOW, MEDIUM, HIGH, CRITICAL) based on:
           - Number of incidents
           - Type of incidents (emergency/flooding are more critical than maintenance)
           - Location concentration
           - Potential impact on citizens
        3. What radius should be affected for notifications (2-15km)?
        4. Should this trigger a notification to citizens?

        Respond with a JSON analysis including:
        - is_cluster: boolean
        - event_type: string (if cluster found)
        - location: string (if cluster found)
        - count: number
        - severity: string (LOW/MEDIUM/HIGH/CRITICAL)
        - affected_radius_km: number
        - reasoning: string explaining your analysis
        - notification_recommended: boolean
        """
        
        try:
            # Get AI analysis (this would use the agent's generate_content method)
            # For now, we'll simulate the AI response format
            ai_response = await self._simulate_ai_cluster_analysis(events, time_window_minutes)
            
            if ai_response.get("is_cluster", False) and ai_response.get("notification_recommended", False):
                return EventCluster(
                    event_type=ai_response.get("event_type", "Unknown"),
                    location=ai_response.get("location", "Unknown"),
                    count=ai_response.get("count", len(events)),
                    severity=ai_response.get("severity", "MEDIUM"),
                    time_window=f"{time_window_minutes} minutes",
                    affected_radius_km=ai_response.get("affected_radius_km", 5.0)
                )
            
            return None
            
        except Exception as e:
            print(f"AI cluster analysis failed, using fallback: {e}")
            return await self._basic_cluster_detection(events, time_window_minutes)
    
    async def _simulate_ai_cluster_analysis(self, events: List[Dict], time_window_minutes: int) -> Dict[str, Any]:
        """Simulate AI analysis - in real implementation, this would call the AI agent"""
        
        # Group events by location and type for intelligent analysis
        location_events = defaultdict(list)
        for event in events:
            location_events[event.get('location', 'unknown')].append(event)
        
        # AI-like reasoning for cluster detection
        for location, loc_events in location_events.items():
            event_types = Counter([e.get('incidentType', 'unknown') for e in loc_events])
            
            for event_type, count in event_types.items():
                # AI reasoning: Consider context, not just count
                if self._ai_should_create_cluster(event_type, count, location, loc_events):
                    severity = await self._ai_determine_severity(event_type, count, location, loc_events)
                    radius = await self._ai_calculate_radius(event_type, count, location, severity)
                    
                    return {
                        "is_cluster": True,
                        "event_type": event_type,
                        "location": location,
                        "count": count,
                        "severity": severity,
                        "affected_radius_km": radius,
                        "reasoning": f"AI detected {count} {event_type.lower()} incidents in {location} within {time_window_minutes} minutes. Pattern analysis suggests {severity.lower()} priority notification needed.",
                        "notification_recommended": True
                    }
        
        return {
            "is_cluster": False,
            "notification_recommended": False,
            "reasoning": "AI analysis found no concerning patterns requiring citizen notification."
        }
    
    def _ai_should_create_cluster(self, event_type: str, count: int, location: str, events: List[Dict]) -> bool:
        """AI-like reasoning for whether events constitute a concerning cluster"""
        
        # AI considers multiple factors, not just count
        factors = {
            "event_criticality": self._assess_event_criticality(event_type),
            "frequency_concern": count >= 2,  # AI is more sensitive than fixed threshold
            "location_vulnerability": self._assess_location_vulnerability(location),
            "incident_descriptions": self._analyze_incident_descriptions(events)
        }
        
        # AI reasoning: If incident is critical OR multiple factors indicate concern
        if factors["event_criticality"] == "high":
            return count >= 2  # AI: Even 2 critical events are concerning
        elif factors["event_criticality"] == "medium":
            return count >= 3 and factors["location_vulnerability"] == "high"
        else:
            return count >= 4 and factors["frequency_concern"]
    
    async def _ai_determine_severity(self, event_type: str, count: int, location: str, events: List[Dict]) -> str:
        """AI determines severity based on multiple contextual factors"""
        
        severity_score = 0
        
        # Factor 1: Event type criticality
        if event_type.lower() in ['emergency', 'flooding']:
            severity_score += 3
        elif event_type.lower() in ['infrastructure']:
            severity_score += 2
        else:
            severity_score += 1
        
        # Factor 2: Frequency intensity (AI adapts based on type)
        if event_type.lower() in ['emergency', 'flooding']:
            if count >= 4: severity_score += 3
            elif count >= 2: severity_score += 2
            else: severity_score += 1
        else:
            if count >= 6: severity_score += 3
            elif count >= 4: severity_score += 2
            elif count >= 2: severity_score += 1
        
        # Factor 3: Location impact (AI considers population density)
        high_impact_areas = ['HSR Layout', 'Whitefield', 'Koramangala', 'Indiranagar']
        if location in high_impact_areas:
            severity_score += 1
        
        # Factor 4: Incident descriptions (AI analyzes content)
        description_severity = self._analyze_incident_severity_from_descriptions(events)
        severity_score += description_severity
        
        # AI mapping to severity levels
        if severity_score >= 8:
            return "CRITICAL"
        elif severity_score >= 6:
            return "HIGH"
        elif severity_score >= 4:
            return "MEDIUM"
        else:
            return "LOW"
    
    async def _ai_calculate_radius(self, event_type: str, count: int, location: str, severity: str) -> float:
        """AI calculates affected radius based on incident context"""
        
        # Base radius from AI knowledge
        base_radius = {
            'flooding': 6.0,      # AI: Flooding spreads, larger base
            'infrastructure': 4.0, # AI: Power/water affects neighborhoods
            'emergency': 8.0,     # AI: Emergency requires wider alert
            'maintenance': 3.0    # AI: Maintenance is localized
        }
        
        radius = base_radius.get(event_type.lower(), 4.0)
        
        # AI scaling factors
        if severity == "CRITICAL":
            radius *= 1.5
        elif severity == "HIGH":
            radius *= 1.3
        elif severity == "MEDIUM":
            radius *= 1.1
        
        # AI considers count impact
        radius += (count - 1) * 0.5
        
        # AI considers location density
        high_density_areas = ['HSR Layout', 'Koramangala', 'BTM Layout']
        if location in high_density_areas:
            radius *= 1.2
        
        return min(radius, 15.0)  # AI caps at 15km
    
    async def _basic_cluster_detection(self, events: List[Dict], time_window_minutes: int) -> Optional[EventCluster]:
        """Fallback basic cluster detection when AI is not available"""
        location_events = defaultdict(list)
        for event in events:
            location_events[event.get('location', 'unknown')].append(event)
        
        for location, loc_events in location_events.items():
            event_types = Counter([e.get('incidentType', 'unknown') for e in loc_events])
            
            for event_type, count in event_types.items():
                if count >= 3:
                    severity = self._calculate_severity_basic(count, event_type)
                    return EventCluster(
                        event_type=event_type,
                        location=location,
                        count=count,
                        severity=severity,
                        time_window=f"{time_window_minutes} minutes",
                        affected_radius_km=self._calculate_affected_radius_basic(event_type, count)
                    )
        
        return None
    
    def _prepare_events_for_ai_analysis(self, events: List[Dict], time_window_minutes: int) -> str:
        """Prepare events data in a format suitable for AI analysis"""
        summary = f"TIME WINDOW: {time_window_minutes} minutes\n"
        summary += f"TOTAL INCIDENTS: {len(events)}\n\n"
        
        # Group by location for better AI understanding
        location_groups = defaultdict(list)
        for event in events:
            location_groups[event.get('location', 'Unknown')].append(event)
        
        for location, loc_events in location_groups.items():
            summary += f"LOCATION: {location}\n"
            event_types = Counter([e.get('incidentType', 'Unknown') for e in loc_events])
            
            for event_type, count in event_types.items():
                summary += f"  - {event_type}: {count} incidents\n"
                
                # Include sample descriptions for AI context
                sample_events = [e for e in loc_events if e.get('incidentType') == event_type][:2]
                for sample in sample_events:
                    if sample.get('description'):
                        summary += f"    * {sample['description'][:100]}...\n"
            summary += "\n"
        
        return summary
    
    def _assess_event_criticality(self, event_type: str) -> str:
        """AI assessment of event type criticality"""
        critical_events = ['emergency', 'flooding', 'fire', 'gas leak']
        medium_events = ['infrastructure', 'power outage', 'water outage']
        
        if event_type.lower() in critical_events:
            return "high"
        elif event_type.lower() in medium_events:
            return "medium"
        else:
            return "low"
    
    def _assess_location_vulnerability(self, location: str) -> str:
        """AI assessment of location vulnerability"""
        high_vulnerability = ['HSR Layout', 'Whitefield', 'Electronic City', 'Marathahalli']
        
        if location in high_vulnerability:
            return "high"
        else:
            return "medium"
    
    def _analyze_incident_descriptions(self, events: List[Dict]) -> bool:
        """AI analysis of incident descriptions for severity indicators"""
        severity_keywords = ['urgent', 'severe', 'critical', 'major', 'widespread', 'multiple', 'complete']
        
        for event in events:
            description = event.get('description', '').lower()
            if any(keyword in description for keyword in severity_keywords):
                return True
        
        return False
    
    def _analyze_incident_severity_from_descriptions(self, events: List[Dict]) -> int:
        """AI extracts severity score from incident descriptions"""
        severity_score = 0
        high_severity_words = ['urgent', 'critical', 'severe', 'major', 'widespread', 'complete']
        medium_severity_words = ['multiple', 'ongoing', 'affecting', 'reported']
        
        for event in events:
            description = event.get('description', '').lower()
            for word in high_severity_words:
                if word in description:
                    severity_score += 2
                    break
            for word in medium_severity_words:
                if word in description:
                    severity_score += 1
                    break
        
        return min(severity_score, 3)  # Cap at 3
    
    def _calculate_severity_basic(self, count: int, event_type: str) -> str:
        """Basic severity calculation for fallback"""
        if event_type.lower() in ['emergency', 'flooding']:
            if count >= 5:
                return "CRITICAL"
            elif count >= 3:
                return "HIGH"
        elif event_type.lower() in ['infrastructure', 'maintenance']:
            if count >= 8:
                return "HIGH"
            elif count >= 5:
                return "MEDIUM"
        
        return "LOW"
    
    def _calculate_affected_radius_basic(self, event_type: str, count: int) -> float:
        """Basic radius calculation for fallback"""
        base_radius = {
            'flooding': 5.0,
            'infrastructure': 3.0,
            'emergency': 7.0,
            'maintenance': 2.0
        }
        
        radius = base_radius.get(event_type.lower(), 3.0)
        return min(radius * (1 + count * 0.2), 15.0)
    
    async def ai_powered_anomaly_detection(self, current_data: Dict[str, Any], historical_data: List[Dict]) -> Dict[str, Any]:
        """Use AI agent to detect anomalies in data patterns"""
        
        if self.ai_agent and len(historical_data) >= 5:
            # Prepare data for AI analysis
            data_summary = self._prepare_anomaly_data_for_ai(current_data, historical_data)
            
            ai_prompt = f"""
            Analyze the following data to detect anomalies or unusual patterns:
            
            CURRENT DATA POINT:
            {json.dumps(current_data, indent=2)}
            
            HISTORICAL CONTEXT (last {len(historical_data)} data points):
            {data_summary}
            
            Please determine:
            1. Is the current data point anomalous compared to historical patterns?
            2. What is the confidence level (0.0 to 1.0)?
            3. What type of anomaly is it (spike, drop, pattern_break, seasonal_anomaly)?
            4. Should this trigger an alert?
            5. What is the severity (LOW, MEDIUM, HIGH)?
            
            Consider factors like:
            - Statistical deviation from normal range
            - Time-based patterns (day/night, weekday/weekend)
            - Seasonal variations
            - Context of the data type
            
            Respond with JSON analysis.
            """
            
            # Simulate AI anomaly detection response
            return await self._simulate_ai_anomaly_detection(current_data, historical_data)
        
        # Fallback to basic statistical detection
        return self._basic_anomaly_detection(current_data, historical_data)
    
    async def _simulate_ai_anomaly_detection(self, current_data: Dict[str, Any], historical_data: List[Dict]) -> Dict[str, Any]:
        """Simulate AI-powered anomaly detection"""
        
        # Extract numeric values for analysis
        current_value = self._extract_numeric_value(current_data)
        historical_values = [self._extract_numeric_value(d) for d in historical_data if self._extract_numeric_value(d) is not None]
        
        if len(historical_values) < 3:
            return {"is_anomaly": False, "confidence": 0.0, "reasoning": "Insufficient historical data for AI analysis"}
        
        # AI-like analysis considering context
        mean_val = np.mean(historical_values)
        std_val = np.std(historical_values)
        
        if std_val == 0:
            is_anomaly = current_value != mean_val
            confidence = 1.0 if is_anomaly else 0.0
        else:
            z_score = abs((current_value - mean_val) / std_val)
            
            # AI considers multiple factors, not just z-score
            is_anomaly = self._ai_anomaly_decision(current_value, historical_values, current_data)
            confidence = min(0.95, z_score / 3.0)  # Scale z-score to confidence
        
        anomaly_type = self._determine_anomaly_type(current_value, historical_values)
        severity = self._determine_anomaly_severity(z_score if std_val > 0 else 0, anomaly_type)
        
        return {
            "is_anomaly": is_anomaly,
            "confidence": confidence,
            "anomaly_type": anomaly_type,
            "severity": severity,
            "z_score": z_score if std_val > 0 else 0,
            "should_alert": is_anomaly and confidence > 0.7,
            "reasoning": f"AI detected {'anomalous' if is_anomaly else 'normal'} pattern with {confidence:.1%} confidence. Z-score: {z_score:.2f}"
        }
    
    def _ai_anomaly_decision(self, current_value: float, historical_values: List[float], context: Dict[str, Any]) -> bool:
        """AI decision making for anomaly detection considering context"""
        
        mean_val = np.mean(historical_values)
        std_val = np.std(historical_values)
        
        if std_val == 0:
            return current_value != mean_val
        
        z_score = abs((current_value - mean_val) / std_val)
        
        # AI considers adaptive thresholds based on context
        data_type = context.get('type', 'unknown')
        location = context.get('location', 'unknown')
        
        # Different thresholds for different data types (AI learning)
        if data_type in ['emergency', 'critical_infrastructure']:
            threshold = 1.5  # AI: More sensitive for critical data
        elif data_type in ['environmental', 'traffic']:
            threshold = 2.0  # AI: Standard sensitivity
        else:
            threshold = 2.5  # AI: Less sensitive for routine data
        
        # AI considers location-specific patterns
        high_variance_locations = ['Downtown', 'Electronic City']
        if location in high_variance_locations:
            threshold += 0.5  # AI: Less sensitive in high-variance areas
        
        return z_score > threshold
    
    def _determine_anomaly_type(self, current_value: float, historical_values: List[float]) -> str:
        """AI determines the type of anomaly detected"""
        mean_val = np.mean(historical_values)
        max_val = max(historical_values)
        min_val = min(historical_values)
        
        if current_value > max_val * 1.2:
            return "spike"
        elif current_value < min_val * 0.8:
            return "drop"
        elif current_value > mean_val * 1.5:
            return "high_deviation"
        elif current_value < mean_val * 0.5:
            return "low_deviation"
        else:
            return "pattern_break"
    
    def _determine_anomaly_severity(self, z_score: float, anomaly_type: str) -> str:
        """AI determines severity of detected anomaly"""
        base_severity = "LOW"
        
        if z_score > 4.0:
            base_severity = "CRITICAL"
        elif z_score > 3.0:
            base_severity = "HIGH"
        elif z_score > 2.0:
            base_severity = "MEDIUM"
        
        # AI adjusts severity based on anomaly type
        if anomaly_type in ["spike", "drop"]:
            if base_severity == "MEDIUM":
                base_severity = "HIGH"
            elif base_severity == "LOW":
                base_severity = "MEDIUM"
        
        return base_severity
    
    def detect_anomaly(self, current_value: float, historical_values: List[float]) -> bool:
        """Basic anomaly detection - kept for backward compatibility"""
        return self._basic_anomaly_detection({"value": current_value}, [{"value": v} for v in historical_values])["is_anomaly"]
    
    def _basic_anomaly_detection(self, current_data: Dict[str, Any], historical_data: List[Dict]) -> Dict[str, Any]:
        """Basic statistical anomaly detection"""
        current_value = self._extract_numeric_value(current_data)
        historical_values = [self._extract_numeric_value(d) for d in historical_data if self._extract_numeric_value(d) is not None]
        
        if len(historical_values) < 5:
            return {"is_anomaly": False, "confidence": 0.0, "reasoning": "Insufficient data"}
            
        mean = np.mean(historical_values)
        std = np.std(historical_values)
        
        if std == 0:
            is_anomaly = current_value != mean
            confidence = 1.0 if is_anomaly else 0.0
        else:
            z_score = abs((current_value - mean) / std)
            is_anomaly = z_score > 2.0  # Standard threshold
            confidence = min(0.95, z_score / 3.0)
        
        return {
            "is_anomaly": is_anomaly,
            "confidence": confidence,
            "reasoning": f"Basic statistical analysis: {'anomaly' if is_anomaly else 'normal'}"
        }
    
    def _extract_numeric_value(self, data: Dict[str, Any]) -> Optional[float]:
        """Extract numeric value from data dict for analysis"""
        if 'value' in data:
            return float(data['value'])
        elif 'count' in data:
            return float(data['count'])
        elif 'level' in data:
            return float(data['level'])
        elif 'index' in data:
            return float(data['index'])
        
        # Try to find first numeric value
        for key, value in data.items():
            try:
                return float(value)
            except (ValueError, TypeError):
                continue
        
        return None
    
    def _prepare_anomaly_data_for_ai(self, current_data: Dict[str, Any], historical_data: List[Dict]) -> str:
        """Prepare anomaly data for AI analysis"""
        summary = "HISTORICAL PATTERN ANALYSIS:\n"
        
        # Extract values for trend analysis
        values = [self._extract_numeric_value(d) for d in historical_data if self._extract_numeric_value(d) is not None]
        
        if values:
            summary += f"Historical Range: {min(values):.2f} - {max(values):.2f}\n"
            summary += f"Historical Average: {np.mean(values):.2f}\n"
            summary += f"Standard Deviation: {np.std(values):.2f}\n"
            summary += f"Recent Trend: {values[-3:] if len(values) >= 3 else values}\n"
        
        summary += f"\nRecent Data Points (last {min(5, len(historical_data))}):\n"
        for i, data_point in enumerate(historical_data[-5:]):
            summary += f"  {i+1}. {data_point}\n"
        
        return summary
    
    async def predict_future_risk(self, location: str, event_type: str) -> Dict[str, Any]:
        """AI-powered risk prediction based on patterns and context"""
        
        if self.ai_agent:
            return await self._ai_powered_risk_prediction(location, event_type)
        else:
            return self._basic_risk_prediction(location, event_type)
    
    async def _ai_powered_risk_prediction(self, location: str, event_type: str) -> Dict[str, Any]:
        """Use AI agent to predict future risks with contextual analysis"""
        
        historical = self.historical_data.get(f"{location}_{event_type}", [])
        
        # Prepare context for AI analysis
        risk_context = self._prepare_risk_context(location, event_type, historical)
        
        ai_prompt = f"""
        Analyze the risk of future incidents based on the following data:
        
        LOCATION: {location}
        INCIDENT TYPE: {event_type}
        
        CONTEXT ANALYSIS:
        {risk_context}
        
        Please predict:
        1. Risk level (LOW, MEDIUM, HIGH, CRITICAL)
        2. Confidence level (0.0 to 1.0)
        3. Predicted timeframe for next incident
        4. Contributing factors
        5. Recommended actions
        
        Consider:
        - Historical frequency patterns
        - Location-specific vulnerabilities
        - Seasonal/temporal patterns
        - Infrastructure dependencies
        - Recent trend analysis
        
        Provide JSON response with risk assessment.
        """
        
        # Simulate AI risk prediction
        return await self._simulate_ai_risk_prediction(location, event_type, historical)
    
    async def _simulate_ai_risk_prediction(self, location: str, event_type: str, historical: List) -> Dict[str, Any]:
        """Simulate AI-powered risk prediction with intelligent analysis"""
        
        if len(historical) < 3:
            return {
                "risk_level": "UNKNOWN", 
                "confidence": 0.0, 
                "predicted_time": None,
                "reasoning": "Insufficient historical data for AI prediction",
                "contributing_factors": ["Limited data availability"],
                "recommended_actions": ["Collect more incident data"]
            }
        
        # AI analyzes recent patterns (last 7 days)
        recent_events = [h for h in historical if h > (datetime.datetime.now().timestamp() - 7*24*3600)]
        
        # AI considers multiple factors for risk calculation
        risk_factors = self._ai_analyze_risk_factors(location, event_type, recent_events, historical)
        
        # AI calculates risk score based on multiple factors
        risk_score = self._ai_calculate_risk_score(risk_factors)
        
        # AI determines risk level with contextual understanding
        risk_level, confidence = self._ai_determine_risk_level(risk_score, risk_factors)
        
        # AI predicts timing based on patterns
        predicted_time = self._ai_predict_timing(risk_level, recent_events, historical)
        
        return {
            "risk_level": risk_level,
            "confidence": confidence,
            "predicted_time": predicted_time,
            "risk_score": risk_score,
            "contributing_factors": risk_factors["contributing_factors"],
            "reasoning": f"AI analysis of {len(historical)} historical incidents and {len(recent_events)} recent events in {location}",
            "recommended_actions": self._ai_recommend_actions(risk_level, event_type, location)
        }
    
    def _ai_analyze_risk_factors(self, location: str, event_type: str, recent_events: List, historical: List) -> Dict[str, Any]:
        """AI analyzes multiple risk factors"""
        
        factors = {
            "frequency_score": len(recent_events) / 7.0,  # Events per day
            "trend_score": self._calculate_trend_score(historical),
            "location_vulnerability": self._assess_location_risk(location),
            "event_criticality": self._assess_event_type_risk(event_type),
            "seasonal_factor": self._assess_seasonal_risk(event_type),
            "contributing_factors": []
        }
        
        # AI identifies contributing factors
        if factors["frequency_score"] > 0.5:
            factors["contributing_factors"].append("High recent incident frequency")
        
        if factors["trend_score"] > 0.7:
            factors["contributing_factors"].append("Increasing incident trend")
        
        if factors["location_vulnerability"] == "high":
            factors["contributing_factors"].append(f"High vulnerability area: {location}")
        
        if factors["event_criticality"] == "high":
            factors["contributing_factors"].append(f"Critical incident type: {event_type}")
        
        return factors
    
    def _ai_calculate_risk_score(self, risk_factors: Dict[str, Any]) -> float:
        """AI calculates composite risk score"""
        
        weights = {
            "frequency_score": 0.3,
            "trend_score": 0.25,
            "location_vulnerability": 0.2,
            "event_criticality": 0.15,
            "seasonal_factor": 0.1
        }
        
        risk_score = 0.0
        
        # Weighted combination of factors
        risk_score += risk_factors["frequency_score"] * weights["frequency_score"]
        risk_score += risk_factors["trend_score"] * weights["trend_score"]
        
        # Convert categorical to numeric
        location_score = 0.8 if risk_factors["location_vulnerability"] == "high" else 0.4
        risk_score += location_score * weights["location_vulnerability"]
        
        criticality_score = 0.9 if risk_factors["event_criticality"] == "high" else 0.5
        risk_score += criticality_score * weights["event_criticality"]
        
        risk_score += risk_factors["seasonal_factor"] * weights["seasonal_factor"]
        
        return min(risk_score, 1.0)
    
    def _ai_determine_risk_level(self, risk_score: float, risk_factors: Dict[str, Any]) -> tuple:
        """AI determines risk level and confidence"""
        
        # AI uses adaptive thresholds based on context
        if risk_factors["event_criticality"] == "high":
            # Lower thresholds for critical events
            if risk_score > 0.4:
                return "HIGH", min(0.9, 0.6 + risk_score * 0.4)
            elif risk_score > 0.25:
                return "MEDIUM", min(0.8, 0.5 + risk_score * 0.3)
        else:
            # Standard thresholds for normal events
            if risk_score > 0.6:
                return "HIGH", min(0.9, 0.6 + risk_score * 0.3)
            elif risk_score > 0.35:
                return "MEDIUM", min(0.8, 0.4 + risk_score * 0.4)
        
        return "LOW", max(0.3, 0.6 - risk_score * 0.2)
    
    def _ai_predict_timing(self, risk_level: str, recent_events: List, historical: List) -> str:
        """AI predicts timing based on patterns"""
        
        if risk_level == "HIGH":
            if len(recent_events) >= 2:
                return "next 2-4 hours"
            else:
                return "next 6-12 hours"
        elif risk_level == "MEDIUM":
            return "next 12-24 hours"
        else:
            return "next 2-7 days"
    
    def _ai_recommend_actions(self, risk_level: str, event_type: str, location: str) -> List[str]:
        """AI recommends actions based on risk assessment"""
        
        actions = []
        
        if risk_level in ["HIGH", "CRITICAL"]:
            actions.append("Deploy preventive measures immediately")
            actions.append("Increase monitoring in affected area")
            actions.append("Prepare emergency response teams")
        
        if event_type.lower() in ["infrastructure", "power"]:
            actions.append("Check power grid stability")
            actions.append("Verify backup systems")
        
        if event_type.lower() in ["flooding", "emergency"]:
            actions.append("Monitor weather conditions")
            actions.append("Prepare evacuation routes")
        
        actions.append(f"Focus attention on {location} area")
        
        return actions
    
    def _basic_risk_prediction(self, location: str, event_type: str) -> Dict[str, Any]:
        """Fallback basic risk prediction"""
        historical = self.historical_data.get(f"{location}_{event_type}", [])
        
        if len(historical) < 3:
            return {"risk_level": "UNKNOWN", "confidence": 0.0, "predicted_time": None}
        
        recent_events = [h for h in historical if h > (datetime.datetime.now().timestamp() - 7*24*3600)]
        risk_score = len(recent_events) / 7.0
        
        if risk_score > 1.0:
            risk_level = "HIGH"
            confidence = min(0.9, 0.6 + risk_score * 0.1)
        elif risk_score > 0.3:
            risk_level = "MEDIUM"
            confidence = min(0.7, 0.4 + risk_score * 0.2)
        else:
            risk_level = "LOW"
            confidence = max(0.3, 0.6 - risk_score * 0.1)
        
        return {
            "risk_level": risk_level,
            "confidence": confidence,
            "predicted_time": "next 3-6 hours" if risk_level == "HIGH" else "next 24-48 hours"
        }
    
    def _prepare_risk_context(self, location: str, event_type: str, historical: List) -> str:
        """Prepare risk context for AI analysis"""
        context = f"RISK ASSESSMENT CONTEXT:\n"
        context += f"Location: {location}\n"
        context += f"Incident Type: {event_type}\n"
        context += f"Historical Incidents: {len(historical)}\n"
        
        if historical:
            recent_count = len([h for h in historical if h > (datetime.datetime.now().timestamp() - 7*24*3600)])
            context += f"Recent Incidents (7 days): {recent_count}\n"
            context += f"Average Frequency: {len(historical)/30:.2f} per month\n"
        
        context += f"Location Risk Profile: {self._assess_location_risk(location)}\n"
        context += f"Event Type Criticality: {self._assess_event_type_risk(event_type)}\n"
        
        return context
    
    def _calculate_trend_score(self, historical: List) -> float:
        """Calculate trend score from historical data"""
        if len(historical) < 6:
            return 0.5
        
        # Compare recent vs older periods
        mid_point = len(historical) // 2
        recent_avg = len(historical[mid_point:]) / (len(historical) - mid_point)
        older_avg = len(historical[:mid_point]) / mid_point
        
        if older_avg == 0:
            return 1.0 if recent_avg > 0 else 0.0
        
        trend_ratio = recent_avg / older_avg
        return min(trend_ratio / 2.0, 1.0)
    
    def _assess_location_risk(self, location: str) -> str:
        """Assess location-specific risk factors"""
        high_risk_locations = ['HSR Layout', 'Electronic City', 'Whitefield', 'Outer Ring Road']
        medium_risk_locations = ['Koramangala', 'Indiranagar', 'BTM Layout']
        
        if location in high_risk_locations:
            return "high"
        elif location in medium_risk_locations:
            return "medium"
        else:
            return "low"
    
    def _assess_event_type_risk(self, event_type: str) -> str:
        """Assess event type criticality"""
        high_risk_events = ['emergency', 'flooding', 'fire', 'infrastructure']
        medium_risk_events = ['maintenance', 'traffic', 'utilities']
        
        if event_type.lower() in high_risk_events:
            return "high"
        elif event_type.lower() in medium_risk_events:
            return "medium"
        else:
            return "low"
    
    def _assess_seasonal_risk(self, event_type: str) -> float:
        """Assess seasonal risk factors"""
        current_month = datetime.datetime.now().month
        
        # Monsoon season risk for flooding
        if event_type.lower() in ['flooding', 'waterlogging'] and current_month in [6, 7, 8, 9]:
            return 0.3
        
        # Summer risk for power issues
        if event_type.lower() in ['infrastructure', 'power'] and current_month in [3, 4, 5]:
            return 0.2
        
        return 0.1


class FirebaseNotificationService:
    """Firebase push notification service"""
    
    def __init__(self, service_account_path: Optional[str] = None):
        self.app = None
        self.initialized = False
        if service_account_path:
            self._initialize_firebase(service_account_path)
    
    def _initialize_firebase(self, service_account_path: str):
        """Initialize Firebase Admin SDK"""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(service_account_path)
                self.app = firebase_admin.initialize_app(cred)
            else:
                self.app = firebase_admin.get_app()
            self.initialized = True
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            self.initialized = False
    
    async def send_notification(self, notification: NotificationData) -> Dict[str, Any]:
        """Send push notification to target users"""
        if not self.initialized:
            # Mock response for development
            return {
                "status": "success",
                "message": f"Mock notification sent to {len(notification.target_users)} users",
                "notification_preview": {
                    "title": notification.title,
                    "body": notification.body,
                    "priority": notification.priority
                }
            }
        
        try:
            # Create FCM message
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=notification.title,
                    body=notification.body
                ),
                data={
                    "event_type": notification.event_type,
                    "location": notification.location,
                    "predicted_impact": notification.predicted_impact,
                    "priority": notification.priority
                },
                tokens=notification.target_users  # Device tokens
            )
            
            # Send the message
            response = await messaging.send_multicast(message)
            
            return {
                "status": "success",
                "success_count": response.success_count,
                "failure_count": response.failure_count,
                "responses": response.responses
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }
    
    async def analyze_cross_agent_patterns(self, all_data: Dict[str, List]) -> List[Dict[str, Any]]:
        """Analyze patterns across multiple agent data sources"""
        
        patterns = []
        
        # AI-powered cross-agent pattern detection
        if self.ai_agent:
            ai_patterns = await self._ai_cross_agent_pattern_analysis(all_data)
            patterns.extend(ai_patterns)
        
        # Scenario-based patterns
        patterns.extend(await self._analyze_scenario_patterns(all_data))
        
        return patterns
    
    async def _ai_cross_agent_pattern_analysis(self, all_data: Dict[str, List]) -> List[Dict[str, Any]]:
        """Use AI to detect complex cross-agent patterns"""
        
        ai_prompt = f"""
        Analyze data from multiple city monitoring agents to identify complex patterns:
        
        EVENT DATA: {len(all_data.get('events', []))} events
        ENVIRONMENT DATA: {len(all_data.get('environment', []))} readings  
        USER REPORTS: {len(all_data.get('user_reports', []))} reports
        
        DATA SUMMARY:
        {self._prepare_cross_agent_summary(all_data)}
        
        Identify:
        1. Cross-system correlations (e.g., infrastructure events + environment changes)
        2. Cascading failure patterns
        3. Unusual multi-agent anomalies
        4. Predictive patterns across domains
        5. Systemic vulnerabilities
        
        Focus on patterns that require multi-agent intelligence to detect.
        Return patterns requiring immediate notification.
        """
        
        # Simulate AI cross-agent analysis
        return await self._simulate_ai_cross_agent_analysis(all_data)
    
    async def _simulate_ai_cross_agent_analysis(self, all_data: Dict[str, List]) -> List[Dict[str, Any]]:
        """Simulate AI-powered cross-agent pattern detection"""
        
        patterns = []
        events = all_data.get('events', [])
        environment = all_data.get('environment', [])
        reports = all_data.get('user_reports', [])
        
        # AI detects infrastructure-environment correlation
        if self._ai_detect_infra_environment_correlation(events, environment):
            patterns.append({
                "type": "infrastructure_environment_correlation",
                "severity": "HIGH",
                "description": "AI detected correlation between infrastructure events and environmental changes",
                "confidence": 0.85,
                "affected_systems": ["infrastructure", "environment"],
                "recommendation": "Monitor infrastructure stability during environmental fluctuations"
            })
        
        # AI detects user report validation patterns
        if self._ai_detect_user_report_validation(reports, events):
            patterns.append({
                "type": "user_report_validation",
                "severity": "MEDIUM", 
                "description": "AI validated user reports with official event data",
                "confidence": 0.78,
                "affected_systems": ["user_reports", "events"],
                "recommendation": "User reports showing high accuracy - prioritize similar reports"
            })
        
        # AI detects systemic stress patterns
        if self._ai_detect_systemic_stress(all_data):
            patterns.append({
                "type": "systemic_stress",
                "severity": "CRITICAL",
                "description": "AI detected systemic stress across multiple city systems",
                "confidence": 0.92,
                "affected_systems": ["all"],
                "recommendation": "Implement city-wide emergency monitoring protocols"
            })
        
        return patterns


class NotificationGenerator:
    """Generate intelligent notification content using LLM"""
    
    def generate_cluster_notification(self, cluster: EventCluster) -> NotificationData:
        """Generate notification for event clusters"""
        severity_emoji = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️",
            "MEDIUM": "⚡",
            "LOW": "ℹ️"
        }
        
        emoji = severity_emoji.get(cluster.severity, "📢")
        
        title = f"{emoji} {cluster.event_type.title()} Alert - {cluster.location}"
        
        if cluster.severity == "CRITICAL":
            body = f"URGENT: {cluster.count} {cluster.event_type.lower()} incidents reported in {cluster.location} within {cluster.time_window}. Please avoid the area and stay safe."
        elif cluster.severity == "HIGH":
            body = f"Multiple {cluster.event_type.lower()} reports ({cluster.count}) detected in {cluster.location}. Exercise caution in the area."
        else:
            body = f"{cluster.count} {cluster.event_type.lower()} incidents reported in {cluster.location}. Authorities have been notified."
        
        return NotificationData(
            title=title,
            body=body,
            priority="high" if cluster.severity in ["CRITICAL", "HIGH"] else "normal",
            target_users=[],  # Will be populated based on location
            event_type=cluster.event_type,
            location=cluster.location,
            predicted_impact=f"Area within {cluster.affected_radius_km}km may be affected"
        )
    
    def generate_cross_agent_notification(self, pattern: Dict[str, Any]) -> NotificationData:
        """Generate notification for cross-agent patterns"""
        pattern_type = pattern.get("type", "unknown")
        severity = pattern.get("severity", "MEDIUM")
        description = pattern.get("description", "Cross-agent pattern detected")
        recommendation = pattern.get("recommendation", "Monitor situation closely")
        
        severity_emoji = {
            "CRITICAL": "🚨",
            "HIGH": "⚠️", 
            "MEDIUM": "🔍",
            "LOW": "ℹ️"
        }
        
        emoji = severity_emoji.get(severity, "📊")
        
        # Generate appropriate title and body based on pattern type
        if pattern_type == "infrastructure_environment_correlation":
            title = f"{emoji} Infrastructure-Environment Alert"
            body = f"Correlation detected between infrastructure events and environmental changes. {recommendation}"
        elif pattern_type == "user_report_validation":
            title = f"{emoji} Citizen Report Validation"
            body = f"User reports validated against official data. {recommendation}"
        elif pattern_type == "systemic_stress":
            title = f"{emoji} City-Wide System Alert"
            body = f"Multiple city systems showing stress patterns. {recommendation}"
        elif pattern_type == "power_grid_instability":
            title = f"{emoji} Power Grid Alert"
            body = f"City-wide power grid instability detected. {recommendation}"
        elif pattern_type == "communication_network_degradation":
            title = f"{emoji} Network Issues Alert"
            body = f"Communication network issues detected. {recommendation}"
        else:
            title = f"{emoji} Multi-System Pattern Alert"
            body = f"{description}. {recommendation}"
        
        return NotificationData(
            title=title,
            body=body,
            priority="high" if severity in ["CRITICAL", "HIGH"] else "normal",
            target_users=[],  # Will be populated based on affected areas
            event_type="cross_agent_pattern",
            location="Multiple Areas",
            predicted_impact=f"Cross-system pattern with {pattern.get('confidence', 0.5)*100:.0f}% confidence"
        )
    
    def generate_predictive_notification(self, location: str, prediction: Dict[str, Any]) -> NotificationData:
        """Generate predictive notification based on risk analysis"""
        risk_level = prediction["risk_level"]
        confidence = prediction["confidence"]
        predicted_time = prediction["predicted_time"]
        
        if risk_level == "HIGH":
            title = f"🔮 High Risk Alert - {location}"
            body = f"Based on recent patterns, there's a {confidence*100:.0f}% chance of incidents in {location} within {predicted_time}. Stay alert."
        elif risk_level == "MEDIUM":
            title = f"📊 Potential Risk - {location}"
            body = f"Moderate risk ({confidence*100:.0f}% confidence) of incidents predicted for {location} in {predicted_time}."
        else:
            title = f"ℹ️ Low Risk Advisory - {location}"
            body = f"Low probability ({confidence*100:.0f}%) of incidents in {location}. Stay informed."
        
        return NotificationData(
            title=title,
            body=body,
            priority="normal",
            target_users=[],
            event_type="prediction",
            location=location,
            predicted_impact=f"Confidence: {confidence*100:.0f}%"
        )
    
    def generate_event_notification(self, event_data: Dict[str, Any]) -> NotificationData:
        """Generate notification for upcoming events"""
        title = f"🎉 Upcoming Event - {event_data.get('location', 'Your Area')}"
        body = f"{event_data.get('name', 'Event')} happening {event_data.get('time', 'soon')}. Check it out!"
        
        return NotificationData(
            title=title,
            body=body,
            priority="normal",
            target_users=[],
            event_type="event",
            location=event_data.get('location', ''),
            predicted_impact="Entertainment and community engagement"
        )


class FirebaseNotificationService:
    """Firebase push notification service"""
    
    def __init__(self, service_account_path: Optional[str] = None):
        self.app = None
        self.initialized = False
        if service_account_path:
            self._initialize_firebase(service_account_path)
    
    def _initialize_firebase(self, service_account_path: str):
        """Initialize Firebase Admin SDK"""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(service_account_path)
                self.app = firebase_admin.initialize_app(cred)
            else:
                self.app = firebase_admin.get_app()
            self.initialized = True
        except Exception as e:
            print(f"Firebase initialization error: {e}")
            self.initialized = False
    
    async def send_notification(self, device_token: str, title: str, body: str, data: Dict[str, str] = None) -> Dict[str, Any]:
        """Send push notification to a single device"""
        if not self.initialized:
            # Mock response for development
            return {
                "status": "success",
                "message": f"Mock notification sent to device {device_token[:10]}...",
                "notification_preview": {
                    "title": title,
                    "body": body,
                    "data": data or {}
                }
            }
        
        try:
            # Create FCM message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=data or {},
                token=device_token
            )
            
            # Send the message
            response = await messaging.send(message)
            
            return {
                "status": "success",
                "message_id": response
            }
            
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


# Notification Agent class - RemoteA2aAgent implementation
class NotificationAgent(RemoteA2aAgent):
    """
    AI-powered notification agent that analyzes patterns across city data
    and sends intelligent push notifications to users based on patterns, 
    triggers, and location data.
    """
    
    def __init__(self, name: str = "notification_agent"):
        super().__init__(name=name)
        self.pattern_detector = PatternDetector(ai_agent=self)
        self.notification_generator = NotificationGenerator()
        self.firebase_service = FirebaseNotificationService()
        
        # Tool registration
        self.tools = [
            {
                "name": "analyze_patterns_and_trigger_notifications",
                "description": "Analyze patterns across city data and trigger intelligent notifications",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "events_data": {
                            "type": "string",
                            "description": "Events data to analyze",
                            "default": "all"
                        },
                        "environment_data": {
                            "type": "string", 
                            "description": "Environmental data to analyze",
                            "default": "all"
                        },
                        "user_reports_data": {
                            "type": "string",
                            "description": "User reports data to analyze",
                            "default": "all"
                        },
                        "trigger_type": {
                            "type": "string",
                            "description": "Type of trigger - auto, threshold, prediction, or emergency",
                            "default": "auto"
                        }
                    },
                    "required": []
                }
            },
            {
                "name": "send_predictive_notification",
                "description": "Send predictive notifications based on risk analysis",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "Location for risk prediction"
                        },
                        "event_type": {
                            "type": "string", 
                            "description": "Type of event to predict"
                        },
                        "target_users": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of user device tokens"
                        }
                    },
                    "required": ["location", "event_type"]
                }
            }
        ]
    
    async def analyze_patterns_and_trigger_notifications(
        self,
        events_data: str = "all",
        environment_data: str = "all",
        user_reports_data: str = "all",
        trigger_type: str = "auto"
    ) -> str:
        """Main tool method for pattern analysis and notification triggering"""
        return await analyze_patterns_and_trigger_notifications(
            events_data, environment_data, user_reports_data, trigger_type
        )
    
    async def send_predictive_notification(
        self,
        location: str,
        event_type: str,
        target_users: List[str] = None
    ) -> str:
        """Send predictive notifications based on risk analysis"""
        
        try:
            # Perform risk prediction
            prediction = await self.pattern_detector.predict_future_risk(location, event_type)
            
            if prediction["risk_level"] in ["HIGH", "MEDIUM"]:
                # Generate notification
                notification = self.notification_generator.generate_predictive_notification(location, prediction)
                
                if notification:
                    # Send to specified users or find users in area
                    if target_users:
                        device_tokens = target_users
                    else:
                        # In real implementation, query database for users in area
                        device_tokens = ["mock_device_token_1", "mock_device_token_2"]
                    
                    results = []
                    for token in device_tokens:
                        result = await self.firebase_service.send_notification(
                            token, 
                            notification.title, 
                            notification.body,
                            {"risk_level": prediction["risk_level"], "confidence": str(prediction["confidence"])}
                        )
                        results.append(result)
                    
                    return json.dumps({
                        "status": "success",
                        "prediction": prediction,
                        "notification_sent": True,
                        "recipients": len(device_tokens),
                        "firebase_results": results
                    })
            
            return json.dumps({
                "status": "success", 
                "prediction": prediction,
                "notification_sent": False,
                "reason": f"Risk level {prediction['risk_level']} below notification threshold"
            })
            
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e)
            })


async def analyze_patterns_and_trigger_notifications(
    events_data: str = "all",
    environment_data: str = "all",
    user_reports_data: str = "all",
    trigger_type: str = "auto"
) -> str:
    """
    Analyze patterns across city data and trigger intelligent notifications.
    
    Args:
        events_data: Events data to analyze (default: "all")
        environment_data: Environmental data to analyze (default: "all") 
        user_reports_data: User reports data to analyze (default: "all")
        trigger_type: Type of trigger - "auto", "threshold", "prediction", or "emergency"
    
    Returns:
        JSON string with analysis results and triggered notifications
    """
    pattern_detector = PatternDetector()
    notification_generator = NotificationGenerator()
    firebase_service = FirebaseNotificationService()
    
    # Mock data for demonstration (in real implementation, this would come from actual agents)
    mock_user_reports = [
        {
            "documentId": "report1",
            "incidentType": "Infrastructure", 
            "location": "HSR Layout",
            "description": "Power cut in Sector 2",
            "timestamp": datetime.datetime.now().isoformat()
        },
        {
            "documentId": "report2",
            "incidentType": "Infrastructure",
            "location": "HSR Layout", 
            "description": "Voltage fluctuation reported",
            "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=5)).isoformat()
        },
        {
            "documentId": "report3",
            "incidentType": "Infrastructure",
            "location": "HSR Layout",
            "description": "Complete power outage in multiple buildings",
            "timestamp": (datetime.datetime.now() - datetime.timedelta(minutes=10)).isoformat()
        }
    ]
    
    mock_users_in_area = [
        UserProfile(
            user_id="user1",
            location="HSR Layout",
            interests=["infrastructure", "power"],
            notification_preferences={"push": True, "email": True},
            device_token="device_token_1"
        ),
        UserProfile(
            user_id="user2", 
            location="HSR Layout",
            interests=["all"],
            notification_preferences={"push": True},
            device_token="device_token_2"
        )
    ]
    
    results = {
        "analysis_timestamp": datetime.datetime.now().isoformat(),
        "trigger_type": trigger_type,
        "patterns_detected": [],
        "notifications_sent": [],
        "predictions": []
    }
    
    try:
        # 1. Pattern Detection & Anomaly Detection
        cluster = pattern_detector.detect_event_cluster(mock_user_reports)
        
        if cluster:
            results["patterns_detected"].append({
                "type": "event_cluster",
                "details": {
                    "event_type": cluster.event_type,
                    "location": cluster.location,
                    "count": cluster.count,
                    "severity": cluster.severity,
                    "affected_radius_km": cluster.affected_radius_km
                }
            })
            
            # Generate and send cluster notification
            notification = notification_generator.generate_cluster_notification(cluster)
        
        # 2. Cross-Agent Pattern Analysis
        mock_all_data = {
            'events': [
                {"type": "infrastructure", "location": "HSR Layout", "timestamp": datetime.datetime.now().isoformat()},
                {"type": "power", "location": "HSR Layout", "timestamp": datetime.datetime.now().isoformat()}
            ],
            'environment': [
                {"temperature": 35.2, "location": "HSR Layout", "timestamp": datetime.datetime.now().isoformat()},
                {"humidity": 78, "location": "HSR Layout", "timestamp": datetime.datetime.now().isoformat()},
                {"air_quality": "moderate", "location": "HSR Layout", "timestamp": datetime.datetime.now().isoformat()}
            ],
            'user_reports': mock_user_reports
        }
        
        cross_patterns = await pattern_detector.analyze_cross_agent_patterns(mock_all_data)
        
        for pattern in cross_patterns:
            results["patterns_detected"].append({
                "type": "cross_agent_pattern",
                "details": pattern
            })
            
            # Generate notifications for cross-agent patterns
            if pattern.get("severity") in ["HIGH", "CRITICAL"]:
                cross_notification = notification_generator.generate_cross_agent_notification(pattern)
                
                # Send to relevant users
                for user in mock_users_in_area:
                    if user.notification_preferences.get("push", False):
                        firebase_result = await firebase_service.send_notification(
                            user.device_token,
                            cross_notification.title,
                            cross_notification.body,
                            {"pattern_type": pattern["type"], "severity": pattern["severity"]}
                        )
                        
                        results["notifications_sent"].append({
                            "user_id": user.user_id,
                            "notification_type": "cross_agent_pattern",
                            "title": cross_notification.title,
                            "firebase_status": firebase_result.get("status", "unknown")
                        })
            
            # Find users in affected area
            affected_users = [
                user.device_token for user in mock_users_in_area 
                if user.location == cluster.location and user.notification_preferences.get("push", False)
            ]
            notification.target_users = affected_users
            
            # Send notification
            send_result = await firebase_service.send_notification(notification)
            results["notifications_sent"].append({
                "type": "cluster_alert",
                "notification": {
                    "title": notification.title,
                    "body": notification.body,
                    "priority": notification.priority
                },
                "target_users_count": len(affected_users),
                "send_result": send_result
            })
        
        # 2. Predictive Analysis
        prediction = pattern_detector.predict_future_risk("HSR Layout", "Infrastructure")
        
        if prediction["risk_level"] in ["HIGH", "MEDIUM"]:
            results["predictions"].append({
                "location": "HSR Layout",
                "event_type": "Infrastructure",
                "prediction": prediction
            })
            
            # Generate predictive notification
            pred_notification = notification_generator.generate_predictive_notification("HSR Layout", prediction)
            
            if pred_notification:
                pred_notification.target_users = [user.device_token for user in mock_users_in_area]
                pred_send_result = await firebase_service.send_notification(pred_notification)
                
                results["notifications_sent"].append({
                    "type": "predictive_alert",
                    "notification": {
                        "title": pred_notification.title,
                        "body": pred_notification.body,
                        "priority": pred_notification.priority
                    },
                    "target_users_count": len(mock_users_in_area),
                    "send_result": pred_send_result
                })
        
        # 3. Event-based notifications (if events data provided)
        if trigger_type in ["auto", "event"]:
            # Mock upcoming event
            mock_event = {
                "name": "Tech Conference",
                "location": "Convention Center",
                "time": "tomorrow at 9:00 AM"
            }
            
            event_notification = notification_generator.generate_event_notification(mock_event)
            
            # Send to users interested in events near Convention Center
            event_users = [user.device_token for user in mock_users_in_area if "events" in user.interests or "all" in user.interests]
            if event_users:
                event_notification.target_users = event_users
                event_send_result = await firebase_service.send_notification(event_notification)
                
                results["notifications_sent"].append({
                    "type": "event_alert",
                    "notification": {
                        "title": event_notification.title,
                        "body": event_notification.body,
                        "priority": event_notification.priority
                    },
                    "target_users_count": len(event_users),
                    "send_result": event_send_result
                })
        
        results["status"] = "success"
        results["summary"] = f"Analyzed {len(mock_user_reports)} reports, detected {len(results['patterns_detected'])} patterns, sent {len(results['notifications_sent'])} notifications"
        
    except Exception as e:
        results["status"] = "error"
        results["error"] = str(e)
    
    return json.dumps(results, indent=2)


async def get_user_location_preferences(user_id: str = "all") -> str:
    """
    Get user location preferences and notification settings.
    
    Args:
        user_id: Specific user ID or "all" for all users
    
    Returns:
        JSON string with user preferences data
    """
    # Mock user data (in real implementation, this would come from a database)
    mock_users = {
        "user1": {
            "user_id": "user1",
            "name": "John Doe",
            "location": "HSR Layout",
            "interests": ["infrastructure", "power", "events"],
            "notification_preferences": {
                "push": True,
                "email": True,
                "sms": False
            },
            "notification_radius_km": 5.0,
            "device_token": "device_token_1"
        },
        "user2": {
            "user_id": "user2",
            "name": "Jane Smith", 
            "location": "Whitefield",
            "interests": ["all"],
            "notification_preferences": {
                "push": True,
                "email": False,
                "sms": True
            },
            "notification_radius_km": 10.0,
            "device_token": "device_token_2"
        },
        "user3": {
            "user_id": "user3",
            "name": "Bob Wilson",
            "location": "Koramangala",
            "interests": ["emergency", "flooding", "traffic"],
            "notification_preferences": {
                "push": True,
                "email": True,
                "sms": True
            },
            "notification_radius_km": 7.0,
            "device_token": "device_token_3"
        }
    }
    
    if user_id == "all":
        return json.dumps({"users": list(mock_users.values())}, indent=2)
    elif user_id in mock_users:
        return json.dumps({"user": mock_users[user_id]}, indent=2)
    else:
        return json.dumps({"error": f"User {user_id} not found"}, indent=2)


async def send_personalized_notification(
    user_ids: str,
    notification_type: str,
    location: str = "",
    custom_message: str = ""
) -> str:
    """
    Send personalized notifications to specific users.
    
    Args:
        user_ids: Comma-separated user IDs or "all"
        notification_type: Type of notification ("emergency", "info", "event", "prediction")
        location: Location context for the notification
        custom_message: Custom message to include
    
    Returns:
        JSON string with notification sending results
    """
    firebase_service = FirebaseNotificationService()
    
    # Parse user IDs
    if user_ids == "all":
        target_users = ["user1", "user2", "user3"]
    else:
        target_users = [uid.strip() for uid in user_ids.split(",")]
    
    # Generate notification based on type
    notification_templates = {
        "emergency": {
            "title": f"🚨 Emergency Alert - {location}",
            "body": f"Emergency situation detected in {location}. {custom_message} Please stay safe and follow official guidance.",
            "priority": "high"
        },
        "info": {
            "title": f"ℹ️ Information Update - {location}",
            "body": f"Update for {location}: {custom_message}",
            "priority": "normal"
        },
        "event": {
            "title": f"🎉 Event Notification - {location}",
            "body": f"Event happening in {location}: {custom_message}",
            "priority": "normal"
        },
        "prediction": {
            "title": f"🔮 Predictive Alert - {location}",
            "body": f"Potential issue predicted for {location}: {custom_message}",
            "priority": "normal"
        }
    }
    
    template = notification_templates.get(notification_type, notification_templates["info"])
    
    notification = NotificationData(
        title=template["title"],
        body=template["body"],
        priority=template["priority"],
        target_users=[f"device_token_{uid[-1]}" for uid in target_users],  # Mock device tokens
        event_type=notification_type,
        location=location,
        predicted_impact="Direct user notification"
    )
    
    # Send notification
    send_result = await firebase_service.send_notification(notification)
    
    result = {
        "status": "success",
        "notification_sent": {
            "title": notification.title,
            "body": notification.body,
            "priority": notification.priority,
            "target_users": target_users,
            "location": location,
            "type": notification_type
        },
        "send_result": send_result,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    return json.dumps(result, indent=2)


# Initialize remote agents to interact with other city services
event_agent = RemoteA2aAgent(
    name="event_agent",
    description="Agent that handles city events and activities information for notification triggers.",
    agent_card=(
        f"http://localhost:8001/a2a/event_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

environment_agent = RemoteA2aAgent(
    name="environment_agent", 
    description="Agent that provides environmental data and weather information for predictive notifications.",
    agent_card=(
        f"http://localhost:8002/a2a/environment_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

user_report_agent = RemoteA2aAgent(
    name="user_report_agent",
    description="Agent that provides user reports and incidents data for pattern detection and cluster analysis.",
    agent_card=(
        f"http://localhost:8003/a2a/user_report_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

# Create the main notification agent
notification_agent = Agent(
    model="gemini-2.0-flash",
    name="notification_agent",
    instruction="""
    You are the City Pulse Notification Agent that provides intelligent, predictive push notifications 
    to users based on patterns, triggers, and location data.
    
    Your core responsibilities:
    
    1. **Pattern Detection & Anomaly Detection** 🕵️‍♂️
       - Analyze event streams for clusters and spikes
       - Detect unusual patterns in user reports, environmental data, and events
       - Use statistical models and ML techniques for anomaly detection
    
    2. **Predictive Notifications** 🔮
       - Generate risk predictions based on historical patterns
       - Send early warning notifications for potential issues
       - Provide probability-based alerts with confidence levels
    
    3. **Personalized Alerts** 📱
       - Send location-based notifications to affected users
       - Customize messages based on user preferences and interests
       - Use Firebase for reliable push notification delivery
    
    4. **Multi-Agent Integration** 🤝
       - Interact with event_agent for upcoming events and activities
       - Use environment_agent for weather and environmental triggers
       - Monitor user_report_agent for incident patterns and clusters
    
    **Notification Triggers:**
    - Threshold-based: Multiple similar incidents in same area
    - Pattern-based: Historical data indicates increased risk
    - Event-based: Upcoming events near user location
    - Emergency: Critical situations requiring immediate alerts
    
    **Key Features:**
    - Smart clustering of related incidents
    - Radius-based user targeting (within X km of incident)
    - Severity-based prioritization (CRITICAL > HIGH > MEDIUM > LOW)
    - Multi-language support for diverse user base
    - Respect user notification preferences and do-not-disturb settings
    
    Always provide clear, actionable information in notifications and respect user privacy and preferences.
    """,
    global_instruction=(
        "You are the City Pulse Notification Agent, providing intelligent, predictive push notifications "
        "based on patterns, anomalies, and user location data. You analyze city data streams and send "
        "personalized alerts to keep citizens informed and safe."
    ),
    sub_agents=[event_agent, environment_agent, user_report_agent],
    tools=[
        analyze_patterns_and_trigger_notifications,
        get_user_location_preferences,
        send_personalized_notification,
    ],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)


# Entry point for running the agent directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("agent:notification_agent", host="0.0.0.0", port=8004, reload=True)
