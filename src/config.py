import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Dummy mode if no API key is provided
USE_DUMMY_MODE = not bool(OPENAI_API_KEY)

# Vector DB location
CHROMA_DB_DIR = "carecover-copilot/data/chroma_db"
