# CareCover Copilot - Healthcare & Policy Navigation System

**Live Web Application:** [https://carecover-copilot-production.up.railway.app/](https://carecover-copilot-production.up.railway.app/)  
**Document Version:** 2.4.0-enterprise  

> CareCover Copilot is an enterprise-grade retrieval-augmented healthcare navigation platform. It parses health insurance policy contracts (PDF format), extracts coverage clauses (Sum Insured, Room Limits, Co-Pay, Pre-Auth rules), compares secondary Super Top-Up policies, queries policy terms in real time, and matches cashless network hospitals with real-time GPS distance calculation and record-level feed provenance.

---

## Overview

CareCover Copilot is designed as an **independent clinical and insurance decision-support navigation system**. It does not diagnose medical conditions, recommend clinical treatment, or guarantee binding insurance claim settlement.

---

## Tech Stack & Architecture

- **Frontend UI:** React 19 + Tailwind CSS v4 (Multi-page glassmorphism interface supporting all 22 official Scheduled Languages of India).
- **Backend API:** Python 3.11+ FastAPI & Uvicorn.
- **Document Processing:** PyMuPDF (`fitz`) text extraction & SHA-256 caching.
- **Vector Engine:** ChromaDB local vector store indexing.
- **LLM Inference:** Groq API (`llama-3.3-70b-versatile`).

---

## Quick Start & Running Locally

### 1. Frontend Development Server
```bash
# Navigate to frontend folder
cd frontend

# Install Node.js dependencies
npm install

# Start local React development server
npm run dev
```
Open `http://localhost:5173` in your browser.

### 2. Backend FastAPI Server
```bash
# Install Python dependencies
pip install -r requirements.txt

# Configure environment variables (.env)
GROQ_API_KEY=your_groq_api_key_here

# Run FastAPI backend server
python main.py
```
Backend API will run at `http://localhost:8000`.

---

## Running with Docker

You can run the entire system in a multi-stage production container:

```bash
# Using Docker Compose (Recommended)
docker-compose up --build -d

# Using Docker CLI:
docker build -t carecover-copilot .
docker run -p 8000:8000 carecover-copilot
```
Navigate to `http://localhost:8000` in your browser.

---

## Safety & Compliance Disclaimers

- **Informational Only:** Not medical advice or a binding guarantee of insurance coverage.
- **DPDP Rules 2025:** Ephemeral in-memory RAM document processing with 0-hour database storage. Users can trigger an instant session RAM purge and generate an auditable deletion certificate (`carecover_deletion_receipt.txt`).
- **CERT-In Directions 70B:** Mandatory 6-hour intimation SLA for cyber security incidents.
- **IRDAI Disclosure:** Independent navigation system. Not officially affiliated with or endorsed by IRDAI. Final cashless settlement is subject solely to direct insurer/TPA confirmation.
