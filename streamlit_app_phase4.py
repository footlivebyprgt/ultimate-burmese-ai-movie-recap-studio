"""
Phase 4: Video Assembly & Branding
This module handles video assembly, watermark addition, and subtitle integration
"""

import streamlit as st
from video_services import (
    combine_video_and_audio,
    add_watermark,
    add_subtitles,
    resize_video,
    get_video_info,
    format_video_duration
)


def render_phase4_ui():
    """
    Render Phase 4: Video Assembly & Branding UI
    """
    st.header("🎬 Step 4: Assemble Video & Add Branding")
    
    st.markdown("""
    Combine your voiceover with the original video, add branding elements,
    and customize the output format.
    """)
    
    # Check if required data is available
    if not st.session_state.input_data.get("video_file") and not st.session_state.input_data.get("youtube_url"):
        st.warning("⚠️ Please provide a video source in Step 1 first.")
        return
    
    if not st.session_state.input_data.get("voiceover_path"):
        st.warning("⚠️ Please generate voiceover in Step 3 first.")
        return
    
    # ========================================================================
    # STEP 4.1: COMBINE VIDEO AND AUDIO
    # ========================================================================
    st.subheader("Step 4.1: Combine Video & Voiceover")
    
    video_file = st.session_state.input_data.get("video_file")
    voiceover_path = st.session_state.input_data.get("voiceover_path")
    
    if video_file and voiceover_path:
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("📹 Video Source: Local File")
        
        with col2:
            st.info("🎙️ Voiceover: Generated")
        
        if st.button("🔗 Combine Video & Voiceover", use_container_width=True, type="primary"):
            with st.spinner("Combining video and voiceover..."):
                # Save video to temporary file
                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp_video:
                    tmp_video.write(video_file.getbuffer())
                    tmp_video_path = tmp_video.name
                
                # Combine video and audio
                combined_path = combine_video_and_audio(
                    video_path=tmp_video_path,
                    audio_path=voiceover_path
                )
                
                if combined_path:
                    st.session_state.input_data["combined_video_path"] = combined_path
                    st.success("✅ Video and voiceover combined successfully!")
                    
                    # Get video info
                    video_info = get_video_info(combined_path)
                    if video_info:
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric("Duration", format_video_duration(video_info["duration"]))
                        
                        with col2:
                            st.metric("Resolution", video_info["resolution"])
                        
                        with col3:
                            st.metric("FPS", f"{video_info['fps']:.1f}")
                        
                        with col4:
                            st.metric("Audio", "✅ Yes" if video_info["has_audio"] else "❌ No")
    else:
        st.info("ℹ️ Video and voiceover are required to combine.")
    
    # ========================================================================
    # STEP 4.2: ADD BRANDING
    # ========================================================================
    st.divider()
    st.subheader("Step 4.2: Add Branding Elements")
    
    combined_video = st.session_state.input_data.get("combined_video_path")
    
    if combined_video:
        branding_tab1, branding_tab2, branding_tab3 = st.tabs([
            "🏷️ Add Watermark",
            "📝 Add Subtitles",
            "📐 Resize Video"
        ])
        
        # Tab 1: Add Watermark
        with branding_tab1:
            st.markdown("Add a logo or watermark to your video:")
            
            watermark_file = st.file_uploader(
                "Upload Watermark Image (PNG with transparency preferred)",
                type=["png", "jpg", "jpeg"],
                key="watermark_upload"
            )
            
            if watermark_file:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    watermark_position = st.selectbox(
                        "Position:",
                        ["top-left", "top-right", "bottom-left", "bottom-right", "center"],
                        key="watermark_position"
                    )
                
                with col2:
                    watermark_opacity = st.slider(
                        "Opacity:",
                        min_value=0.0,
                        max_value=1.0,
                        value=0.7,
                        step=0.1,
                        key="watermark_opacity"
                    )
                
                with col3:
                    watermark_scale = st.slider(
                        "Size (% of video width):",
                        min_value=5,
                        max_value=50,
                        value=20,
                        step=5,
                        key="watermark_scale"
                    )
                
                if st.button("🏷️ Add Watermark", use_container_width=True):
                    with st.spinner("Adding watermark..."):
                        # Save watermark to temporary file
                        import tempfile
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_watermark:
                            tmp_watermark.write(watermark_file.getbuffer())
                            tmp_watermark_path = tmp_watermark.name
                        
                        # Add watermark
                        watermarked_path = add_watermark(
                            video_path=combined_video,
                            watermark_path=tmp_watermark_path,
                            position=watermark_position,
                            opacity=watermark_opacity,
                            scale=watermark_scale / 100.0
                        )
                        
                        if watermarked_path:
                            st.session_state.input_data["combined_video_path"] = watermarked_path
                            st.success("✅ Watermark added successfully!")
        
        # Tab 2: Add Subtitles
        with branding_tab2:
            st.markdown("Add Burmese subtitles to your video:")
            
            subtitle_text = st.text_area(
                "Subtitle Text:",
                placeholder="Enter the subtitle text (Burmese or English)",
                height=100,
                key="subtitle_text"
            )
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                subtitle_position = st.selectbox(
                    "Position:",
                    ["top", "center", "bottom"],
                    key="subtitle_position"
                )
            
            with col2:
                subtitle_font_size = st.slider(
                    "Font Size:",
                    min_value=20,
                    max_value=100,
                    value=40,
                    step=5,
                    key="subtitle_font_size"
                )
            
            with col3:
                subtitle_color = st.selectbox(
                    "Color:",
                    ["white", "black", "yellow", "red", "green", "blue"],
                    key="subtitle_color"
                )
            
            if subtitle_text:
                if st.button("📝 Add Subtitles", use_container_width=True):
                    with st.spinner("Adding subtitles..."):
                        # Add subtitles
                        subtitled_path = add_subtitles(
                            video_path=combined_video,
                            subtitle_text=subtitle_text,
                            position=subtitle_position,
                            font_size=subtitle_font_size,
                            color=subtitle_color
                        )
                        
                        if subtitled_path:
                            st.session_state.input_data["combined_video_path"] = subtitled_path
                            st.success("✅ Subtitles added successfully!")
        
        # Tab 3: Resize Video
        with branding_tab3:
            st.markdown("Resize video for different platforms:")
            
            aspect_ratio = st.selectbox(
                "Target Aspect Ratio:",
                {
                    "16:9 (YouTube, Desktop)": "16:9",
                    "9:16 (TikTok, Instagram Reels)": "9:16",
                    "1:1 (Instagram, Facebook)": "1:1",
                    "4:3 (Classic)": "4:3"
                },
                key="aspect_ratio"
            )
            
            if st.button("📐 Resize Video", use_container_width=True):
                with st.spinner(f"Resizing video to {aspect_ratio}..."):
                    # Resize video
                    resized_path = resize_video(
                        video_path=combined_video,
                        aspect_ratio=aspect_ratio
                    )
                    
                    if resized_path:
                        st.session_state.input_data["combined_video_path"] = resized_path
                        st.success(f"✅ Video resized to {aspect_ratio}!")
    else:
        st.info("ℹ️ Combine video and voiceover first to add branding elements.")
    
    # ========================================================================
    # STEP 4.3: PREVIEW & DOWNLOAD
    # ========================================================================
    st.divider()
    st.subheader("Step 4.3: Preview & Download")
    
    final_video = st.session_state.input_data.get("combined_video_path")
    
    if final_video:
        col1, col2 = st.columns(2)
        
        with col1:
            # Get video info
            video_info = get_video_info(final_video)
            if video_info:
                st.markdown("**Video Information:**")
                st.metric("Duration", format_video_duration(video_info["duration"]))
                st.metric("Resolution", video_info["resolution"])
                st.metric("FPS", f"{video_info['fps']:.1f}")
        
        with col2:
            # Download button
            with open(final_video, "rb") as video_file_obj:
                st.download_button(
                    label="📥 Download Final Video",
                    data=video_file_obj.read(),
                    file_name="movie_recap_final.mp4",
                    mime="video/mp4",
                    use_container_width=True
                )
        
        # Video preview
        st.video(final_video)
    else:
        st.info("ℹ️ Combine video and voiceover to preview and download.")
    
    # ========================================================================
    # PROCEED TO NEXT STEP
    # ========================================================================
    st.divider()
    
    if final_video:
        if st.button("➡️ Proceed to Deployment & Management", use_container_width=True, type="primary"):
            st.success("✅ Ready for Phase 5: Deployment & Project Management!")
            st.info("(Final phase will be implemented soon)")


# Main execution
if __name__ == "__main__":
    # This is for testing purposes
    st.set_page_config(page_title="Phase 4 - Video Assembly", layout="wide")
    
    # Initialize session state
    if "input_data" not in st.session_state:
        st.session_state.input_data = {}
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {}
    
    render_phase4_ui()
