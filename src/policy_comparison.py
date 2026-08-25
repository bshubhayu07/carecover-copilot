from typing import Dict, Any, Optional
from src/policy_extractor import PolicyProfile

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
            "policy_a_val": f"₹{policy_a.sum_insured_inr:,.0f}",
            "policy_b_val": f"₹{policy_b.sum_insured_inr:,.0f}",
            "winner": "Policy A" if policy_a.sum_insured_inr >= policy_b.sum_insured_inr else "Policy B"
        },
        {
            "dimension": "Room Eligibility",
            "policy_a_val": policy_a.room_eligibility or "No Limit",
            "policy_b_val": policy_b.room_eligibility or "No Limit",
            "winner": "Policy A" if "single" in (policy_a.room_eligibility or "").lower() or "no capping" in (policy_a.room_eligibility or "").lower() else "Policy B"
        },
        {
            "dimension": "Co-Payment %",
            "policy_a_val": f"{policy_a.co_payment_percentage}% Co-Pay",
            "policy_b_val": f"{policy_b.co_payment_percentage}% Co-Pay",
            "winner": "Policy A" if policy_a.co_payment_percentage <= policy_b.co_payment_percentage else "Policy B"
        },
        {
            "dimension": "Cataract Sub-Limit",
            "policy_a_val": f"₹{policy_a.cataract_sublimit_inr:,.0f}" if policy_a.cataract_sublimit_inr else "No Sub-limit",
            "policy_b_val": f"₹{policy_b.cataract_sublimit_inr:,.0f}" if policy_b.cataract_sublimit_inr else "No Sub-limit",
            "winner": "Policy A" if not policy_a.cataract_sublimit_inr else ("Policy B" if not policy_b.cataract_sublimit_inr else "Policy A")
        },
        {
            "dimension": "Joint Replacement Limit",
            "policy_a_val": f"₹{policy_a.joint_replacement_sublimit_inr:,.0f}" if policy_a.joint_replacement_sublimit_inr else "No Sub-limit",
            "policy_b_val": f"₹{policy_b.joint_replacement_sublimit_inr:,.0f}" if policy_b.joint_replacement_sublimit_inr else "No Sub-limit",
            "winner": "Policy A" if not policy_a.joint_replacement_sublimit_inr else "Policy B"
        },
        {
            "dimension": "Cashless Pre-Auth SLA",
            "policy_a_val": f"{policy_a.pre_auth_sla_hours} Hours",
            "policy_b_val": f"{policy_b.pre_auth_sla_hours} Hours",
            "winner": "Policy A" if policy_a.pre_auth_sla_hours <= policy_b.pre_auth_sla_hours else "Policy B"
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
