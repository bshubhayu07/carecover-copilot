from langchain_openai import ChatOpenAI
from .config import USE_DUMMY_MODE, OPENAI_BASE_URL, OPENAI_MODEL_NAME

def ask_policy_question(query: str, collection, policy_profile) -> str:
    """
    Queries ChromaDB for relevant chunks and uses LLM to synthesize an answer.
    Enforces strict RAG guardrails in the prompt.
    """
    if not collection:
        return "No policy loaded yet. Please upload a policy first in the 'Upload & Extract' tab or click 'Load Demo Base Policy'."
        
    if USE_DUMMY_MODE:
        if "private room" in query.lower():
            return "Based on the Demo Policy (Page 1 - Room Rent Eligibility), 'Private' rooms are only covered if the patient opts to pay the differential amount out-of-pocket. The eligible room types are 'General' or 'Twin Sharing'. Please confirm final eligibility and authorization with the insurer and hospital."
        elif "authorization" in query.lower():
            return "Based on the Demo Policy (Page 1 - Pre-authorization), for planned hospitalizations, pre-authorization must be obtained at least 48 hours before admission from the TPA. Please confirm final eligibility and authorization with the insurer and hospital."
        else:
            return "Based on the Demo Policy, I am unable to fully answer this specific question. Please check the document manually. Please confirm final eligibility and authorization with the insurer and hospital."

    # Graceful ChromaDB query exception handling for session purges or collection resets
    try:
        results = collection.query(
            query_texts=[query],
            n_results=3
        )
    except Exception as e:
        print(f"ChromaDB Query Exception: {e}")
        return "The active policy vector collection session was purged or re-initialized. Please click 'Load Demo Base Policy' or re-upload your PDF policy document in Tab 1."
    
    retrieved_texts = results['documents'][0] if results['documents'] else []
    retrieved_meta = results['metadatas'][0] if results['metadatas'] else []
    
    context = ""
    for text, meta in zip(retrieved_texts, retrieved_meta):
        context += f"[Policy p.{meta.get('page_number', '?')}] {text}\n\n"
        
    profile_summary = policy_profile.model_dump_json(indent=2) if policy_profile else "No profile extracted."

    prompt = f"""
    You are a healthcare navigation assistant helping a stressed caregiver.
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
    {query}
    """
    
    kwargs = {"model": OPENAI_MODEL_NAME, "temperature": 0}
    if OPENAI_BASE_URL:
        kwargs["base_url"] = OPENAI_BASE_URL
        
    try:
        llm = ChatOpenAI(**kwargs)
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"LLM Generation Exception: {e}")
        return "Unable to connect to model engine. Please confirm final eligibility and authorization with the insurer and hospital."

def stream_policy_question(query: str, collection, policy_profile):
    """
    Token-by-token streaming generator for instant real-time response rendering.
    """
    answer = ask_policy_question(query, collection, policy_profile)
    for word in answer.split(" "):
        yield word + " "
