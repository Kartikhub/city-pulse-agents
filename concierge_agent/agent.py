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
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools.example_tool import ExampleTool
from google.genai import types
import json


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
            "parts": [{"text": "What events are happening on Friday"}],
        },
        "output": [
            {
                "role": "model",
                "parts": [{"text": "On Friday, July 25th, there is a Summer Music Festival at Central Park from 7:00 PM to 11:00 PM."}],
            }
        ],
    },
    {
        "input": {
            "role": "user",
            "parts": [{"text": "What are the events happening on Sunday and what will the air quality be in those events?"}],
        },
        "output": [
            {
                "role": "model",
                "parts": [{"text": "On Sunday, July 27th, there is a Tech Conference at Convention Center from 9:00 AM to 5:00 PM."}],
            },
            {
                "role": "model",
                "parts": [{"text": "Air quality at Convention Center: Good (Index: 38). Excellent conditions for the conference!"}],
            }
        ],
    }
])

def return_events_ui(type: str, name: str, location: str, description: str) -> str:
    """
    {
    "name": "return_events_ui",
    "description": "Creates or displays an event in the user interface with the given details. Use this to add new events to a calendar or list.",
    "parameters": {
        "type": "object",
        "properties": {
        "type": {
            "type": "string",
            "description": "The category or type of the event, for example: 'meeting', 'appointment', 'social', or 'reminder'."
        },
        "name": {
            "type": "string",
            "description": "The official name or title of the event."
        },
        "location": {
            "type": "string",
            "description": "The physical address or virtual link for the event location."
        },
        "description": {
            "type": "string",
            "description": "A brief summary or detailed description of the event's purpose and agenda."
        }
        },
        "required": ["type", "name", "location", "description"]
    }
    }
    """
    event_data = {
            "type": type,
            "name": name,
            "location": location,
            "description": description
        }
    return json.dumps(event_data)

event_agent = RemoteA2aAgent(
    name="event_agent",
    description="Agent that handles city events and activities information.",
    agent_card=(
        f"http://localhost:8001/a2a/event_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

environment_agent = RemoteA2aAgent(
    name="environment_agent", 
    description="Agent that handles environmental data and weather information for all locations or specific locations.",
    agent_card=(
        f"http://localhost:8002/a2a/environment_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

root_agent = Agent(
    model="gemini-2.5-flash",
    name="concierge_agent",
    instruction="""
      CRITICAL: **Call the respective return_element_ui tool to return properly formatted data if called by a UI user before final response.**

      You are the City Pulse Concierge Agent that provides city information.
      You have access to event_agent and environment_agent.
      You have 2 types of interactions.
      1: User Interaction
      CRITICAL: When users ask about BOTH events AND air quality:
      1. Call event_agent to get events and locations
      2. IMMEDIATELY call environment_agent with the location from step 1
      3. Provide both results in one response
      
    """,
    global_instruction=(
        "You are City Pulse Concierge agent, serving UI for both API and user interactions, ready to help with city events and environmental information based on location."
    ),
    sub_agents=[event_agent, environment_agent],
    tools=[example_tool, return_events_ui],
    generate_content_config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.OFF,
            ),
        ]
    ),
)
