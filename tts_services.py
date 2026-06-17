"""
Text-to-Speech Services
Handles audio generation using Edge TTS and Pro Dubbing Engine
"""

import asyncio
import tempfile
from typing import Optional, List, Dict, Tuple
import streamlit as st

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    from pydub import AudioSegment
except ImportError:
    AudioSegment = None


# ============================================================================
# VOICE CONFIGURATION
# ============================================================================

VOICE_MAP = {
    "my": {
        "Male": "my-MM-ThihaNeural",
        "Female": "my-MM-NilarNeural"
    },
    "en": {
        "Male": "en-US-GuyNeural",
        "Female": "en-US-AvaNeural"
    },
    "th": {
        "Male": "th-TH-NiwatNeural",
        "Female": "th-TH-PremwadeeNeural"
    },
    "ja": {
        "Male": "ja-JP-KeitaNeural",
        "Female": "ja-JP-NanamiNeural"
    },
    "ko": {
        "Male": "ko-KR-InJoonNeural",
        "Female": "ko-KR-SunHiNeural"
    },
    "vi": {
        "Male": "vi-VN-NamMinhNeural",
        "Female": "vi-VN-HoaiMyNeural"
    }
}

LANGUAGE_NAMES = {
    "my": "Burmese",
    "en": "English",
    "th": "Thai",
    "ja": "Japanese",
    "ko": "Korean",
    "vi": "Vietnamese"
}


# ============================================================================
# EDGE TTS - TEXT TO SPEECH
# ============================================================================

async def generate_speech_async(
    text: str,
    language: str = "my",
    gender: str = "Male",
    speed: float = 1.0,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Generate speech from text using Edge TTS (async)
    
    Args:
        text: Text to convert to speech
        language: Language code (my, en, th, ja, ko, vi)
        gender: Voice gender (Male, Female)
        speed: Speech speed (0.5 - 2.0)
        output_path: Path to save audio file
        
    Returns:
        Path to generated audio file or None if generation fails
    """
    if edge_tts is None:
        st.error("Edge TTS is not installed. Cannot generate speech.")
        return None
    
    try:
        # Get voice
        voice = VOICE_MAP.get(language, {}).get(gender)
        if not voice:
            st.error(f"Voice not available for {LANGUAGE_NAMES.get(language, language)} - {gender}")
            return None
        
        # Generate output path if not provided
        if not output_path:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        
        # Create communicate object
        communicate = edge_tts.Communicate(text, voice, rate=f"{int((speed - 1) * 100):+d}%")
        
        # Save audio
        await communicate.save(output_path)
        
        return output_path
    
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None


def generate_speech(
    text: str,
    language: str = "my",
    gender: str = "Male",
    speed: float = 1.0,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Generate speech from text using Edge TTS (sync wrapper)
    
    Args:
        text: Text to convert to speech
        language: Language code
        gender: Voice gender
        speed: Speech speed
        output_path: Path to save audio file
        
    Returns:
        Path to generated audio file or None if generation fails
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(
        generate_speech_async(text, language, gender, speed, output_path)
    )


async def generate_speech_batch_async(
    text_segments: List[Dict],
    language: str = "my",
    gender: str = "Male",
    speed: float = 1.0
) -> List[Optional[str]]:
    """
    Generate speech for multiple text segments in parallel (async)
    
    Args:
        text_segments: List of dicts with 'text' and optional 'id' keys
        language: Language code
        gender: Voice gender
        speed: Speech speed
        
    Returns:
        List of paths to generated audio files
    """
    if edge_tts is None:
        st.error("Edge TTS is not installed.")
        return [None] * len(text_segments)
    
    try:
        # Get voice
        voice = VOICE_MAP.get(language, {}).get(gender)
        if not voice:
            st.error(f"Voice not available for {LANGUAGE_NAMES.get(language, language)} - {gender}")
            return [None] * len(text_segments)
        
        # Create tasks for parallel generation
        tasks = []
        for segment in text_segments:
            text = segment.get("text", "")
            segment_id = segment.get("id", 0)
            
            output_path = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f"_segment_{segment_id}.mp3"
            ).name
            
            communicate = edge_tts.Communicate(text, voice, rate=f"{int((speed - 1) * 100):+d}%")
            tasks.append(communicate.save(output_path))
        
        # Run all tasks concurrently
        await asyncio.gather(*tasks)
        
        # Return paths
        output_paths = []
        for i, segment in enumerate(text_segments):
            segment_id = segment.get("id", i)
            output_path = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=f"_segment_{segment_id}.mp3"
            ).name
            output_paths.append(output_path)
        
        return output_paths
    
    except Exception as e:
        st.error(f"Error generating speech batch: {str(e)}")
        return [None] * len(text_segments)


def generate_speech_batch(
    text_segments: List[Dict],
    language: str = "my",
    gender: str = "Male",
    speed: float = 1.0
) -> List[Optional[str]]:
    """
    Generate speech for multiple text segments in parallel (sync wrapper)
    
    Args:
        text_segments: List of dicts with 'text' and optional 'id' keys
        language: Language code
        gender: Voice gender
        speed: Speech speed
        
    Returns:
        List of paths to generated audio files
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(
        generate_speech_batch_async(text_segments, language, gender, speed)
    )


# ============================================================================
# AUDIO PROCESSING
# ============================================================================

def get_audio_duration(audio_file_path: str) -> Optional[float]:
    """
    Get duration of audio file in seconds
    
    Args:
        audio_file_path: Path to audio file
        
    Returns:
        Duration in seconds or None if extraction fails
    """
    if AudioSegment is None:
        st.error("PyDub is not installed. Cannot get audio duration.")
        return None
    
    try:
        audio = AudioSegment.from_file(audio_file_path)
        duration_seconds = len(audio) / 1000.0
        return duration_seconds
    
    except Exception as e:
        st.error(f"Error getting audio duration: {str(e)}")
        return None


def adjust_audio_speed(
    audio_file_path: str,
    speed_factor: float,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Adjust audio playback speed
    
    Args:
        audio_file_path: Path to audio file
        speed_factor: Speed factor (0.5 - 2.0, where 1.0 is normal)
        output_path: Path to save adjusted audio
        
    Returns:
        Path to adjusted audio file or None if adjustment fails
    """
    if AudioSegment is None:
        st.error("PyDub is not installed. Cannot adjust audio speed.")
        return None
    
    try:
        # Load audio
        audio = AudioSegment.from_file(audio_file_path)
        
        # Adjust speed using frame rate
        # This is a simple speed adjustment method
        audio_with_altered_frame_rate = audio._spawn(
            audio.raw_data,
            overrides={"frame_rate": int(audio.frame_rate * speed_factor)}
        )
        
        # Generate output path if not provided
        if not output_path:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        
        # Export audio
        audio_with_altered_frame_rate.export(output_path, format="mp3")
        
        return output_path
    
    except Exception as e:
        st.error(f"Error adjusting audio speed: {str(e)}")
        return None


def merge_audio_files(
    audio_files: List[str],
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Merge multiple audio files into one
    
    Args:
        audio_files: List of paths to audio files
        output_path: Path to save merged audio
        
    Returns:
        Path to merged audio file or None if merge fails
    """
    if AudioSegment is None:
        st.error("PyDub is not installed. Cannot merge audio files.")
        return None
    
    try:
        # Load first audio file
        merged_audio = AudioSegment.from_file(audio_files[0])
        
        # Concatenate other audio files
        for audio_file in audio_files[1:]:
            audio = AudioSegment.from_file(audio_file)
            merged_audio += audio
        
        # Generate output path if not provided
        if not output_path:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        
        # Export merged audio
        merged_audio.export(output_path, format="mp3")
        
        return output_path
    
    except Exception as e:
        st.error(f"Error merging audio files: {str(e)}")
        return None


def add_silence(
    duration_ms: int,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Create audio file with silence
    
    Args:
        duration_ms: Duration of silence in milliseconds
        output_path: Path to save silence audio
        
    Returns:
        Path to silence audio file or None if creation fails
    """
    if AudioSegment is None:
        st.error("PyDub is not installed. Cannot create silence.")
        return None
    
    try:
        # Create silence
        silence = AudioSegment.silent(duration=duration_ms)
        
        # Generate output path if not provided
        if not output_path:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
        
        # Export silence
        silence.export(output_path, format="mp3")
        
        return output_path
    
    except Exception as e:
        st.error(f"Error creating silence: {str(e)}")
        return None


# ============================================================================
# VOICE UTILITIES
# ============================================================================

def get_available_voices() -> Dict[str, List[str]]:
    """
    Get list of available voices
    
    Returns:
        Dictionary with languages and available genders
    """
    return {
        lang: list(genders.keys())
        for lang, genders in VOICE_MAP.items()
    }


def get_language_name(language_code: str) -> str:
    """
    Get full language name from code
    
    Args:
        language_code: Language code (my, en, th, etc.)
        
    Returns:
        Full language name
    """
    return LANGUAGE_NAMES.get(language_code, language_code.upper())


def validate_voice_parameters(
    language: str,
    gender: str,
    speed: float
) -> Tuple[bool, str]:
    """
    Validate voice generation parameters
    
    Args:
        language: Language code
        gender: Voice gender
        speed: Speech speed
        
    Returns:
        Tuple of (is_valid, message)
    """
    # Check language
    if language not in VOICE_MAP:
        return False, f"Unsupported language: {language}"
    
    # Check gender
    if gender not in VOICE_MAP[language]:
        return False, f"Unsupported gender for {LANGUAGE_NAMES[language]}: {gender}"
    
    # Check speed
    if not (0.5 <= speed <= 2.0):
        return False, "Speed must be between 0.5 and 2.0"
    
    return True, "Valid voice parameters"
