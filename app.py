import sys
import os
import json
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
if "checked_items" not in st.session_state:
    st.session_state.checked_items = {}

# --- Sidebar ---
with st.sidebar:
    st.title("🏥 CareCover Copilot")
    st.caption("Clinical & insurance decision-support navigation tool.")
    
    if USE_DUMMY_MODE:
        st.warning("⚠️ Running in Demo Mode (No OpenAI Key). Using pre-configured mock data.")
    else:
        st.success("✅ OpenAI Key detected. Running live model.")
        
    st.markdown("---")
    st.markdown("""
    **Important Disclaimer:**
    For informational support only. Not medical advice, a diagnosis, or a guarantee of insurance coverage.
    """)

# --- Main App --- 4 Tabs Only ---
tab1, tab2, tab3, tab4 = st.tabs([
    "📂 Upload & Extract", 
    "💬 Ask Your Policy", 
    "🏥 Find Hospital Options", 
    "🛤️ Care Journey & Safety"
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
        st.markdown("---")
        st.markdown("### Extracted Policy Summary")
        profile = st.session_state.policy_profile
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Insurer Name", profile.insurer_name or "N/A")
            st.metric("Room Eligibility", profile.room_eligibility or "N/A")
        with c2:
            st.metric("Policy Name", profile.policy_name or "N/A")
            st.metric("Co-Pay Terms", profile.co_pay or "N/A")
        with c3:
            st.metric("Sum Insured (INR)", f"₹{profile.sum_insured_inr:,.0f}" if profile.sum_insured_inr else "N/A")
            st.metric("Pre-Auth Required", "Yes" if profile.pre_authorization_required else "No")
            
        if profile.evidence:
            with st.expander("🔍 View Policy Text Evidence & Quotes"):
                for ev in profile.evidence:
                    st.info(f"**Field**: `{ev.field}` | **Page {ev.page}**: \"_{ev.quote}_\"")
                    
        # Interactive Download Feature
        profile_json = json.dumps(profile.model_dump(), indent=2)
        st.download_button(
            label="📥 Download Extracted Policy Profile (JSON)",
            data=profile_json,
            file_name="carecover_policy_profile.json",
            mime="application/json"
        )

# TAB 2: Ask Your Policy
with tab2:
    st.header("Ask Questions About Your Coverage")
    st.info("💡 **Suggested Questions:**\n- Is a private room covered?\n- Is pre-authorization required for emergency admission?\n- What exclusions should I check before procedure?\n- What documents are needed for reimbursement claims?")
    
    query = st.text_input("Enter your policy question:")
    if st.button("Ask Assistant"):
        if not st.session_state.collection:
            st.warning("Please upload a policy first in the 'Upload & Extract' tab.")
        elif check_medical_advice_query(query):
            st.error(get_guardrail_response())
        else:
            with st.spinner("Analyzing policy clauses..."):
                answer = ask_policy_question(query, st.session_state.collection, st.session_state.policy_profile)
                st.success(answer)

# TAB 3: Find Hospital Options (Interactive Filters Added)
with tab3:
    st.header("Hospital Network & Room Matching")
    st.write("Match your policy constraints against our directory across major Indian metropolitan cities.")
    
    col_city, col_spec, col_search = st.columns([1, 1, 1])
    
    with col_city:
        available_cities = get_all_cities()
        city = st.selectbox("Select City", available_cities)
    with col_spec:
        specialty_filter = st.selectbox("Filter Specialty", ["All Specialties", "Cardiology", "Oncology", "Orthopedics", "Neurology", "Pediatrics", "Gastroenterology"])
    with col_search:
        search_query = st.text_input("Search Hospital Name", "")
        
    c_net, c_emerg = st.columns(2)
    with c_net:
        in_network_only = st.checkbox("Show In-Network Only", value=False)
    with c_emerg:
        emergency_only = st.checkbox("Show Emergency Available Only", value=False)
        
    profile_to_use = st.session_state.policy_profile
    if not profile_to_use:
        st.info("ℹ️ Using default DemoCare policy parameters. (Upload a custom policy in 'Upload & Extract' for personalized matching!)")
        profile_to_use = PolicyProfile(
            insurer_name="DemoCare",
            room_eligibility="General, Twin Sharing",
            pre_authorization_required=True
        )
        
    df = get_hospitals_by_city(city)
    if df.empty:
        st.error(f"No hospitals found for '{city}' in directory.")
    else:
        # Apply interactive filters
        matches = match_hospitals(df, profile_to_use, city)
        
        filtered_matches = []
        for m in matches:
            if in_network_only and m['network_status'] != "In Network":
                continue
            if specialty_filter != "All Specialties" and specialty_filter.lower() not in m['specialties'].lower():
                continue
            if search_query and search_query.lower() not in m['name'].lower():
                continue
            filtered_matches.append(m)
            
        st.subheader(f"Found {len(filtered_matches)} hospitals matching filters in {city}")
        
        for m in filtered_matches:
            with st.container():
                st.markdown(f"### 🏥 {m['name']}")
                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    status_color = "green" if m['network_status'] == "In Network" else "red"
                    st.markdown(f"**Network Status:** :{status_color}[{m['network_status']}]")
                    st.markdown(f"**Eligible Room:** {m['eligible_room']}")
                with col2:
                    st.markdown(f"**Specialties:** {m['specialties']}")
                    st.markdown(f"**Approx. Distance:** {m['distance']} km")
                with col3:
                    st.metric("Match Score", f"{m['score']} pts")
                    
                st.info(f"💡 **Matching Explanation:** {m['explanation']}")
                st.warning(f"⚠️ **Notice:** {m['caveat']}")
                st.markdown("---")

# TAB 4: Care Journey & Safety (Combined Tab + Interactive Tools)
with tab4:
    st.header("🛤️ Care Journey, Claim Estimator & Safety Guidelines")
    st.caption("Combined guidance timeline, out-of-pocket calculator, patient checklist, and medical disclaimers.")
    
    subtab1, subtab2, subtab3 = st.tabs([
        "📊 Out-of-Pocket Claim Estimator",
        "📋 Interactive Patient Checklist",
        "🛡️ Safety Disclaimers & Data Privacy"
    ])
    
    # SUBTAB 1: Interactive Claim Estimator
    with subtab1:
        st.subheader("💰 Interactive Out-of-Pocket Estimator")
        st.write("Estimate your personal cost sharing based on expected hospital bills and policy rules.")
        
        col_bill, col_copay = st.columns(2)
        with col_bill:
            total_bill = st.number_input("Estimated Hospital Bill (INR)", min_value=10000, max_value=2000000, value=150000, step=10000)
        with col_copay:
            copay_pct = st.slider("Co-Pay Percentage (%)", min_value=0, max_value=30, value=10)
            
        non_medical_items = st.number_input("Non-Medical Items / Consumables (INR)", min_value=0, max_value=100000, value=5000, step=1000)
        
        copay_amount = (total_bill - non_medical_items) * (copay_pct / 100.0)
        estimated_cashless = max(0.0, total_bill - non_medical_items - copay_amount)
        estimated_out_of_pocket = total_bill - estimated_cashless
        
        st.markdown("#### Cost Breakdown Estimate:")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Estimated Approved Cashless", f"₹{estimated_cashless:,.0f}")
        with m2:
            st.metric("Co-Pay Share", f"₹{copay_amount:,.0f}")
        with m3:
            st.metric("Estimated Out-of-Pocket Cost", f"₹{estimated_out_of_pocket:,.0f}", delta=f"-₹{estimated_out_of_pocket:,.0f}", delta_color="inverse")
            
        st.caption("Note: This is an indicative estimation model for decision support only. Final settlement is decided solely by your insurer/TPA.")
        
    # SUBTAB 2: Interactive Patient Checklist
    with subtab2:
        st.subheader("📋 Step-by-Step Admission & Claims Checklist")
        st.write("Check off items as you prepare for hospitalization to track your readiness.")
        
        timeline = get_journey_timeline()
        total_tasks = sum(len(stage['checklist']) for stage in timeline)
        
        checked_count = 0
        for stage_idx, stage in enumerate(timeline):
            st.markdown(f"#### {stage['icon']} Stage {stage_idx+1}: {stage['stage']}")
            st.write(stage['description'])
            
            for item_idx, item in enumerate(stage['checklist']):
                key = f"task_{stage_idx}_{item_idx}"
                is_checked = st.checkbox(item, key=key)
                if is_checked:
                    checked_count += 1
            st.markdown("---")
            
        # Live Progress Bar
        progress_pct = int((checked_count / total_tasks) * 100) if total_tasks > 0 else 0
        st.markdown(f"### Overall Readiness Progress: {progress_pct}%")
        st.progress(progress_pct / 100.0)
        
    # SUBTAB 3: Safety & Limitations
    with subtab3:
        st.subheader("🛡️ Safety Disclaimers & Data Privacy Statement")
        st.warning("""
        ### ⚠️ Important Clinical & Insurance Disclaimer
        This application is a **decision-support information tool only**. 
        - It **does not** provide medical advice, diagnose health conditions, or recommend clinical treatments.
        - It **does not** guarantee insurance coverage, pre-authorization, or claim settlement.
        - Always consult a qualified medical professional for health concerns and verify policy terms directly with your insurer.
        """)
        
        st.info("""
        ### 🔒 Data Privacy & synthetic Demo Rules
        - **No Real Health Data:** Do not upload real patient data, credentials, or proprietary policy files.
        - **Local Processing:** All vector stores and extraction run locally or via secured API keys.
        - **Synthetic Hospital Directory:** Hospital options and indicative cost bands are generated for demonstration purposes.
        """)
