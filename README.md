# City Pulse Agents - A2A System

A City Pulse agent system built with Google ADK (Agent Development Kit) following the Agent-to-Agent (A2A) protocol, inspired by the original A2A sample architecture.

## Overview

This system demonstrates A2A architecture with four specialized agents:

- **Concierge Agent** (`concierge_agent`): Main orchestrator that delegates tasks to specialized sub-agents
- **Event Agent** (`event_agent`): Remote A2A agent that provides city events and activities information
- **Environment Agent** (`environment_agent`): Remote A2A agent that provides environmental data and weather information
- **Social News Agent** (`social_news_agent`): Remote A2A agent that provides social media posts, trending topics, and news articles for Bangalore

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌────────────────────┐    ┌─────────────────┐
│ Concierge Agent │───▶│   Event Agent    │    │ Environment Agent  │    │Social News Agent│
│  (Local)        │    │ (localhost:8001) │    │ (localhost:8002)   │    │(localhost:8005) │
│                 │    │                  │    │                    │    │                 │
│                 │───▶│                  │◀───│                    │◀───│                 │
└─────────────────┘    └──────────────────┘    └────────────────────┘    └─────────────────┘
```

## Setup and Usage

### Prerequisites

1. **Install Google ADK**:
   ```bash
   pip install google-adk
   ```

2. **Set up authentication**: Configure your `.env` files in each agent directory with appropriate Google Cloud credentials.

### Running the System

1. **Start the Event Agent server**:
   ```bash
   cd events/event_agent
   adk api_server --port 8001
   ```

2. **Start the Environment Agent server**:
   ```bash
   cd environment/environment_agent  
   adk api_server --port 8002
   ```

3. **Start the Social News Agent server**:
   ```bash
   cd social_news__agent/social_news_agent
   adk api_server --port 8005
   ```

4. **Run the Concierge Agent**:
   ```bash
   cd concierge_agent
   adk web
   ```

> **Note**: You may see experimental feature warnings when starting the agents. These are normal and can be safely ignored.

### Example Interactions

- "What events are happening this weekend?"
- "How's the air quality today?"  
- "What's trending on social media in Bangalore?"
- "Any breaking news today?"
- "Give me the complete city pulse for Bangalore"

## Features

### 1. **Remote A2A Agent Integration**
- Event and Environment agents run as separate services
- Communication via HTTP using A2A protocol
- Agent cards define capabilities and endpoints

### 2. **Agent Orchestration**
- Concierge agent intelligently delegates based on user requests
- Can chain operations and combine results from multiple agents
- Provides unified, user-friendly responses

### 3. **Social Media & News Integration**
- Unified social media and news agent 
- Trending topics and social sentiment analysis
- Breaking news with integrated regular news
- Area-specific news for Bangalore neighborhoods

### 4. **Dummy Data Implementation** 
- No database required - all data is hardcoded for demonstration
- Realistic sample data for events and environmental conditions
- Easy to extend with real data sources

## Project Structure

```
city-pulse-agents/
├── concierge_agent/
│   ├── __init__.py
│   ├── agent.py          # Main orchestrator with RemoteA2aAgent references
│   └── .env
├── events/
│   └── event_agent/
│       ├── __init__.py  
│       ├── agent.py      # Event data provider
│       ├── agent.json    # A2A agent card
│       └── .env
├── environment/
│   └── environment_agent/
│       ├── __init__.py
│       ├── agent.py      # Environment data provider  
│       ├── agent.json    # A2A agent card
│       └── .env
└── social_news/
    └── social_news_agent/
        ├── __init__.py
        ├── agent.py      # Social media & news data provider
        ├── agent.json    # A2A agent card
        └── .env
```

This follows the same pattern as the original ADK A2A Basic sample, adapted for City Pulse use cases.
