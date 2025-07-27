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

import os
import vertexai
from vertexai import rag
from vertexai.generative_models import GenerativeModel, Tool
from google.adk import Agent
from google.genai import types
from google.adk.tools import FunctionTool
from typing import Dict, List, Optional, Any

# Import configuration
from .config import (
    PROJECT_ID,
    LOCATION,
    EMBEDDING_MODEL,
    RAG_CORPUS_NAME,
    DEFAULT_TOP_K,
    DEFAULT_CHUNK_SIZE,
    DEFAULT_CHUNK_OVERLAP,
    DEFAULT_VECTOR_DISTANCE_THRESHOLD,
    MAX_EMBEDDING_REQUESTS_PER_MIN,
    GENERATIVE_MODEL
)

# Initialize Vertex AI
vertexai.init(project=PROJECT_ID, location=LOCATION)

# Global variable to store the RAG corpus for events
events_rag_corpus = None

# Auto-initialize with the demo corpus we created earlier
def auto_initialize_corpus():
    """Auto-initialize with existing corpus"""
    global events_rag_corpus
    demo_corpus_id = "projects/1076746085148/locations/us-central1/ragCorpora/4611686018427387904"
    events_rag_corpus = type('RagCorpus', (), {'name': demo_corpus_id})()
    return demo_corpus_id

# Auto-initialize on module load
auto_initialize_corpus()

def initialize_existing_corpus(corpus_id: Optional[str] = None) -> str:
    """
    Initialize with an existing RAG corpus.
    
    Args:
        corpus_id: Optional specific corpus ID to use
        
    Returns:
        Status message about initialization
    """
    global events_rag_corpus
    
    try:
        if corpus_id:
            # Use specific corpus ID
            events_rag_corpus = type('RagCorpus', (), {'name': corpus_id})()
            return f"Initialized with existing corpus: {corpus_id}"
        else:
            # For demo purposes, use the corpus we created earlier
            demo_corpus_id = "projects/1076746085148/locations/us-central1/ragCorpora/4611686018427387904"
            events_rag_corpus = type('RagCorpus', (), {'name': demo_corpus_id})()
            return f"Initialized with demo corpus: {demo_corpus_id}"
            
    except Exception as e:
        return f"Error initializing corpus: {str(e)}"

def create_event_rag_corpus(corpus_name: str = RAG_CORPUS_NAME) -> str:
    """
    Create a RAG corpus for city events if it doesn't exist.
    
    Args:
        corpus_name: Name for the RAG corpus
        
    Returns:
        Status message about corpus creation
    """
    global events_rag_corpus
    
    try:
        # Configure embedding model
        embedding_model_config = rag.RagEmbeddingModelConfig(
            vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
                publisher_model=EMBEDDING_MODEL
            )
        )
        
        # Create RagCorpus
        events_rag_corpus = rag.create_corpus(
            display_name=corpus_name,
            backend_config=rag.RagVectorDbConfig(
                rag_embedding_model_config=embedding_model_config
            ),
        )
        
        return f"Successfully created RAG corpus: {events_rag_corpus.name}"
    except Exception as e:
        return f"Error creating RAG corpus: {str(e)}"

def import_event_documents(file_paths: List[str]) -> str:
    """
    Import event documents into the RAG corpus.
    
    Args:
        file_paths: List of GCS paths or Google Drive links to event documents
        
    Returns:
        Status message about import operation
    """
    global events_rag_corpus
    
    if not events_rag_corpus:
        return "Error: RAG corpus not created. Please create corpus first."
    
    try:
        # Import Files to the RagCorpus
        rag.import_files(
            events_rag_corpus.name,
            file_paths,
            transformation_config=rag.TransformationConfig(
                chunking_config=rag.ChunkingConfig(
                    chunk_size=DEFAULT_CHUNK_SIZE,
                    chunk_overlap=DEFAULT_CHUNK_OVERLAP,
                ),
            ),
            max_embedding_requests_per_min=MAX_EMBEDDING_REQUESTS_PER_MIN,
        )
        
        return f"Successfully imported {len(file_paths)} documents into RAG corpus"
    except Exception as e:
        return f"Error importing documents: {str(e)}"

def search_events_rag(query: str, top_k: int = DEFAULT_TOP_K) -> str:
    """
    Search for events using RAG retrieval.
    
    Args:
        query: Search query for events
        top_k: Number of top results to return
        
    Returns:
        Search results from RAG corpus
    """
    global events_rag_corpus
    
    if not events_rag_corpus:
        return get_city_events_fallback()
    
    try:
        # Configure retrieval
        rag_retrieval_config = rag.RagRetrievalConfig(
            top_k=top_k,
            filter=rag.Filter(vector_distance_threshold=DEFAULT_VECTOR_DISTANCE_THRESHOLD),
        )
        
        # Perform retrieval query
        response = rag.retrieval_query(
            rag_resources=[
                rag.RagResource(
                    rag_corpus=events_rag_corpus.name,
                )
            ],
            text=query,
            rag_retrieval_config=rag_retrieval_config,
        )
        
        # Format response
        if response and response.contexts:
            results = []
            contexts = response.contexts.contexts if hasattr(response.contexts, 'contexts') else response.contexts
            for context in contexts:
                results.append(f"Event: {context.text}")
            return f"Found {len(results)} relevant events:\n" + "\n".join(results)
        else:
            return "No relevant events found in RAG corpus."
            
    except Exception as e:
        return f"Error searching events: {str(e)}. Using fallback data: {get_city_events_fallback()}"

def generate_event_response_with_rag(question: str) -> str:
    """
    Generate a response about events using RAG-enhanced generation.
    
    Args:
        question: Question about events
        
    Returns:
        AI-generated response enhanced with RAG
    """
    global events_rag_corpus
    
    if not events_rag_corpus:
        return f"RAG corpus not available. {get_city_events_fallback()}"
    
    try:
        # Configure retrieval
        rag_retrieval_config = rag.RagRetrievalConfig(
            top_k=DEFAULT_TOP_K,
            filter=rag.Filter(vector_distance_threshold=DEFAULT_VECTOR_DISTANCE_THRESHOLD),
        )
        
        # Create a RAG retrieval tool
        rag_retrieval_tool = Tool.from_retrieval(
            retrieval=rag.Retrieval(
                source=rag.VertexRagStore(
                    rag_resources=[
                        rag.RagResource(
                            rag_corpus=events_rag_corpus.name,
                        )
                    ],
                    rag_retrieval_config=rag_retrieval_config,
                ),
            )
        )
        
        # Create a Gemini model instance with RAG
        rag_model = GenerativeModel(
            model_name=GENERATIVE_MODEL, 
            tools=[rag_retrieval_tool]
        )
        
        # Generate response
        response = rag_model.generate_content(question)
        return response.text
        
    except Exception as e:
        return f"Error generating RAG response: {str(e)}. Using fallback: {get_city_events_fallback()}"


# RAG Function Tools
initialize_corpus_tool = FunctionTool(initialize_existing_corpus)

create_corpus_tool = FunctionTool(create_event_rag_corpus)

import_documents_tool = FunctionTool(import_event_documents)

search_events_tool = FunctionTool(search_events_rag)

generate_response_tool = FunctionTool(generate_event_response_with_rag)


def get_city_events_fallback() -> str:
    """Fallback function to get dummy city events if RAG is unavailable.
    
    Returns:
        A string with fallback city events information.
    """
    events_data = {
        "events": [
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
            }
        ]
    }
    
    event_list = []
    for event in events_data["events"]:
        event_list.append(f"{event['name']} at {event['location']} on {event['date']} from {event['time']} ({event['category']})")
    
    return f"Current city events (fallback data): {', '.join(event_list)}"


root_agent = Agent(
    model='gemini-2.0-flash',
    name='event_agent',
    description='Event agent that provides information about city events and activities using Vertex AI RAG Engine.',
    instruction="""
      You are an Event Agent that manages city events and activities using Vertex AI RAG Engine (Vector Database).
      
      IMPORTANT: This agent uses RAG (Retrieval-Augmented Generation) with vector search, NOT MCP or Firestore.
      
      CAPABILITIES:
      - Initialize with existing RAG corpus (auto-initialized on startup)
      - Create new RAG corpus for event documents
      - Import event documents from GCS or Google Drive into RAG corpus
      - Search events using vector similarity in RAG corpus
      - Generate AI-enhanced responses about events using RAG retrieval
      
      TOOLS AVAILABLE:
      - initialize_existing_corpus: Initialize with an existing RAG corpus (auto-initialized)
      - create_event_rag_corpus: Create a new RAG corpus for events
      - import_event_documents: Import event documents into the RAG corpus
      - search_events_rag: Search for events using vector similarity (PRIMARY TOOL)
      - generate_event_response_with_rag: Generate AI responses enhanced with RAG
      
      WORKFLOW:
      1. The RAG corpus is auto-initialized on startup with existing event data
      2. For user queries about events, ALWAYS use search_events_rag first
      3. For conversational responses, use generate_event_response_with_rag
      4. Provide detailed event information including dates, times, locations, and categories
      
      The RAG system provides semantic search capabilities over event documents.
      Be helpful and provide clear details about timing, location, and event categories.
      Format dates in YYYY-MM-DD format and times as ranges (e.g., "7:00 PM - 11:00 PM").
      
      Current event data includes:
      - Summer festivals and music events
      - Community activities and art walks  
      - Business networking and conferences
      - Family-friendly events and activities
      - Regular weekly/monthly recurring events
    """,
    tools=[
        initialize_corpus_tool,
        create_corpus_tool,
        import_documents_tool,
        search_events_tool,
        generate_response_tool,
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
