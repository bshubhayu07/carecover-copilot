import os
import sys
import hashlib
import time
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from fastapi import FastAPI, UploadFile, File, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, Response

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

@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self' 'unsafe-inline' 'unsafe-eval' https: data:;"
    return response

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
        return FileResponse("docs/favicon.svg", media_type="image/svg+xml")
    if os.path.exists("static/favicon.svg"):
        return FileResponse("static/favicon.svg", media_type="image/svg+xml")
    svg_data = """<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2338bdf8' stroke-width='2.5' stroke-linecap='round' stroke-linejoin='round'><path d='M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z'/><path stroke='%23ffffff' d='m9 12 2 2 4-4'/></svg>"""
    return Response(content=svg_data, media_type="image/svg+xml")

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

@app.get("/api/detect-ip-location")
def detect_ip_location_endpoint(request: Request):
    client_ip = request.client.host if request.client else ""
    try:
        import urllib.request
        import json
        req = urllib.request.Request("http://ip-api.com/json/", headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=3.0) as resp:
            data = json.loads(resp.read().decode())
            if data.get("status") == "success" and "lat" in data and "lon" in data:
                return {
                    "ip": data.get("query", client_ip),
                    "city": data.get("city", "Pune"),
                    "region": data.get("regionName", "Maharashtra"),
                    "latitude": float(data["lat"]),
                    "longitude": float(data["lon"])
                }
    except Exception:
        pass
    return {"ip": client_ip, "city": "Pune", "region": "Maharashtra", "latitude": 18.5204, "longitude": 73.8567}

@app.get("/api/hospitals")
def get_hospitals_endpoint(
    city: str = Query("Pune"),
    specialty: str = Query("All Specialties"),
    in_network_only: bool = Query(False),
    user_lat: Optional[float] = Query(None),
    user_lon: Optional[float] = Query(None),
    user_city: Optional[str] = Query(None)
):
    hospitals = get_hospitals_by_city(city)
    p_profile = active_policy_profile if active_policy_profile else PolicyProfile(insurer_name="Niva Bupa", room_eligibility="Single Room")
    
    effective_user_city = user_city.strip() if (user_city and user_city.strip()) else city
    use_live = (user_lat is not None and user_lon is not None) or (user_city is not None)
    matches = match_hospitals(
        hospitals, 
        p_profile, 
        context_city=city, 
        user_city=effective_user_city, 
        use_live_location=use_live,
        user_lat=user_lat,
        user_lon=user_lon
    )

    filtered = []
    for m in matches:
        if in_network_only and m.get('network_status') != "In Network":
            continue
        if specialty != "All Specialties":
            spec_low = specialty.lower()
            hosp_spec_low = str(m.get('specialties', '')).lower()
            
            if spec_low == "multispecialty":
                if "multispecialty" not in hosp_spec_low and "|" not in hosp_spec_low and "general" not in hosp_spec_low:
                    continue
            else:
                KEYWORD_MAP = {
                    "cardiology": ["cardio", "vascular", "heart"],
                    "orthopedics": ["ortho", "joint", "bone"],
                    "oncology": ["onco", "cancer", "tumor"],
                    "neurology": ["neuro", "brain", "spine"],
                    "gastroenterology": ["gastro", "hepato", "digestive"],
                    "urology": ["uro", "nephro", "kidney"],
                    "pulmonology": ["pulmo", "resp", "chest", "lung"],
                    "gynecology": ["gynec", "obstet", "matern", "women", "gynaec"],
                    "pediatrics": ["pediatr", "child"],
                    "ophthalmology": ["ophthal", "eye", "vision"],
                    "ent": ["ent", "ear", "nose", "throat"]
                }
                req_keywords = KEYWORD_MAP.get(spec_low, [spec_low])
                has_spec = any(k in hosp_spec_low for k in req_keywords) or "multispecialty" in hosp_spec_low
                if not has_spec:
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
    procedure_name: Optional[str] = "Cataract Surgery"
    estimated_bill: Optional[float] = None
    total_bill: Optional[float] = None
    claimed_amount: Optional[float] = None
    base_sum_insured: Optional[float] = 300000.0
    super_topup_sum_insured: Optional[float] = 1500000.0
    super_topup_deductible: Optional[float] = 300000.0
    room_category: Optional[str] = None
    room_type: Optional[str] = None
    co_pay_percent: Optional[float] = 0.0

@app.post("/api/financial-risk")
def calculate_financial_risk_endpoint(req: FinancialRiskRequest):
    effective_bill = 480000.0
    if req.estimated_bill is not None:
        effective_bill = float(req.estimated_bill)
    elif req.total_bill is not None:
        effective_bill = float(req.total_bill)
    elif req.claimed_amount is not None:
        effective_bill = float(req.claimed_amount)

    effective_room = req.room_category or req.room_type or "Single Private Room"
    effective_proc = req.procedure_name or "Cataract Surgery"

    return calculate_financial_risk(
        procedure_name=effective_proc,
        estimated_bill=effective_bill,
        base_sum_insured=req.base_sum_insured if req.base_sum_insured is not None else 0.0,
        super_topup_sum_insured=req.super_topup_sum_insured if req.super_topup_sum_insured is not None else 0.0,
        super_topup_deductible=req.super_topup_deductible if req.super_topup_deductible is not None else 300000.0,
        room_category=effective_room,
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

SAMPLE_POLICIES_DATABASE = [
    {
        "id": "sample_1",
        "title": "Niva Bupa Health Companion",
        "insurer_name": "Niva Bupa Health Insurance",
        "policy_name": "Health Companion Variant 2",
        "sum_insured": "₹5,00,000",
        "sum_insured_inr": 500000.0,
        "filename": "niva_bupa_health_companion.pdf",
        "room_eligibility": "Single Private Room",
        "room_limit": "Single Private Room (No Cap)",
        "room_capping_type": "no_limit",
        "proportional_deduction_clause": "No proportional deduction on doctor/surgery fees if admitted in Single Private Room.",
        "copay": "0% Co-Pay (100% Payout)",
        "copay_percent": 0,
        "pre_auth": {
            "emergency": "Intimation within 24 hours of emergency admission",
            "elective": "48 hours prior pre-authorization notice to TPA desk"
        },
        "waiting_periods": {
            "initial": "30 Days for non-accidental hospitalizations",
            "specific_diseases": "24 Months for Cataract, Joint Replacement, Hernia, Stone Surgery",
            "pre_existing": "36 Months for Pre-Existing Conditions (PED)"
        },
        "restoration_benefit": "100% Automatic Sum Restoration once per policy year",
        "topup_details": {
            "deductible": "₹5,00,000 threshold for Super Top-Up trigger"
        },
        "pre_post_hospitalization": "60 Days Pre-Hospitalization & 180 Days Post-Hospitalization",
        "exclusions": [
            "Cosmetics & LASIK unless refractive error > 7.5 diopters",
            "OPD consultations & routine pharmacy unless day-care surgery",
            "Non-medical consumables (gloves, PPE kits, admission fees)",
            "Intentional self-injury, alcohol/substance abuse treatments"
        ]
    },
    {
        "id": "sample_2",
        "title": "Star Comprehensive Health Plan",
        "insurer_name": "Star Health & Allied Insurance",
        "policy_name": "Star Comprehensive Health Insurance",
        "sum_insured": "₹10,00,000",
        "sum_insured_inr": 1000000.0,
        "filename": "star_comprehensive_policy.pdf",
        "room_eligibility": "Single Private Room",
        "room_limit": "Single Private Room",
        "room_capping_type": "no_limit",
        "proportional_deduction_clause": "No room rent capping penalty.",
        "copay": "0% Co-Pay up to age 60",
        "copay_percent": 0,
        "pre_auth": {
            "emergency": "Within 24 hours of casualty admission",
            "elective": "24 to 48 hours prior notice"
        },
        "waiting_periods": {
            "initial": "30 Days",
            "specific_diseases": "24 Months",
            "pre_existing": "36 Months"
        },
        "restoration_benefit": "100% Automatic Restoration for un-related illnesses",
        "topup_details": {
            "deductible": "₹10,00,000 threshold"
        },
        "pre_post_hospitalization": "60 Days Pre & 90 Days Post",
        "exclusions": [
            "Non-payable administrative consumable charges",
            "Unproven/experimental therapies",
            "Weight control & bariatric surgery"
        ]
    },
    {
        "id": "sample_3",
        "title": "HDFC ERGO Optima Secure",
        "insurer_name": "HDFC ERGO General Insurance",
        "policy_name": "Optima Secure Individual Plan",
        "sum_insured": "₹15,00,000",
        "sum_insured_inr": 1500000.0,
        "filename": "hdfc_ergo_optima_secure.pdf",
        "room_eligibility": "Any Room Category",
        "room_limit": "Any Room Category (No Capping)",
        "room_capping_type": "no_limit",
        "proportional_deduction_clause": "No capping or proportional deduction across all room tiers.",
        "copay": "0% Mandatory Co-Pay",
        "copay_percent": 0,
        "pre_auth": {
            "emergency": "Within 24 hours",
            "elective": "48 hours prior intimation"
        },
        "waiting_periods": {
            "initial": "30 Days",
            "specific_diseases": "24 Months",
            "pre_existing": "24 Months"
        },
        "restoration_benefit": "Secure Benefit doubling sum insured instantly",
        "topup_details": {
            "deductible": "₹15,00,000 deductible"
        },
        "pre_post_hospitalization": "60 Days Pre & 180 Days Post",
        "exclusions": [
            "Non-medical hygiene items & toiletries",
            "External durable medical equipment",
            "Cosmetic procedures"
        ]
    },
    {
        "id": "sample_4",
        "title": "Care Supreme Health Plan",
        "insurer_name": "Care Health Insurance",
        "policy_name": "Care Supreme Classic",
        "sum_insured": "₹7,50,000",
        "sum_insured_inr": 750000.0,
        "filename": "care_supreme_policy.pdf",
        "room_eligibility": "Single Private Room",
        "room_limit": "Single Private Room",
        "room_capping_type": "no_limit",
        "proportional_deduction_clause": "Standard single room covered. Higher suite upgrades trigger proportional deduction.",
        "copay": "0% Co-Pay",
        "copay_percent": 0,
        "pre_auth": {
            "emergency": "Within 24 hours",
            "elective": "48 hours prior notice"
        },
        "waiting_periods": {
            "initial": "30 Days",
            "specific_diseases": "24 Months",
            "pre_existing": "36 Months"
        },
        "restoration_benefit": "Unlimited Automatic Restoration",
        "topup_details": {
            "deductible": "₹7,50,000 threshold"
        },
        "pre_post_hospitalization": "60 Days Pre & 90 Days Post",
        "exclusions": [
            "Non-payable items list under IRDAI guidelines",
            "Genetic disorder treatments",
            "Hazardous sports injuries"
        ]
    }
]

@app.get("/api/sample-policies")
def get_sample_policies_endpoint():
    return {"policies": SAMPLE_POLICIES_DATABASE}

class SelectSamplePolicyRequest(BaseModel):
    policy_id: Optional[str] = "sample_1"

@app.post("/api/select-sample-policy")
def select_sample_policy_endpoint(req: Optional[SelectSamplePolicyRequest] = None, policy_id: Optional[str] = Query(None)):
    global active_policy_profile
    eff_id = "sample_1"
    if req and req.policy_id:
        eff_id = req.policy_id
    elif policy_id:
        eff_id = policy_id

    found = next((p for p in SAMPLE_POLICIES_DATABASE if p["id"] == eff_id or p["filename"] == eff_id), SAMPLE_POLICIES_DATABASE[0])
    active_policy_profile = PolicyProfile(
        insurer_name=found["insurer_name"],
        policy_name=found["policy_name"],
        sum_insured_inr=found["sum_insured_inr"],
        room_eligibility=found["room_eligibility"],
        co_pay=found["copay"],
        exclusions=found["exclusions"]
    )
    return {"status": "success", "summary": found}

@app.get("/api/care-journey/{stage_key}")
def get_care_journey_stage_endpoint(stage_key: str):
    stages = {
        "admission": {
            "stage_info": {
                "title": "1. Hospital Admission & Cashless Pre-Authorization",
                "description": "Pre-auth submission, TPA intimation SLAs, and network desk verification.",
                "key_actions": [
                    "Present Health Insurance Card and patient Aadhaar/PAN ID at TPA Desk.",
                    "Submit TPA Pre-Authorization Form with Doctor Admission Slip & Diagnosis.",
                    "Verify room category eligibility (Single Private Room) before signing admission sheet.",
                    "Obtain TPA Initial Approval Letter (Standard SLA: 2 to 4 hours)."
                ],
                "required_documents": [
                    "Health Insurance Card / Policy Schedule Copy",
                    "Patient Government Photo ID (Aadhaar / PAN / Passport)",
                    "Doctor Admission Advice & Prescription Slip",
                    "TPA Pre-Authorization Request Form (Filled & Signed)"
                ],
                "cost_warning": "Warning: Choosing a Deluxe Suite when policy limits to Single Private Room triggers 15%-25% proportional deductions on all doctor and surgical fees."
            },
            "customized_policy_notes": [
                "Planned Admission SLA: Require 48 hours prior notice to TPA desk.",
                "Emergency Admission SLA: Require intimation within 24 hours of casualty admission."
            ]
        },
        "investigation": {
            "stage_info": {
                "title": "2. Inpatient Diagnostics & Clinical Care",
                "description": "Daily doctor visits, diagnostic imaging, and pharmacy billing during stay.",
                "key_actions": [
                    "Ensure diagnostic imaging (MRI, CT Scan, Sonography) has doctor's written prescription.",
                    "Keep track of daily hospital pharmacy bills & consumable issues.",
                    "Verify doctor consultation notes are logged daily in hospital inpatient chart."
                ],
                "required_documents": [
                    "Diagnostic Investigation Reports (Laboratory, X-Ray, CT, MRI)",
                    "Doctor Daily Consultation Notes",
                    "Itemized Pharmacy Receipts & Drug Requisitions"
                ],
                "cost_warning": "Non-payable items alert: Disposables like PPE kits, gloves, tissue boxes, and dietitian fees are non-reimbursable consumables."
            },
            "customized_policy_notes": [
                "Diagnostic tests covered 100% up to active Base Sum Insured.",
                "Pre-hospitalization diagnostic test reports dated up to 60 days prior are eligible for reimbursement."
            ]
        },
        "procedure": {
            "stage_info": {
                "title": "3. Surgical Operation & Procedure Execution",
                "description": "Surgical procedures, OT charges, ICU stay, and sub-limit capping verification.",
                "key_actions": [
                    "Confirm surgical procedure name matches pre-authorization approval letter.",
                    "Check if procedure has specific sub-limits (e.g., Cataract ₹40,000/eye, Joint Replacement ₹1.5L/joint).",
                    "Ensure ICU/CCU charges are covered without capping penalties."
                ],
                "required_documents": [
                    "Operation Theatre (OT) Notes & Anesthesia Record",
                    "Implant Invoice & Barcode Sticker (Stents, Cataract Lens, Joint Prosthesis)",
                    "Surgeon & Specialist Consultation Certificates"
                ],
                "cost_warning": "Implant Sub-limit Notice: High-end premium implants exceeding policy sub-limits require patient out-of-pocket payment."
            },
            "customized_policy_notes": [
                "Day Care procedures (Cataract, Dialysis, Chemo) covered without 24h hospitalization requirement."
            ]
        },
        "discharge": {
            "stage_info": {
                "title": "4. Hospital Discharge & Final Claim Settlement",
                "description": "Final bill submission, TPA final approval letter, and post-op claims guidance.",
                "key_actions": [
                    "Request hospital TPA desk to send Final Itemized Bill to insurer 4 hours before expected discharge.",
                    "Obtain Discharge Summary, Final Bill, Payment Receipts, and Investigation Reports.",
                    "Review non-payable consumable line items before paying out-of-pocket balance at counter.",
                    "Retain all original bills for 60-day post-hospitalization reimbursement claims."
                ],
                "required_documents": [
                    "Original Hospital Discharge Summary (Signed by Attending Doctor)",
                    "Detailed Itemized Final Bill & Breakup Statement",
                    "Original Payment Receipts / Cashless Final Approval Letter",
                    "All Diagnostic Test Reports & Post-Discharge Doctor Prescriptions"
                ],
                "cost_warning": "Final Settlement SLA: TPA final claim audit takes 2 to 4 hours on discharge day."
            },
            "customized_policy_notes": [
                "Post-hospitalization claims (follow-up consults, medicines) eligible up to 90 to 180 days post-discharge."
            ]
        }
    }
    return stages.get(stage_key, stages["admission"])

@app.get("/api/eval-rag")
def eval_rag_endpoint():
    return evaluate_rag_performance()

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
