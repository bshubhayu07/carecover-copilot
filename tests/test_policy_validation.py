import pytest
from src.policy_extractor import validate_is_policy_document, extract_policy_profile

def test_non_policy_document_rejected():
    non_policy_text = "This is a computer science assignment on data structures and algorithms. Problem 1: Implement a binary search tree."
    is_valid, err_msg = validate_is_policy_document(non_policy_text)
    assert is_valid is False
    assert "not contain health insurance policy clauses" in err_msg

def test_real_policy_document_accepted():
    policy_text = "Niva Bupa Health Companion Policy Contract. Base Sum Insured is Rs 500000. Inpatient hospitalization room rent covered for Single Private Room without room capping."
    is_valid, err_msg = validate_is_policy_document(policy_text)
    assert is_valid is True
    assert err_msg == ""

    profile = extract_policy_profile(policy_text)
    assert "Niva Bupa" in profile.insurer_name
    assert profile.sum_insured_inr == 500000
