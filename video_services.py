"""
Video Services
Handles video assembly, branding, and subtitle integration
"""

import os
import tempfile
from typing import Optional, Tuple, List
import streamlit as st

try:
    from moviepy.editor import (
        VideoFileClip,
        AudioFileClip,
        CompositeAudioClip,
        CompositeVideoClip,
        TextClip,
        ImageClip,
        concatenate_videoclips
    )
except ImportError:
    VideoFileClip = None

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = None


# ============================================================================
# VIDEO ASSEMBLY
# ============================================================================

def combine_video_and_audio(
    video_path: str,
    audio_path: str,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Combine video and audio files
    
    Args:
        video_path: Path to video file
        audio_path: Path to audio file
        output_path: Path to save combined video
        
    Returns:
        Path to combined video or None if combination fails
    """
    if VideoFileClip is None:
        st.error("MoviePy is not installed. Cannot combine video and audio.")
        return None
    
    try:
        # Load video and audio
        video = VideoFileClip(video_path)
        audio = AudioFileClip(audio_path)
        
        # Set audio to video
        video_with_audio = video.set_audio(audio)
        
        # Generate output path if not provided
        if not output_path:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        
        # Write video
        with st.spinner("Combining video and audio..."):
            video_with_audio.write_videofile(
                output_path,
                verbose=False,
                logger=None,
                codec="libx264",
                audio_codec="aac"
            )
        
        # Close clips
        video.close()
        audio.close()
        video_with_audio.close()
        
        return output_path
    
    except Exception as e:
        st.error(f"Error combining video and audio: {str(e)}")
        return None


def add_watermark(
    video_path: str,
    watermark_path: str,
    position: str = "top-right",
    opacity: float = 0.7,
    scale: float = 0.2,
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Add watermark/logo to video
    
    Args:
        video_path: Path to video file
        watermark_path: Path to watermark image
        position: Position (top-left, top-right, bottom-left, bottom-right, center)
        opacity: Watermark opacity (0.0 - 1.0)
        scale: Watermark scale relative to video width (0.0 - 1.0)
        output_path: Path to save watermarked video
        
    Returns:
        Path to watermarked video or None if operation fails
    """
    if VideoFileClip is None:
        st.error("MoviePy is not installed. Cannot add watermark.")
        return None
    
    try:
        # Load video
        video = VideoFileClip(video_path)
        
        # Load watermark
        watermark = ImageClip(watermark_path)
        
        # Calculate watermark size
        watermark_width = int(video.w * scale)
        watermark_height = int(watermark.h * (watermark_width / watermark.w))
        watermark = watermark.resize((watermark_width, watermark_height))
        
        # Set opacity
        watermark = watermark.set_opacity(opacity)
        
        # Calculate position
        positions = {
            "top-left": (10, 10),
            "top-right": (video.w - watermark_width - 10, 10),
            "bottom-left": (10, video.h - watermark_height - 10),
            "bottom-right": (video.w - watermark_width - 10, video.h - watermark_height - 10),
            "center": ((video.w - watermark_width) // 2, (video.h - watermark_height) // 2)
        }
        
        watermark_pos = positions.get(position, positions["top-right"])
        watermark = watermark.set_position(watermark_pos)
        
        # Composite video with watermark
        final_video = CompositeVideoClip([video, watermark.set_duration(video.duration)])
        
        # Generate output path if not provided
        if not output_path:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        
        # Write video
        with st.spinner("Adding watermark..."):
            final_video.write_videofile(
                output_path,
                verbose=False,
                logger=None,
                codec="libx264",
                audio_codec="aac"
            )
        
        # Close clips
        video.close()
        watermark.close()
        final_video.close()
        
        return output_path
    
    except Exception as e:
        st.error(f"Error adding watermark: {str(e)}")
        return None


def add_subtitles(
    video_path: str,
    subtitle_text: str,
    position: str = "bottom",
    font_size: int = 40,
    color: str = "white",
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Add text subtitles to video
    
    Args:
        video_path: Path to video file
        subtitle_text: Text to add as subtitle
        position: Position (top, center, bottom)
        font_size: Font size
        color: Text color (white, black, yellow, etc.)
        output_path: Path to save video with subtitles
        
    Returns:
        Path to video with subtitles or None if operation fails
    """
    if VideoFileClip is None:
        st.error("MoviePy is not installed. Cannot add subtitles.")
        return None
    
    try:
        # Load video
        video = VideoFileClip(video_path)
        
        # Create text clip
        txt_clip = TextClip(
            subtitle_text,
            fontsize=font_size,
            color=color,
            font="Arial",
            method="caption",
            size=(video.w - 40, None)
        )
        
        # Calculate position
        positions = {
            "top": ("center", 20),
            "center": ("center", "center"),
            "bottom": ("center", video.h - font_size - 20)
        }
        
        txt_pos = positions.get(position, positions["bottom"])
        txt_clip = txt_clip.set_position(txt_pos)
        txt_clip = txt_clip.set_duration(video.duration)
        
        # Composite video with text
        final_video = CompositeVideoClip([video, txt_clip])
        
        # Generate output path if not provided
        if not output_path:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        
        # Write video
        with st.spinner("Adding subtitles..."):
            final_video.write_videofile(
                output_path,
                verbose=False,
                logger=None,
                codec="libx264",
                audio_codec="aac"
            )
        
        # Close clips
        video.close()
        txt_clip.close()
        final_video.close()
        
        return output_path
    
    except Exception as e:
        st.error(f"Error adding subtitles: {str(e)}")
        return None


def resize_video(
    video_path: str,
    aspect_ratio: str = "16:9",
    output_path: Optional[str] = None
) -> Optional[str]:
    """
    Resize video to different aspect ratios
    
    Args:
        video_path: Path to video file
        aspect_ratio: Target aspect ratio (16:9, 9:16, 1:1, 4:3)
        output_path: Path to save resized video
        
    Returns:
        Path to resized video or None if operation fails
    """
    if VideoFileClip is None:
        st.error("MoviePy is not installed. Cannot resize video.")
        return None
    
    try:
        # Load video
        video = VideoFileClip(video_path)
        
        # Calculate new dimensions based on aspect ratio
        ratio_map = {
            "16:9": (16, 9),
            "9:16": (9, 16),
            "1:1": (1, 1),
            "4:3": (4, 3)
        }
        
        target_ratio = ratio_map.get(aspect_ratio, (16, 9))
        target_width_ratio, target_height_ratio = target_ratio
        
        # Calculate new dimensions
        current_ratio = video.w / video.h
        target_ratio_value = target_width_ratio / target_height_ratio
        
        if current_ratio > target_ratio_value:
            # Video is too wide
            new_width = int(video.h * target_ratio_value)
            new_height = video.h
        else:
            # Video is too tall
            new_width = video.w
            new_height = int(video.w / target_ratio_value)
        
        # Crop video to new dimensions
        x_center = video.w / 2
        y_center = video.h / 2
        
        x1 = int(x_center - new_width / 2)
        y1 = int(y_center - new_height / 2)
        
        resized_video = video.crop(x1=x1, y1=y1, x2=x1 + new_width, y2=y1 + new_height)
        
        # Generate output path if not provided
        if not output_path:
            output_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4").name
        
        # Write video
        with st.spinner(f"Resizing video to {aspect_ratio}..."):
            resized_video.write_videofile(
                output_path,
                verbose=False,
                logger=None,
                codec="libx264",
                audio_codec="aac"
            )
        
        # Close clips
        video.close()
        resized_video.close()
        
        return output_path
    
    except Exception as e:
        st.error(f"Error resizing video: {str(e)}")
        return None


# ============================================================================
# VIDEO INFORMATION
# ============================================================================

def get_video_info(video_path: str) -> Optional[dict]:
    """
    Get video information
    
    Args:
        video_path: Path to video file
        
    Returns:
        Dictionary with video information or None if retrieval fails
    """
    if VideoFileClip is None:
        st.error("MoviePy is not installed. Cannot get video info.")
        return None
    
    try:
        video = VideoFileClip(video_path)
        
        info = {
            "duration": video.duration,
            "width": video.w,
            "height": video.h,
            "fps": video.fps,
            "resolution": f"{video.w}x{video.h}",
            "aspect_ratio": f"{video.w}:{video.h}",
            "has_audio": video.audio is not None
        }
        
        video.close()
        
        return info
    
    except Exception as e:
        st.error(f"Error getting video info: {str(e)}")
        return None


def format_video_duration(seconds: float) -> str:
    """
    Format video duration to HH:MM:SS
    
    Args:
        seconds: Duration in seconds
        
    Returns:
        Formatted duration string
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    else:
        return f"{minutes:02d}:{secs:02d}"
