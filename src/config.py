import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME")

# Streamlit secrets fallback configuration
try:
    import streamlit as st
    if not OPENAI_API_KEY and "OPENAI_API_KEY" in st.secrets:
        OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    if not OPENAI_BASE_URL and "OPENAI_BASE_URL" in st.secrets:
        OPENAI_BASE_URL = st.secrets["OPENAI_BASE_URL"]
    if not OPENAI_MODEL_NAME and "OPENAI_MODEL_NAME" in st.secrets:
        OPENAI_MODEL_NAME = st.secrets["OPENAI_MODEL_NAME"]
except Exception:
    pass

if not OPENAI_MODEL_NAME:
    if OPENAI_BASE_URL and "groq" in OPENAI_BASE_URL.lower():
        OPENAI_MODEL_NAME = "llama-3.3-70b-versatile"
    else:
        OPENAI_MODEL_NAME = "gpt-4o-mini"

# Fallback mode flag
USE_DUMMY_MODE = not bool(OPENAI_API_KEY)

# Local vector store directory
CHROMA_DB_DIR = "carecover-copilot/data/chroma_db"
