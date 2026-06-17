"""
AI Services Integration
Handles Whisper AI transcription and Gemini AI script generation
"""

import os
import tempfile
from typing import Optional, Dict
import streamlit as st

try:
    import openai
except ImportError:
    openai = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


# ============================================================================
# WHISPER AI - AUDIO TRANSCRIPTION
# ============================================================================

def transcribe_audio_whisper(audio_file_path: str, api_key: str) -> Optional[str]:
    """
    Transcribe audio file using OpenAI Whisper API
    
    Args:
        audio_file_path: Path to audio file
        api_key: OpenAI API key
        
    Returns:
        Transcribed text or None if transcription fails
    """
    if openai is None:
        st.error("OpenAI library is not installed. Cannot transcribe audio.")
        return None
    
    if not api_key:
        st.error("OpenAI API key is required for audio transcription.")
        return None
    
    try:
        # Set API key
        openai.api_key = api_key
        
        # Open audio file
        with open(audio_file_path, "rb") as audio_file:
            # Call Whisper API
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file,
                language="my"  # Burmese language code
            )
        
        return transcript.get("text", None)
    
    except Exception as e:
        st.error(f"Error transcribing audio: {str(e)}")
        return None


def extract_audio_from_video(video_file_path: str) -> Optional[str]:
    """
    Extract audio from video file using moviepy
    
    Args:
        video_file_path: Path to video file
        
    Returns:
        Path to extracted audio file or None if extraction fails
    """
    try:
        from moviepy.editor import VideoFileClip
    except ImportError:
        st.error("MoviePy is not installed. Cannot extract audio from video.")
        return None
    
    try:
        # Load video
        video = VideoFileClip(video_file_path)
        
        # Extract audio
        if video.audio is None:
            st.error("Video file does not contain audio track.")
            return None
        
        # Save audio to temporary file
        audio_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        
        # Close video
        video.close()
        
        return audio_path
    
    except Exception as e:
        st.error(f"Error extracting audio from video: {str(e)}")
        return None


# ============================================================================
# GEMINI AI - SCRIPT GENERATION
# ============================================================================

def generate_movie_recap_script(
    transcript_or_text: str,
    video_duration: Optional[float] = None,
    custom_prompt: Optional[str] = None,
    api_key: Optional[str] = None
) -> Optional[str]:
    """
    Generate Burmese movie recap script using Gemini AI
    
    Args:
        transcript_or_text: Transcript or script text
        video_duration: Duration of video in seconds (for timing estimation)
        custom_prompt: Custom instructions for script generation
        api_key: Gemini API key
        
    Returns:
        Generated script or None if generation fails
    """
    if genai is None:
        st.error("Google Generative AI library is not installed.")
        return None
    
    if not api_key:
        st.error("Gemini API key is required for script generation.")
        return None
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        # Prepare prompt
        duration_hint = ""
        if video_duration:
            # Estimate target script length (roughly 130 words per minute)
            target_words = int((video_duration / 60) * 130)
            duration_hint = f"\n\nEstimated target length: approximately {target_words} words (for {video_duration/60:.1f} minutes of video)."
        
        custom_instruction = ""
        if custom_prompt:
            custom_instruction = f"\n\nAdditional instructions: {custom_prompt}"
        
        prompt = f"""
        You are a professional movie recap writer for Burmese audiences. 
        
        Please create an engaging and concise movie recap script in Burmese based on the following content:
        
        {transcript_or_text}
        
        Requirements:
        1. Write in clear, conversational Burmese language
        2. Keep the recap engaging and entertaining
        3. Include key plot points and important character developments
        4. Add some emotional depth and humor where appropriate
        5. Format the script with clear sections (Introduction, Plot Summary, Key Scenes, Conclusion)
        6. Make it suitable for voiceover narration{duration_hint}{custom_instruction}
        
        Please provide the script directly without any preamble or explanation.
        """
        
        # Generate content
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            st.error("Gemini API returned empty response.")
            return None
    
    except Exception as e:
        st.error(f"Error generating script with Gemini: {str(e)}")
        return None


def refine_script_with_gemini(
    original_script: str,
    refinement_instruction: str,
    api_key: Optional[str] = None
) -> Optional[str]:
    """
    Refine or edit script using Gemini AI
    
    Args:
        original_script: Original script text
        refinement_instruction: Instructions for refinement
        api_key: Gemini API key
        
    Returns:
        Refined script or None if refinement fails
    """
    if genai is None:
        st.error("Google Generative AI library is not installed.")
        return None
    
    if not api_key:
        st.error("Gemini API key is required for script refinement.")
        return None
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        prompt = f"""
        Please refine the following Burmese movie recap script based on the given instruction.
        
        Original Script:
        {original_script}
        
        Refinement Instruction:
        {refinement_instruction}
        
        Please provide the refined script directly without any preamble or explanation.
        Keep the script in Burmese language.
        """
        
        # Generate content
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            st.error("Gemini API returned empty response.")
            return None
    
    except Exception as e:
        st.error(f"Error refining script with Gemini: {str(e)}")
        return None


def translate_script(
    script: str,
    target_language: str = "en",
    api_key: Optional[str] = None
) -> Optional[str]:
    """
    Translate script to another language using Gemini AI
    
    Args:
        script: Script text to translate
        target_language: Target language code (e.g., "en" for English)
        api_key: Gemini API key
        
    Returns:
        Translated script or None if translation fails
    """
    if genai is None:
        st.error("Google Generative AI library is not installed.")
        return None
    
    if not api_key:
        st.error("Gemini API key is required for script translation.")
        return None
    
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        
        language_map = {
            "en": "English",
            "th": "Thai",
            "ja": "Japanese",
            "ko": "Korean",
            "vi": "Vietnamese",
            "zh": "Chinese"
        }
        
        target_lang_name = language_map.get(target_language, target_language)
        
        prompt = f"""
        Please translate the following Burmese movie recap script to {target_lang_name}.
        
        Original Script (Burmese):
        {script}
        
        Please provide the translated script directly without any preamble or explanation.
        Maintain the same structure and formatting as the original script.
        """
        
        # Generate content
        response = model.generate_content(prompt)
        
        if response.text:
            return response.text.strip()
        else:
            st.error("Gemini API returned empty response.")
            return None
    
    except Exception as e:
        st.error(f"Error translating script with Gemini: {str(e)}")
        return None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_api_keys(gemini_key: Optional[str], openai_key: Optional[str]) -> Dict[str, bool]:
    """
    Validate API keys
    
    Args:
        gemini_key: Gemini API key
        openai_key: OpenAI API key
        
    Returns:
        Dictionary with validation results
    """
    results = {
        "gemini_valid": False,
        "openai_valid": False,
        "gemini_message": "",
        "openai_message": ""
    }
    
    # Validate Gemini key
    if gemini_key:
        if len(gemini_key) > 20:  # Basic validation
            results["gemini_valid"] = True
            results["gemini_message"] = "✅ Gemini API key appears valid"
        else:
            results["gemini_message"] = "❌ Gemini API key appears invalid (too short)"
    else:
        results["gemini_message"] = "⚠️ Gemini API key not provided"
    
    # Validate OpenAI key
    if openai_key:
        if openai_key.startswith("sk-") and len(openai_key) > 20:
            results["openai_valid"] = True
            results["openai_message"] = "✅ OpenAI API key appears valid"
        else:
            results["openai_message"] = "❌ OpenAI API key appears invalid"
    else:
        results["openai_message"] = "⚠️ OpenAI API key not provided (optional for text-only input)"
    
    return results
