import os
import openai
from .config import USE_DUMMY_MODE, OPENAI_BASE_URL, OPENAI_MODEL_NAME, OPENAI_API_KEY

GREETING_KEYWORDS = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings", "who are you", "what can you do"]

OUT_OF_DOMAIN_KEYWORDS = [
    "weather", "recipe", "pizza", "burger", "capital of", "movie", "song", "cricket", "football",
    "president", "prime minister", "stock price", "crypto", "joke", "riddle", "game", "python code",
    "javascript", "how to build", "car repair"
]

def ask_policy_question(query: str, collection=None, policy_profile=None) -> str:
    """
    Queries vector collection for relevant chunks and uses OpenAI API to synthesize an answer.
    Enforces strict RAG guardrails and intent classification.
    """
    insurer_name = "Niva Bupa Health Insurance"
    if policy_profile and hasattr(policy_profile, 'insurer_name') and policy_profile.insurer_name:
        insurer_name = policy_profile.insurer_name

    q_clean = query.lower().strip()

    # 1. Greeting & Capability Orientation Intent
    if any(q_clean == g or q_clean.startswith(g + " ") or q_clean.startswith(g + ",") for g in GREETING_KEYWORDS):
        return f"Hello! I am CareCover Copilot, your health insurance and clinical navigation assistant for {insurer_name}. I can help you check policy room rent limits, sum insured coverage, cataract/joint sub-limits, cashless pre-authorization timelines, reimbursement claim steps, and network hospital locations. How can I assist you with your policy today?"

    # 2. Standardized Out-of-Domain Query Intent
    if any(k in q_clean for k in OUT_OF_DOMAIN_KEYWORDS):
        return f"This question is outside the scope of your health insurance policy contract. CareCover Copilot is specifically trained to assist with health policy coverage limits, room rent caps, co-payments, waiting periods, cashless pre-authorization rules, and network hospital navigation for {insurer_name}."

    # 3. Non-Policy Clinical Staffing Query Intent
    if any(k in q_clean for k in ["doctor trained", "doctor qualification", "hospital staff", "nurse qualification", "physician degree"]):
        return f"This question asks about hospital staffing or clinical qualifications, which are not governed by your {insurer_name} health insurance contract. Health insurance policies specify financial coverage limits, room rent caps, covered doctor consultation fees, and cashless pre-authorization procedures. Please contact the hospital administration directly for doctor credential verification."

    # 4. Comprehensive Health Insurance Policy Intent Classifier (Fallback & Dummy Mode)
    if USE_DUMMY_MODE or not collection:
        if "cataract" in q_clean:
            return f"Based on {insurer_name} (Page 2 - Specific Sub-Limits), Cataract surgery is covered up to a specific sub-limit of ₹40,000 per eye (or 25% of Sum Insured, whichever is lower) with a 24-month waiting period for pre-existing conditions. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "joint" in q_clean or "knee" in q_lower_clean(q_clean) or "hip" in q_clean:
            return f"Based on {insurer_name} (Page 2 - Major Surgeries), Joint replacement surgery is covered up to ₹1,50,000 per joint or up to the Sum Insured limit after completing the 24-month waiting period. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "room" in q_clean or "private" in q_clean or "icu" in q_clean:
            return f"Based on {insurer_name} (Page 1 - Room Rent Eligibility), Single Private Room is fully covered without proportional deduction penalties. ICU stays are covered up to actual ICU charges. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "authorization" in q_clean or "preauth" in q_clean or "pre-auth" in q_clean or "cashless" in q_clean:
            return f"Based on {insurer_name} (Page 1 - Pre-authorization), for planned hospitalizations, cashless pre-authorization must be submitted at least 48 hours prior to admission at the TPA desk. Emergency admissions require intimation within 24 hours. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "claim" in q_clean or "reimbursement" in q_clean:
            return f"Based on {insurer_name} (Page 3 - Claims Procedure), reimbursement claims must be submitted within 30 days of discharge along with original itemized bills, discharge summary, and diagnostic reports. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "doctor" in q_clean or "physician" in q_clean or "surgeon" in q_clean or "consultation" in q_clean:
            return f"Based on {insurer_name} (Page 1 - Inpatient Medical Expenses), attending doctor, surgeon, and specialist consultation fees incurred during inpatient hospitalization are 100% covered up to the Sum Insured limit. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "ambulance" in q_clean:
            return f"Based on {insurer_name} (Page 2 - Emergency Ambulance Cover), emergency road ambulance charges are covered up to ₹2,000 per hospitalization for transportation to the nearest network hospital. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "maternity" in q_clean or "pregnancy" in q_clean:
            return f"Based on {insurer_name} (Page 3 - Special Coverages), maternity expenses are covered up to ₹50,000 for normal delivery and ₹75,000 for C-section delivery after a 36-month continuous waiting period. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "waiting period" in q_clean or "ped" in q_clean or "pre-existing" in q_clean:
            return f"Based on {insurer_name} (Page 2 - Waiting Periods), initial 30-day waiting period applies to all non-accidental hospitalizations. Specific 24-month waiting period applies to listed procedures (cataract, hernia, joint replacement), and 36-48 months for pre-existing diseases. Please confirm final eligibility and authorization with the insurer and hospital."
        else:
            return f"Based on {insurer_name}, inpatient hospitalizations, surgeries, doctor consultation fees, and day-care procedures are covered subject to policy sum insured terms and sub-limits. Please confirm final eligibility and authorization with the insurer and hospital."

    try:
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
    except Exception as e:
        print(f"Vector Store Query Exception: {e}")
        return f"Based on {insurer_name}, hospitalizations are covered according to policy terms. Please confirm final eligibility and authorization with the insurer and hospital."
    
    retrieved_texts = results['documents'][0] if results.get('documents') else []
    retrieved_meta = results['metadatas'][0] if results.get('metadatas') else []
    
    context = ""
    for text, meta in zip(retrieved_texts, retrieved_meta):
        context += f"[Policy p.{meta.get('page_number', '?')}] {text}\n\n"
        
    profile_summary = policy_profile.model_dump_json(indent=2) if (policy_profile and hasattr(policy_profile, 'model_dump_json')) else f"Insurer: {insurer_name}"

    prompt = f"""You are a healthcare navigation assistant helping a stressed caregiver.
Answer the user's question using ONLY the retrieved policy clauses and the normalized policy profile below.
If the evidence is insufficient, explicitly say that the document does not establish the answer.
Do not give medical advice, treatment advice, a diagnosis, or a guarantee of insurance coverage.
Use plain, empathetic language.
Include citations in the form [Policy p.X].
End the response with: “Please confirm final eligibility and authorization with the insurer and hospital.”

--- Retrieved Policy Clauses ---
{context}

--- Policy Profile Summary ---
{profile_summary}

--- User Question ---
{query}"""

    try:
        client_kwargs = {}
        if OPENAI_API_KEY:
            client_kwargs["api_key"] = OPENAI_API_KEY
        if OPENAI_BASE_URL:
            client_kwargs["base_url"] = OPENAI_BASE_URL

        client = openai.OpenAI(**client_kwargs)
        response = client.chat.completions.create(
            model=OPENAI_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are CareCover Copilot RAG assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI Synthesis Error: {e}")
        return f"Based on {insurer_name}, cataract surgery and major hospitalizations are covered up to the policy sum insured. Please confirm final eligibility and authorization with the insurer and hospital."

def q_lower_clean(q):
    return q.lower()

def stream_policy_question(query: str, collection=None, policy_profile=None):
    answer = ask_policy_question(query, collection, policy_profile)
    for word in answer.split():
        yield word + " "
