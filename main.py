import os
import sys
import hashlib
import time
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import USE_DUMMY_MODE, CHROMA_DB_DIR
from src.pdf_ingestion import ingest_pdf
from src.policy_extractor import extract_policy_profile
from src.hospital_repository import get_hospitals_by_city
from src.eligibility_engine import match_hospitals
from src.policy_schema import PolicyProfile

app = FastAPI(
    title="CareCover Copilot API",
    description="Independent Healthcare & Policy Decision Support Navigation Backend API",
    version="2.4.0-enterprise"
)

# Enforce strict CORS whitelist (Prevents wildcard CORS vulnerability)
ALLOWED_ORIGINS = [
    "https://bshubhayu07.github.io",
    "http://localhost:5173",
    "http://localhost:8000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "CareCover Copilot Enterprise API",
        "version": "2.4.0-enterprise",
        "cors_enforced": True,
        "upload_hardening": "25MB Limit | %PDF- Validated"
    }

@app.post("/api/extract-policy")
async def extract_policy_endpoint(file: UploadFile = File(...)):
    contents = await file.read()
    
    # 1. Enforce 25 MB max payload threshold
    if len(contents) > 25 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File size exceeds 25 MB enterprise limit.")

    # 2. Enforce %PDF- magic bytes header check
    if not contents.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="Invalid file type. File header is not a valid PDF (%PDF-).")

    # 3. Cryptographically sanitize filename (Prevents path traversal attacks)
    file_hash = hashlib.sha256(contents).hexdigest()[:16]
    temp_path = f"data/temp_{file_hash}.pdf"
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
        df = get_hospitals_by_city("Pune")

    demo_profile = PolicyProfile(insurer_name="Niva Bupa", room_eligibility="Single Room")
    matches = match_hospitals(df, demo_profile, context_city=city, user_city=city, use_live_location=False)

    filtered = []
    for m in matches:
        if in_network_only and m.get('network_status') != "In Network":
            continue
        if specialty != "All Specialties" and specialty.lower() not in m.get('specialties', '').lower():
            continue
        filtered.append(m)

    return filtered

# Serve static frontend files if available in docs/
if os.path.exists("docs"):
    app.mount("/", StaticFiles(directory="docs", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    # reload=False for production readiness
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
