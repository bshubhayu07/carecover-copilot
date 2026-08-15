import json
from langchain_openai import ChatOpenAI
from typing import Dict, Any
from pydantic import ValidationError
from fpdf import FPDF
from .policy_schema import PolicyProfile
from .config import USE_DUMMY_MODE, OPENAI_BASE_URL

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

    kwargs = {"model": OPENAI_MODEL_NAME, "temperature": 0}
    if OPENAI_BASE_URL:
        kwargs["base_url"] = OPENAI_BASE_URL
        
    llm = ChatOpenAI(**kwargs)
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
        return PolicyProfile()
    except Exception as e:
        print(f"LLM Error: {e}")
        return PolicyProfile()

def generate_policy_pdf(profile: PolicyProfile) -> bytes:
    """Generates a PDF byte stream of the extracted policy profile."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(0, 10, text="CareCover Copilot - Extracted Policy Summary", new_x="LMARGIN", new_y="NEXT", align='C')
    pdf.ln(6)
    
    fields = [
        ("Insurer Name", profile.insurer_name or "N/A"),
        ("Policy Name", profile.policy_name or "N/A"),
        ("Sum Insured", f"INR {profile.sum_insured_inr:,.0f}" if profile.sum_insured_inr else "N/A"),
        ("Room Eligibility", profile.room_eligibility or "N/A"),
        ("Room Rent Limit", profile.room_rent_limit or "N/A"),
        ("Co-Pay Terms", profile.co_pay or "N/A"),
        ("Pre-Authorization Required", "Yes" if profile.pre_authorization_required else "No"),
        ("Network Hospital Terms", profile.network_hospital_terms or "N/A")
    ]
    
    for label, val in fields:
        pdf.set_font("Helvetica", 'B', 11)
        pdf.cell(65, 8, text=f"{label}:")
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(0, 8, text=str(val))
        pdf.ln(1)
        
    if profile.waiting_periods:
        pdf.ln(4)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, text="Waiting Periods:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=10)
        for wp in profile.waiting_periods:
            pdf.multi_cell(0, 6, text=f"- {wp}")
            
    if profile.exclusions:
        pdf.ln(4)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, text="Exclusions:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=10)
        for ex in profile.exclusions:
            pdf.multi_cell(0, 6, text=f"- {ex}")
            
    if profile.claim_documents:
        pdf.ln(4)
        pdf.set_font("Helvetica", 'B', 12)
        pdf.cell(0, 8, text="Required Claim Documents:", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", size=10)
        for doc in profile.claim_documents:
            pdf.multi_cell(0, 6, text=f"- {doc}")
            
    return bytes(pdf.output())
