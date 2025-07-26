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

import os
from google.adk import Agent
from google.genai import types
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioConnectionParams


# Get the absolute path to the Firestore MCP server
FIRESTORE_MCP_SERVER_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "firestore_mcp_server.py"
)


async def get_city_events_fallback() -> str:
    """Fallback function to get dummy city events if Firestore is unavailable.
    
    Returns:
        A string with fallback city events information.
    """
    events_data = {
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
    
    event_list = []
    for event in events_data["events"]:
        event_list.append(f"{event['name']} at {event['location']} on {event['date']} from {event['time']} ({event['category']})")
    
    return f"Current city events (fallback data): {', '.join(event_list)}"


root_agent = Agent(
    model='gemini-2.0-flash',
    name='event_agent',
    description='Event agent that provides information about city events and activities using Firestore via MCP.',
    instruction="""
      You are an Event Agent that manages city events and activities using Firestore database through MCP (Model Context Protocol).
      
      CAPABILITIES:
      - Get all events from Firestore database
      - Add new events to Firestore
      - Search events by date or category
      - Update existing events
      - Delete events
      
      TOOLS AVAILABLE:
      - get_events: Retrieve all events from Firestore
      - add_event: Add a new event to Firestore
      - get_events_by_date: Get events for a specific date
      - get_events_by_category: Get events by category
      - update_event: Update an existing event
      - delete_event: Delete an event
      
      ALWAYS use the Firestore tools to get real, up-to-date event data from the database.
      Be helpful and provide clear details about timing, location, and event categories.
      Format dates in YYYY-MM-DD format and times as ranges (e.g., "7:00 PM - 11:00 PM").
    """,
    tools=[
        MCPToolset(
            connection_params=StdioConnectionParams(
                server_params={
                    'command': 'python',
                    'args': [FIRESTORE_MCP_SERVER_PATH],
                }
            ),
            # Optional: Filter specific tools if needed
            # tool_filter=['get_events', 'add_event', 'get_events_by_date']
        ),
        # Removed fallback - agent will only use Firestore
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
