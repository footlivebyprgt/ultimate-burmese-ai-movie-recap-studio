"""
Ultimate Burmese AI Movie Recap Studio - Main Application
Integrated application combining all 5 phases
"""

import streamlit as st
from streamlit_app_phase1 import render_phase1_ui
from streamlit_app_phase2 import render_phase2_ui
from streamlit_app_phase3 import render_phase3_ui
from streamlit_app_phase4 import render_phase4_ui
from streamlit_app_phase5 import render_phase5_ui

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="🎬 Ultimate Burmese AI Movie Recap Studio",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding-top: 2rem;
        }
        .stTabs [data-baseweb="tab-list"] button {
            font-size: 16px;
            font-weight: bold;
        }
        .phase-header {
            text-align: center;
            font-size: 2rem;
            font-weight: bold;
            color: #FF6B6B;
            margin-bottom: 1rem;
        }
        .phase-progress {
            background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%);
            height: 8px;
            border-radius: 4px;
            margin-bottom: 2rem;
        }
        .info-box {
            background-color: #E8F4F8;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #0084FF;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# INITIALIZE SESSION STATE
# ============================================================================

if "input_data" not in st.session_state:
    st.session_state.input_data = {
        "input_type": None,
        "video_file": None,
        "youtube_url": None,
        "script_file": None,
        "script_text": None,
        "video_metadata": None,
        "transcript": None,
        "generated_script": None,
        "voiceover_path": None,
        "voiceover_duration": None,
        "combined_video_path": None,
        "project_id": None,
        "project_name": None
    }

if "api_keys" not in st.session_state:
    st.session_state.api_keys = {
        "gemini_key": None,
        "openai_key": None
    }

if "current_phase" not in st.session_state:
    st.session_state.current_phase = 1

# ============================================================================
# SIDEBAR - NAVIGATION & SETTINGS
# ============================================================================

with st.sidebar:
    st.header("🎬 Ultimate Recap Studio")
    
    # Phase Navigation
    st.markdown("### 📍 Navigation")
    
    phase_options = {
        "Phase 1: Upload Content": 1,
        "Phase 2: Generate Script": 2,
        "Phase 3: Create Voiceover": 3,
        "Phase 4: Assemble Video": 4,
        "Phase 5: Deploy & Manage": 5
    }
    
    selected_phase = st.selectbox(
        "Go to Phase:",
        list(phase_options.keys()),
        index=st.session_state.current_phase - 1,
        key="phase_selector"
    )
    
    st.session_state.current_phase = phase_options[selected_phase]
    
    st.divider()
    
    # API Keys Configuration
    st.markdown("### 🔐 API Configuration")
    
    # Check for Streamlit Secrets
    secret_gemini = st.secrets.get("GEMINI_API_KEY", "")
    secret_openai = st.secrets.get("OPENAI_API_KEY", "")
    
    if secret_gemini:
        st.session_state.api_keys["gemini_key"] = secret_gemini
        st.success("✅ Gemini Key: Loaded")
    else:
        gemini_key = st.text_input(
            "Gemini API Key",
            type="password",
            help="Get from https://aistudio.google.com/app/apikey",
            key="gemini_input"
        )
        st.session_state.api_keys["gemini_key"] = gemini_key
    
    if secret_openai:
        st.session_state.api_keys["openai_key"] = secret_openai
        st.success("✅ OpenAI Key: Loaded")
    else:
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Get from https://platform.openai.com/api-keys",
            key="openai_input"
        )
        st.session_state.api_keys["openai_key"] = openai_key
    
    st.divider()
    
    # Project Status
    st.markdown("### 📊 Project Status")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.input_data.get("input_type"):
            st.success("✅ Input")
        else:
            st.warning("⚠️ Input")
    
    with col2:
        if st.session_state.input_data.get("generated_script"):
            st.success("✅ Script")
        else:
            st.warning("⚠️ Script")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.session_state.input_data.get("voiceover_path"):
            st.success("✅ Voiceover")
        else:
            st.warning("⚠️ Voiceover")
    
    with col2:
        if st.session_state.input_data.get("combined_video_path"):
            st.success("✅ Video")
        else:
            st.warning("⚠️ Video")
    
    st.divider()
    
    # Help & Info
    st.markdown("### ℹ️ Help & Info")
    
    if st.button("📖 Documentation", use_container_width=True):
        st.info("Documentation: Check the README.md file in the GitHub repository")
    
    if st.button("🐛 Report Issue", use_container_width=True):
        st.info("Report issues on GitHub: https://github.com/footlivebyprgt/ultimate-burmese-ai-movie-recap-studio/issues")
    
    st.divider()
    
    st.markdown("""
    **Version:** 1.0.0 (Beta)  
    **Made with ❤️ for Burmese creators**
    """)

# ============================================================================
# MAIN CONTENT - PHASE RENDERING
# ============================================================================

# Progress Bar
st.markdown(f"""
    <div style="width: {st.session_state.current_phase * 20}%; height: 8px; background: linear-gradient(90deg, #FF6B6B 0%, #4ECDC4 100%); border-radius: 4px; margin-bottom: 2rem;"></div>
""", unsafe_allow_html=True)

# Phase Header
st.markdown(f"""
    <div class="phase-header">
    🎬 Phase {st.session_state.current_phase}: {list(phase_options.keys())[st.session_state.current_phase - 1].split(": ")[1]}
    </div>
""", unsafe_allow_html=True)

# Render Current Phase
if st.session_state.current_phase == 1:
    render_phase1_ui()

elif st.session_state.current_phase == 2:
    render_phase2_ui()

elif st.session_state.current_phase == 3:
    render_phase3_ui()

elif st.session_state.current_phase == 4:
    render_phase4_ui()

elif st.session_state.current_phase == 5:
    render_phase5_ui()

# ============================================================================
# FOOTER
# ============================================================================

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    if st.session_state.current_phase > 1:
        if st.button("⬅️ Previous Phase", use_container_width=True):
            st.session_state.current_phase -= 1
            st.rerun()

with col2:
    st.markdown(f"**Phase {st.session_state.current_phase} of 5**")

with col3:
    if st.session_state.current_phase < 5:
        if st.button("Next Phase ➡️", use_container_width=True):
            st.session_state.current_phase += 1
            st.rerun()

st.markdown("""
---
**🎬 Ultimate Burmese AI Movie Recap Studio** v1.0  
Built with Streamlit, Google Gemini AI, and OpenAI Whisper  
[GitHub](https://github.com/footlivebyprgt) | [Support](https://github.com/footlivebyprgt/ultimate-burmese-ai-movie-recap-studio/issues)
""")
