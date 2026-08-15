import sys
import os
import streamlit as st

# Ensure project root is in Python path for Streamlit Cloud & local execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import USE_DUMMY_MODE, CHROMA_DB_DIR
from src.pdf_ingestion import ingest_pdf
from src.chunking import chunk_text
from src.embeddings import initialize_vector_store
from src.policy_extractor import extract_policy_profile
from src.retrieval import ask_policy_question
from src.guardrails import check_medical_advice_query, get_guardrail_response
from src.hospital_repository import get_hospitals_by_city, get_all_cities
from src.eligibility_engine import match_hospitals
from src.journey_guidance import get_journey_timeline
from src.policy_schema import PolicyProfile

st.set_page_config(page_title="CareCover Copilot", page_icon="🏥", layout="wide")

# Session state initialization
if "policy_profile" not in st.session_state:
    st.session_state.policy_profile = None
if "collection" not in st.session_state:
    st.session_state.collection = None
if "raw_text" not in st.session_state:
    st.session_state.raw_text = ""

# --- Sidebar ---
with st.sidebar:
    st.title("🏥 CareCover Copilot")
    st.caption("Clinical and insurance decision-support information tool.")
    
    if USE_DUMMY_MODE:
        st.warning("⚠️ Running in Demo Mode (No OpenAI Key). Using pre-configured mock data.")
    else:
        st.success("✅ OpenAI Key detected. Running live model.")
        
    st.markdown("---")
    st.markdown("""
    **Important Disclaimer:**
    For informational support only. Not medical advice, a diagnosis, or a guarantee of insurance coverage.
    """)

# --- Main App ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📂 Upload & Extract", 
    "💬 Ask Your Policy", 
    "🏥 Find Hospital Options", 
    "🛤️ Care Journey", 
    "🛡️ Safety & Limitations"
])

# TAB 1: Upload & Extract
with tab1:
    st.header("Upload Policy Document")
    uploaded_file = st.file_uploader("Upload your Health Insurance Policy (PDF)", type=["pdf"])
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Load Demo Policy"):
            if os.path.exists("data/demo_policy.pdf"):
                with st.spinner("Processing demo policy..."):
                    pages = ingest_pdf("data/demo_policy.pdf")
                    st.session_state.raw_text = " ".join([p["text"] for p in pages])
                    chunks = chunk_text(pages)
                    st.session_state.collection = initialize_vector_store(chunks, CHROMA_DB_DIR, USE_DUMMY_MODE)
                    st.session_state.policy_profile = extract_policy_profile(st.session_state.raw_text)
                    st.success("Demo Policy Loaded & Extracted!")
            else:
                st.error("Demo policy not found. Run generate_demo_pdf.py first.")
                
    with col2:
        if uploaded_file is not None:
            if st.button("Process Uploaded Policy"):
                # Save temporarily
                temp_path = f"data/temp_{uploaded_file.name}"
                os.makedirs("data", exist_ok=True)
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                    
                with st.spinner("Processing policy..."):
                    pages = ingest_pdf(temp_path)
                    st.session_state.raw_text = " ".join([p["text"] for p in pages])
                    chunks = chunk_text(pages)
                    st.session_state.collection = initialize_vector_store(chunks, CHROMA_DB_DIR, USE_DUMMY_MODE)
                    st.session_state.policy_profile = extract_policy_profile(st.session_state.raw_text)
                    st.success("Policy Extracted Successfully!")
                    
                os.remove(temp_path)
                
    if st.session_state.policy_profile:
        st.markdown("### Extracted Policy Profile")
        profile = st.session_state.policy_profile
        
        st.write(f"**Insurer**: {profile.insurer_name}")
        st.write(f"**Policy Name**: {profile.policy_name}")
        st.write(f"**Room Eligibility**: {profile.room_eligibility}")
        st.write(f"**Co-Pay Terms**: {profile.co_pay}")
        st.write(f"**Pre-Auth Required**: {'Yes' if profile.pre_authorization_required else 'No'}")
        
        if profile.evidence:
            with st.expander("View Evidence (Citations from Document)"):
                for ev in profile.evidence:
                    st.info(f"Field: {ev.field} | Page {ev.page}: '{ev.quote}'")

# TAB 2: Ask Your Policy
with tab2:
    st.header("Ask Questions About Your Coverage")
    st.info("💡 Example: Is a private room covered? / Is pre-authorization required?")
    
    query = st.text_input("Enter your question here:")
    if st.button("Ask"):
        if not st.session_state.collection:
            st.warning("Please upload a policy first in the 'Upload & Extract' tab.")
        elif check_medical_advice_query(query):
            st.error(get_guardrail_response())
        else:
            with st.spinner("Searching policy..."):
                answer = ask_policy_question(query, st.session_state.collection, st.session_state.policy_profile)
                st.success(answer)

# TAB 3: Find Hospital Options
with tab3:
    st.header("Hospital Network Matching")
    st.write("Match your policy constraints against our directory across major Indian metropolitan cities.")
    
    available_cities = get_all_cities()
    city = st.selectbox("Select City", available_cities)
    
    if st.button("Find Matching Hospitals"):
        profile_to_use = st.session_state.policy_profile
        if not profile_to_use:
            st.info("ℹ️ Showing hospital directory using default DemoCare policy parameters. (Load a custom policy in 'Upload & Extract' for personalized policy matching!)")
            profile_to_use = PolicyProfile(
                insurer_name="DemoCare",
                room_eligibility="General, Twin Sharing",
                pre_authorization_required=True
            )
            
        df = get_hospitals_by_city(city)
        if df.empty:
            st.error(f"No hospitals found for '{city}' in directory.")
        else:
            matches = match_hospitals(df, profile_to_use, city)
            st.subheader(f"Found {len(matches)} hospitals in {city}")
            for m in matches:
                with st.container():
                    st.markdown(f"### {m['name']}")
                    col1, col2 = st.columns(2)
                    with col1:
                        status_color = "green" if m['network_status'] == "In Network" else "red"
                        st.markdown(f"**Network Status:** :{status_color}[{m['network_status']}]")
                        st.markdown(f"**Eligible Room:** {m['eligible_room']}")
                    with col2:
                        st.markdown(f"**Specialties:** {m['specialties']}")
                        st.markdown(f"**Match Score:** {m['score']}")
                    
                    st.info(f"**Why this match?** {m['explanation']}")
                    st.warning(f"**Notice:** {m['caveat']}")
                    st.markdown("---")

# TAB 4: Care Journey
with tab4:
    st.header("Hospitalization Care Journey")
    st.write("Step-by-step guidance for admission and claims.")
    
    timeline = get_journey_timeline()
    for stage in timeline:
        st.subheader(f"{stage['icon']} {stage['stage']}")
        st.write(stage['description'])
        for item in stage['checklist']:
            st.markdown(f"- [ ] {item}")
        st.markdown("---")

# TAB 5: Safety & Limitations
with tab5:
    st.header("Safety & Limitations")
    st.markdown("""
    ### Important Disclaimer
    This application is built for **informational support only**. It is NOT medical advice, a diagnosis, or a guarantee of insurance coverage.
    
    ### Data Privacy
    - Do not upload real patient data, credentials, or proprietary insurance information.
    - This app processes data locally (or via OpenAI if configured).
    
    ### Limitations
    - The AI model may hallucinate or misinterpret ambiguous policy wording.
    - The deterministic matching engine is based on synthetic data and simplified rules.
    - Always verify final eligibility, room rates, and pre-authorization directly with your insurer and hospital desk.
    """)
