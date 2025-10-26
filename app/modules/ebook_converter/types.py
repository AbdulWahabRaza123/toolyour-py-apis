"""
eBook converter types.
"""

from pydantic import BaseModel
from typing import Optional


class EBookConversionOptions(BaseModel):
    """Options for eBook format conversions."""
    
    encoding: str = "utf-8"
    include_images: bool = True
    include_metadata: bool = True
    include_toc: bool = True
    quality: str = "high"  # high, medium, low
    format_version: str = "3.0"  # For EPUB versions


class EBookServiceResponse(BaseModel):
    """Response model for eBook conversion service."""
    
    status: int
    message: str
    data: Optional[bytes] = None
    format: Optional[str] = None
    error: Optional[str] = None
