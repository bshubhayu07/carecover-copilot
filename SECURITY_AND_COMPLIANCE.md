# CareCover Copilot - Enterprise Security, Architecture & Compliance Specification

**Document Version:** 2.4.0-enterprise  
**Release Date:** August 16, 2026  
**Audit Status:** Enterprise Production Verification  

---

## Executive Summary
CareCover Copilot is an independent clinical and health insurance decision-support navigation system. This document details the technical architecture, data privacy controls, upload hardening, feed provenance governance, and regulatory compliance disclosures in accordance with the **Digital Personal Data Protection (DPDP Rules 2025)**, **CERT-In Cyber Security Directions 70B**, and **IRDAI Health Regulations 2024**.

---

## 1. Technical Architecture & Ephemeral Memory Lifecycle

### 1.1 Ephemeral RAM Processing (Zero Storage)
- **Document Ingestion:** Health insurance policy PDFs are parsed exclusively in temporary RAM session buffers (`io.BytesIO`).
- **Vector Stores:** Document vector embeddings are initialized in session-isolated ChromaDB collections using local ONNX / MiniLM embeddings.
- **Disk Lifetime:** 0 hours. No raw PDF text or extracted policy summaries are written to permanent long-term databases.

### 1.2 Session Data Deletion Protocol
- **Trigger:** User clicks "Purge & Delete Session Data Now" in the sidebar.
- **Action:** Wipes active application state memory references, purges ChromaDB vector collections, and unlinks temporary session files.
- **Audit Receipt:** Generates an Ephemeral Data Deletion Receipt (`DEL-CERT-[HASH]`) verifying zero bytes remain in active memory.

---

## 2. Upload Hardening & Security Controls

| Hardening Requirement | Technical Specification | Enforcement Status |
| :--- | :--- | :--- |
| **Max File Size** | Strict 25 MB payload threshold | Enforced (`src/pdf_ingestion.py`) |
| **Max Page Count** | Maximum 50 pages per document | Enforced (`src/pdf_ingestion.py`) |
| **Header Validation** | Magic-byte check (`%PDF-` signature verification) | Enforced (`src/pdf_ingestion.py`) |
| **Payload Failure Handling** | Catches corrupt files & returns clear UI error alerts | Enforced |

---

## 3. CERT-In Incident Response & DPDP Rules 2025

### 3.1 CERT-In Incident Intimation SLA (Directions 70B)
- **6-Hour Mandatory Intimation:** Cyber security incidents, unexpected system outages, or data anomalies are intimated to CERT-In (`incident@cert-in.org.in`) within 6 hours of detection as prescribed under CERT-In Cyber Security Directions 70B.
- **Incident Response Officer:** `security@carecovercopilot.in` (SLA: Acknowledgment within 2 hours).

### 3.2 DPDP Rules 2025 & Grievance Redressal
- **Explicit Consent:** Mandatory user consent prior to document parsing.
- **Grievance Redressal Nodal Officer:** Designated Privacy Officer (`grievance@carecovercopilot.in` | SLA: 72 business hours | Ref: `#GRV-2026-88192`).

---

## 4. Data Provenance & Insurer Feed Governance

### 4.1 Record-Level Feed Attributes
Every hospital network result displays:
- **Source Feed ID:** Unique versioned feed tag (e.g. `FEED-NIVABUPA-20260816-01`).
- **Refresh Frequency:** Daily automated sync at 00:00 IST.
- **Authoritative Notice:** Sourced directly from published insurer/TPA network lists (*Niva Bupa, Star Health, ICICI Lombard, Medi Assist*).

### 4.2 IRDAI Authoritative Disclosure
Final cashless network participation and claim settlement is subject solely to direct confirmation by your insurer/TPA at the time of hospital admission. CareCover Copilot is an independent navigation tool and is NOT officially affiliated with or endorsed by IRDAI.
