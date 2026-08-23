import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

if not OPENAI_MODEL_NAME:
    if OPENAI_BASE_URL and "groq" in OPENAI_BASE_URL.lower():
        OPENAI_MODEL_NAME = "llama-3.3-70b-versatile"
    else:
        OPENAI_MODEL_NAME = "gpt-4o-mini"

# Fallback mode flag
USE_DUMMY_MODE = not bool(OPENAI_API_KEY)

# Local vector store directory
CHROMA_DB_DIR = "carecover-copilot/data/chroma_db"
