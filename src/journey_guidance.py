from typing import Dict, Any, List

def get_journey_timeline() -> List[Dict[str, Any]]:
    """
    Returns the care journey stages with informational, non-medical checklists.
    """
    return [
        {
            "stage": "Admission",
            "description": "Preparation and arrival at the hospital.",
            "checklist": [
                "Carry Govt ID (Aadhaar/PAN) of patient and policyholder.",
                "Carry physical or digital copy of the Insurance Cashless Card.",
                "Submit Pre-authorization request at the insurance desk if planned.",
                "Ensure chosen room matches policy eligibility (e.g., Twin-Sharing) to avoid extra charges.",
                "Pay the mandatory admission deposit (usually refunded if cashless is approved)."
            ]
        },
        {
            "stage": "Investigation & Treatment",
            "description": "During your stay at the hospital.",
            "checklist": [
                "Save all pharmacy and consumable bills. Non-medical items (gloves, masks) are often excluded from coverage.",
                "If upgrading your room mid-stay, note that doctor and surgery fees may increase proportionately.",
                "Keep the insurance desk informed of any changes to the planned procedure."
            ]
        },
        {
            "stage": "Discharge & Claim",
            "description": "Leaving the hospital and settling bills.",
            "checklist": [
                "The hospital will send the final bill to the TPA. Approval takes 2-6 hours.",
                "Check the final approval letter for deductions (co-pay, non-medical items).",
                "Pay the deductible/co-pay amount directly to the hospital.",
                "Collect original Discharge Summary, Final Itemized Bill, and Reports.",
                "If reimbursement mode: Submit all originals to the insurer within 15-30 days."
            ]
        }
    ]
