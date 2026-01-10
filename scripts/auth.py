
import os
import json
from google import genai
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GEMINI_CREDENTIALS_PATH = os.path.expanduser("~/.gemini/oauth_creds.json")
# Discovered via scripts/discover_project.py
DISCOVERED_PROJECT_ID = os.getenv("DISCOVERED_PROJECT_ID")
LOCATION = "us-central1"

def get_client():
    """
    Returns a configured genai.Client.
    Prioritizes GEMINI_API_KEY.
    Falls back to Gemini CLI credentials (~/.gemini/oauth_creds.json) using Vertex AI mode.
    """
    # 1. Try API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        return genai.Client(api_key=api_key)
    
    # 2. Try Gemini CLI Credentials
    if os.path.exists(GEMINI_CREDENTIALS_PATH):
        try:
            with open(GEMINI_CREDENTIALS_PATH, "r") as f:
                creds_data = json.load(f)
            
            # Reconstruct credentials
            creds = Credentials(
                token=creds_data.get("access_token"),
                refresh_token=creds_data.get("refresh_token"),
                token_uri="https://oauth2.googleapis.com/token",
                client_id=creds_data.get("client_id"), 
                client_secret=creds_data.get("client_secret"),
                scopes=creds_data.get("scope").split(" ") if isinstance(creds_data.get("scope"), str) else None,
            )
            
            print(f"Authenticated using Gemini CLI credentials (Vertex AI mode, Project: {DISCOVERED_PROJECT_ID})")
            
            return genai.Client(
                vertexai=True,
                project=DISCOVERED_PROJECT_ID,
                location=LOCATION,
                credentials=creds
            )
                
        except Exception as e:
            print(f"Warning: Failed to use Gemini CLI credentials: {e}")
    
    print("Error: No valid authentication found.")
    print("Please set GEMINI_API_KEY in .env or ensure you are logged in via Gemini CLI.")
    exit(1)
