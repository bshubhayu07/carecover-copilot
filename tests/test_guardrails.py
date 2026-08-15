from src.guardrails import check_medical_advice_query

def test_medical_advice_detection():
    # Should flag
    assert check_medical_advice_query("How do I cure my cancer?") == True
    assert check_medical_advice_query("What dose of medicine should I take?") == True
    
    # Should pass (not medical advice, just policy checking)
    assert check_medical_advice_query("Does my policy cover cancer treatment?") == False
    assert check_medical_advice_query("Is a private room covered?") == False
