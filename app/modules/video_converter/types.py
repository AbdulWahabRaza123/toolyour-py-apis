"""
Video converter types.
"""

from pydantic import BaseModel, validator
from typing import Optional


class VideoConversionOptions(BaseModel):
    """Options for video format conversions."""
    
    # Video quality settings
    quality: str = "medium"  # low, medium, high, ultra
    resolution: str = "720p"  # 480p, 720p, 1080p, 4k
    bitrate: str = "1000k"  # Video bitrate (e.g., "500k", "1000k", "2000k")
    fps: int = 30  # Frames per second
    
    # Audio settings
    audio_bitrate: str = "128k"  # Audio bitrate
    audio_codec: str = "aac"  # Audio codec (aac, mp3, ac3)
    
    # Processing options
    trim_start: float = 0.0  # Start trimming at this time (seconds)
    trim_end: Optional[float] = None  # End trimming at this time (seconds)
    speed: float = 1.0  # Playback speed (0.5x to 2.0x)
    volume: float = 1.0  # Volume multiplier (0.1 to 2.0)
    
    # Security limits
    max_duration: int = 300  # Maximum duration in seconds (5 minutes)
    max_file_size: int = 100 * 1024 * 1024  # Maximum file size (100MB)
    
    @validator('max_duration')
    def validate_max_duration(cls, v):
        if v > 600:  # 10 minutes absolute maximum
            raise ValueError("Maximum duration cannot exceed 10 minutes (600 seconds)")
        return v
    
    @validator('max_file_size')
    def validate_max_file_size(cls, v):
        if v > 500 * 1024 * 1024:  # 500MB absolute maximum
            raise ValueError("Maximum file size cannot exceed 500MB")
        return v
    
    @validator('speed')
    def validate_speed(cls, v):
        if not 0.25 <= v <= 4.0:
            raise ValueError("Speed must be between 0.25x and 4.0x")
        return v
    
    @validator('volume')
    def validate_volume(cls, v):
        if not 0.1 <= v <= 2.0:
            raise ValueError("Volume must be between 0.1 and 2.0")
        return v


class VideoServiceResponse(BaseModel):
    """Response model for video conversion service."""
    
    status: int
    message: str
    data: Optional[bytes] = None
    format: Optional[str] = None
    duration: Optional[float] = None  # Video duration in seconds
    file_size: Optional[int] = None  # File size in bytes
    resolution: Optional[str] = None  # Video resolution
    bitrate: Optional[str] = None  # Video bitrate
    fps: Optional[int] = None  # Frames per second
    error: Optional[str] = None
