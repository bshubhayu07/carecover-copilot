import sys
import os
import streamlit as st
import streamlit.components.v1 as components

# Ensure project root is in Python path for Streamlit Cloud & local execution
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(
    page_title="CareCover Copilot - Enterprise Navigation System", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit header, footer, padding, and menu bars
st.markdown("""
<style>
#MainMenu {visibility: hidden !important;}
footer {visibility: hidden !important;}
header {visibility: hidden !important;}
.stDeployButton {display: none !important;}
div[data-testid="stDecoration"] {display: none !important;}
div[data-testid="stStatusWidget"] {display: none !important;}
.viewerBadge_container__1QS-Z {display: none !important;}
div[data-testid="stToolbar"] {display: none !important;}
div[data-testid="stHeader"] {display: none !important;}
button[title="View app in Streamlit Cloud"] {display: none !important;}
a[href*="streamlit.io"] {display: none !important;}
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 0rem !important;
    padding-right: 0rem !important;
    max-width: 100% !important;
}
iframe {
    width: 100% !important;
    border: none !important;
}
</style>
""", unsafe_allow_html=True)

# Render the React web application full-screen inside Streamlit Cloud
LIVE_APP_URL = "https://bshubhayu07.github.io/carecover-copilot/"

components.iframe(LIVE_APP_URL, height=950, scrolling=True)
