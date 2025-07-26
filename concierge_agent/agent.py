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

import json

from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from google.adk.tools.example_tool import ExampleTool
from google.genai import types


# --- JSON Formatter Sub-Agent ---
def format_to_json(data: str, data_type: str = "general") -> str:
    """Convert text data to structured JSON format."""
    try:
        if data_type == "events":
            # Parse event data and structure it
            lines = data.split(',')
            events = []
            for line in lines:
                line = line.strip()
                if 'at' in line and 'on' in line:
                    parts = line.split(' at ')
                    if len(parts) >= 2:
                        name = parts[0].strip()
                        rest = parts[1].split(' on ')
                        if len(rest) >= 2:
                            location = rest[0].strip()
                            date_time = rest[1].strip()
                            events.append({
                                "name": name,
                                "location": location,
                                "datetime": date_time
                            })
            return json.dumps({"events": events}, indent=2)
        
        elif data_type == "environment":
            # Parse environmental data and structure it
            result = {"environmental_data": {}}
            if "Temperature" in data:
                import re
                temp_match = re.search(r'Temperature (\d+°C)', data)
                if temp_match:
                    result["environmental_data"]["temperature"] = temp_match.group(1)
                
                humidity_match = re.search(r'Humidity (\d+%)', data)
                if humidity_match:
                    result["environmental_data"]["humidity"] = humidity_match.group(1)
                
                weather_match = re.search(r'Weather ([^,]+)', data)
                if weather_match:
                    result["environmental_data"]["weather"] = weather_match.group(1).strip()
                
                # Extract air quality info
                if "Air Quality" in data:
                    aq_match = re.search(r'Air Quality: ([^(]+)\(Index: (\d+)', data)
                    if aq_match:
                        result["environmental_data"]["air_quality"] = {
                            "status": aq_match.group(1).strip(),
                            "index": int(aq_match.group(2))
                        }
            
            return json.dumps(result, indent=2)
        
        else:
            # General formatting
            return json.dumps({"data": data, "type": data_type}, indent=2)
            
    except Exception as e:
        return json.dumps({"error": f"Failed to format data: {str(e)}", "raw_data": data}, indent=2)


json_formatter_agent = Agent(
    name="json_formatter_agent",
    description="Handles converting text data to structured JSON format.",
    instruction="""
      You are responsible for converting text data received from other agents into structured JSON format.
      When asked to format data, you must call the format_to_json tool with the data and specify the data type.
      Data types can be: 'events', 'environment', or 'general'.
    """,
    tools=[format_to_json],
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
    },
    {
        "input": {
            "role": "user",
            "parts": [{"text": "What events are happening this weekend in JSON format?"}],
        },
        "output": [
            {
                "role": "model",
                "parts": [{"text": "Here are the upcoming events: Summer Music Festival at Central Park on July 25th from 7:00 PM to 11:00 PM."}],
            },
            {"role": "model", "parts": [{"text": "{\n  \"events\": [\n    {\n      \"name\": \"Summer Music Festival\",\n      \"location\": \"Central Park\",\n      \"datetime\": \"July 25th from 7:00 PM to 11:00 PM\"\n    }\n  ]\n}"}]}
        ],
    },
    {
        "input": {
            "role": "user",
            "parts": [{"text": "Give me air quality data in JSON format"}],
        },
        "output": [
            {
                "role": "model",
                "parts": [{"text": "The air quality is Good with an index of 42. Great day for outdoor activities!"}],
            },
            {
                "role": "model",
                "parts": [{"text": "{\n  \"environmental_data\": {\n    \"air_quality\": {\n      \"status\": \"Good\",\n      \"index\": 42\n    },\n    \"temperature\": \"24°C\",\n    \"weather\": \"Partly Cloudy\"\n  }\n}"}],
            }
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
    description="Agent that handles environmental data and weather information for all locations or specific locations.",
    agent_card=(
        f"http://localhost:8002/a2a/environment_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="concierge_agent",
    instruction="""
      You are the City Pulse Concierge Agent that provides city information.
      You have access to event_agent, environment_agent, and json_formatter_agent.
      
      CRITICAL WORKFLOW:
      1. When users ask about events: Call event_agent to get events data and return the response in normal text format
      2. When users ask about environment/air quality: Call environment_agent to get environmental data and return in normal text format
      3. When users ask about BOTH events AND air quality:
         a. Call event_agent to get events and locations
         b. Call environment_agent with the location from step a
         c. Provide both results in one response in normal text format
      
      JSON FORMAT REQUESTS:
      - When users explicitly request "JSON format" or "in JSON":
        1. First call the appropriate agent (event_agent or environment_agent) to get the data
        2. Then immediately call json_formatter_agent with the data and correct data_type
        3. Return ONLY the JSON output from json_formatter_agent - no additional text or explanation
      - For events JSON: use data_type="events"
      - For environment JSON: use data_type="environment"
      - For combined requests in JSON: call both agents sequentially, then format each with json_formatter_agent
      
      When JSON is requested, the final response must be pure JSON only - no extra text before or after.
    """,
    global_instruction=(
        "You are City Pulse Bot, ready to help with city events and environmental information based on location."
    ),
    sub_agents=[event_agent, environment_agent, json_formatter_agent],
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
