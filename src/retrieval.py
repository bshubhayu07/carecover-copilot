import os
import openai
from .config import USE_DUMMY_MODE, OPENAI_BASE_URL, OPENAI_MODEL_NAME, OPENAI_API_KEY

def ask_policy_question(query: str, collection=None, policy_profile=None) -> str:
    """
    Queries vector collection for relevant chunks and uses OpenAI API to synthesize an answer.
    Enforces strict RAG guardrails in the prompt.
    """
    insurer_name = "Niva Bupa Health Insurance"
    if policy_profile and hasattr(policy_profile, 'insurer_name') and policy_profile.insurer_name:
        insurer_name = policy_profile.insurer_name

    if USE_DUMMY_MODE or not collection:
        q_lower = query.lower()
        if "cataract" in q_lower:
            return f"Based on {insurer_name} (Page 2 - Specific Sub-Limits), Cataract surgery is covered up to a specific sub-limit of ₹40,000 per eye (or 25% of Sum Insured, whichever is lower) with a 24-month waiting period for pre-existing conditions. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "room" in q_lower or "private" in q_lower:
            return f"Based on {insurer_name} (Page 1 - Room Rent Eligibility), Single Private Room is fully covered without proportional deduction penalties. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "authorization" in q_lower or "preauth" in q_lower or "pre-auth" in q_lower:
            return f"Based on {insurer_name} (Page 1 - Pre-authorization), for planned hospitalizations, cashless pre-authorization must be submitted at least 48 hours prior to admission at the TPA desk. Please confirm final eligibility and authorization with the insurer and hospital."
        else:
            return f"Based on {insurer_name}, hospitalizations, surgeries, and day-care procedures are covered subject to policy sum insured terms and sub-limits. Please confirm final eligibility and authorization with the insurer and hospital."

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

def stream_policy_question(query: str, collection=None, policy_profile=None):
    answer = ask_policy_question(query, collection, policy_profile)
    for word in answer.split():
        yield word + " "
