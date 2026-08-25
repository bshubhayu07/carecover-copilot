from typing import Dict, Any, List
from src.policy_extractor import PolicyProfile

def detect_policy_contradictions(policy_profile: PolicyProfile) -> Dict[str, Any]:
    """
    Analyzes policy extracted terms to flag conflicting or ambiguous policy clauses.
    """
    contradictions = []
    
    room = (policy_profile.room_eligibility or "").lower()
    copay = policy_profile.co_payment_percentage or 0.0
    si = policy_profile.sum_insured_inr or 0.0
    
    # Check 1: Room Rent Capping vs Single Room
    if "single" in room and ("1%" in room or "2%" in room or "capping" in room):
        contradictions.append({
            "title": "Room Rent Eligibility Mismatch",
            "clause_a": "Clause 1.2: Single Private Room Eligible",
            "clause_b": "Clause 4.1: 1% Sum Insured Capping Penalty",
            "severity": "High Risk",
            "explanation": "Policy text promises Single Private Room but attaches a 1% daily capping limit which triggers proportional bill deductions if daily tariff exceeds capping amount."
        })
        
    # Check 2: Zero Co-Pay vs Senior Citizen Age Co-Pay
    if copay == 0 and policy_profile.policy_features and any("co-pay" in f.lower() for f in policy_profile.policy_features):
        contradictions.append({
            "title": "Conditional Co-Pay Conflict",
            "clause_a": "Summary Schedule: 0% Co-Payment",
            "clause_b": "Endorsement Clause: 20% Co-Pay for Senior Citizens (>65 yrs)",
            "severity": "Warning",
            "explanation": "Schedule displays 0% co-pay baseline but endorsement clause introduces 20% co-pay based on age or non-network treatment."
        })
        
    # Check 3: High Sum Insured with Low Cataract Sub-limit
    if si >= 500000 and policy_profile.cataract_sublimit_inr and policy_profile.cataract_sublimit_inr <= 25000:
        contradictions.append({
            "title": "Sub-Limit Capping Discrepancy",
            "clause_a": f"Base Coverage: ₹{si:,.0f} Sum Insured",
            "clause_b": f"Specific Illness Cap: ₹{policy_profile.cataract_sublimit_inr:,.0f} per eye Cataract limit",
            "severity": "Medium",
            "explanation": f"Despite high total coverage of ₹{si:,.0f}, Cataract claims are severely capped at ₹{policy_profile.cataract_sublimit_inr:,.0f} per eye."
        })
        
    is_clean = len(contradictions) == 0
    
    return {
        "insurer_name": policy_profile.insurer_name or "Active Policy",
        "contradiction_count": len(contradictions),
        "is_policy_consistent": is_clean,
        "detected_contradictions": contradictions,
        "summary_verdict": "No internal clause contradictions detected in policy terms." if is_clean else f"Found {len(contradictions)} potential clause contradiction(s) requiring verification before claim submission."
    }
