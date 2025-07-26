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
import pandas as pd
import numpy as np


async def analyze_city_data() -> str:
    """Analyze city data and provide insights.
    
    Returns:
        A string with analysis results and insights.
    """
    # Sample city data analysis
    city_data = {
        "metrics": [
            {
                "name": "Population Growth",
                "value": 2.5,
                "unit": "%",
                "period": "2025 Q2"
            },
            {
                "name": "Employment Rate",
                "value": 95.8,
                "unit": "%",
                "period": "2025 Q2"
            },
            {
                "name": "Public Transport Usage",
                "value": 450000,
                "unit": "daily riders",
                "period": "July 2025"
            }
        ]
    }
    
    analysis_results = []
    for metric in city_data["metrics"]:
        analysis_results.append(f"{metric['name']}: {metric['value']}{metric['unit']} ({metric['period']})")
    
    return f"City Analysis Results: {', '.join(analysis_results)}"


root_agent = Agent(
    model='gemini-2.0-flash',
    name='analyst_agent',
    description='Analyst agent that provides data analysis and insights about city metrics.',
    instruction="""
      You analyze city data and provide insights about various metrics.
      When asked about city analysis, call the analyze_city_data tool to get current insights.
      Be precise and analytical in your responses, focusing on trends and patterns.
    """,
    tools=[
        analyze_city_data,
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
