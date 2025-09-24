import json
import os

def load_config(config_path="configs/app_config.json"):
    """Load application configuration from JSON file."""
    with open(config_path) as f:
        return json.load(f)

def get_gemini_api_key():
    """Get Gemini API key from environment variables."""
    return os.getenv("GEMINI_API_KEY")

def format_api_response(data):
    """Format API response data."""
    return json.dumps(data, indent=2)