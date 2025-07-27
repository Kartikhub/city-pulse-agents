import os
from google.adk import Application
from concierge_agent.agent import root_agent

# Create ADK Application
app_instance = Application(
    agents=[root_agent],
    session_service_uri="sqlite:///./sessions.db"
)

# Get FastAPI app
app = app_instance.get_fast_api_app(
    allow_origins=["*"],
    web=True
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
