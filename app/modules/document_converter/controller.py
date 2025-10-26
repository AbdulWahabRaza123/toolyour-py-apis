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


async def convert_docx_to_html(
    file: UploadFile = File(...),
) -> Response:
    """
    Convert DOCX file to HTML.
    
    Args:
        file: Uploaded DOCX file
        
    Returns:
        HTML file as response
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
        result = await document_converter_service.convert_docx_to_html(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        # Return HTML file
        filename = file.filename.rsplit('.', 1)[0] + '.html'
        
        return Response(
            content=result.data,
            media_type="text/html",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_docx_to_html controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


async def convert_pdf_to_txt(
    file: UploadFile = File(...),
) -> Response:
    """
    Convert PDF file to plain text.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        Text file as response
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .pdf files are supported"
            )

        # Read file content
        file_content = await file.read()

        # Convert document
        result = await document_converter_service.convert_pdf_to_txt(file_content)

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
        logger.error("Error in convert_pdf_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


async def convert_txt_to_docx(
    file: UploadFile = File(...),
) -> Response:
    """
    Convert text file to DOCX.
    
    Args:
        file: Uploaded text file
        
    Returns:
        DOCX file as response
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

        # Convert document
        result = await document_converter_service.convert_txt_to_docx(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        # Return DOCX file
        filename = file.filename.rsplit('.', 1)[0] + '.docx'
        
        return Response(
            content=result.data,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_txt_to_docx controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


async def convert_pdf_to_docx(
    file: UploadFile = File(...),
) -> Response:
    """
    Convert PDF file to DOCX.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        DOCX file as response
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .pdf files are supported"
            )

        # Read file content
        file_content = await file.read()

        # Convert document
        result = await document_converter_service.convert_pdf_to_docx(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        # Return DOCX file
        filename = file.filename.rsplit('.', 1)[0] + '.docx'
        
        return Response(
            content=result.data,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_pdf_to_docx controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )




async def convert_xlsx_to_csv(
    file: UploadFile = File(...),
) -> Response:
    """
    Convert XLSX file to CSV.
    
    Args:
        file: Uploaded XLSX file
        
    Returns:
        CSV file as response
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.xlsx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xlsx files are supported"
            )

        # Read file content
        file_content = await file.read()

        # Convert document
        result = await document_converter_service.convert_xlsx_to_csv(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        # Return CSV file
        filename = file.filename.rsplit('.', 1)[0] + '.csv'
        
        return Response(
            content=result.data,
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_xlsx_to_csv controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


async def convert_csv_to_xlsx(
    file: UploadFile = File(...),
) -> Response:
    """
    Convert CSV file to XLSX.
    
    Args:
        file: Uploaded CSV file
        
    Returns:
        XLSX file as response
    """
    try:
        # Validate file type
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .csv files are supported"
            )

        # Read file content
        file_content = await file.read()

        # Convert document
        result = await document_converter_service.convert_csv_to_xlsx(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        # Return XLSX file
        filename = file.filename.rsplit('.', 1)[0] + '.xlsx'
        
        return Response(
            content=result.data,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={
                "Content-Disposition": f"attachment; filename={filename}"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_csv_to_xlsx controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


# HTML conversions
async def convert_html_to_pdf(
    file: UploadFile = File(...),
    page_size: str = Form("A4"),
    orientation: str = Form("portrait"),
    margin: float = Form(20.0)
) -> Response:
    """Convert HTML file to PDF."""
    try:
        if not file.filename.lower().endswith('.html'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .html files are supported"
            )

        file_content = await file.read()
        options = ConversionOptions(
            page_size=page_size,
            orientation=orientation,
            margin=margin
        )

        result = await document_converter_service.convert_html_to_pdf(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.pdf'
        return Response(
            content=result.data,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_html_to_pdf controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

async def convert_html_to_docx(
    file: UploadFile = File(...)
) -> Response:
    """Convert HTML file to DOCX."""
    try:
        if not file.filename.lower().endswith('.html'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .html files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_html_to_docx(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.docx'
        return Response(
            content=result.data,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_html_to_docx controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

async def convert_html_to_txt(
    file: UploadFile = File(...)
) -> Response:
    """Convert HTML file to TXT."""
    try:
        if not file.filename.lower().endswith('.html'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .html files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_html_to_txt(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.txt'
        return Response(
            content=result.data,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_html_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

async def convert_html_to_md(
    file: UploadFile = File(...)
) -> Response:
    """Convert HTML file to Markdown."""
    try:
        if not file.filename.lower().endswith('.html'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .html files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_html_to_md(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.md'
        return Response(
            content=result.data,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_html_to_md controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

# Markdown conversions
async def convert_md_to_pdf(
    file: UploadFile = File(...),
    page_size: str = Form("A4"),
    orientation: str = Form("portrait"),
    margin: float = Form(20.0)
) -> Response:
    """Convert Markdown file to PDF."""
    try:
        if not file.filename.lower().endswith('.md'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .md files are supported"
            )

        file_content = await file.read()
        options = ConversionOptions(
            page_size=page_size,
            orientation=orientation,
            margin=margin
        )

        result = await document_converter_service.convert_md_to_pdf(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.pdf'
        return Response(
            content=result.data,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_md_to_pdf controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

async def convert_md_to_docx(
    file: UploadFile = File(...)
) -> Response:
    """Convert Markdown file to DOCX."""
    try:
        if not file.filename.lower().endswith('.md'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .md files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_md_to_docx(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.docx'
        return Response(
            content=result.data,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_md_to_docx controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

async def convert_md_to_txt(
    file: UploadFile = File(...)
) -> Response:
    """Convert Markdown file to TXT."""
    try:
        if not file.filename.lower().endswith('.md'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .md files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_md_to_txt(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.txt'
        return Response(
            content=result.data,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_md_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

async def convert_md_to_html(
    file: UploadFile = File(...)
) -> Response:
    """Convert Markdown file to HTML."""
    try:
        if not file.filename.lower().endswith('.md'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .md files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_md_to_html(file_content)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.html'
        return Response(
            content=result.data,
            media_type="text/html",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_md_to_html controller", error=str(e))
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

