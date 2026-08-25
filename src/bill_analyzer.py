from typing import List, Dict, Any, Optional

STANDARD_NON_PAYABLE_CONSUMABLES = [
    "gloves", "ppe kit", "mask", "sanitizer", "thermometer", "syringes",
    "cotton", "gauge", "bed sheet", "registration fee", "admission charge",
    "admin fee", "dietitian fee", "patient gown", "tissue paper", "apron"
]

def analyze_hospital_bill(
    bill_items: List[Dict[str, Any]],
    room_category: str = "Single Private Room",
    base_sum_insured: float = 300000.0,
    co_pay_percent: float = 0.0
) -> Dict[str, Any]:
    """
    Parses itemized hospital bill line items and categorizes expenses into Covered Medical Claims
    vs Non-Payable Consumables, room rent capping penalties, and net payable amounts.
    """
    total_bill_amount = 0.0
    covered_medical_amount = 0.0
    non_payable_consumables_amount = 0.0
    
    analyzed_items = []
    
    for item in bill_items:
        name = str(item.get("description", item.get("name", "Medical Expense"))).strip()
        amount = float(item.get("amount", 0.0))
        total_bill_amount += amount
        
        name_lower = name.lower()
        is_non_payable = any(keyword in name_lower for keyword in STANDARD_NON_PAYABLE_CONSUMABLES)
        
        if is_non_payable:
            non_payable_consumables_amount += amount
            analyzed_items.append({
                "description": name,
                "amount": round(amount, 2),
                "status": "Non-Payable Consumable",
                "reason": "Standard non-medical administrative/disposable item excluded under IRDAI guidelines."
            })
        else:
            covered_medical_amount += amount
            analyzed_items.append({
                "description": name,
                "amount": round(amount, 2),
                "status": "Covered Medical Expense",
                "reason": "Eligible active medical treatment charge."
            })
    
    # Calculate room rent capping penalty
    room_rent_penalty_percent = 0.0
    if "deluxe" in room_category.lower() or "suite" in room_category.lower():
        room_rent_penalty_percent = 0.15  # 15% proportional deduction penalty
    
    room_penalty_deduction = round(covered_medical_amount * room_rent_penalty_percent, 2)
    payable_after_room_penalty = max(0.0, covered_medical_amount - room_penalty_deduction)
    
    co_pay_deduction = round(payable_after_room_penalty * (co_pay_percent / 100.0), 2)
    net_claim_payable = round(max(0.0, payable_after_room_penalty - co_pay_deduction), 2)
    
    if base_sum_insured > 0:
        approved_insurance_payout = min(net_claim_payable, base_sum_insured)
    else:
        approved_insurance_payout = 0.0
        
    estimated_out_of_pocket = round(total_bill_amount - approved_insurance_payout, 2)
    
    return {
        "total_bill_amount": round(total_bill_amount, 2),
        "covered_medical_amount": round(covered_medical_amount, 2),
        "non_payable_consumables_amount": round(non_payable_consumables_amount, 2),
        "room_rent_penalty_deduction": room_penalty_deduction,
        "co_pay_deduction": co_pay_deduction,
        "net_claim_payable": net_claim_payable,
        "approved_insurance_payout": approved_insurance_payout,
        "estimated_out_of_pocket": estimated_out_of_pocket,
        "itemized_line_items": analyzed_items,
        "deduction_summary": [
            f"Non-Medical Consumables: ₹{non_payable_consumables_amount:,.2f}",
            f"Room Rent Penalty ({int(room_rent_penalty_percent*100)}%): ₹{room_penalty_deduction:,.2f}",
            f"Co-Pay ({co_pay_percent}%): ₹{co_pay_deduction:,.2f}"
        ]
    }
