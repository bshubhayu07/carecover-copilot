import os
import sys
import hashlib
import time
from fastapi import FastAPI, UploadFile, File, Form, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import USE_DUMMY_MODE, CHROMA_DB_DIR
from src.pdf_ingestion import ingest_pdf, validate_pdf_file
from src.chunking import chunk_text
from src.embeddings import initialize_vector_store
from src.policy_extractor import extract_policy_profile
from src.retrieval import ask_policy_question
from src.hospital_repository import get_hospitals_by_city, get_all_cities
from src.eligibility_engine import match_hospitals
from src.policy_schema import PolicyProfile

app = FastAPI(
    title="CareCover Copilot API",
    description="Independent Healthcare & Policy Decision Support Navigation Backend API",
    version="2.4.0-enterprise"
)

# Enable CORS for React frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "online", "system": "CareCover Copilot Enterprise API", "version": "2.4.0"}

@app.post("/api/extract-policy")
async def extract_policy_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    
    # Save temporary file for validation & ingestion
    temp_path = f"data/temp_{file.filename}"
    os.makedirs("data", exist_ok=True)
    with open(temp_path, "wb") as f:
        f.write(contents)
        
    try:
        pages = ingest_pdf(temp_path)
        raw_text = " ".join([p["text"] for p in pages])
        profile = extract_policy_profile(raw_text)
        return profile.dict()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/api/hospitals")
def get_hospitals_endpoint(city: str = "Pune", specialty: str = "All Specialties", in_network_only: bool = False):
    df = get_hospitals_by_city(city)
    if df.empty:
        return []
    
    demo_profile = PolicyProfile(insurer_name="Niva Bupa", room_eligibility="Single Room")
    matches = match_hospitals(df, demo_profile, context_city=city, user_city=city, use_live_location=False)
    
    filtered = []
    for m in matches:
        if in_network_only and m['network_status'] != "In Network":
            continue
        if specialty != "All Specialties" and specialty.lower() not in m['specialties'].lower():
            continue
        filtered.append(m)
    return filtered

# Serve static frontend files if available in docs/
if os.path.exists("docs"):
    app.mount("/", StaticFiles(directory="docs", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
