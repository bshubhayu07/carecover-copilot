from typing import Dict, Any

def calculate_out_of_pocket_estimate(
    total_bill: float,
    non_medical_items: float,
    allowed_room_rate: float,
    chosen_room_rate: float,
    copay_pct: float
) -> Dict[str, Any]:
    """
    Calculates out-of-pocket claim estimates and room rent proportional deduction penalties.
    """
    if chosen_room_rate > allowed_room_rate and allowed_room_rate > 0:
        prop_ratio = allowed_room_rate / float(chosen_room_rate)
        prop_penalty_pct = round((1.0 - prop_ratio) * 100, 1)
    else:
        prop_ratio = 1.0
        prop_penalty_pct = 0.0

    associated_fees = max(0.0, total_bill - non_medical_items) * 0.70
    approved_assoc_fees = associated_fees * prop_ratio
    prop_deduction_loss = associated_fees - approved_assoc_fees

    eligible_base = max(0.0, total_bill - non_medical_items - prop_deduction_loss)
    copay_amount = eligible_base * (copay_pct / 100.0)
    estimated_cashless = max(0.0, eligible_base - copay_amount)
    estimated_out_of_pocket = total_bill - estimated_cashless

    return {
        "total_bill": total_bill,
        "non_medical_items": non_medical_items,
        "proportional_penalty_pct": prop_penalty_pct,
        "proportional_deduction_loss": round(prop_deduction_loss, 2),
        "copay_amount": round(copay_amount, 2),
        "estimated_cashless": round(estimated_cashless, 2),
        "estimated_out_of_pocket": round(estimated_out_of_pocket, 2)
    }
