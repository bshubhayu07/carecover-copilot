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
            # Add some heuristic to differentiate policy check from medical check
            # "Does policy cover cancer" is OK. "I have cancer what to do" is not.
            if "cover" not in query_lower and "policy" not in query_lower:
                return True
    return False

def get_guardrail_response() -> str:
    return "I am an insurance navigation assistant and cannot provide medical advice, diagnosis, or treatment recommendations. Please consult a qualified healthcare professional or a doctor for your symptoms."
