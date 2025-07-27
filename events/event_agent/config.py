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
Configuration for Event Agent RAG setup.
"""

import os

# Google Cloud Configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "city-pulse-467120")
LOCATION = "us-central1"

# RAG Configuration
EMBEDDING_MODEL = "publishers/google/models/text-embedding-005"
RAG_CORPUS_NAME = "city_events_corpus"
RAG_CORPUS_DESCRIPTION = "Vector database for city events and activities"

# RAG Retrieval Settings
DEFAULT_TOP_K = 3
DEFAULT_CHUNK_SIZE = 512
DEFAULT_CHUNK_OVERLAP = 100
DEFAULT_VECTOR_DISTANCE_THRESHOLD = 0.5
MAX_EMBEDDING_REQUESTS_PER_MIN = 1000

# Generative Model Settings
GENERATIVE_MODEL = "gemini-2.0-flash-001"

# Sample event document paths (GCS or Google Drive)
SAMPLE_EVENT_DOCUMENTS = [
    "gs://city-pulse-events-bucket-467120/summer_festivals.txt",
    "gs://city-pulse-events-bucket-467120/business_events.txt", 
    "gs://city-pulse-events-bucket-467120/community_events.txt"
]
