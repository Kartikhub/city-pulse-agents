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

from google.adk import Agent
from google.genai import types


async def get_environment_data(location: str = "all") -> str:
    """Get current environmental conditions and air quality data for a specific location or all locations.
    
    Args:
        location: The location to get environmental data for. Options: "Central Park", "Downtown Square", 
                 "Convention Center", or "all" for all locations.
    
    Returns:
        A string with current environmental information for the specified location(s).
    """
    env_data = {
        "temperature": "24°C",
        "humidity": "65%",
        "air_quality_by_location": {
            "Central Park": {
                "index": 42,
                "status": "Good",
                "pm25": "12 μg/m³",
                "pm10": "18 μg/m³"
            },
            "Downtown Square": {
                "index": 55,
                "status": "Moderate",
                "pm25": "18 μg/m³",
                "pm10": "25 μg/m³"
            },
            "Convention Center": {
                "index": 38,
                "status": "Good",
                "pm25": "10 μg/m³",
                "pm10": "15 μg/m³"
            }
        },
        "weather": "Partly Cloudy",
        "uv_index": 6,
        "wind": {
            "speed": "15 km/h",
            "direction": "NW"
        },
        "recommendations": [
            "Great day for outdoor activities",
            "Consider sunscreen due to moderate UV levels",
            "Air quality varies by location - check specific areas before outdoor events"
        ]
    }
    
    # Format air quality by location
    if location == "all":
        air_quality_details = []
        for loc, aq_data in env_data['air_quality_by_location'].items():
            air_quality_details.append(f"{loc}: {aq_data['status']} (Index: {aq_data['index']}, PM2.5: {aq_data['pm25']}, PM10: {aq_data['pm10']})")
        
        return (f"Current environmental conditions: Temperature {env_data['temperature']}, "
                f"Humidity {env_data['humidity']}, Weather {env_data['weather']}, "
                f"UV Index {env_data['uv_index']}, Wind {env_data['wind']['speed']} {env_data['wind']['direction']}. "
                f"Air Quality by Location: {'; '.join(air_quality_details)}. "
                f"Recommendations: {', '.join(env_data['recommendations'])}")
    else:
        # Return data for specific location
        if location in env_data['air_quality_by_location']:
            aq_data = env_data['air_quality_by_location'][location]
            return (f"Environmental conditions at {location}: Temperature {env_data['temperature']}, "
                    f"Humidity {env_data['humidity']}, Weather {env_data['weather']}, "
                    f"UV Index {env_data['uv_index']}, Wind {env_data['wind']['speed']} {env_data['wind']['direction']}. "
                    f"Air Quality: {aq_data['status']} (Index: {aq_data['index']}, PM2.5: {aq_data['pm25']}, PM10: {aq_data['pm10']}). "
                    f"Recommendations: {', '.join(env_data['recommendations'])}")
        else:
            available_locations = list(env_data['air_quality_by_location'].keys())
            return (f"Location '{location}' not found. Available locations: {', '.join(available_locations)}. "
                    f"General conditions: Temperature {env_data['temperature']}, Weather {env_data['weather']}, "
                    f"UV Index {env_data['uv_index']}, Wind {env_data['wind']['speed']} {env_data['wind']['direction']}.")


root_agent = Agent(
    model='gemini-2.5-flash-lite',
    name='environment_agent',
    description='Environment agent that provides environmental data including weather, air quality, and health recommendations.',
    instruction="""
      You provide environmental information including weather, air quality, and health recommendations.
      When asked about environmental conditions, call the get_environment_data tool to get current data.
      You can provide data for specific locations (Central Park, Downtown Square, Convention Center) or all locations.
      If a user asks about conditions at a specific location or for a specific event, use the location parameter.
      Provide clear, actionable information about air quality and weather conditions.
    """,
    tools=[
        get_environment_data,
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
