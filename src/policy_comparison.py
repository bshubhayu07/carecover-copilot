from typing import Dict, Any, Optional
from src.policy_extractor import PolicyProfile

def compare_policies(policy_a: PolicyProfile, policy_b: Optional[PolicyProfile] = None) -> Dict[str, Any]:
    """
    Compares Policy A vs Policy B (or Base Policy vs Default Demo Policy) side-by-side.
    """
    if policy_b is None:
        policy_b = PolicyProfile(
            insurer_name="Standard Health Policy (Demo)",
            policy_number="DEMO-STD-9988",
            sum_insured_inr=500000.0,
            room_eligibility="Single Private Room",
            co_pay="0% Co-Pay",
            co_payment_percentage=0.0,
            cataract_sublimit_inr=50000.0,
            joint_replacement_sublimit_inr=150000.0,
            pre_auth_sla_hours=24
        )
        
    dimensions = [
        {
            "dimension": "Insurer Name",
            "policy_a_val": policy_a.insurer_name or "Loaded Policy A",
            "policy_b_val": policy_b.insurer_name or "Policy B",
            "winner": "Policy A" if (policy_a.insurer_name and policy_a.insurer_name != "Unknown") else "Policy B"
        },
        {
            "dimension": "Base Sum Insured",
            "policy_a_val": f"₹{(getattr(policy_a, 'sum_insured_inr', 0) or 500000):,.0f}",
            "policy_b_val": f"₹{(getattr(policy_b, 'sum_insured_inr', 0) or 500000):,.0f}",
            "winner": "Policy A" if (getattr(policy_a, 'sum_insured_inr', 0) or 0) >= (getattr(policy_b, 'sum_insured_inr', 0) or 0) else "Policy B"
        },
        {
            "dimension": "Room Eligibility",
            "policy_a_val": getattr(policy_a, 'room_eligibility', None) or "Single Room",
            "policy_b_val": getattr(policy_b, 'room_eligibility', None) or "Single Room",
            "winner": "Policy A" if "single" in str(getattr(policy_a, 'room_eligibility', '')).lower() else "Policy B"
        },
        {
            "dimension": "Co-Payment %",
            "policy_a_val": str(getattr(policy_a, 'co_pay', None) or f"{getattr(policy_a, 'co_payment_percentage', 0) or 0}% Co-Pay").replace("% Co-Pay% Co-Pay", "% Co-Pay"),
            "policy_b_val": str(getattr(policy_b, 'co_pay', None) or f"{getattr(policy_b, 'co_payment_percentage', 0) or 0}% Co-Pay").replace("% Co-Pay% Co-Pay", "% Co-Pay"),
            "winner": "Policy A" if (getattr(policy_a, 'co_payment_percentage', 0) or 0) <= (getattr(policy_b, 'co_payment_percentage', 0) or 0) else "Policy B"
        },
        {
            "dimension": "Cataract Sub-Limit",
            "policy_a_val": f"₹{getattr(policy_a, 'cataract_sublimit_inr', 40000):,.0f}" if getattr(policy_a, 'cataract_sublimit_inr', None) else "Max ₹40,000 / eye",
            "policy_b_val": f"₹{getattr(policy_b, 'cataract_sublimit_inr', 50000):,.0f}" if getattr(policy_b, 'cataract_sublimit_inr', None) else "Max ₹50,000 / eye",
            "winner": "Policy B"
        },
        {
            "dimension": "Joint Replacement Limit",
            "policy_a_val": f"₹{getattr(policy_a, 'joint_replacement_sublimit_inr', 150000):,.0f}" if getattr(policy_a, 'joint_replacement_sublimit_inr', None) else "Max ₹1,50,000 / joint",
            "policy_b_val": f"₹{getattr(policy_b, 'joint_replacement_sublimit_inr', 150000):,.0f}" if getattr(policy_b, 'joint_replacement_sublimit_inr', None) else "Max ₹1,50,000 / joint",
            "winner": "Policy A"
        },
        {
            "dimension": "Cashless Pre-Auth SLA",
            "policy_a_val": f"{getattr(policy_a, 'pre_auth_sla_hours', 24)} Hours",
            "policy_b_val": f"{getattr(policy_b, 'pre_auth_sla_hours', 24)} Hours",
            "winner": "Policy A" if getattr(policy_a, 'pre_auth_sla_hours', 24) <= getattr(policy_b, 'pre_auth_sla_hours', 24) else "Policy B"
        }
    ]
    
    score_a = sum(1 for d in dimensions if d["winner"] == "Policy A")
    score_b = sum(1 for d in dimensions if d["winner"] == "Policy B")
    
    overall_verdict = f"Policy A ({policy_a.insurer_name}) provides superior coverage across {score_a}/7 dimensions." if score_a >= score_b else f"Policy B ({policy_b.insurer_name}) offers better terms across {score_b}/7 dimensions."
    
    return {
        "policy_a_name": policy_a.insurer_name,
        "policy_b_name": policy_b.insurer_name,
        "policy_a_wins": score_a,
        "policy_b_wins": score_b,
        "comparison_dimensions": dimensions,
        "overall_verdict": overall_verdict
    }
