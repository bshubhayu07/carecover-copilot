from typing import Dict, Any, List

def get_journey_timeline() -> List[Dict[str, Any]]:
    """
    Returns the complete 9-stage interactive Care Journey with policy requirements attached to each stage.
    """
    return [
        {
            "step": 1,
            "stage": "Diagnosis & Prescription",
            "icon": "🩺",
            "description": "Initial clinical diagnosis and specialist prescription.",
            "policy_requirement": "Doctor must issue itemized consultation slip and diagnostic test reports. OPD consultation fees are excluded unless day-care surgery is advised.",
            "checklist": [
                "Collect original prescription with doctor's registration number.",
                "Ensure diagnostic test reports (MRI, CT, Blood tests) are dated within 30 days.",
                "Verify if procedure requires pre-existing condition (PED) waiting period check."
            ]
        },
        {
            "step": 2,
            "stage": "Hospital Selection",
            "icon": "🏥",
            "description": "Choosing cashless network hospital and room category.",
            "policy_requirement": "Selected hospital must be in Insurer Cashless Network to avoid reimbursement delays. Room category must match policy eligibility (e.g. Single Private Room) to prevent proportional penalty deductions on doctor/surgery fees.",
            "checklist": [
                "Filter hospital by cashless network status and procedure specialty.",
                "Confirm room category eligibility (Single Private vs Twin Sharing).",
                "Check distance to hospital and emergency road ambulance cover limit (₹2,000)."
            ]
        },
        {
            "step": 3,
            "stage": "Insurance Verification",
            "icon": "🛡️",
            "description": "Verifying policy sum insured, active status, and waiting periods.",
            "policy_requirement": "Primary Base Policy Sum Insured balance must be sufficient. Super Top-Up deductible trigger threshold evaluated for secondary coverage.",
            "checklist": [
                "Verify active Sum Insured balance.",
                "Check procedure sub-limits (e.g. Cataract ₹40,000/eye, Joint Replacement ₹1,50,000/joint).",
                "Check if 24-month or 48-month waiting period for pre-existing diseases is complete."
            ]
        },
        {
            "step": 4,
            "stage": "Pre-Authorization (Pre-Auth)",
            "icon": "📝",
            "description": "TPA pre-authorization submission prior to admission.",
            "policy_requirement": "Planned admissions require cashless pre-auth submission at least 48 hours prior. Emergency admissions require intimation within 24 hours of admission.",
            "checklist": [
                "Submit Pre-Auth Request Form at hospital TPA/Insurance Desk.",
                "Attach doctor's advice note, diagnostic reports, and Health ID card.",
                "Track TPA initial approval SLA (Standard SLA: 2 to 4 hours)."
            ]
        },
        {
            "step": 5,
            "stage": "Hospital Admission",
            "icon": "🛏️",
            "description": "Patient check-in and initial admission deposit.",
            "policy_requirement": "Patient and policyholder ID verification mandatory. Hospital admission deposit is usually refunded upon receipt of TPA initial cashless letter.",
            "checklist": [
                "Carry original Govt Photo ID (Aadhaar/PAN) and Health Insurance ID card.",
                "Hand over initial TPA cashless pre-authorization approval letter.",
                "Pay refundable security deposit if required by hospital rules."
            ]
        },
        {
            "step": 6,
            "stage": "Inpatient Treatment",
            "icon": "💉",
            "description": "Surgical procedure, doctor visits, and inpatient care.",
            "policy_requirement": "Non-payable non-medical items (gloves, PPE kits, hygiene packs, food) are excluded from coverage (~5-8% of bill).",
            "checklist": [
                "Keep daily track of doctor consultation notes and pharmacy charges.",
                "Avoid room category upgrades mid-stay to prevent proportional deduction penalties.",
                "Intimate insurer immediately if treatment plan or surgery extends beyond initial pre-auth amount."
            ]
        },
        {
            "step": 7,
            "stage": "Discharge & Final Approval",
            "icon": "📄",
            "description": "Final bill submission to TPA and patient discharge.",
            "policy_requirement": "Hospital submits final itemized bill to TPA. Final cashless approval letter issued within 2 to 6 hours.",
            "checklist": [
                "Review final TPA approval letter for non-payable item deductions and co-pay %.",
                "Pay co-payment amount and non-medical items directly to hospital cashier.",
                "Collect original Discharge Summary, Final Itemized Bill, and Diagnostic Reports."
            ]
        },
        {
            "step": 8,
            "stage": "Claim Filing & Audit",
            "icon": "📋",
            "description": "Submitting reimbursement claim or post-hospitalization bills.",
            "policy_requirement": "Reimbursement claims must be submitted to insurer/TPA within 30 days of discharge (Post-hospitalization bills within 60 days).",
            "checklist": [
                "Fill and sign TPA Claim Form Part-A and Part-B.",
                "Attach original discharge summary, doctor prescriptions, and payment receipts.",
                "Keep digital scans of all submitted original documents for audit trail."
            ]
        },
        {
            "step": 9,
            "stage": "Reimbursement & Super Top-Up Trigger",
            "icon": "💰",
            "description": "Claim settlement and secondary Super Top-Up payout.",
            "policy_requirement": "If total claim exceeds primary base policy sum insured, Super Top-Up policy is activated once deductible threshold is crossed.",
            "checklist": [
                "Track claim settlement status via TPA portal / SMS updates.",
                "If claim exceeds base policy limit, submit primary claim settlement summary to Super Top-Up insurer.",
                "Verify final bank account credit via NEFT/IMPS."
            ]
        }
    ]
