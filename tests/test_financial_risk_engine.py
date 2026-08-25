import pytest
from src.financial_risk_engine import calculate_financial_risk

def test_financial_risk_calculation():
    result = calculate_financial_risk(
        procedure_name="Joint Replacement Surgery",
        estimated_bill=480000.0,
        base_sum_insured=300000.0,
        super_topup_sum_insured=1500000.0,
        super_topup_deductible=300000.0,
        room_category="Single Private Room",
        co_pay_percent=0.0
    )

    assert result["hospital_bill"] == 480000.0
    assert result["primary_base_payout"] == 150000.0  # Joint cap 1,50,000
    assert result["estimated_out_of_pocket"] > 0
    assert "topup_status" in result
    assert "deductions_breakdown" in result

def test_financial_risk_cataract_sublimit():
    result = calculate_financial_risk(
        procedure_name="Cataract Surgery",
        estimated_bill=80000.0,
        base_sum_insured=500000.0,
        super_topup_sum_insured=1500000.0,
        super_topup_deductible=300000.0,
        room_category="Single Private Room",
        co_pay_percent=0.0
    )

    assert result["hospital_bill"] == 80000.0
    assert result["primary_base_payout"] <= 40000.0  # Cataract cap 40,000
