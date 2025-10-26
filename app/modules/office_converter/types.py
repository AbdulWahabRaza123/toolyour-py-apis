"""
Office converter types.
"""

from pydantic import BaseModel
from typing import Optional


class OfficeConversionOptions(BaseModel):
    """Options for office format conversions."""
    
    encoding: str = "utf-8"
    include_formatting: bool = True
    include_images: bool = True
    include_charts: bool = True
    sheet_name: Optional[str] = None
    slide_number: Optional[int] = None


class OfficeServiceResponse(BaseModel):
    """Response model for office conversion service."""
    
    status: int
    message: str
    data: Optional[bytes] = None
    format: Optional[str] = None
    error: Optional[str] = None
