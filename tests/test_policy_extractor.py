from src.policy_extractor import extract_policy_profile
import os
from src.config import USE_DUMMY_MODE

def test_extractor_dummy_mode():
    if USE_DUMMY_MODE:
        profile = extract_policy_profile("dummy text")
        assert profile.insurer_name == "DemoCare"
        assert profile.sum_insured_inr == 500000
