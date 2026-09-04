import os

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "openrouter/free")
LLM_TIMEOUT = float(os.getenv("LLM_TIMEOUT", "30"))
LLM_STUB = os.getenv("LLM_STUB", "1")

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)