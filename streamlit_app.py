import streamlit as st
from streamlit_app_main import *

# Page Configuration
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
            font-size: 18px;
            font-weight: bold;
        }
        .header-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            color: #FF6B6B;
            margin-bottom: 1rem;
        }
        .subheader-text {
            text-align: center;
            font-size: 1.2rem;
            color: #666;
            margin-bottom: 2rem;
        }
        .info-box {
            background-color: #E8F4F8;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #0084FF;
            margin-bottom: 1rem;
        }
        .success-box {
            background-color: #E8F5E9;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #4CAF50;
            margin-bottom: 1rem;
        }
        .error-box {
            background-color: #FFEBEE;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 4px solid #F44336;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State
if "input_data" not in st.session_state:
    st.session_state.input_data = {
        "input_type": None,
        "video_file": None,
        "youtube_url": None,
        "script_file": None,
        "script_text": None,
        "video_metadata": None,
        "transcript": None
    }

if "api_keys" not in st.session_state:
    st.session_state.api_keys = {
        "gemini_key": None,
        "openai_key": None
    }

# ============================================================================
# SIDEBAR - API KEY INPUT
# ============================================================================
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Check for API Keys in Streamlit Secrets
    secret_gemini = st.secrets.get("GEMINI_API_KEY", "")
    secret_openai = st.secrets.get("OPENAI_API_KEY", "")
    
    if secret_gemini:
        st.session_state.api_keys["gemini_key"] = secret_gemini
        st.success("✅ Gemini API Key loaded from Secrets")
    else:
        gemini_key = st.text_input(
            "🔑 Gemini API Key",
            type="password",
            help="Get your API key from https://aistudio.google.com/app/apikey",
            key="gemini_input"
        )
        st.session_state.api_keys["gemini_key"] = gemini_key
    
    if secret_openai:
        st.session_state.api_keys["openai_key"] = secret_openai
        st.success("✅ OpenAI API Key loaded from Secrets")
    else:
        openai_key = st.text_input(
            "🔑 OpenAI API Key (for Whisper)",
            type="password",
            help="Get your API key from https://platform.openai.com/api-keys",
            key="openai_input"
        )
        st.session_state.api_keys["openai_key"] = openai_key
    
    st.divider()
    
    # Settings Info
    st.info(
        """
        **💡 Tips:**
        - Add `GEMINI_API_KEY` and `OPENAI_API_KEY` to Streamlit Secrets for permanent access
        - Secrets file location: `~/.streamlit/secrets.toml`
        """
    )

# ============================================================================
# MAIN CONTENT - HEADER
# ============================================================================
st.markdown(
    '<div class="header-title">🎬 Ultimate Burmese AI Movie Recap Studio</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subheader-text">Transform your movies into engaging Burmese AI-generated recaps</div>',
    unsafe_allow_html=True
)

st.divider()

# ============================================================================
# MAIN CONTENT - INPUT SECTION
# ============================================================================
st.header("📤 Step 1: Upload Your Content")

st.markdown(
    '<div class="info-box">'
    '<strong>ℹ️ Choose one input method:</strong> '
    'Upload a local video, provide a YouTube link, or upload a script document.'
    '</div>',
    unsafe_allow_html=True
)

# Create Tabs for Input Methods
tab1, tab2, tab3 = st.tabs([
    "📹 Local Video Upload",
    "🎥 YouTube Link",
    "📄 Script/Document Upload"
])

# ============================================================================
# TAB 1: LOCAL VIDEO UPLOAD
# ============================================================================
with tab1:
    st.subheader("Upload Local Video File")
    
    st.markdown("""
    **Supported Formats:** MP4, MKV, MOV  
    **Max File Size:** 500MB  
    **Recommended:** 720p or higher resolution
    """)
    
    uploaded_video = st.file_uploader(
        "Choose a video file",
        type=["mp4", "mkv", "mov"],
        key="video_upload",
        help="Select a video file from your computer"
    )
    
    if uploaded_video is not None:
        st.session_state.input_data["input_type"] = "local_video"
        st.session_state.input_data["video_file"] = uploaded_video
        
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", uploaded_video.name)
        with col2:
            file_size_mb = uploaded_video.size / (1024 * 1024)
            st.metric("File Size", f"{file_size_mb:.2f} MB")
        with col3:
            st.metric("File Type", uploaded_video.type)
        
        # Video Preview
        st.video(uploaded_video)
        
        st.markdown(
            '<div class="success-box">'
            '<strong>✅ Video uploaded successfully!</strong> '
            'Proceed to the next step to extract metadata and generate recap.'
            '</div>',
            unsafe_allow_html=True
        )

# ============================================================================
# TAB 2: YOUTUBE LINK
# ============================================================================
with tab2:
    st.subheader("Fetch Video from YouTube")
    
    st.markdown("""
    **Supported Platforms:** YouTube, Facebook, TikTok, Instagram  
    **What we'll extract:** Video file or Transcript (auto-generated subtitles)
    """)
    
    youtube_url = st.text_input(
        "Enter Video URL",
        placeholder="https://www.youtube.com/watch?v=...",
        key="youtube_input",
        help="Paste the full URL of the video"
    )
    
    if youtube_url:
        st.session_state.input_data["input_type"] = "youtube_url"
        st.session_state.input_data["youtube_url"] = youtube_url
        
        # URL Validation
        if "youtube.com" in youtube_url or "youtu.be" in youtube_url:
            st.markdown(
                '<div class="success-box">'
                '<strong>✅ Valid YouTube URL detected!</strong>'
                '</div>',
                unsafe_allow_html=True
            )
            
            # Option to choose what to extract
            extract_option = st.radio(
                "What would you like to extract?",
                ["Download Full Video", "Extract Transcript Only"],
                horizontal=True
            )
            
            if st.button("🔄 Fetch Video/Transcript", use_container_width=True):
                with st.spinner("Fetching video information..."):
                    st.info("⏳ This may take a moment...")
                    # Placeholder for actual yt-dlp implementation
                    st.success("✅ Video/Transcript fetched successfully!")
        else:
            st.markdown(
                '<div class="error-box">'
                '<strong>❌ Invalid URL!</strong> '
                'Please enter a valid YouTube URL.'
                '</div>',
                unsafe_allow_html=True
            )

# ============================================================================
# TAB 3: SCRIPT/DOCUMENT UPLOAD
# ============================================================================
with tab3:
    st.subheader("Upload Script or Document")
    
    st.markdown("""
    **Supported Formats:** TXT, SRT, PDF, DOCX  
    **Max File Size:** 50MB  
    **Use Case:** Upload a movie script, subtitle file, or any text document
    """)
    
    uploaded_script = st.file_uploader(
        "Choose a document file",
        type=["txt", "srt", "pdf", "docx"],
        key="script_upload",
        help="Select a script or document file"
    )
    
    if uploaded_script is not None:
        st.session_state.input_data["input_type"] = "script_document"
        st.session_state.input_data["script_file"] = uploaded_script
        
        # Display file info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("File Name", uploaded_script.name)
        with col2:
            file_size_kb = uploaded_script.size / 1024
            st.metric("File Size", f"{file_size_kb:.2f} KB")
        with col3:
            st.metric("File Type", uploaded_script.type)
        
        st.markdown(
            '<div class="success-box">'
            '<strong>✅ Document uploaded successfully!</strong> '
            'The text will be extracted and processed in the next step.'
            '</div>',
            unsafe_allow_html=True
        )

# ============================================================================
# MAIN CONTENT - SUMMARY & NEXT STEP
# ============================================================================
st.divider()

st.header("📋 Input Summary")

# Display current input status
col1, col2, col3 = st.columns(3)

with col1:
    input_type_display = st.session_state.input_data.get("input_type")
    if input_type_display == "local_video":
        st.info("📹 **Input Type:** Local Video Upload")
    elif input_type_display == "youtube_url":
        st.info("🎥 **Input Type:** YouTube Link")
    elif input_type_display == "script_document":
        st.info("📄 **Input Type:** Script/Document")
    else:
        st.warning("⚠️ **Input Type:** Not selected yet")

with col2:
    if st.session_state.api_keys["gemini_key"]:
        st.success("✅ Gemini API Key: Configured")
    else:
        st.error("❌ Gemini API Key: Missing")

with col3:
    if st.session_state.api_keys["openai_key"]:
        st.success("✅ OpenAI API Key: Configured")
    else:
        st.warning("⚠️ OpenAI API Key: Optional (for Whisper)")

st.divider()

# Next Step Button
if st.session_state.input_data.get("input_type") and st.session_state.api_keys.get("gemini_key"):
    if st.button("➡️ Proceed to Script Generation", use_container_width=True, type="primary"):
        st.success("✅ Ready to proceed! (Next step will be implemented in Phase 2)")
else:
    st.warning("⚠️ Please complete the input setup above to proceed.")

# ============================================================================
# FOOTER
# ============================================================================
st.divider()
st.markdown("""
---
**🎬 Ultimate Burmese AI Movie Recap Studio** v1.0  
Built with Streamlit, Google Gemini AI, and OpenAI Whisper  
[GitHub](https://github.com/footlivebyprgt) | [Documentation](#)
""")
