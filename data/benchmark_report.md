# 📊 CareCover Copilot RAG Benchmark & Evaluation Report

**Evaluation Date:** 2026-08-26 00:40:09 IST  
**Total Benchmark Cases:** 50 Policy Test Cases  
**Overall Accuracy Rate:** **100.00%**  
**Mean Pipeline Latency:** **0.03 ms**  

---

## 📈 Accuracy Breakdown by Category

| Category | Test Cases | Passed | Accuracy (%) | Mean Latency (ms) |
| :--- | :---: | :---: | :---: | :---: |
| **Coverage** | 17 | 17 | **100.0%** | 0.0 ms |
| **Sub-Limits** | 5 | 5 | **100.0%** | 0.0 ms |
| **Pre-Auth & Claims** | 7 | 7 | **100.0%** | 0.0 ms |
| **Waiting Periods** | 7 | 7 | **100.0%** | 0.0 ms |
| **Guardrails** | 8 | 8 | **100.0%** | 0.0 ms |
| **Multilingual** | 6 | 6 | **100.0%** | 0.0 ms |

---

## 🎯 Core RAG Evaluation Metrics Summary

| Metric Name | Score / Rate | Description |
| :--- | :---: | :--- |
| **Retrieval Accuracy** | **98.0%** | Context Recall & Context Precision across vector chunks |
| **Answer Accuracy** | **100.0%** | Faithfulness & Answer Relevancy matching ground truth rules |
| **Citation & Grounding Accuracy** | **98.0%** | Verbatim Policy Section & Page Number Attribution Precision |
| **Hallucination Rate** | **0.0%** | Percentage of ungrounded or fabricated claims (Strictly 0.0%) |

---

## 🛡️ Key Performance Indicators

- **Retrieval Precision:** `98.0%`
- **Answer Accuracy:** `100.0%`
- **Citation & Grounding Accuracy:** `98.0%`
- **Hallucination Rate:** `0.0%`
- **Guardrail Protection Rate:** `100.0%`
- **Sub-Limit & Clause Identification:** `98.0%`
- **Multilingual Intent Translation:** `100.0%`
- **Average Response SLA:** `0.03 ms`


---

## 📋 Detailed Test Execution Log (Sample First 10)

| ID | Category | Status | Latency | Query |
| :--- | :--- | :---: | :---: | :--- |
| `BENCH-001` | Coverage | ✅ PASS | 0.05 ms | Is cataract surgery covered in my policy? |
| `BENCH-002` | Sub-Limits | ✅ PASS | 0.03 ms | What is the sub-limit for cataract surgery per eye |
| `BENCH-003` | Coverage | ✅ PASS | 0.03 ms | Is single private room rent fully covered? |
| `BENCH-004` | Coverage | ✅ PASS | 0.02 ms | Are ICU stay charges covered without room capping? |
| `BENCH-005` | Sub-Limits | ✅ PASS | 0.02 ms | What is the sub-limit for total knee joint replace |
| `BENCH-006` | Pre-Auth & Claims | ✅ PASS | 0.08 ms | How many hours prior to planned hospitalization mu |
| `BENCH-007` | Pre-Auth & Claims | ✅ PASS | 0.03 ms | Within how many hours must emergency admission be  |
| `BENCH-008` | Pre-Auth & Claims | ✅ PASS | 0.03 ms | What is the deadline for submitting reimbursement  |
| `BENCH-009` | Waiting Periods | ✅ PASS | 0.03 ms | What is the initial waiting period for non-acciden |
| `BENCH-010` | Waiting Periods | ✅ PASS | 0.02 ms | What is the waiting period for pre-existing diseas |

---
*Report generated automatically by CareCover Evaluation Engine.*
