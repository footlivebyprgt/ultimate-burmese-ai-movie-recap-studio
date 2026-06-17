"""
Phase 5: Deployment & Project Management
This module handles project saving, management, and deployment options
"""

import streamlit as st
from project_management import (
    ProjectDatabase,
    create_project_directory,
    get_project_size,
    format_file_size,
    export_project_as_json,
    backup_project,
    cleanup_old_backups
)
from datetime import datetime
import os


def render_phase5_ui():
    """
    Render Phase 5: Deployment & Project Management UI
    """
    st.header("🚀 Step 5: Deployment & Project Management")
    
    st.markdown("""
    Save your project, manage files, and prepare for deployment.
    """)
    
    # ========================================================================
    # STEP 5.1: SAVE PROJECT
    # ========================================================================
    st.subheader("Step 5.1: Save Project")
    
    col1, col2 = st.columns(2)
    
    with col1:
        project_name = st.text_input(
            "Project Name:",
            placeholder="My Movie Recap Project",
            key="project_name_input"
        )
    
    with col2:
        project_description = st.text_area(
            "Project Description (Optional):",
            placeholder="Describe your project...",
            height=100,
            key="project_description"
        )
    
    if project_name:
        if st.button("💾 Save Project", use_container_width=True, type="primary"):
            with st.spinner("Saving project..."):
                # Initialize project database
                db = ProjectDatabase()
                
                # Create project
                project_id = db.create_project(project_name, project_description)
                
                if project_id:
                    # Create project directory
                    project_dir = create_project_directory(project_name)
                    
                    # Save project data
                    project_data = {
                        "project_id": project_id,
                        "project_name": project_name,
                        "description": project_description,
                        "created_at": datetime.now().isoformat(),
                        "status": "completed",
                        "input_data": st.session_state.input_data
                    }
                    
                    # Export as JSON
                    json_path = export_project_as_json(
                        project_data,
                        os.path.join(project_dir, f"{project_name}_metadata.json")
                    )
                    
                    if json_path:
                        st.success(f"✅ Project saved successfully! (ID: {project_id})")
                        st.info(f"📁 Project directory: {project_dir}")
                        
                        # Save to session state
                        st.session_state.input_data["project_id"] = project_id
                        st.session_state.input_data["project_name"] = project_name
    else:
        st.warning("⚠️ Please enter a project name.")
    
    # ========================================================================
    # STEP 5.2: PROJECT MANAGEMENT
    # ========================================================================
    st.divider()
    st.subheader("Step 5.2: Project Management")
    
    # Initialize database
    db = ProjectDatabase()
    
    # Get all projects
    projects = db.get_projects()
    
    if projects:
        st.markdown("**Your Projects:**")
        
        # Create tabs for different project views
        view_tab1, view_tab2 = st.tabs(["📋 Project List", "📊 Project Statistics"])
        
        # Tab 1: Project List
        with view_tab1:
            for project in projects:
                with st.expander(f"📁 {project['name']} (Status: {project['status']})"):
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Created", project['created_at'][:10])
                    
                    with col2:
                        st.metric("Updated", project['updated_at'][:10])
                    
                    with col3:
                        st.metric("Status", project['status'])
                    
                    if project['description']:
                        st.markdown(f"**Description:** {project['description']}")
                    
                    # Get project files
                    files = db.get_project_files(project['id'])
                    
                    if files:
                        st.markdown("**Project Files:**")
                        for file in files:
                            st.write(f"- {file['name']} ({file['type']})")
                    
                    # Project actions
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        if st.button(f"📥 Export", key=f"export_{project['id']}", use_container_width=True):
                            st.info(f"Export feature for project {project['name']} coming soon!")
                    
                    with col2:
                        if st.button(f"💾 Backup", key=f"backup_{project['id']}", use_container_width=True):
                            project_dir = f"projects/{project['name']}"
                            if os.path.exists(project_dir):
                                backup_path = backup_project(project_dir)
                                if backup_path:
                                    st.success(f"✅ Backup created: {backup_path}")
                            else:
                                st.warning("Project directory not found.")
                    
                    with col3:
                        if st.button(f"🗑️ Delete", key=f"delete_{project['id']}", use_container_width=True):
                            if db.delete_project(project['id']):
                                st.success(f"✅ Project deleted!")
                                st.rerun()
        
        # Tab 2: Project Statistics
        with view_tab2:
            st.markdown("**Project Statistics:**")
            
            total_projects = len(projects)
            completed_projects = len([p for p in projects if p['status'] == 'completed'])
            in_progress_projects = len([p for p in projects if p['status'] == 'in_progress'])
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Projects", total_projects)
            
            with col2:
                st.metric("Completed", completed_projects)
            
            with col3:
                st.metric("In Progress", in_progress_projects)
    else:
        st.info("ℹ️ No projects yet. Save your first project above!")
    
    # ========================================================================
    # STEP 5.3: DEPLOYMENT OPTIONS
    # ========================================================================
    st.divider()
    st.subheader("Step 5.3: Deployment Options")
    
    deployment_tab1, deployment_tab2, deployment_tab3 = st.tabs([
        "🎬 Social Media",
        "☁️ Cloud Storage",
        "📤 Direct Upload"
    ])
    
    # Tab 1: Social Media
    with deployment_tab1:
        st.markdown("**Upload to Social Media Platforms:**")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📱 YouTube", use_container_width=True):
                st.info("YouTube integration coming soon! You can manually upload your video to YouTube.")
        
        with col2:
            if st.button("🎵 TikTok", use_container_width=True):
                st.info("TikTok integration coming soon! Resize your video to 9:16 aspect ratio for best results.")
        
        with col3:
            if st.button("📸 Instagram", use_container_width=True):
                st.info("Instagram integration coming soon! Use 1:1 or 9:16 aspect ratio for Reels.")
    
    # Tab 2: Cloud Storage
    with deployment_tab2:
        st.markdown("**Upload to Cloud Storage:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("☁️ Google Drive", use_container_width=True):
                st.info("Google Drive integration coming soon!")
        
        with col2:
            if st.button("☁️ Dropbox", use_container_width=True):
                st.info("Dropbox integration coming soon!")
    
    # Tab 3: Direct Upload
    with deployment_tab3:
        st.markdown("**Direct Upload Options:**")
        
        final_video = st.session_state.input_data.get("combined_video_path")
        
        if final_video:
            col1, col2 = st.columns(2)
            
            with col1:
                # Download video
                with open(final_video, "rb") as video_file:
                    st.download_button(
                        label="📥 Download Video (MP4)",
                        data=video_file.read(),
                        file_name="movie_recap_final.mp4",
                        mime="video/mp4",
                        use_container_width=True
                    )
            
            with col2:
                # Get video info
                from video_services import get_video_info
                video_info = get_video_info(final_video)
                
                if video_info:
                    file_size = os.path.getsize(final_video)
                    st.metric("File Size", format_file_size(file_size))
        else:
            st.info("ℹ️ Complete all previous steps to download your final video.")
    
    # ========================================================================
    # STEP 5.4: SETTINGS & PREFERENCES
    # ========================================================================
    st.divider()
    st.subheader("Step 5.4: Settings & Preferences")
    
    settings_tab1, settings_tab2 = st.tabs(["⚙️ Application Settings", "📋 About"])
    
    # Tab 1: Application Settings
    with settings_tab1:
        st.markdown("**Application Settings:**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            auto_save = st.checkbox(
                "Auto-save projects",
                value=True,
                help="Automatically save projects every 5 minutes"
            )
        
        with col2:
            keep_backups = st.number_input(
                "Keep backups:",
                min_value=1,
                max_value=20,
                value=5,
                help="Number of backups to keep"
            )
        
        if st.button("🧹 Clean Up Old Backups", use_container_width=True):
            cleanup_old_backups(keep_count=keep_backups)
            st.success("✅ Old backups cleaned up!")
    
    # Tab 2: About
    with settings_tab2:
        st.markdown("""
        ### 🎬 Ultimate Burmese AI Movie Recap Studio
        
        **Version:** 1.0.0  
        **Status:** Beta
        
        **Features:**
        - Multi-input support (Local Video, YouTube, Documents)
        - AI-powered script generation (Gemini)
        - Audio transcription (Whisper)
        - Professional voiceover (Edge TTS)
        - Video assembly & branding
        - Project management & backup
        
        **Technology Stack:**
        - Streamlit (Frontend)
        - Google Gemini AI (Script Generation)
        - OpenAI Whisper (Transcription)
        - Edge TTS (Text-to-Speech)
        - MoviePy (Video Processing)
        
        **Support:**
        For issues, questions, or suggestions, please visit:
        [GitHub Repository](https://github.com/footlivebyprgt/ultimate-burmese-ai-movie-recap-studio)
        """)
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    st.divider()
    st.subheader("🎉 Project Completion Summary")
    
    if st.session_state.input_data.get("project_name"):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Project", st.session_state.input_data.get("project_name", "N/A"))
        
        with col2:
            st.metric("Status", "✅ Completed")
        
        with col3:
            script_length = len(st.session_state.input_data.get("generated_script", ""))
            st.metric("Script Length", f"{script_length} chars")
        
        with col4:
            voiceover_duration = st.session_state.input_data.get("voiceover_duration", 0)
            st.metric("Voiceover", f"{voiceover_duration:.1f}s")
        
        st.success("✅ Your movie recap project is ready! You can now download and share it on social media.")
    else:
        st.info("ℹ️ Complete all steps and save your project to see the summary.")


# Main execution
if __name__ == "__main__":
    # This is for testing purposes
    st.set_page_config(page_title="Phase 5 - Deployment", layout="wide")
    
    # Initialize session state
    if "input_data" not in st.session_state:
        st.session_state.input_data = {}
    if "api_keys" not in st.session_state:
        st.session_state.api_keys = {}
    
    render_phase5_ui()
