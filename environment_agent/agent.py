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


async def get_environment_data() -> str:
    """Get current environmental conditions and air quality data.
    
    Returns:
        A string with current environmental information.
    """
    env_data = {
        "temperature": "24°C",
        "humidity": "65%",
        "air_quality": {
            "index": 42,
            "status": "Good",
            "pm25": "12 μg/m³",
            "pm10": "18 μg/m³"
        },
        "weather": "Partly Cloudy",
        "uv_index": 6,
        "wind": {
            "speed": "15 km/h",
            "direction": "NW"
        },
        "recommendations": [
            "Great day for outdoor activities",
            "Consider sunscreen due to moderate UV levels"
        ]
    }
    
    return (f"Current environmental conditions: Temperature {env_data['temperature']}, "
            f"Humidity {env_data['humidity']}, Weather {env_data['weather']}, "
            f"Air Quality {env_data['air_quality']['status']} (Index: {env_data['air_quality']['index']}), "
            f"UV Index {env_data['uv_index']}, Wind {env_data['wind']['speed']} {env_data['wind']['direction']}. "
            f"Recommendations: {', '.join(env_data['recommendations'])}")


root_agent = Agent(
    model='gemini-2.0-flash',
    name='environment_agent',
    description='Environment agent that provides environmental data including weather, air quality, and health recommendations.',
    instruction="""
      You provide environmental information including weather, air quality, and health recommendations.
      When asked about environmental conditions, call the get_environment_data tool to get current data.
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
