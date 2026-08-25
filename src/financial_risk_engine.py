from typing import Dict, Any, Optional

def calculate_financial_risk(
    procedure_name: str,
    estimated_bill: float,
    base_sum_insured: float = 500000.0,
    super_topup_sum_insured: float = 1500000.0,
    super_topup_deductible: float = 300000.0,
    room_category: str = "Single Private Room",
    co_pay_percent: float = 0.0,
    is_network_hospital: bool = True
) -> Dict[str, Any]:
    """
    Calculates detailed financial risk, expected primary insurance payout, super top-up trigger,
    non-payable consumables, proportional room rent deductions, and final out-of-pocket expenses.
    """
    proc_clean = procedure_name.lower().strip()
    
    # 1. Determine sub-limits based on procedure
    sublimit_cap: Optional[float] = None
    sublimit_applied_name = None

    if "cataract" in proc_clean or "eye" in proc_clean:
        sublimit_cap = 40000.0
        sublimit_applied_name = "Cataract Surgery Sub-Limit (₹40,000 per eye)"
    elif "joint" in proc_clean or "knee" in proc_clean or "hip" in proc_clean:
        sublimit_cap = 150000.0
        sublimit_applied_name = "Joint Replacement Sub-Limit (₹1,50,000 per joint)"
    elif "stent" in proc_clean or "cardiac" in proc_clean:
        sublimit_cap = 250000.0
        sublimit_applied_name = "Cardiac Stent Sub-Limit (₹2,50,000 per stent)"

    # 2. Non-payable non-medical items (gloves, PPE, admin fee) ~ 6% of bill
    non_payable_consumables = round(estimated_bill * 0.06, 2)
    payable_medical_bill = estimated_bill - non_payable_consumables

    # 3. Room rent proportional deduction penalty
    room_penalty_deduction = 0.0
    if "suite" in room_category.lower() or "deluxe" in room_category.lower():
        room_penalty_deduction = round(payable_medical_bill * 0.15, 2)
        payable_medical_bill -= room_penalty_deduction

    # 4. Procedure sub-limit cap check
    sublimit_deduction = 0.0
    if sublimit_cap and payable_medical_bill > sublimit_cap:
        sublimit_deduction = payable_medical_bill - sublimit_cap
        payable_claim_amount = sublimit_cap
    else:
        payable_claim_amount = payable_medical_bill

    # 5. Co-pay calculation
    co_pay_amount = round(payable_claim_amount * (co_pay_percent / 100.0), 2)
    net_eligible_claim = payable_claim_amount - co_pay_amount

    # 6. Primary Base Policy Payout
    if base_sum_insured > 0:
        primary_base_payout = min(net_eligible_claim, base_sum_insured)
    else:
        primary_base_payout = 0.0

    remaining_unpaid_claim = max(0.0, net_eligible_claim - primary_base_payout)

    # 7. Super Top-Up Trigger & Payout
    topup_triggered = False
    super_topup_payout = 0.0
    
    # Super top-up triggers when total claim exceeds deductible
    if super_topup_sum_insured > 0 and net_eligible_claim > super_topup_deductible and remaining_unpaid_claim > 0:
        topup_triggered = True
        super_topup_payout = min(remaining_unpaid_claim, super_topup_sum_insured)

    # 8. Total Out-of-Pocket Expense
    if base_sum_insured == 0 and super_topup_sum_insured == 0:
        primary_base_payout = 0.0
        super_topup_payout = 0.0
        total_insurance_payout = 0.0
        estimated_out_of_pocket = round(estimated_bill, 2)
    else:
        total_insurance_payout = primary_base_payout + super_topup_payout
        estimated_out_of_pocket = round(estimated_bill - total_insurance_payout, 2)

    return {
        "hospital_bill": round(estimated_bill, 2),
        "primary_base_payout": round(primary_base_payout, 2),
        "super_topup_payout": round(super_topup_payout, 2),
        "total_insurance_contribution": round(total_insurance_payout, 2),
        "estimated_out_of_pocket": max(0.0, estimated_out_of_pocket),
        "topup_triggered": topup_triggered,
        "topup_status": "Active & Triggered" if topup_triggered else "Not Triggered (Deductible not met)",
        "deductions_breakdown": {
            "non_payable_consumables": non_payable_consumables,
            "room_penalty_deduction": room_penalty_deduction,
            "sublimit_deduction": sublimit_deduction,
            "sublimit_name": sublimit_applied_name,
            "co_pay_amount": co_pay_amount
        }
    }
