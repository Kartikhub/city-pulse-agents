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


async def get_city_events() -> str:
    """Get current city events and activities.
    
    Returns:
        A string with current city events information.
    """
    events_data = {
        "events": [
            {
                "name": "Summer Music Festival",
                "location": "Central Park",
                "time": "7:00 PM - 11:00 PM",
                "date": "2025-08-02",
                "category": "Entertainment"
            },
            {
                "name": "Farmers Market", 
                "location": "Downtown Square",
                "time": "8:00 AM - 2:00 PM",
                "date": "2025-08-02",
                "category": "Shopping"
            },
            {
                "name": "Tech Conference",
                "location": "Convention Center", 
                "time": "9:00 AM - 5:00 PM",
                "date": "2025-08-03",
                "category": "Business"
            }
        ]
    }
    
    event_list = []
    for event in events_data["events"]:
        event_list.append(f"{event['name']} at {event['location']} on {event['date']} from {event['time']} ({event['category']})")
    
    return f"Current city events: {', '.join(event_list)}"


root_agent = Agent(
    model='gemini-2.0-flash',
    name='event_agent',
    description='Event agent that provides information about city events and activities.',
    instruction="""
      You provide information about city events, activities, and entertainment.
      When asked about events, call the get_city_events tool to get current event information.
      Be helpful and provide clear details about timing, location, and event categories.
    """,
    tools=[
        get_city_events,
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
