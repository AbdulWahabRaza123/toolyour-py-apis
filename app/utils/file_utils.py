"""
File utilities.
"""

import os
from typing import List
from fastapi import UploadFile

from app.core.config import settings, get_allowed_extensions


def validate_file_type(file: UploadFile) -> bool:
    """Validate file type based on extension."""
    allowed_extensions = get_allowed_extensions()
    
    # Check file extension
    if not file.filename:
        return False
    
    file_extension = os.path.splitext(file.filename)[1].lower().lstrip('.')
    if file_extension not in allowed_extensions:
        return False
    
    return True


def validate_file_size(file: UploadFile, max_size: int) -> bool:
    """Validate file size."""
    if file.size and file.size > max_size:
        return False
    return True


def get_file_extension(filename: str) -> str:
    """Get file extension from filename."""
    return os.path.splitext(filename)[1].lower().lstrip('.')


def is_image_file(filename: str) -> bool:
    """Check if file is an image."""
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp']
    return get_file_extension(filename) in image_extensions


def is_document_file(filename: str) -> bool:
    """Check if file is a document."""
    doc_extensions = ['pdf', 'doc', 'docx', 'txt', 'rtf']
    return get_file_extension(filename) in doc_extensions


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage."""
    # Remove or replace unsafe characters
    unsafe_chars = '<>:"/\\|?*'
    for char in unsafe_chars:
        filename = filename.replace(char, '_')
    
    # Limit filename length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:255-len(ext)] + ext
    
    return filename
