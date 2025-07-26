# setup_firestore_events.py
"""
Script to initialize Firestore with sample event data.
Run this script once to populate your Firestore database with initial events.
"""

import os
from google.cloud import firestore
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def setup_firestore_events():
    """Initialize Firestore with sample events."""
    try:
        # Initialize Firestore client
        db = firestore.Client()
        print("Connected to Firestore successfully.")
        
        # Sample events data
        sample_events = [
            {
                "name": "Summer Music Festival",
                "location": "Central Park",
                "time": "7:00 PM - 11:00 PM",
                "date": "2025-07-25",
                "category": "Entertainment"
            },
            {
                "name": "Farmers Market",
                "location": "Downtown Square", 
                "time": "8:00 AM - 2:00 PM",
                "date": "2025-07-26",
                "category": "Shopping"
            },
            {
                "name": "Tech Conference",
                "location": "Convention Center",
                "time": "9:00 AM - 5:00 PM", 
                "date": "2025-07-27",
                "category": "Business"
            },
            {
                "name": "Food Truck Rally",
                "location": "City Plaza",
                "time": "12:00 PM - 8:00 PM",
                "date": "2025-07-28",
                "category": "Food"
            },
            {
                "name": "Art Gallery Opening",
                "location": "Modern Art Museum",
                "time": "6:00 PM - 9:00 PM",
                "date": "2025-07-29",
                "category": "Culture"
            }
        ]
        
        # Add events to Firestore
        events_ref = db.collection('events')
        
        print("Adding sample events to Firestore...")
        for event in sample_events:
            doc_ref = events_ref.add(event)
            print(f"✅ Added event: {event['name']} (ID: {doc_ref[1].id})")
        
        print(f"\n🎉 Successfully added {len(sample_events)} events to Firestore!")
        print("\nYour event agent can now use the following Firestore operations:")
        print("- Get all events")
        print("- Add new events")
        print("- Search by date or category")
        print("- Update existing events")
        print("- Delete events")
        
    except Exception as e:
        print(f"❌ Error setting up Firestore events: {e}")
        print("\nMake sure you have:")
        print("1. Set up Google Cloud credentials")
        print("2. Enabled Firestore in your project")
        print("3. Set GOOGLE_CLOUD_PROJECT in your .env file")

if __name__ == "__main__":
    setup_firestore_events()
