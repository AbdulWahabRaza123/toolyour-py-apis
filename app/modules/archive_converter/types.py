"""
Archive converter types.
"""

from pydantic import BaseModel
from typing import Optional


class ArchiveConversionOptions(BaseModel):
    """Options for archive format conversions."""
    
    compression_level: int = 6  # 0-9, where 9 is maximum compression
    password: Optional[str] = None
    include_hidden: bool = False
    preserve_permissions: bool = True
    compression_method: str = "deflate"  # deflate, bzip2, lzma


class ArchiveServiceResponse(BaseModel):
    """Response model for archive conversion service."""
    
    status: int
    message: str
    data: Optional[bytes] = None
    format: Optional[str] = None
    error: Optional[str] = None
