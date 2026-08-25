import re

def check_medical_advice_query(query: str) -> bool:
    """
    Checks if the user is asking for medical advice, diagnosis, or treatment.
    Returns True if the query looks like a medical question.
    """
    medical_keywords = [
        "diagnose", "symptom", "pain", "cure", "treatment for", "should I take",
        "medicine", "dose", "prescription", "fever", "cancer", "surgery for",
        "what disease", "is this normal"
    ]
    query_lower = query.lower()
    for kw in medical_keywords:
        if kw in query_lower:
            if "cover" not in query_lower and "policy" not in query_lower:
                return True
    return False

def get_guardrail_response() -> str:
    return "I am an insurance navigation assistant and cannot provide medical advice, diagnosis, or treatment recommendations. Please consult a qualified healthcare professional or a doctor for your symptoms."

def validate_query_safety(query: str) -> tuple[bool, str]:
    q_lower = query.lower()
    
    # Prompt injection & security guardrails
    injection_keywords = [
        "ignore previous", "system prompt", "print secret", "api key",
        "select * from", "eval(", "os.system", "unrestricted assistant",
        "drop table", "<script>"
    ]
    if any(kw in q_lower for kw in injection_keywords):
        return False, "Security Violation: Query contains prohibited system override or security injection patterns."

    if check_medical_advice_query(query):
        return False, get_guardrail_response()
        
    return True, ""

def apply_response_guardrails(response_text: str) -> str:
    # Only append insurance disclaimer if response is about policy coverage terms or claims
    policy_keywords = ["covered", "sub-limit", "claim", "deductible", "room rent", "pre-authorization", "waiting period", "co-pay", "sum insured"]
    if any(kw in response_text.lower() for kw in policy_keywords):
        disclaimer = "\n\nNotice: Please confirm final eligibility and authorization with the insurer and hospital."
        if "confirm final eligibility" not in response_text.lower():
            return response_text + disclaimer
    return response_text
