from typing import Dict, Any

DOCUMENT_KEYWORDS = {
    "Health Insurance Policy": ["policy schedule", "sum insured", "insurer", "premium", "coverage", "uic", "policyholder"],
    "Hospital Itemized Bill": ["invoice", "tax invoice", "final bill", "receipt", "particulars", "total amount", "room charges", "ot charges"],
    "Doctor Prescription": ["rx", "diagnosis", "doctor", "medicine", "dosage", "tablets", "consultation", "dr."],
    "Hospital Discharge Summary": ["discharge summary", "date of admission", "date of discharge", "clinical history", "treatment given", "condition at discharge"],
    "Cashless Pre-Auth Claim Form": ["pre-authorization request", "tpa", "cashless claim", "network hospital", "claim form"]
}

def classify_document(text_content: str, filename: str = "") -> Dict[str, Any]:
    """
    Automatically classifies an uploaded document into 1 of 5 healthcare document types.
    """
    text_lower = (text_content + " " + filename).lower()
    
    scores = {}
    for doc_type, keywords in DOCUMENT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        scores[doc_type] = score
        
    best_doc_type = max(scores, key=scores.get)
    confidence = min(98, 60 + scores[best_doc_type] * 10) if scores[best_doc_type] > 0 else 55
    
    return {
        "filename": filename,
        "classified_document_type": best_doc_type if scores[best_doc_type] > 0 else "Health Insurance Policy",
        "confidence_score_percent": confidence,
        "detected_type_label": f"{best_doc_type if scores[best_doc_type] > 0 else 'Health Insurance Policy'} ({confidence}% Confidence)",
        "detected_features": [kw for kw in DOCUMENT_KEYWORDS.get(best_doc_type, []) if kw in text_lower]
    }
