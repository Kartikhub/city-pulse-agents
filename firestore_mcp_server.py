# firestore_mcp_server.py
import asyncio
import json
import os
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# MCP Server Imports
from mcp import types as mcp_types
from mcp.server.lowlevel import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio

# Firestore Imports
from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

# Load environment variables
load_dotenv()

# Initialize Firestore client
print("Initializing Firestore client...")
try:
    # Initialize Firestore client with project from environment
    db = firestore.Client()
    print("Firestore client initialized successfully.")
except Exception as e:
    print(f"Error initializing Firestore client: {e}")
    db = None

# Create MCP Server instance
print("Creating MCP Server instance...")
app = Server("firestore-mcp-server")

@app.list_tools()
async def list_firestore_tools() -> List[mcp_types.Tool]:
    """MCP handler to list available Firestore tools."""
    print("MCP Server: Received list_tools request.")
    
    tools = [
        mcp_types.Tool(
            name="get_events",
            description="Retrieve all events from Firestore",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        ),
        mcp_types.Tool(
            name="add_event",
            description="Add a new event to Firestore",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Event name"},
                    "location": {"type": "string", "description": "Event location"},
                    "time": {"type": "string", "description": "Event time (e.g., '7:00 PM - 11:00 PM')"},
                    "date": {"type": "string", "description": "Event date (YYYY-MM-DD format)"},
                    "category": {"type": "string", "description": "Event category"}
                },
                "required": ["name", "location", "time", "date", "category"]
            }
        ),
        mcp_types.Tool(
            name="get_events_by_date",
            description="Get events for a specific date",
            inputSchema={
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "Date in YYYY-MM-DD format"}
                },
                "required": ["date"]
            }
        ),
        mcp_types.Tool(
            name="get_events_by_category",
            description="Get events by category",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Event category"}
                },
                "required": ["category"]
            }
        ),
        mcp_types.Tool(
            name="update_event",
            description="Update an existing event in Firestore",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "string", "description": "Event document ID"},
                    "name": {"type": "string", "description": "Event name"},
                    "location": {"type": "string", "description": "Event location"},
                    "time": {"type": "string", "description": "Event time"},
                    "date": {"type": "string", "description": "Event date"},
                    "category": {"type": "string", "description": "Event category"}
                },
                "required": ["event_id"]
            }
        ),
        mcp_types.Tool(
            name="delete_event",
            description="Delete an event from Firestore",
            inputSchema={
                "type": "object",
                "properties": {
                    "event_id": {"type": "string", "description": "Event document ID"}
                },
                "required": ["event_id"]
            }
        )
    ]
    
    print(f"MCP Server: Advertising {len(tools)} Firestore tools")
    return tools

@app.call_tool()
async def call_firestore_tool(name: str, arguments: Dict[str, Any]) -> List[mcp_types.Content]:
    """MCP handler to execute Firestore tool calls."""
    print(f"MCP Server: Received call_tool request for '{name}' with args: {arguments}")
    
    if not db:
        error_response = {"error": "Firestore client not initialized"}
        return [mcp_types.TextContent(type="text", text=json.dumps(error_response))]
    
    try:
        if name == "get_events":
            return await handle_get_events()
            
        elif name == "add_event":
            return await handle_add_event(arguments)
            
        elif name == "get_events_by_date":
            return await handle_get_events_by_date(arguments.get("date"))
            
        elif name == "get_events_by_category":
            return await handle_get_events_by_category(arguments.get("category"))
            
        elif name == "update_event":
            return await handle_update_event(arguments)
            
        elif name == "delete_event":
            return await handle_delete_event(arguments.get("event_id"))
            
        else:
            error_response = {"error": f"Tool '{name}' not implemented"}
            return [mcp_types.TextContent(type="text", text=json.dumps(error_response))]
            
    except Exception as e:
        print(f"MCP Server: Error executing tool '{name}': {e}")
        error_response = {"error": f"Failed to execute tool '{name}': {str(e)}"}
        return [mcp_types.TextContent(type="text", text=json.dumps(error_response))]

async def handle_get_events() -> List[mcp_types.Content]:
    """Get all events from Firestore."""
    events_ref = db.collection('events')
    docs = events_ref.stream()
    
    events = []
    for doc in docs:
        event_data = doc.to_dict()
        event_data['id'] = doc.id
        events.append(event_data)
    
    result = {"events": events, "count": len(events)}
    return [mcp_types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_add_event(event_data: Dict[str, Any]) -> List[mcp_types.Content]:
    """Add a new event to Firestore."""
    events_ref = db.collection('events')
    doc_ref = events_ref.add(event_data)
    
    result = {
        "success": True,
        "message": "Event added successfully",
        "event_id": doc_ref[1].id,
        "event_data": event_data
    }
    return [mcp_types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_get_events_by_date(date: str) -> List[mcp_types.Content]:
    """Get events for a specific date."""
    events_ref = db.collection('events')
    query = events_ref.where(filter=FieldFilter("date", "==", date))
    docs = query.stream()
    
    events = []
    for doc in docs:
        event_data = doc.to_dict()
        event_data['id'] = doc.id
        events.append(event_data)
    
    result = {"events": events, "date": date, "count": len(events)}
    return [mcp_types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_get_events_by_category(category: str) -> List[mcp_types.Content]:
    """Get events by category."""
    events_ref = db.collection('events')
    query = events_ref.where(filter=FieldFilter("category", "==", category))
    docs = query.stream()
    
    events = []
    for doc in docs:
        event_data = doc.to_dict()
        event_data['id'] = doc.id
        events.append(event_data)
    
    result = {"events": events, "category": category, "count": len(events)}
    return [mcp_types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_update_event(update_data: Dict[str, Any]) -> List[mcp_types.Content]:
    """Update an existing event."""
    event_id = update_data.pop("event_id")
    events_ref = db.collection('events')
    doc_ref = events_ref.document(event_id)
    
    # Remove None values
    update_data = {k: v for k, v in update_data.items() if v is not None}
    
    doc_ref.update(update_data)
    
    result = {
        "success": True,
        "message": "Event updated successfully",
        "event_id": event_id,
        "updated_fields": update_data
    }
    return [mcp_types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def handle_delete_event(event_id: str) -> List[mcp_types.Content]:
    """Delete an event from Firestore."""
    events_ref = db.collection('events')
    doc_ref = events_ref.document(event_id)
    doc_ref.delete()
    
    result = {
        "success": True,
        "message": "Event deleted successfully",
        "event_id": event_id
    }
    return [mcp_types.TextContent(type="text", text=json.dumps(result, indent=2))]

async def run_mcp_stdio_server():
    """Run the MCP server over stdio."""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        print("MCP Stdio Server: Starting handshake with client...")
        await app.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=app.name,
                server_version="1.0.0",
                capabilities=app.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )
        print("MCP Stdio Server: Run loop finished or client disconnected.")

if __name__ == "__main__":
    print("Launching Firestore MCP Server...")
    try:
        asyncio.run(run_mcp_stdio_server())
    except KeyboardInterrupt:
        print("\nFirestore MCP Server stopped by user.")
    except Exception as e:
        print(f"Firestore MCP Server encountered an error: {e}")
    finally:
        print("Firestore MCP Server process exiting.")
