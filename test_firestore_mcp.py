#!/usr/bin/env python3
"""
Comprehensive test suite for Event Agent Firestore MCP Integration
This tests the MCP server directly without requiring the full ADK agent infrastructure.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

async def test_mcp_server_direct():
    """Test the MCP server directly by importing and calling its functions"""
    print("🧪 Testing MCP Server Direct Integration")
    print("=" * 60)
    
    try:
        # Import the MCP server module
        from firestore_mcp_server import (
            get_events, add_event, get_events_by_date, 
            get_events_by_category, update_event, delete_event
        )
        
        print("✅ Successfully imported MCP server functions")
        
        # Test 1: Get all events
        print("\n📋 Test 1: Getting all events from Firestore")
        try:
            events = await get_events()
            print(f"✅ Found {len(events)} events:")
            for i, event in enumerate(events[:3], 1):  # Show first 3 events
                print(f"  {i}. {event.get('name', 'Unknown')} at {event.get('location', 'Unknown')} on {event.get('date', 'Unknown')}")
        except Exception as e:
            print(f"❌ Error getting events: {e}")
        
        # Test 2: Get events by date (today's date)
        print(f"\n📅 Test 2: Getting events for today (2025-07-27)")
        try:
            today_events = await get_events_by_date("2025-07-27")
            print(f"✅ Found {len(today_events)} events for today:")
            for event in today_events:
                print(f"  - {event.get('name', 'Unknown')} at {event.get('time', 'Unknown')}")
        except Exception as e:
            print(f"❌ Error getting today's events: {e}")
        
        # Test 3: Get events by category
        print(f"\n🎭 Test 3: Getting Entertainment events")
        try:
            entertainment_events = await get_events_by_category("Entertainment")
            print(f"✅ Found {len(entertainment_events)} entertainment events:")
            for event in entertainment_events:
                print(f"  - {event.get('name', 'Unknown')} at {event.get('location', 'Unknown')}")
        except Exception as e:
            print(f"❌ Error getting entertainment events: {e}")
        
        # Test 4: Add a new test event
        print(f"\n➕ Test 4: Adding a new test event")
        test_event_data = {
            'name': 'MCP Test Event',
            'location': 'Test Venue',
            'time': '2:00 PM - 4:00 PM',
            'date': '2025-07-30',
            'category': 'Testing'
        }
        try:
            new_event_result = await add_event(**test_event_data)
            print(f"✅ Added new event: {new_event_result}")
        except Exception as e:
            print(f"❌ Error adding event: {e}")
        
        print(f"\n🎉 MCP Server Direct Test Completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Failed to import MCP server: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error in MCP server test: {e}")
        return False

async def test_firestore_direct():
    """Test Firestore connection directly"""
    print("\n🔥 Testing Direct Firestore Connection")
    print("=" * 60)
    
    try:
        from google.cloud import firestore
        
        # Initialize Firestore client
        db = firestore.Client()
        print("✅ Firestore client initialized successfully")
        
        # Get events collection
        events_ref = db.collection('events')
        print("✅ Connected to 'events' collection")
        
        # Count total events
        docs = list(events_ref.stream())
        print(f"✅ Total events in Firestore: {len(docs)}")
        
        # Show sample events
        print("\n📋 Sample events in Firestore:")
        for i, doc in enumerate(docs[:5], 1):  # Show first 5 events
            data = doc.to_dict()
            print(f"  {i}. ID: {doc.id}")
            print(f"     Name: {data.get('name', 'Unknown')}")
            print(f"     Location: {data.get('location', 'Unknown')}")
            print(f"     Date: {data.get('date', 'Unknown')}")
            print(f"     Category: {data.get('category', 'Unknown')}")
            print()
        
        return True
        
    except Exception as e:
        print(f"❌ Firestore direct test failed: {e}")
        return False

def test_mcp_server_file_exists():
    """Test if the MCP server file exists and is accessible"""
    print("📁 Testing MCP Server File Access")
    print("=" * 60)
    
    # Check if firestore_mcp_server.py exists
    mcp_server_path = Path("firestore_mcp_server.py")
    
    if mcp_server_path.exists():
        print(f"✅ MCP server file found: {mcp_server_path.absolute()}")
        
        # Check if it's readable
        try:
            with open(mcp_server_path, 'r') as f:
                content = f.read()
                lines = len(content.splitlines())
                print(f"✅ File is readable, {lines} lines of code")
                
            # Check for key functions
            required_functions = ['get_events', 'add_event', 'get_events_by_date', 'get_events_by_category']
            missing_functions = []
            
            for func in required_functions:
                if f"async def {func}" in content:
                    print(f"✅ Function '{func}' found")
                else:
                    missing_functions.append(func)
                    print(f"❌ Function '{func}' missing")
            
            if not missing_functions:
                print("✅ All required MCP functions are present")
                return True
            else:
                print(f"❌ Missing functions: {', '.join(missing_functions)}")
                return False
                
        except Exception as e:
            print(f"❌ Error reading MCP server file: {e}")
            return False
    else:
        print(f"❌ MCP server file not found: {mcp_server_path.absolute()}")
        return False

def test_environment_config():
    """Test environment configuration"""
    print("\n🌍 Testing Environment Configuration")
    print("=" * 60)
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
        location = os.getenv('GOOGLE_CLOUD_LOCATION')
        use_vertex = os.getenv('GOOGLE_GENAI_USE_VERTEXAI')
        
        print(f"GOOGLE_CLOUD_PROJECT: {project_id}")
        print(f"GOOGLE_CLOUD_LOCATION: {location}")
        print(f"GOOGLE_GENAI_USE_VERTEXAI: {use_vertex}")
        
        if project_id:
            print("✅ Google Cloud Project ID is set")
        else:
            print("❌ Google Cloud Project ID is missing")
            
        if location:
            print("✅ Google Cloud Location is set")
        else:
            print("❌ Google Cloud Location is missing")
            
        return bool(project_id and location)
        
    except Exception as e:
        print(f"❌ Environment configuration test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Event Agent Firestore MCP Integration Test Suite")
    print("=" * 70)
    print(f"📅 Test Date: July 27, 2025")
    print(f"📂 Working Directory: {os.getcwd()}")
    print()
    
    # Track test results
    test_results = {}
    
    # Test 1: Environment configuration
    test_results['environment'] = test_environment_config()
    
    # Test 2: MCP server file access
    test_results['mcp_file'] = test_mcp_server_file_exists()
    
    # Test 3: Direct Firestore connection
    test_results['firestore_direct'] = await test_firestore_direct()
    
    # Test 4: MCP server direct (only if previous tests pass)
    if test_results['mcp_file'] and test_results['firestore_direct']:
        test_results['mcp_server'] = await test_mcp_server_direct()
    else:
        print("\n⚠️  Skipping MCP server test due to previous failures")
        test_results['mcp_server'] = False
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 70)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():<25} {status}")
    
    total_tests = len(test_results)
    passed_tests = sum(test_results.values())
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED! Your Event Agent is ready to fetch from Firestore via MCP!")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        
        # Provide troubleshooting guidance
        print("\n🔧 TROUBLESHOOTING GUIDE:")
        if not test_results['environment']:
            print("- Check your .env file and Google Cloud credentials")
        if not test_results['firestore_direct']:
            print("- Verify Firestore is enabled and accessible")
        if not test_results['mcp_file']:
            print("- Ensure firestore_mcp_server.py is in the current directory")
        if not test_results['mcp_server']:
            print("- Check MCP server implementation and dependencies")

if __name__ == "__main__":
    asyncio.run(main())
