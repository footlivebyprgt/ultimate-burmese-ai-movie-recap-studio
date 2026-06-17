"""
Phase 3: Audio & Voiceover Production
This module handles TTS generation and audio processing
"""

import streamlit as st
from tts_services import (
    generate_speech,
    generate_speech_batch,
    get_audio_duration,
    adjust_audio_speed,
    merge_audio_files,
    add_silence,
    get_available_voices,
    get_language_name,
    validate_voice_parameters
)
import tempfile


def render_phase3_ui():
    """
    Render Phase 3: Audio & Voiceover Production UI
    """
    st.header("🎙️ Step 3: Generate Voiceover")
    
    st.markdown("""
    Create professional Burmese voiceover for your movie recap script.
    Choose your preferred voice, language, and audio settings.
    """)
    
    # Check if script is available
    if not st.session_state.input_data.get("generated_script"):
        st.warning("⚠️ Please complete Step 2 (Generate Script) first.")
        return
    
    script = st.session_state.input_data.get("generated_script")
    
    # ========================================================================
    # STEP 3.1: VOICE CONFIGURATION
    # ========================================================================
    st.subheader("Step 3.1: Configure Voice")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        language = st.selectbox(
            "Language:",
            {
                "Burmese": "my",
                "English": "en",
                "Thai": "th",
                "Japanese": "ja",
                "Korean": "ko",
                "Vietnamese": "vi"
            },
            key="tts_language"
        )
    
    with col2:
        gender = st.selectbox(
            "Voice Gender:",
            ["Male", "Female"],
            key="tts_gender"
        )
    
    with col3:
        speed = st.slider(
            "Speech Speed:",
            min_value=0.5,
            max_value=2.0,
            value=1.0,
            step=0.1,
            help="0.5 = slower, 1.0 = normal, 2.0 = faster",
            key="tts_speed"
        )
    
    with col4:
        pitch = st.slider(
            "Pitch:",
            min_value=-20,
            max_value=20,
            value=0,
            step=5,
            help="Adjust voice pitch (limited support)",
            key="tts_pitch"
        )
    
    # Validate voice parameters
    is_valid, message = validate_voice_parameters(language, gender, speed)
    
    if not is_valid:
        st.error(f"❌ {message}")
        return
    
    # ========================================================================
    # STEP 3.2: PREVIEW & GENERATE VOICEOVER
    # ========================================================================
    st.divider()
    st.subheader("Step 3.2: Generate Voiceover")
    
    # Display script preview
    with st.expander("📋 Script Preview", expanded=False):
        st.text_area(
            "Script to be converted to speech:",
            value=script,
            height=200,
            disabled=True
        )
    
    # Calculate estimated duration
    word_count = len(script.split())
    estimated_duration = (word_count / 130) * 60  # Rough estimate: 130 words per minute
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Word Count", f"{word_count} words")
    
    with col2:
        st.metric("Estimated Duration", f"{estimated_duration:.1f} seconds")
    
    with col3:
        st.metric("Language", get_language_name(language))
    
    # Generate voiceover button
    if st.button("🎙️ Generate Voiceover", use_container_width=True, type="primary"):
        with st.spinner("Generating voiceover with Edge TTS..."):
            # Generate speech
            audio_path = generate_speech(
                text=script,
                language=language,
                gender=gender,
                speed=speed
            )
            
            if audio_path:
                st.session_state.input_data["voiceover_path"] = audio_path
                st.success("✅ Voiceover generated successfully!")
                
                # Get audio duration
                duration = get_audio_duration(audio_path)
                if duration:
                    st.info(f"⏱️ Audio Duration: {duration:.1f} seconds")
                    st.session_state.input_data["voiceover_duration"] = duration
                
                # Play audio
                st.audio(audio_path, format="audio/mp3")
    
    # ========================================================================
    # STEP 3.3: AUDIO ADJUSTMENTS
    # ========================================================================
    st.divider()
    st.subheader("Step 3.3: Audio Adjustments")
    
    voiceover_path = st.session_state.input_data.get("voiceover_path")
    
    if voiceover_path:
        adjustment_tab1, adjustment_tab2, adjustment_tab3 = st.tabs([
            "⚙️ Speed Adjustment",
            "🔇 Add Silence",
            "📊 Audio Info"
        ])
        
        # Tab 1: Speed Adjustment
        with adjustment_tab1:
            st.markdown("Adjust the voiceover speed if needed:")
            
            new_speed = st.slider(
                "Adjusted Speed:",
                min_value=0.5,
                max_value=2.0,
                value=1.0,
                step=0.1,
                key="audio_speed_adjustment"
            )
            
            if new_speed != 1.0:
                if st.button("⚙️ Apply Speed Adjustment", use_container_width=True):
                    with st.spinner("Adjusting audio speed..."):
                        adjusted_path = adjust_audio_speed(
                            audio_file_path=voiceover_path,
                            speed_factor=new_speed
                        )
                        
                        if adjusted_path:
                            st.session_state.input_data["voiceover_path"] = adjusted_path
                            st.success("✅ Audio speed adjusted!")
                            
                            # Get new duration
                            new_duration = get_audio_duration(adjusted_path)
                            if new_duration:
                                st.info(f"⏱️ New Duration: {new_duration:.1f} seconds")
                                st.session_state.input_data["voiceover_duration"] = new_duration
                            
                            # Play adjusted audio
                            st.audio(adjusted_path, format="audio/mp3")
        
        # Tab 2: Add Silence
        with adjustment_tab2:
            st.markdown("Add silence before or after the voiceover:")
            
            col1, col2 = st.columns(2)
            
            with col1:
                silence_before = st.number_input(
                    "Silence Before (seconds):",
                    min_value=0,
                    max_value=10,
                    value=0,
                    step=0.5,
                    key="silence_before"
                )
            
            with col2:
                silence_after = st.number_input(
                    "Silence After (seconds):",
                    min_value=0,
                    max_value=10,
                    value=0,
                    step=0.5,
                    key="silence_after"
                )
            
            if silence_before > 0 or silence_after > 0:
                if st.button("🔇 Add Silence", use_container_width=True):
                    with st.spinner("Adding silence..."):
                        audio_files = []
                        
                        # Add silence before
                        if silence_before > 0:
                            silence_path = add_silence(int(silence_before * 1000))
                            if silence_path:
                                audio_files.append(silence_path)
                        
                        # Add main voiceover
                        audio_files.append(voiceover_path)
                        
                        # Add silence after
                        if silence_after > 0:
                            silence_path = add_silence(int(silence_after * 1000))
                            if silence_path:
                                audio_files.append(silence_path)
                        
                        # Merge audio files
                        merged_path = merge_audio_files(audio_files)
                        
                        if merged_path:
                            st.session_state.input_data["voiceover_path"] = merged_path
                            st.success("✅ Silence added!")
                            
                            # Get new duration
                            new_duration = get_audio_duration(merged_path)
                            if new_duration:
                                st.info(f"⏱️ New Duration: {new_duration:.1f} seconds")
                                st.session_state.input_data["voiceover_duration"] = new_duration
                            
                            # Play audio with silence
                            st.audio(merged_path, format="audio/mp3")
        
        # Tab 3: Audio Info
        with adjustment_tab3:
            st.markdown("Audio Information:")
            
            duration = get_audio_duration(voiceover_path)
            if duration:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Duration", f"{duration:.1f} seconds")
                
                with col2:
                    minutes = duration / 60
                    st.metric("Duration (MM:SS)", f"{int(minutes)}:{int((minutes % 1) * 60):02d}")
                
                with col3:
                    st.metric("Format", "MP3")
    else:
        st.info("ℹ️ Generate voiceover first to enable audio adjustments.")
    
    # ========================================================================
    # DOWNLOAD VOICEOVER
    # ========================================================================
    st.divider()
    
    final_voiceover = st.session_state.input_data.get("voiceover_path")
    
    if final_voiceover:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # Download voiceover
            with open(final_voiceover, "rb") as audio_file:
                st.download_button(
                    label="📥 Download Voiceover",
                    data=audio_file.read(),
                    file_name="movie_recap_voiceover.mp3",
                    mime="audio/mp3",
                    use_container_width=True
                )
        
        with col2:
            # View audio info
            if st.button("📊 View Audio Info", use_container_width=True):
                duration = get_audio_duration(final_voiceover)
                if duration:
                    st.info(f"Duration: {duration:.1f} seconds ({int(duration/60)}:{int(duration%60):02d})")
        
        with col3:
            # Proceed to next step
            if st.button("➡️ Proceed to Video Assembly", use_container_width=True, type="primary"):
                st.success("✅ Ready for Phase 4: Video Assembly & Branding!")
                st.info("(Next phase will be implemented soon)")


# Main execution
if __name__ == "__main__":
    # This is for testing purposes
    st.set_page_config(page_title="Phase 3 - Voiceover Production", layout="wide")
    
    # Initialize session state
    if "input_data" not in st.session_state:
        st.session_state.input_data = {}
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {}
    
    render_phase3_ui()
