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
                "parts": [{"text": "Here's the latest city information: There's a Summer Music Festival tonight at Central Park, and the air quality is Good with pleasant weather conditions."}],
            },
        ],
    },
])

event_agent = RemoteA2aAgent(
    name="event_agent",
    description="Agent that handles city events and activities information.",
    agent_card=(
        f"http://localhost:8001/a2a/event_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

environment_agent = RemoteA2aAgent(
    name="environment_agent", 
    description="Agent that handles environmental data and weather information.",
    agent_card=(
        f"http://localhost:8002/a2a/environment_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

root_agent = Agent(
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
