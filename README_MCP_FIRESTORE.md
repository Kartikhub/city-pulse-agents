# Firestore MCP Integration for Event Agent

This integration allows your Event Agent to communicate with Google Firestore using the Model Context Protocol (MCP).

## 🚀 Setup Instructions

### 1. Prerequisites

Make sure you have the required packages installed:
```bash
pip install mcp google-cloud-firestore
```

### 2. Google Cloud Setup

1. **Create a Google Cloud Project** (if you don't have one)
2. **Enable Firestore API**:
   - Go to Google Cloud Console
   - Navigate to APIs & Services > Library
   - Search for "Firestore" and enable it
3. **Set up authentication**:
   - Create a service account key
   - Download the JSON key file
   - Set the environment variable: `export GOOGLE_APPLICATION_CREDENTIALS="path/to/your/key.json"`

### 3. Environment Configuration

Update your `.env` files in the agent directories:
```env
GOOGLE_GENAI_USE_VERTEXAI=TRUE
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
```

### 4. Initialize Firestore with Sample Data

Run the setup script to populate Firestore with sample events:
```bash
python setup_firestore_events.py
```

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────────┐    ┌──────────────────┐
│   Event Agent   │───▶│ Firestore MCP Server │───▶│   Google Cloud   │
│   (ADK Agent)   │    │   (Python Process)  │    │    Firestore     │
│                 │    │                     │    │    Database      │
└─────────────────┘    └─────────────────────┘    └──────────────────┘
```

The Event Agent uses MCPToolset to communicate with a custom MCP server (`firestore_mcp_server.py`) that handles all Firestore operations.

## 🛠️ Available Tools

The Firestore MCP server provides these tools to the Event Agent:

### 1. **get_events**
- **Description**: Retrieve all events from Firestore
- **Parameters**: None
- **Usage**: "Show me all events"

### 2. **add_event**
- **Description**: Add a new event to Firestore
- **Parameters**: 
  - `name` (string): Event name
  - `location` (string): Event location
  - `time` (string): Event time range
  - `date` (string): Event date (YYYY-MM-DD)
  - `category` (string): Event category
- **Usage**: "Add a new concert at Madison Square Garden on 2025-08-01"

### 3. **get_events_by_date**
- **Description**: Get events for a specific date
- **Parameters**: 
  - `date` (string): Date in YYYY-MM-DD format
- **Usage**: "What events are happening on July 27th?"

### 4. **get_events_by_category**
- **Description**: Get events by category
- **Parameters**: 
  - `category` (string): Event category
- **Usage**: "Show me all entertainment events"

### 5. **update_event**
- **Description**: Update an existing event
- **Parameters**: 
  - `event_id` (string): Firestore document ID
  - Other fields (optional): name, location, time, date, category
- **Usage**: "Update the music festival location to Central Park"

### 6. **delete_event**
- **Description**: Delete an event from Firestore
- **Parameters**: 
  - `event_id` (string): Firestore document ID
- **Usage**: "Cancel the tech conference"

## 🔄 Running the System

### 1. Start the Event Agent with MCP
```bash
cd events/event_agent
adk api_server --port 8001
```

The Event Agent will automatically:
- Start the Firestore MCP server as a subprocess
- Connect to it via stdio (standard input/output)
- Make Firestore tools available to the agent

### 2. Test the Integration

You can interact with the Event Agent through the concierge agent:
```bash
cd concierge_agent
adk web
```

Try these example prompts:
- "What events are happening this weekend?"
- "Add a new yoga class at the community center tomorrow at 10 AM"
- "Show me all entertainment events"
- "Update the farmers market time to 9 AM - 3 PM"

## 🛡️ Fallback Mechanism

The Event Agent includes a fallback mechanism:
- If Firestore is unavailable, it uses `get_city_events_fallback()`
- This ensures the agent always has event data to provide
- Users get a seamless experience even during connectivity issues

## 📁 File Structure

```
city-pulse-agents/
├── firestore_mcp_server.py          # MCP server for Firestore operations
├── setup_firestore_events.py        # Script to initialize sample data
├── events/
│   └── event_agent/
│       ├── agent.py                  # Updated with MCP integration
│       ├── agent.json                # Agent configuration
│       └── .env                      # Environment variables
└── README_MCP_FIRESTORE.md          # This file
```

## 🔧 Troubleshooting

### Common Issues:

1. **"Firestore client not initialized"**
   - Check your Google Cloud credentials
   - Verify GOOGLE_CLOUD_PROJECT is set correctly
   - Ensure Firestore API is enabled

2. **"Permission denied"**
   - Verify your service account has Firestore permissions
   - Check that the credentials file path is correct

3. **"Tool not found" errors**
   - Ensure the MCP server is running
   - Check the file path to `firestore_mcp_server.py`
   - Verify MCP and google-cloud-firestore packages are installed

### Debug Mode:

Run the MCP server separately to see logs:
```bash
python firestore_mcp_server.py
```

## 🌟 Benefits of MCP Integration

1. **Separation of Concerns**: Database logic is separate from agent logic
2. **Reusability**: The MCP server can be used by other MCP clients
3. **Scalability**: Easy to add more database operations
4. **Standardization**: Uses the open MCP protocol
5. **Flexibility**: Can be deployed separately or as a subprocess

## 📚 Next Steps

- Add authentication and authorization to the MCP server
- Implement event search with more complex queries
- Add event validation and business logic
- Create additional MCP servers for other data sources
- Deploy the MCP server to Cloud Run for production use

## 🤝 Contributing

To add new Firestore operations:
1. Add the tool definition in `list_firestore_tools()`
2. Implement the handler in `call_firestore_tool()`
3. Create the corresponding async function
4. Update this documentation

For more information about MCP, visit: https://modelcontextprotocol.io/
