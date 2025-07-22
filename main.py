#!/usr/bin/env python3
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

"""
City Pulse Agents Demo

This script demonstrates the City Pulse agent orchestration system.
The concierge_agent orchestrates requests to event_agent and environment_agent
using the Google ADK framework.
"""

from agents.concierge_agent import concierge_agent


def main():
    """Demonstrate the City Pulse agent system."""
    
    print("=== City Pulse Agent System Demo ===\n")
    
    # Test event information request
    print("🎭 Testing Event Information Request:")
    print("-" * 50)
    event_response = concierge_agent.send_message("What events are happening this weekend?")
    print(f"Response: {event_response.text}\n")
    
    # Test environment information request
    print("🌤️ Testing Environment Information Request:")
    print("-" * 50)
    env_response = concierge_agent.send_message("How's the air quality and weather today?")
    print(f"Response: {env_response.text}\n")
    
    # Test combined information request
    print("🏙️ Testing Combined Information Request:")
    print("-" * 50)
    combined_response = concierge_agent.send_message("Give me a complete city update - events and environment")
    print(f"Response: {combined_response.text}\n")
    
    print("=== Demo Complete ===")


if __name__ == "__main__":
    main()
