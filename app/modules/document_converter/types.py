"""
Type definitions for document conversion module.
"""

from typing import Optional, Union
from pydantic import BaseModel


class ServiceResponse(BaseModel):
    """Standard service response model."""
    status: int
    message: str
    data: Optional[Union[bytes, str, dict]] = None
    format: Optional[str] = None
    error: Optional[str] = None


class FileInput(BaseModel):
    """File input model."""
    file_buffer: bytes
    filename: Optional[str] = None


class ConversionOptions(BaseModel):
    """Options for document conversion."""
    quality: int = 100
    page_size: str = "A4"  # A4, Letter, Legal
    orientation: str = "portrait"  # portrait, landscape
    margin: int = 20  # margin in mm

