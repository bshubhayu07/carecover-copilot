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
    if check_medical_advice_query(query):
        return False, get_guardrail_response()
    return True, ""

def apply_response_guardrails(response_text: str) -> str:
    disclaimer = "\n\nNotice: Please confirm final eligibility and authorization with the insurer and hospital."
    if "confirm final eligibility" not in response_text.lower():
        return response_text + disclaimer
    return response_text
