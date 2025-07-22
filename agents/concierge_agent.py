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

from google.adk.agents import Agent
from google.adk.tools.example_tool import ExampleTool
from google.genai import types


# --- Event Sub-Agent ---
def get_city_events() -> dict:
    """Get current city events and activities."""
    return {
        "events": [
            {
                "name": "Summer Music Festival",
                "location": "Central Park",
                "time": "7:00 PM - 11:00 PM",
                "date": "2025-07-25",
                "category": "Entertainment"
            },
            {
                "name": "Farmers Market",
                "location": "Downtown Square",
                "time": "8:00 AM - 2:00 PM",
                "date": "2025-07-26",
                "category": "Shopping"
            },
            {
                "name": "Tech Conference",
                "location": "Convention Center",
                "time": "9:00 AM - 5:00 PM",
                "date": "2025-07-27",
                "category": "Business"
            }
        ]
    }


event_agent = Agent(
    name="event_agent",
    description="Handles city events, activities, and entertainment information.",
    instruction="""
      You are responsible for providing information about city events, activities, and entertainment.
      When asked about events, you must call the get_city_events tool to get current event information.
      Provide helpful details about timing, location, and event categories.
    """,
    tools=[get_city_events],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)


# --- Environment Sub-Agent ---
def get_environment_data() -> dict:
    """Get current environmental conditions and air quality data."""
    return {
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


environment_agent = Agent(
    name="environment_agent",
    description="Provides environmental data including weather, air quality, and health recommendations.",
    instruction="""
      You are responsible for providing environmental information including weather, air quality, and health recommendations.
      When asked about environmental conditions, you must call the get_environment_data tool to get current data.
      Provide clear, actionable information about air quality and weather conditions.
    """,
    tools=[get_environment_data],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)


example_tool = ExampleTool([
    {
        "input": {
            "role": "user",
            "parts": [{"text": "What events are happening this weekend?"}],
        },
        "output": [
            {"role": "model", "parts": [{"text": "Here are the upcoming events: Summer Music Festival at Central Park on July 25th from 7:00 PM to 11:00 PM."}]}
        ],
    },
    {
        "input": {
            "role": "user",
            "parts": [{"text": "How's the air quality today?"}],
        },
        "output": [{
            "role": "model",
            "parts": [{"text": "The air quality is Good with an index of 42. Great day for outdoor activities!"}],
        }],
    },
    {
        "input": {
            "role": "user",
            "parts": [{"text": "Give me both event and environment information."}],
        },
        "output": [
            {
                "role": "model",
                "parts": [{"text": "Here's the latest information: There's a Summer Music Festival tonight at Central Park, and the air quality is Good with pleasant weather conditions."}],
            },
        ],
    },
])


concierge_agent = Agent(
    model="gemini-2.0-flash",
    name="concierge_agent",
    instruction="""
      You are the City Pulse Concierge Agent, a helpful assistant that provides personalized city information.
      You delegate event-related requests to the event_agent and environment-related requests to the environment_agent.
      Follow these steps:
      1. If the user asks about events, activities, or entertainment, delegate to the event_agent.
      2. If the user asks about weather, air quality, or environmental conditions, delegate to the environment_agent.
      3. If the user asks for comprehensive city information, call both agents and combine the results.
      4. Always provide personalized, helpful responses based on the agent data.
      Always clarify and combine the results in a user-friendly manner.
    """,
    global_instruction=(
        "You are City Pulse Concierge, ready to help with city events and environmental information."
    ),
    sub_agents=[event_agent, environment_agent],
    tools=[example_tool],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
