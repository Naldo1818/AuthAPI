import os

from dotenv import load_dotenv
from supabase import create_client, Client

# Load variables from .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash-lite")
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "30"))
LLM_STUB = os.getenv("LLM_STUB", "1")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)