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


async def get_user_reports(incident_type: str = "all", location: str = "all") -> str:
    """Get user reports and incidents from the city.
    
    Args:
        incident_type: The type of incident to filter by. Options: "Flooding", "Infrastructure", 
                      "Emergency", "Maintenance", or "all" for all types.
        location: The location to filter reports by. Options: "BIEC", "Central Park", 
                 "Downtown Square", "Convention Center", or "all" for all locations.
    
    Returns:
        A string with current user reports and incidents information.
    """
    reports_data = {
        "reports": [
            {
                "documentId": "lg0g7PXXVlhd63raAa2P",
                "description": "Flood inside hall 1",
                "incidentType": "Flooding",
                "location": "BIEC",
                "mediaDescription": [
                    "Scene Description: A concrete electric pole has collapsed and is lying across a roadway or street. The electrical wires connected to the pole are either sagging or tangled, adding to the chaotic scene. Broken pieces of the pole and other debris are scattered around, indicating a forceful impact or structural failure. There may be vehicles visible in the background or nearby, suggesting this occurred in an urban or semi-urban area. The sky appears overcast, contributing to a gloomy or post-disaster atmosphere. The image captures a sense of disruption, possibly due to a storm, accident, or infrastructural failure."
                ],
                "timestamp": "July 26, 2025 at 12:17:49 PM UTC+5:30",
                "userId": "J0CtwbNDO7VJ5s1u1jH3cNhlxIF3"
            },
            {
                "documentId": "mk1h8QYYWmie74sbBb3Q",
                "description": "Traffic light malfunction at main intersection",
                "incidentType": "Infrastructure",
                "location": "Downtown Square",
                "mediaDescription": [
                    "Scene Description: Traffic light displaying all colors simultaneously, causing confusion among drivers. Several vehicles are stopped at the intersection waiting for clear signals. No traffic police visible at the scene. The malfunction appears to be affecting the entire intersection's traffic flow."
                ],
                "timestamp": "July 26, 2025 at 11:45:30 AM UTC+5:30",
                "userId": "K1DuxcOEP8WK6t2v2iI4dOimyJG4"
            },
            {
                "documentId": "np2i9RZZXnje85tcCc4R",
                "description": "Water pipe burst near convention entrance",
                "incidentType": "Emergency",
                "location": "Convention Center",
                "mediaDescription": [
                    "Scene Description: Large water pipe has burst, creating a significant water leak near the main entrance. Water is flowing across the walkway, making it difficult for pedestrians to access the building. Maintenance crews have been notified but have not yet arrived on scene."
                ],
                "timestamp": "July 26, 2025 at 10:30:15 AM UTC+5:30",
                "userId": "L2EwyeRF9XL7u3w3jJ5eOpmzKH5"
            },
            {
                "documentId": "oq3j0SAAYoke96udDd5S", 
                "description": "Broken bench in park area",
                "incidentType": "Maintenance",
                "location": "Central Park",
                "mediaDescription": [
                    "Scene Description: Wooden park bench with broken slats and damaged support structure. The bench appears unsafe for public use. Located near the main walking path, posing a potential safety hazard for park visitors."
                ],
                "timestamp": "July 26, 2025 at 9:15:45 AM UTC+5:30",
                "userId": "M3FxzfSG0YM8v4x4kK6fPqnALI6"
            }
        ]
    }
    
    # Filter reports by incident type and location
    filtered_reports = []
    for report in reports_data["reports"]:
        # Check if report matches incident type filter
        type_match = (incident_type == "all" or report["incidentType"] == incident_type)
        # Check if report matches location filter
        location_match = (location == "all" or report["location"] == location)
        
        if type_match and location_match:
            filtered_reports.append(report)
    
    if not filtered_reports:
        return f"No user reports found for incident type '{incident_type}' at location '{location}'"
    
    # Format the filtered reports
    report_summaries = []
    for report in filtered_reports:
        media_desc = report["mediaDescription"][0][:100] + "..." if report["mediaDescription"] and len(report["mediaDescription"][0]) > 100 else report["mediaDescription"][0] if report["mediaDescription"] else "No media description"
        
        report_summaries.append(
            f"Report ID: {report['documentId']}, "
            f"Type: {report['incidentType']}, "
            f"Location: {report['location']}, "
            f"Description: {report['description']}, "
            f"Time: {report['timestamp']}, "
            f"Media: {media_desc}"
        )
    
    return f"User Reports ({len(filtered_reports)} found): {' | '.join(report_summaries)}"


async def get_report_by_id(document_id: str) -> str:
    """Get detailed information about a specific user report by document ID.
    
    Args:
        document_id: The document ID of the report to retrieve.
    
    Returns:
        A string with detailed report information or error message if not found.
    """
    reports_data = {
        "reports": [
            {
                "documentId": "lg0g7PXXVlhd63raAa2P",
                "description": "Flood inside hall 1",
                "incidentType": "Flooding",
                "location": "BIEC",
                "mediaDescription": [
                    "Scene Description: A concrete electric pole has collapsed and is lying across a roadway or street. The electrical wires connected to the pole are either sagging or tangled, adding to the chaotic scene. Broken pieces of the pole and other debris are scattered around, indicating a forceful impact or structural failure. There may be vehicles visible in the background or nearby, suggesting this occurred in an urban or semi-urban area. The sky appears overcast, contributing to a gloomy or post-disaster atmosphere. The image captures a sense of disruption, possibly due to a storm, accident, or infrastructural failure."
                ],
                "timestamp": "July 26, 2025 at 12:17:49 PM UTC+5:30",
                "userId": "J0CtwbNDO7VJ5s1u1jH3cNhlxIF3"
            },
            {
                "documentId": "mk1h8QYYWmie74sbBb3Q",
                "description": "Traffic light malfunction at main intersection",
                "incidentType": "Infrastructure",
                "location": "Downtown Square",
                "mediaDescription": [
                    "Scene Description: Traffic light displaying all colors simultaneously, causing confusion among drivers. Several vehicles are stopped at the intersection waiting for clear signals. No traffic police visible at the scene. The malfunction appears to be affecting the entire intersection's traffic flow."
                ],
                "timestamp": "July 26, 2025 at 11:45:30 AM UTC+5:30",
                "userId": "K1DuxcOEP8WK6t2v2iI4dOimyJG4"
            },
            {
                "documentId": "np2i9RZZXnje85tcCc4R",
                "description": "Water pipe burst near convention entrance",
                "incidentType": "Emergency",
                "location": "Convention Center",
                "mediaDescription": [
                    "Scene Description: Large water pipe has burst, creating a significant water leak near the main entrance. Water is flowing across the walkway, making it difficult for pedestrians to access the building. Maintenance crews have been notified but have not yet arrived on scene."
                ],
                "timestamp": "July 26, 2025 at 10:30:15 AM UTC+5:30",
                "userId": "L2EwyeRF9XL7u3w3jJ5eOpmzKH5"
            },
            {
                "documentId": "oq3j0SAAYoke96udDd5S", 
                "description": "Broken bench in park area",
                "incidentType": "Maintenance",
                "location": "Central Park",
                "mediaDescription": [
                    "Scene Description: Wooden park bench with broken slats and damaged support structure. The bench appears unsafe for public use. Located near the main walking path, posing a potential safety hazard for park visitors."
                ],
                "timestamp": "July 26, 2025 at 9:15:45 AM UTC+5:30",
                "userId": "M3FxzfSG0YM8v4x4kK6fPqnALI6"
            }
        ]
    }
    
    # Find the report by document ID
    for report in reports_data["reports"]:
        if report["documentId"] == document_id:
            media_descriptions = "; ".join(report["mediaDescription"]) if report["mediaDescription"] else "No media description available"
            return (f"Report Details - ID: {report['documentId']}, "
                   f"Incident Type: {report['incidentType']}, "
                   f"Location: {report['location']}, "
                   f"Description: {report['description']}, "
                   f"Timestamp: {report['timestamp']}, "
                   f"User ID: {report['userId']}, "
                   f"Media Description: {media_descriptions}")
    
    return f"Report with document ID '{document_id}' not found."


root_agent = Agent(
    model='gemini-2.0-flash',
    name='user_report_agent',
    description='User report agent that provides information about citizen reports, incidents, and emergency situations in the city.',
    instruction="""
      You provide information about user reports, incidents, and emergency situations reported by citizens.
      When asked about reports or incidents, call the get_user_reports tool to get current report information.
      You can filter reports by incident type (Flooding, Infrastructure, Emergency, Maintenance) and location (BIEC, Central Park, Downtown Square, Convention Center).
      When asked about a specific report, use the get_report_by_id tool with the document ID.
      Be helpful and provide clear details about incident types, locations, timestamps, and descriptions.
      Prioritize emergency and safety-related incidents in your responses.
    """,
    tools=[
        get_user_reports,
        get_report_by_id,
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
