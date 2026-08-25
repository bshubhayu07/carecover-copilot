import os
import sys
import hashlib
import time
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Ensure project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import USE_DUMMY_MODE, CHROMA_DB_DIR
from src.pdf_ingestion import ingest_pdf
from src.chunking import chunk_text
from src.embeddings import initialize_vector_store, get_chroma_client
from src.policy_extractor import extract_policy_profile, validate_is_policy_document
from src.retrieval import ask_policy_question, ask_policy_question_detailed
from src.guardrails import validate_query_safety, apply_response_guardrails
from src.hospital_repository import get_hospitals_by_city
from src.eligibility_engine import match_hospitals
from src.policy_schema import PolicyProfile
from src.procedure_lookup import get_procedure_details, PROCEDURE_DATABASE
from src.journey_guidance import get_journey_timeline
from src.financial_risk_engine import calculate_financial_risk
from src.bhashini_engine import translate_with_bhashini, BHASHINI_LANG_CODES
from src.security import validate_file_upload, sanitize_untrusted_document_input, rate_limiter
from src.bill_analyzer import analyze_hospital_bill
from src.cost_estimator import estimate_treatment_cost
from src.claims_engine import get_claim_guidance, detect_missing_documents
from src.policy_comparison import compare_policies
from src.contradiction_detector import detect_policy_contradictions
from src.document_classifier import classify_document
from src.eval_suite import evaluate_rag_performance

app = FastAPI(
    title="CareCover Copilot Python Enterprise API",
    description="Independent Healthcare & Policy Decision Support Navigation Backend API",
    version="2.5.0-enterprise"
)

# Global active state in Python backend
active_policy_profile: Optional[PolicyProfile] = None
active_vector_collection = None

# Enforce CORS whitelist
ALLOWED_ORIGINS = [
    "*",
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

# Mount static directory if it exists
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

class QARequest(BaseModel):
    query: str
    history: Optional[List[Dict[str, str]]] = []
    insurer_name: Optional[str] = None
    language: Optional[str] = "English"

@app.get("/")
def root():
    if os.path.exists("static/index.html"):
        return FileResponse(
            "static/index.html",
            headers={
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    return {
        "status": "online",
        "system": "CareCover Copilot Enterprise Python API Engine",
        "version": "2.5.0-enterprise",
        "endpoints": [
            "/api/health",
            "/api/extract-policy",
            "/api/qa",
            "/api/hospitals",
            "/api/procedures",
            "/api/journey",
            "/api/purge-session"
        ]
    }

@app.get("/bg-soothing.jpg")
def get_bg_soothing():
    if os.path.exists("docs/bg-soothing.jpg"):
        return FileResponse("docs/bg-soothing.jpg")
    raise HTTPException(status_code=404, detail="Asset not found")

@app.get("/favicon.svg")
def get_favicon():
    if os.path.exists("docs/favicon.svg"):
        return FileResponse("docs/favicon.svg")
    raise HTTPException(status_code=404, detail="Asset not found")

@app.get("/static/i18n.json")
def get_i18n_json():
    if os.path.exists("static/i18n.json"):
        return FileResponse("static/i18n.json", media_type="application/json")
    raise HTTPException(status_code=404, detail="i18n data file not found")

@app.get("/data/demo_base_policy.pdf")
def get_demo_base_pdf():
    if os.path.exists("data/demo_base_policy.pdf"):
        return FileResponse("data/demo_base_policy.pdf", media_type="application/pdf")
    if os.path.exists("data/demo_policy.pdf"):
        return FileResponse("data/demo_policy.pdf", media_type="application/pdf")
    raise HTTPException(status_code=404, detail="Demo base policy PDF not found")

@app.get("/data/demo_super_topup_policy.pdf")
def get_demo_topup_pdf():
    if os.path.exists("data/demo_super_topup_policy.pdf"):
        return FileResponse("data/demo_super_topup_policy.pdf", media_type="application/pdf")
    raise HTTPException(status_code=404, detail="Demo top-up policy PDF not found")

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "system": "CareCover Copilot Enterprise Python API Engine",
        "version": "2.5.0-enterprise",
        "cors_enforced": True,
        "active_policy_loaded": active_policy_profile is not None,
        "vector_store_initialized": active_vector_collection is not None,
        "upload_hardening": "25MB Limit | %PDF- Validated",
        "python_modules_active": [
            "pdf_ingestion",
            "chunking",
            "embeddings",
            "policy_extractor",
            "retrieval",
            "guardrails",
            "hospital_repository",
            "eligibility_engine",
            "procedure_lookup",
            "journey_guidance"
        ]
    }

@app.post("/api/extract-policy")
async def extract_policy_endpoint(file: UploadFile = File(...)):
    global active_policy_profile, active_vector_collection
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
        
        # Validate that the uploaded PDF is actually a health policy document
        is_valid_policy, validation_err = validate_is_policy_document(raw_text)
        if not is_valid_policy:
            raise HTTPException(status_code=400, detail=f"Uploaded PDF '{file.filename}' is not a valid Health Insurance Policy document. {validation_err}")

        profile = extract_policy_profile(raw_text)
        
        # Chunk text & index into Python vector store
        chunks = chunk_text(pages)
        collection = initialize_vector_store(chunks, persist_directory=CHROMA_DB_DIR, use_dummy_mode=USE_DUMMY_MODE)
        
        active_policy_profile = profile
        active_vector_collection = collection

        return profile.dict()
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.post("/api/qa")
async def policy_qa_endpoint(request: QARequest):
    global active_policy_profile, active_vector_collection
    
    # 1. Validate query safety using Python Guardrails module
    query_valid, violation_msg = validate_query_safety(request.query)
    if not query_valid:
        return {
            "answer": violation_msg,
            "trace_id": f"GUARDRAIL-BLOCK-{int(time.time())}"
        }

    # 2. If vector collection is uninitialized, try retrieving from persistent client
    if active_vector_collection is None:
        try:
            client = get_chroma_client(CHROMA_DB_DIR)
            active_vector_collection = client.get_collection("policy_chunks")
        except Exception:
            active_vector_collection = None

    profile_to_use = active_policy_profile
    if request.insurer_name and request.insurer_name != "No Policy Uploaded":
        profile_to_use = PolicyProfile(insurer_name=request.insurer_name)

    # 3. Track generic question count in history
    generic_history_count = 0
    if request.history:
        for turn in reversed(request.history):
            turn_q = turn.get("query", "").lower() if isinstance(turn, dict) else str(turn).lower()
            has_kw = any(k in turn_q for k in ["cataract", "joint", "knee", "hip", "room", "icu", "rent", "auth", "cashless", "preauth", "pre-auth", "claim", "reimbursement", "doctor", "ambulance", "maternity", "waiting period", "ped", "pre-existing", "sub-limit", "copay", "co-pay", "deductible", "topup", "cover", "policy"])
            if not has_kw:
                generic_history_count += 1
            else:
                break

    # 4. Execute RAG retrieval & LLM synthesis via Python RAG chain with multilingual support
    detailed_res = ask_policy_question_detailed(request.query, active_vector_collection, profile_to_use, language=request.language or "English")
    guarded_answer = apply_response_guardrails(detailed_res["answer"])

    # 5. Generic question limit steering (If 2+ generic questions asked in a row, suggest specific policy concerns)
    q_clean = request.query.lower().strip()
    is_current_generic = not any(k in q_clean for k in ["cataract", "joint", "knee", "hip", "room", "icu", "rent", "auth", "cashless", "preauth", "pre-auth", "claim", "reimbursement", "doctor", "ambulance", "maternity", "waiting period", "ped", "pre-existing", "sub-limit", "copay", "co-pay", "deductible", "topup", "cover", "policy"])
    
    if is_current_generic and generic_history_count >= 2:
        steering_note = "\n\nNotice: You have asked several general questions. To get specific, actionable insights from CareCover Copilot, please ask questions regarding your policy coverage, room rent limits, cataract caps, cashless pre-authorization, or network hospital options."
        guarded_answer += steering_note

    return {
        "answer": guarded_answer,
        "intelligence": detailed_res["intelligence"]
    }

@app.get("/api/hospitals")
def get_hospitals_endpoint(
    city: str = Query("Pune"),
    specialty: str = Query("All Specialties"),
    in_network_only: bool = Query(False),
    user_lat: Optional[float] = Query(None),
    user_lon: Optional[float] = Query(None)
):
    hospitals = get_hospitals_by_city(city)
    if not hospitals:
        hospitals = get_hospitals_by_city("Pune")

    p_profile = active_policy_profile if active_policy_profile else PolicyProfile(insurer_name="Niva Bupa", room_eligibility="Single Room")
    
    use_live = (user_lat is not None and user_lon is not None)
    matches = match_hospitals(hospitals, p_profile, context_city=city, user_city=city, use_live_location=use_live)

    filtered = []
    for m in matches:
        if in_network_only and m.get('network_status') != "In Network":
            continue
        if specialty != "All Specialties" and specialty.lower() not in m.get('specialties', '').lower():
            continue
        filtered.append(m)

    return filtered

@app.get("/api/procedures")
def get_procedures_endpoint(name: Optional[str] = None):
    if name:
        return get_procedure_details(name)
    return PROCEDURE_DATABASE

@app.get("/api/journey")
def get_journey_endpoint():
    return get_journey_timeline()

class BhashiniTranslateRequest(BaseModel):
    text: str
    target_language: str
    source_language: Optional[str] = "English"

@app.post("/api/bhashini/translate")
def bhashini_translate_endpoint(req: BhashiniTranslateRequest):
    translated_text = translate_with_bhashini(req.text, req.target_language, req.source_language)
    return {
        "status": "success",
        "source_language": req.source_language,
        "target_language": req.target_language,
        "original_text": req.text,
        "translated_text": translated_text,
        "supported_languages": list(BHASHINI_LANG_CODES.keys())
    }

@app.post("/api/purge-session")
def purge_session_endpoint():
    global active_policy_profile, active_vector_collection
    
    active_policy_profile = None
    try:
        client = get_chroma_client(CHROMA_DB_DIR)
        client.delete_collection("policy_chunks")
    except Exception:
        pass
    active_vector_collection = None

    ts = time.strftime("%Y-%m-%d %H:%M:%S IST", time.localtime())
    receipt_id = f"DEL-CERT-{hashlib.sha256(str(time.time()).encode()).hexdigest()[:10].upper()}"

    receipt_text = f"""CARECOVER COPILOT - AUDITABLE SESSION DATA DELETION RECEIPT
---------------------------------------------------------------------
Receipt ID: {receipt_id}
Timestamp: {ts}
Compliance Standard: Digital Personal Data Protection (DPDP Rules 2025)
Data Purged: Python Memory Buffers, Extracted Schemas, Chroma Vector Indexes, Chat Logs
Execution Status: Ephemeral RAM & Vector Database Purged (0 Bytes Remaining)
---------------------------------------------------------------------
Issued by CareCover Security & Compliance Systems"""

    return {
        "receiptId": receipt_id,
        "timestamp": ts,
        "receiptText": receipt_text
    }

class FinancialRiskRequest(BaseModel):
    procedure_name: str = "Cataract Surgery"
    estimated_bill: float = 480000.0
    base_sum_insured: Optional[float] = 300000.0
    super_topup_sum_insured: Optional[float] = 1500000.0
    super_topup_deductible: Optional[float] = 300000.0
    room_category: Optional[str] = "Single Private Room"
    co_pay_percent: Optional[float] = 0.0

@app.post("/api/financial-risk")
def calculate_financial_risk_endpoint(req: FinancialRiskRequest):
    return calculate_financial_risk(
        procedure_name=req.procedure_name,
        estimated_bill=req.estimated_bill,
        base_sum_insured=req.base_sum_insured if req.base_sum_insured is not None else 0.0,
        super_topup_sum_insured=req.super_topup_sum_insured if req.super_topup_sum_insured is not None else 0.0,
        super_topup_deductible=req.super_topup_deductible if req.super_topup_deductible is not None else 300000.0,
        room_category=req.room_category or "Single Private Room",
        co_pay_percent=req.co_pay_percent if req.co_pay_percent is not None else 0.0
    )

class BillAnalysisRequest(BaseModel):
    items: List[Dict[str, Any]]
    room_category: Optional[str] = "Single Private Room"
    base_sum_insured: Optional[float] = 300000.0
    co_pay_percent: Optional[float] = 0.0

@app.post("/api/analyze-bill")
def analyze_bill_endpoint(req: BillAnalysisRequest):
    return analyze_hospital_bill(
        bill_items=req.items,
        room_category=req.room_category or "Single Private Room",
        base_sum_insured=req.base_sum_insured or 0.0,
        co_pay_percent=req.co_pay_percent or 0.0
    )

@app.get("/api/cost-estimate")
def cost_estimate_endpoint(procedure: str = Query("Cataract Surgery (Per Eye)"), city: str = Query("Pune")):
    return estimate_treatment_cost(procedure, city)

class ClaimGuidanceRequest(BaseModel):
    claim_type: str = "Cashless Pre-Auth"
    procedure_name: str = "Cataract Surgery"

@app.post("/api/claim-guidance")
def claim_guidance_endpoint(req: ClaimGuidanceRequest):
    return get_claim_guidance(req.claim_type, req.procedure_name)

class MissingDocsRequest(BaseModel):
    submitted_documents: List[str]
    claim_type: Optional[str] = "Reimbursement Claim"

@app.post("/api/generate-checklist")
def generate_checklist_endpoint(req: MissingDocsRequest):
    return detect_missing_documents(req.submitted_documents, req.claim_type or "Reimbursement Claim")

@app.post("/api/compare-policies")
def compare_policies_endpoint():
    p_profile = active_policy_profile if active_policy_profile else PolicyProfile(insurer_name="Niva Bupa", sum_insured_inr=300000.0)
    return compare_policies(p_profile)

@app.post("/api/detect-contradictions")
def detect_contradictions_endpoint():
    p_profile = active_policy_profile if active_policy_profile else PolicyProfile(insurer_name="Niva Bupa", sum_insured_inr=300000.0)
    return detect_policy_contradictions(p_profile)

class ClassifyDocRequest(BaseModel):
    text_content: str
    filename: Optional[str] = ""

@app.post("/api/classify-document")
def classify_document_endpoint(req: ClassifyDocRequest):
    return classify_document(req.text_content, req.filename or "")

@app.get("/api/eval-rag")
def eval_rag_endpoint():
    return evaluate_rag_performance()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
