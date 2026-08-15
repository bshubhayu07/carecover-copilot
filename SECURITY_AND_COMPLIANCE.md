# CareCover Copilot - Security, Architecture & Compliance Audit Specification

## Executive Summary
CareCover Copilot is an independent clinical and health insurance decision-support navigation system. This document outlines the technical architecture, data privacy controls, security audit specifications, and regulatory compliance disclosures in accordance with the **Digital Personal Data Protection (DPDP) Act 2023** and **IRDAI Health Insurance Regulations 2024**.

---

## 1. Technical Architecture & Memory Lifecycle

### 1.1 Ephemeral Memory Model (Zero Persistent Storage)
- **Document Processing:** Uploaded health insurance policy PDFs are parsed exclusively in temporary RAM session buffers (`io.BytesIO`).
- **Vector Embeddings:** Document vector embeddings are initialized in session-isolated ChromaDB collections using local ONNX / MiniLM embeddings.
- **Disk Lifetime:** 0 hours. No raw PDF text or extracted policy summaries are written to permanent long-term databases.

### 1.2 Cryptographic Session Deletion Protocol
- **Trigger:** User clicks "Purge & Delete Session Data Now" in the sidebar.
- **Action:** Wipes Python `st.session_state` RAM memory references, purges ChromaDB vector collections, and unlinks temporary session files.
- **Audit Receipt:** Generates a SHA-256 Cryptographic Deletion Certificate (`DEL-CERT-[HASH]`) verifying zero bytes remain in active memory.

---

## 2. Regulatory Compliance & Disclaimers

### 2.1 IRDAI Non-Endorsement & Data Source Statement
- **Independent Navigation Tool:** CareCover Copilot is an independent software navigation tool. It is **NOT** affiliated with, sponsored by, or officially endorsed by the Insurance Regulatory and Development Authority of India (IRDAI).
- **Data Source Directories:** Hospital network listings are sourced directly from insurer/TPA published cashless directories (*Niva Bupa, Star Health, ICICI Lombard, Medi Assist*) pursuant to IRDAI Health Insurance Regulations 2024 (Master Circular on Health Insurance Products).

### 2.2 Medical & Insurance Advice Disclaimer
- **Non-Clinical:** CareCover Copilot does not provide medical diagnoses, treatment recommendations, or clinical advice.
- **Non-Binding:** Policy extractions and room rent calculations are indicative decision-support models. Final pre-authorization and claim settlements are decided solely by the respective insurer and Third-Party Administrator (TPA).

---

## 3. Data Privacy & DPDP Act 2023 Controls

| DPDP Requirement | Technical Implementation | Audit Status |
| :--- | :--- | :--- |
| **Explicit Consent (Sec 6)** | Mandatory consent checkbox prior to PDF file upload | Verified Active |
| **Right to Erasure (Sec 8)** | Cryptographic 1-click session data purge & deletion receipt | Verified Active |
| **Grievance Redressal (Sec 13)** | Designated Privacy Nodal Officer (`grievance@carecovercopilot.in`) | SLA: 72 hours |
| **In-Transit Encryption** | Mandatory TLS 1.3 / SSL encrypted transport | 256-bit AES |

---

## 4. AI Guardrails & RAG Evaluation Metrics

1. **Ground-Truth Citation Constraint:** Every RAG response is strictly bounded by retrieved policy clauses with explicit page citations (`[Policy p.X]`).
2. **Medical Query Guardrail:** Queries asking for medical diagnoses or drug prescriptions are intercepted by a deterministic safety classifier and redirected to emergency services (`112 / 108`).
3. **Auditable Traceability:** Every Q&A answer generates a unique trace hash (`RAG-TRACE-[MD5]`) for session verification.

---

## 5. Security & Incident Response SLA
- **Vulnerability Reporting:** Security researchers can report vulnerabilities to `security@carecovercopilot.in`.
- **Triage SLA:** Initial acknowledgement within 12 hours; resolution within 48 hours.
