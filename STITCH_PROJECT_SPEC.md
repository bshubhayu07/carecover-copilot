# CareCover Copilot - Project Specification & Architecture Guide

**Project Name:** CareCover Copilot  
**Version:** 2.4.0-enterprise  
**Category:** Healthcare & Insurance Decision-Support System  
**Repository:** `https://github.com/bshubhayu07/carecover-copilot.git`  
**Live Application:** `https://carecover-copilot-keivlj6ggku4xesbfkyxkz.streamlit.app/`  
**Target Platform / Deployment:** Stitch / GCP Cloud Run / Streamlit Enterprise  

---

## 1. Executive Summary

**CareCover Copilot** is an enterprise-grade, multi-lingual health insurance policy parsing, cashless hospital matching, and clinical decision-support navigation platform designed for the Indian healthcare ecosystem. 

It enables patients and policyholders to upload complex insurance policy contracts (PDF format), extract structured coverage terms (Sum Insured, Room Eligibility, Co-Pay, Pre-Authorization Rules), compare secondary Super Top-Up policies, query policy clauses in natural language via real-time LLM token streaming, and locate nearby cashless network hospitals with real-time GPS distance calculation and record-level feed provenance.

---

## 2. Core Functional Modules

### 2.1 Tab 1: Upload & Policy Extractor
- **Upload Hardening:** Strict 25 MB file size limit, 50-page maximum limit, and `%PDF-` magic-byte payload validation.
- **SHA-256 Vector Caching:** Computes document hashes to accelerate ingestion and prevent duplicate embedding computation.
- **Dual-Policy Engine:** Supports simultaneous analysis of primary base health policies and secondary Super Top-Up policies, calculating combined sum insured limits and deductible execution thresholds.
- **PDF Export Engine:** Generates downloadable formatted PDF policy summaries (`carecover_policy_summary.pdf`) and TPA Pre-Authorization Request forms (`carecover_pre_authorization_tpa_form.pdf`).

### 2.2 Tab 2: Policy Q&A Assistant (RAG Engine)
- **RAG Architecture:** PyMuPDF text chunking + ChromaDB local vector store indexing + Groq Llama-3.3-70B LLM inference engine.
- **Real-Time Token Streaming:** Zero-perceived latency text generation (`st.write_stream`).
- **Medical Advice Safety Guardrail:** Intercepts medical treatment/prescription queries and redirects to emergency services (`112 / 108`).
- **Auditable Traceability:** Appends unique RAG audit hashes (`RAG-TRACE-[MD5]`) to every assistant response.
- **Feedback & Escalation Loop:** Built-in user reporting widget generating support tickets (`#TKT-SUPP-[HASH]`).

### 2.3 Tab 3: Cashless Hospital & Room Matching Engine
- **Multi-City Network Directory:** Sourced directly from published insurer/TPA network feeds (*Niva Bupa, Star Health, ICICI Lombard, Medi Assist*).
- **Record-Level Data Provenance:** Displays versioned feed IDs (e.g. `FEED-NIVABUPA-20260816-01`), daily refresh timestamps (00:00 IST), and IRDAI provider disclosure disclaimers.
- **GPS Distance Calculation:** Computes Haversine distance relative to the user's active location.

### 2.4 Tab 4: Care Journey & Proportional Rent Penalty Calculator
- **Proportional Room Rent Simulator:** Calculates penalty deductions on associated doctor/surgery fees when choosing a hospital room rate higher than policy limits.
- **Out-of-Pocket Estimator:** Computes approved cashless amounts vs user out-of-pocket shares based on co-pay percentages and non-medical consumables.
- **Interactive Patient Checklist:** Step-by-step progress tracking from pre-admission to post-discharge reimbursement claims.

---

## 3. Technology Stack & Infrastructure

- **Language & Runtime:** Python 3.10+
- **User Interface Framework:** Streamlit (Custom styled with responsive CSS)
- **PDF Parsing Engine:** PyMuPDF (`fitz`)
- **Vector Database:** ChromaDB (Ephemeral session-isolated collection instances)
- **Embeddings:** Local ONNX / SentenceTransformers (`all-MiniLM-L6-v2`)
- **LLM Engine:** Groq API (`llama-3.3-70b-versatile`)
- **Document Generation:** ReportLab PDF Engine
- **Unit Testing Suite:** Pytest (`tests/test_eligibility_engine.py`, `tests/test_guardrails.py`, `tests/test_policy_extractor.py`)

---

## 4. Multi-Lingual Architecture (22 Scheduled Indian Languages)

CareCover Copilot natively supports **all 22 officially recognized Scheduled Languages of India** under the 8th Schedule of the Constitution of India, plus English:

1. English
2. Assamese (অসমীয়া)
3. Bengali (বাংলা)
4. Bodo (बर')
5. Dogri (डोगरी)
6. Gujarati (ગુજરાતી)
7. Hindi (हिंदी)
8. Kannada (ಕನ್ನಡ)
9. Kashmiri (कॉशुर)
10. Konkani (कोंकणी)
11. Maithili (मैथिली)
12. Malayalam (മലയാളം)
13. Manipuri (মৈতৈলোন্)
14. Marathi (मराठी)
15. Nepali (नेपाली)
16. Odia (ଓଡ଼ିଆ)
17. Punjabi (ਪੰਜਾਬੀ)
18. Sanskrit (संस्कृतम्)
19. Santali (ᱥᱟᱱᱛᱟᱲᱤ)
20. Sindhi (सिंधी)
21. Tamil (தமிழ்)
22. Telugu (తెలుగు)
23. Urdu (اردو)

---

## 5. Security, Privacy & Regulatory Compliance

- **DPDP Rules 2025 Alignment:** Ephemeral session RAM data retention (0-hour persistent database storage). Users can trigger instant RAM purges and generate auditable deletion receipts (`carecover_deletion_receipt.txt`).
- **CERT-In Cyber Security Directions 70B:** Mandatory 6-hour intimation SLA for cyber security incidents to `incident@cert-in.org.in`.
- **IRDAI Non-Endorsement Disclosure:** Explicit statements clarifying that CareCover Copilot is an independent navigation tool and final cashless settlement is subject solely to direct insurer/TPA confirmation.
- **Currencies:** Official Indian Numbering System (`INR 5,00,000`, `INR 15,00,000`, `INR 1,00,00,000`).

---

## 6. Environment & Installation Guide

```bash
# 1. Clone repository
git clone https://github.com/bshubhayu07/carecover-copilot.git
cd carecover-copilot

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables (.env)
GROQ_API_KEY=your_groq_api_key_here

# 4. Run automated test suite
python -m pytest tests/

# 5. Launch local application
streamlit run app.py
```

---
*Generated for Stitch Integration & GCP Deployment Pipeline | CareCover Copilot Systems*
