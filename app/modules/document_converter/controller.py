"""
Document conversion controller.
Handles HTTP requests for document conversion.
"""

from typing import Optional
from fastapi import UploadFile, File, Form, HTTPException, status
from fastapi.responses import Response

from .service import document_converter_service
from .types import ConversionOptions
import structlog

logger = structlog.get_logger(__name__)


async def convert_docx_to_pdf(
    file: UploadFile = File(...),
    page_size: str = Form("A4"),
    orientation: str = Form("portrait"),
    margin: int = Form(20),
) -> Response:
    """
    Convert DOCX file to PDF.
    
    Args:
        file: Uploaded DOCX file
        page_size: Page size (A4, letter, legal)
        orientation: Page orientation (portrait, landscape)
        margin: Page margin in mm
        
    Returns:
        PDF file as response
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .docx files are supported"
            )

        # Read file content
        file_content = await file.read()

        # Create conversion options
        options = ConversionOptions(
            page_size=page_size,
            orientation=orientation,
            margin=margin
        )

        # Convert document
        result = await document_converter_service.convert_docx_to_pdf(
            file_content,
            options
        )

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        # Return PDF file
        filename = file.filename.rsplit('.', 1)[0] + '.pdf'
        
        return Response(
            content=result.data,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_docx_to_pdf controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


async def convert_docx_to_txt(
    file: UploadFile = File(...),
) -> Response:
    """
    Convert DOCX file to plain text.
    
    Args:
        file: Uploaded DOCX file
        
    Returns:
        Text file as response
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .docx files are supported"
            )

        # Read file content
        file_content = await file.read()

        # Convert document
        result = await document_converter_service.convert_docx_to_txt(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        # Return text file
        filename = file.filename.rsplit('.', 1)[0] + '.txt'
        
        return Response(
            content=result.data,
            media_type="text/plain",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_docx_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


async def convert_txt_to_pdf(
    file: UploadFile = File(...),
    page_size: str = Form("A4"),
    orientation: str = Form("portrait"),
    margin: int = Form(20),
) -> Response:
    """
    Convert plain text file to PDF.
    
    Args:
        file: Uploaded text file
        page_size: Page size (A4, letter, legal)
        orientation: Page orientation (portrait, landscape)
        margin: Page margin in mm
        
    Returns:
        PDF file as response
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.txt'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .txt files are supported"
            )

        # Read file content
        file_content = await file.read()

        # Create conversion options
        options = ConversionOptions(
            page_size=page_size,
            orientation=orientation,
            margin=margin
        )

        # Convert document
        result = await document_converter_service.convert_txt_to_pdf(
            file_content,
            options
        )

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        # Return PDF file
        filename = file.filename.rsplit('.', 1)[0] + '.pdf'
        
        return Response(
            content=result.data,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_txt_to_pdf controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


async def get_supported_conversions():
    """
    Get list of supported document conversions.
    
    Returns:
        Dictionary of supported conversions
    """
    return {
        "supported_conversions": document_converter_service.supported_conversions,
        "message": "List of supported document format conversions"
    }

