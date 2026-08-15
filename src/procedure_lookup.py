from typing import Dict, Any

PROCEDURE_DATABASE = {
    "Cataract Surgery": {
        "sub_limit": "INR 40,000 per eye (max INR 80,000 total)",
        "waiting_period": "24 months specific illness waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["Ophthalmologist Consultation Note", "A-Scan Biometry Report", "Lens Invoice Sticker"],
        "guidance": "Cataract is classified as a Day Care procedure. Ensure lens brand invoice is preserved for claim approval."
    },
    "Total Knee Replacement": {
        "sub_limit": "Capped at INR 2,50,000 per knee or room limit baseline",
        "waiting_period": "24 to 48 months pre-existing / specific disease clause",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["X-Ray Weight Bearing View Report", "Orthopedic Surgeon Recommendation", "Implant Serial Sticker"],
        "guidance": "Inpatient admission required (min 48 hours). Verify implant cost capping rules with TPA."
    },
    "Angioplasty / Stenting": {
        "sub_limit": "Up to Base Sum Insured (Stent cost capped as per NPPA guidelines)",
        "waiting_period": "30 days initial, 36 months if pre-existing cardiac history",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Coronary Angiography (CAG) Report", "Cardiologist Referral", "Stent Barcode & Invoice"],
        "guidance": "Emergency pre-authorization permitted within 24 hours of hospital admission."
    },
    "Maternity / Normal & C-Section": {
        "sub_limit": "INR 50,000 for Normal Delivery, INR 75,000 for C-Section",
        "waiting_period": "24 to 36 months continuous coverage",
        "day_care_eligible": False,
        "pre_auth_required": True,
        "documents": ["Obstetrician ANC Notes", "USG Scan Reports", "Discharge Summary & Birth Certificate"],
        "guidance": "Check if newborn baby cover is included from Day 1 or after 90 days."
    },
    "Appendectomy / Gallbladder Surgery": {
        "sub_limit": "Up to Base Sum Insured",
        "waiting_period": "30 days initial waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["USG Abdomen / CT Scan Report", "Surgeon OT Notes", "Histopathology Report"],
        "guidance": "Laparoscopic procedures are fully covered under day care or inpatient benefit."
    },
    "Dialysis / Chemotherapy": {
        "sub_limit": "Covered under Day Care Procedures (Subject to annual sum insured)",
        "waiting_period": "30 days initial waiting period",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["Oncologist / Nephrologist Treatment Plan", "Chemo / Dialysis Cycle Sheets", "Pharmacy Bills"],
        "guidance": "Day care procedures do not require 24-hour hospitalization."
    }
}

def get_procedure_details(procedure_name: str) -> Dict[str, Any]:
    return PROCEDURE_DATABASE.get(procedure_name, {
        "sub_limit": "As per base policy sum insured",
        "waiting_period": "30 days initial, 24 months specific illness",
        "day_care_eligible": True,
        "pre_auth_required": True,
        "documents": ["Consultation Note", "Diagnostic Test Report", "Itemized Final Bill"],
        "guidance": "Verify pre-authorization requirements with hospital TPA desk."
    })
