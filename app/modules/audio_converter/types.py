"""
Audio converter types.
"""

from pydantic import BaseModel
from typing import Optional


class AudioConversionOptions(BaseModel):
    """Options for audio format conversions."""
    
    bitrate: str = "192k"  # Audio bitrate (e.g., "128k", "192k", "320k")
    sample_rate: int = 44100  # Sample rate in Hz
    channels: int = 2  # Number of audio channels (1=mono, 2=stereo)
    quality: str = "high"  # Quality setting (low, medium, high, lossless)
    normalize: bool = True  # Normalize audio levels
    fade_in: float = 0.0  # Fade in duration in seconds
    fade_out: float = 0.0  # Fade out duration in seconds
    trim_start: float = 0.0  # Start trimming at this time (seconds)
    trim_end: Optional[float] = None  # End trimming at this time (seconds)


class AudioServiceResponse(BaseModel):
    """Response model for audio conversion service."""
    
    status: int
    message: str
    data: Optional[bytes] = None
    format: Optional[str] = None
    duration: Optional[float] = None  # Audio duration in seconds
    bitrate: Optional[str] = None
    sample_rate: Optional[int] = None
    channels: Optional[int] = None
    error: Optional[str] = None
