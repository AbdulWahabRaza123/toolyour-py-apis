"""
Web converter types.
"""

from pydantic import BaseModel
from typing import Optional


class WebConversionOptions(BaseModel):
    """Options for web format conversions."""
    
    encoding: str = "utf-8"
    pretty_print: bool = True
    include_headers: bool = True
    delimiter: str = ","
    quote_char: str = '"'
    escape_char: str = "\\"


class WebServiceResponse(BaseModel):
    """Response model for web conversion service."""
    
    status: int
    message: str
    data: Optional[bytes] = None
    format: Optional[str] = None
    error: Optional[str] = None
