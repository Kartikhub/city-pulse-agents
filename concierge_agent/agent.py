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
            "parts": [{"text": "What's trending on social media in Bangalore?"}],
        },
        "output": [
            {"role": "model", "parts": [{"text": "Trending in Bangalore: #BangaloreTraffic, #PowerCut, #AirQuality, #TechCity, #BLRMusic. Recent posts show mixed sentiment about traffic issues but positive excitement about the music scene."}]}
        ],
    },
    {
        "input": {
            "role": "user",
            "parts": [{"text": "Any breaking news today?"}],
        },
        "output": [
            {"role": "model", "parts": [{"text": "🚨 Breaking News: BBMP Announces New Digital Governance Platform - Citizens can now access all municipal services through a single digital platform. Published 2 hours ago."}]}
        ],
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
            "parts": [{"text": "Give me the complete city pulse for Bangalore"}],
        },
        "output": [
            {
                "role": "model",
                "parts": [{"text": "🌆 **BANGALORE CITY PULSE - July 26, 2025**\n\n📅 **EVENTS:** Summer Music Festival at Central Park tonight (7:00 PM - 11:00 PM)\n\n🌍 **ENVIRONMENT:** Air quality is Good (Index: 42) - perfect for outdoor activities!\n\n📱 **SOCIAL BUZZ:** Trending: #TechCity, #BLRMusic, #PowerCut. People are excited about tech meetups but frustrated with infrastructure issues.\n\n📰 **BREAKING NEWS:** 🔴 BBMP launches new digital governance platform at 8:00 PM today - all municipal services now available online!\n\nYour city is vibrant with events, clean air, active social discussions, and progressive governance updates!"}],
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

social_news_agent = RemoteA2aAgent(
    name="social_news_agent",
    description="Agent that handles social media posts, trending topics, news articles with integrated breaking news, and area-specific updates for Bangalore.",
    agent_card=(
        f"http://localhost:8005/a2a/social_news_agent{AGENT_CARD_WELL_KNOWN_PATH}"
    ),
)

root_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="concierge_agent",
    instruction="""
      You are the City Pulse Concierge Agent that provides comprehensive city information for Bangalore.
      You have access to event_agent, environment_agent, and social_news_agent.
      
      CAPABILITIES:
      - event_agent: Get events and activities happening in the city
      - environment_agent: Get environmental data, weather, and air quality information
      - social_news_agent: Get social media posts, trending topics, news articles with integrated breaking news, and area-specific updates (excludes traffic/weather/environment)
      
      CRITICAL: When users ask about multiple types of information:
      1. Call relevant agents to get specific data
      2. Combine and present results in a cohesive response
      3. Always provide comprehensive city pulse information when requested
      
      For social media trending topics, news articles, or breaking news, use social_news_agent.
      Never say you cannot provide information - you have access to all city data through specialized agents.
    """,
    global_instruction=(
        "You are City Pulse Bot, ready to help with comprehensive city information including events, environment, social media, and news for Bangalore."
    ),
    sub_agents=[event_agent, environment_agent, social_news_agent],
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
