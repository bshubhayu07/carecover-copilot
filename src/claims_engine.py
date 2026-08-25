from typing import Dict, Any, List

MANDATORY_CLAIM_DOCUMENTS = {
    "Cashless Pre-Auth": [
        {"name": "Pre-Authorization Request Form (Filled & Signed)", "required": True},
        {"name": "Health Card / Policy Copy", "required": True},
        {"name": "Patient Aadhaar Card / Govt ID Proof", "required": True},
        {"name": "Treating Doctor Consultation Slip & Prescription", "required": True},
        {"name": "Diagnostic Reports (MRI, CT, Blood Tests)", "required": True}
    ],
    "Reimbursement Claim": [
        {"name": "Original Claim Form (Part A & Part B)", "required": True},
        {"name": "Original Discharge Summary", "required": True},
        {"name": "Original Hospital Itemized Final Bill", "required": True},
        {"name": "Original Payment Receipts & Paid Stamp Slips", "required": True},
        {"name": "Pharmacy Bills with Batch Numbers & Prescriptions", "required": True},
        {"name": "Cancelled Cheque for NEFT Direct Bank Transfer", "required": True}
    ]
}

def get_claim_guidance(claim_type: str = "Cashless Pre-Auth", procedure_name: str = "Cataract Surgery") -> Dict[str, Any]:
    """
    Returns complete step-by-step guidance for Pre-Hospitalization, Claim Submission, Checklist, and Post-Hospitalization.
    """
    docs = MANDATORY_CLAIM_DOCUMENTS.get(claim_type, MANDATORY_CLAIM_DOCUMENTS["Cashless Pre-Auth"])
    
    pre_hosp_steps = [
        "1. Intimate Insurer/TPA at least 48 hours prior to planned admission (or within 24 hours for emergency).",
        "2. Obtain itemized pre-admission cost estimate from hospital billing desk.",
        "3. Ensure doctor consultation slip contains registration number and date within 30 days.",
        "4. Confirm hospital cashless network status and TPA desk working hours."
    ]
    
    post_hosp_steps = [
        "1. Collect original signed discharge summary and itemized final bill upon discharge.",
        "2. Preserve all post-hospitalization bills (consultations, diagnostics, medicines) up to 60 days post-discharge.",
        "3. Submit post-hospitalization reimbursement claim within 30 days of treatment completion.",
        "4. Keep TPA claim reference number saved for status tracking."
    ]
    
    status_tracker_stages = [
        {"stage": 1, "title": "Claim Intimated / Submitted", "status": "Completed"},
        {"stage": 2, "title": "TPA Verification & Query Review", "status": "Active"},
        {"stage": 3, "title": "Pre-Auth / Claim Approval", "status": "Pending"},
        {"stage": 4, "title": "Direct Bank NEFT Settlement", "status": "Pending"}
    ]
    
    return {
        "claim_type": claim_type,
        "procedure_name": procedure_name,
        "pre_hospitalization_checklist": pre_hosp_steps,
        "mandatory_documents": docs,
        "post_hospitalization_guidance": post_hosp_steps,
        "claim_status_stages": status_tracker_stages
    }

def detect_missing_documents(submitted_doc_names: List[str], claim_type: str = "Reimbursement Claim") -> Dict[str, Any]:
    """
    Identifies which mandatory documents are missing from the user's claim file.
    """
    required_docs = MANDATORY_CLAIM_DOCUMENTS.get(claim_type, MANDATORY_CLAIM_DOCUMENTS["Reimbursement Claim"])
    submitted_set = {doc.lower().strip() for doc in submitted_doc_names}
    
    missing = []
    present = []
    
    for req in required_docs:
        req_name = req["name"]
        if any(keyword in submitted_set for keyword in req_name.lower().split()):
            present.append(req_name)
        else:
            missing.append(req_name)
            
    is_complete = len(missing) == 0
    
    return {
        "claim_type": claim_type,
        "total_required_count": len(required_docs),
        "submitted_count": len(present),
        "missing_count": len(missing),
        "is_claim_ready": is_complete,
        "present_documents": present,
        "missing_documents": missing,
        "warning_message": "All required documents must be submitted to prevent TPA claim rejection or delays." if not is_complete else "All required documents present!"
    }
