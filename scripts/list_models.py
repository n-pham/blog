# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "google-genai",
#     "python-dotenv",
# ]
# ///
import os
import auth
from google import genai

client = auth.get_client()

try:
    print("Listing models...")
    for model in client.models.list(config={"page_size": 100}):
        if "gemini" in model.name or "flash" in model.name:
            print(f"Model: {model.name}")
except Exception as e:
    print(f"Error: {e}")
