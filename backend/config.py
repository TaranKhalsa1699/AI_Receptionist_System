import os
from dotenv import load_dotenv

# Load key-value pairs from .env file to environment variables
load_dotenv()

def get_env_var(key: str) -> str:
    """
    Retrieve an environment variable or raise an error if it's missing.
    """
    value = os.getenv(key)
    if not value:
        raise ValueError(f"Missing required environment variable: {key}")
    return value

# Required Environment Variables
try:
    OPENAI_API_KEY = get_env_var("OPENAI_API_KEY")
    SUPABASE_URL = get_env_var("SUPABASE_URL")
    # Try to get Service Role Key first (Bypasses RLS), fall back to standard Key
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
    if not SUPABASE_KEY:
        raise ValueError("Missing SUPABASE_SERVICE_ROLE_KEY or SUPABASE_KEY")
    WEBHOOK_URL = get_env_var("WEBHOOK_URL")
    GOOGLE_API_KEY= get_env_var("GOOGLE_API_KEY")
except ValueError as e:
    # Fail fast at startup
    print(f"CRITICAL: Configuration Error: {e}")
    raise
