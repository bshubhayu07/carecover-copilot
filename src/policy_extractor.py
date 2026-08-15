import json
from langchain_openai import ChatOpenAI
from typing import Dict, Any
from pydantic import ValidationError
from .policy_schema import PolicyProfile
from .config import USE_DUMMY_MODE

def extract_policy_profile(text_chunks: str) -> PolicyProfile:
    """
    Uses an LLM with structured output to extract the policy profile from the given text chunks.
    In dummy mode, returns a hardcoded parsed profile for the demo PDF.
    """
    if USE_DUMMY_MODE:
        # Fallback dummy logic if no OpenAI key
        return PolicyProfile(
            insurer_name="DemoCare",
            policy_name="Comprehensive Health Insurance",
            sum_insured_inr=500000,
            room_eligibility="General, Twin Sharing",
            room_rent_limit="1% for Normal (max 5000), 2% for ICU (max 10000)",
            co_pay="10% flat, 20% for age > 60",
            waiting_periods=[
                "30 days initial waiting period",
                "24 months for Cataract, Hernia, Joint Replacements",
                "48 months for Pre-existing diseases"
            ],
            exclusions=[
                "Maternity expenses",
                "Cosmetic surgeries",
                "Alcohol/drug abuse",
                "OPD expenses not leading to hospitalization"
            ],
            pre_authorization_required=True,
            network_hospital_terms="Cashless only at Network Hospitals. 10% deduction at non-network.",
            claim_documents=[
                "Duly filled claim form",
                "Original hospital discharge summary",
                "Original itemized bills and receipts",
                "Consultation notes and diagnostic reports",
                "KYC and canceled cheque"
            ],
            evidence=[
                {"field": "sum_insured_inr", "page": 1, "quote": "base Sum Insured is INR 5,00,000"}
            ]
        )

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    structured_llm = llm.with_structured_output(PolicyProfile)
    
    prompt = f"""
    You are an expert insurance analyst. Extract the policy details from the following text and fill out the structured format.
    If a detail is missing, leave it empty or null.
    Never invent numbers, coverage terms, or restrictions.
    For each extracted main field, provide exact quotes in the 'evidence' list with the page number if known.
    
    --- Document Text ---
    {text_chunks}
    """
    
    try:
        profile = structured_llm.invoke(prompt)
        return profile
    except ValidationError as e:
        print(f"Validation Error during extraction: {e}")
        # Fallback to empty if it fails completely
        return PolicyProfile()
    except Exception as e:
        print(f"LLM Error: {e}")
        return PolicyProfile()
