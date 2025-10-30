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
import json as _json
import io as _io
from typing import List

logger = structlog.get_logger(__name__)


async def convert_docx_to_pdf(
    file: UploadFile = File(None),
    page_size: str = Form("A4"),
    orientation: str = Form("portrait"),
    margin: int = Form(20),
    files: List[UploadFile] = File(None),
    archive: UploadFile = File(None),
    urls: Optional[str] = Form(None),
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
        # Batch mode
        if (files and len(files) > 0) or archive is not None or urls:
            items: list[tuple[str, bytes]] = []
            if files:
                for f in files:
                    items.append((f.filename, await f.read()))
            if archive is not None:
                items.extend(await document_converter_service.extract_archive(archive.filename, await archive.read()))
            if urls:
                try:
                    url_list = _json.loads(urls)
                    if not isinstance(url_list, list):
                        raise ValueError()
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid urls payload. Provide JSON array of strings.")
                items.extend(await document_converter_service.download_urls(url_list))
            result = await document_converter_service.batch_convert(items, target_format="pdf", allowed_sources=["docx"])
            if result.status != 200:
                raise HTTPException(status_code=result.status, detail=result.message)
            return Response(content=result.data, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=batch_docx_to_pdf.zip"})

        # Single
        if file is None or not file.filename.lower().endswith('.docx'):
            raise HTTPException(status_code=400, detail="Provide a .docx file or use files/archive/urls for batch")
        file_content = await file.read()
        options = ConversionOptions(page_size=page_size, orientation=orientation, margin=margin)
        result = await document_converter_service.convert_docx_to_pdf(file_content, options)
        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        filename = file.filename.rsplit('.', 1)[0] + '.pdf'
        return Response(content=result.data, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}"})

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


async def convert_docx_to_rtf(
    file: UploadFile = File(...),
) -> Response:
    """
    Convert DOCX file to RTF.
    """
    try:
        if not file.filename.lower().endswith('.docx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .docx files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_docx_to_rtf(file_content)

        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        filename = file.filename.rsplit('.', 1)[0] + '.rtf'
        return Response(
            content=result.data,
            media_type="application/rtf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_docx_to_rtf controller", error=str(e))
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
    file: UploadFile = File(None),
    files: List[UploadFile] = File(None),
    archive: UploadFile = File(None),
    urls: Optional[str] = Form(None),
) -> Response:
    """
    Convert PDF file to plain text.
    
    Args:
        file: Uploaded PDF file
        
    Returns:
        Text file as response
    """
    try:
        if (files and len(files) > 0) or archive is not None or urls:
            items: list[tuple[str, bytes]] = []
            if files:
                for f in files:
                    items.append((f.filename, await f.read()))
            if archive is not None:
                items.extend(await document_converter_service.extract_archive(archive.filename, await archive.read()))
            if urls:
                try:
                    url_list = _json.loads(urls)
                    if not isinstance(url_list, list):
                        raise ValueError()
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid urls payload. Provide JSON array of strings.")
                items.extend(await document_converter_service.download_urls(url_list))
            result = await document_converter_service.batch_convert(items, target_format="txt", allowed_sources=["pdf"])
            if result.status != 200:
                raise HTTPException(status_code=result.status, detail=result.message)
            return Response(content=result.data, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=batch_pdf_to_txt.zip"})

        if file is None or not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Provide a .pdf file or use files/archive/urls for batch")
        file_content = await file.read()
        result = await document_converter_service.convert_pdf_to_txt(file_content)
        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        filename = file.filename.rsplit('.', 1)[0] + '.txt'
        return Response(content=result.data, media_type="text/plain", headers={"Content-Disposition": f"attachment; filename={filename}"})

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_pdf_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


async def convert_txt_to_docx(
    file: UploadFile = File(None),
    files: List[UploadFile] = File(None),
    archive: UploadFile = File(None),
    urls: Optional[str] = Form(None),
) -> Response:
    """
    Convert text file to DOCX.
    
    Args:
        file: Uploaded text file
        
    Returns:
        DOCX file as response
    """
    try:
        if (files and len(files) > 0) or archive is not None or urls:
            items: list[tuple[str, bytes]] = []
            if files:
                for f in files:
                    items.append((f.filename, await f.read()))
            if archive is not None:
                items.extend(await document_converter_service.extract_archive(archive.filename, await archive.read()))
            if urls:
                try:
                    url_list = _json.loads(urls)
                    if not isinstance(url_list, list):
                        raise ValueError()
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid urls payload. Provide JSON array of strings.")
                items.extend(await document_converter_service.download_urls(url_list))
            result = await document_converter_service.batch_convert(items, target_format="docx", allowed_sources=["txt"])
            if result.status != 200:
                raise HTTPException(status_code=result.status, detail=result.message)
            return Response(content=result.data, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=batch_txt_to_docx.zip"})

        if file is None or not file.filename.lower().endswith('.txt'):
            raise HTTPException(status_code=400, detail="Provide a .txt file or use files/archive/urls for batch")
        file_content = await file.read()
        result = await document_converter_service.convert_txt_to_docx(file_content)
        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        filename = file.filename.rsplit('.', 1)[0] + '.docx'
        return Response(content=result.data, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": f"attachment; filename={filename}"})

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_txt_to_docx controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )


async def convert_txt_to_rtf(
    file: UploadFile = File(...),
) -> Response:
    """Convert TXT file to RTF."""
    try:
        if not file.filename.lower().endswith('.txt'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .txt files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_txt_to_rtf(file_content)

        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        filename = file.filename.rsplit('.', 1)[0] + '.rtf'
        return Response(
            content=result.data,
            media_type="application/rtf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_txt_to_rtf controller", error=str(e))
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


async def convert_pdf_to_rtf(
    file: UploadFile = File(...),
) -> Response:
    """
    Convert PDF file to RTF.
    """
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .pdf files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_pdf_to_rtf(file_content)

        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        filename = file.filename.rsplit('.', 1)[0] + '.rtf'
        return Response(
            content=result.data,
            media_type="application/rtf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_pdf_to_rtf controller", error=str(e))
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
    file: UploadFile = File(None),
    page_size: str = Form("A4"),
    orientation: str = Form("portrait"),
    margin: float = Form(20.0),
    files: List[UploadFile] = File(None),
    archive: UploadFile = File(None),
    urls: Optional[str] = Form(None)
) -> Response:
    """Convert Markdown file to PDF."""
    try:
        if (files and len(files) > 0) or archive is not None or urls:
            items: list[tuple[str, bytes]] = []
            if files:
                for f in files:
                    items.append((f.filename, await f.read()))
            if archive is not None:
                items.extend(await document_converter_service.extract_archive(archive.filename, await archive.read()))
            if urls:
                try:
                    url_list = _json.loads(urls)
                    if not isinstance(url_list, list):
                        raise ValueError()
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid urls payload. Provide JSON array of strings.")
                items.extend(await document_converter_service.download_urls(url_list))
            result = await document_converter_service.batch_convert(items, target_format="pdf", allowed_sources=["md"])
            if result.status != 200:
                raise HTTPException(status_code=result.status, detail=result.message)
            return Response(content=result.data, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=batch_md_to_pdf.zip"})

        if file is None or not file.filename.lower().endswith('.md'):
            raise HTTPException(status_code=400, detail="Provide a .md file or use files/archive/urls for batch")
        file_content = await file.read()
        options = ConversionOptions(page_size=page_size, orientation=orientation, margin=margin)
        result = await document_converter_service.convert_md_to_pdf(file_content, options)
        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        filename = file.filename.rsplit('.', 1)[0] + '.pdf'
        return Response(content=result.data, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}"})

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

async def convert_txt_to_md(
    file: UploadFile = File(...),
) -> Response:
    """Convert TXT file to MD."""
    try:
        if not file.filename.lower().endswith('.txt'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .txt files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_txt_to_md(file_content)

        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        filename = file.filename.rsplit('.', 1)[0] + '.md'
        return Response(
            content=result.data,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_txt_to_md controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

async def convert_rtf_to_txt(
    file: UploadFile = File(...),
) -> Response:
    """Convert RTF file to TXT."""
    try:
        if not file.filename.lower().endswith('.rtf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .rtf files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_rtf_to_txt(file_content)

        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        filename = file.filename.rsplit('.', 1)[0] + '.txt'
        return Response(
            content=result.data,
            media_type="text/plain",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_rtf_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

async def convert_rtf_to_pdf(
    file: UploadFile = File(None),
    files: List[UploadFile] = File(None),
    archive: UploadFile = File(None),
    urls: Optional[str] = Form(None),
) -> Response:
    """Convert RTF file to PDF."""
    try:
        if (files and len(files) > 0) or archive is not None or urls:
            items: list[tuple[str, bytes]] = []
            if files:
                for f in files:
                    items.append((f.filename, await f.read()))
            if archive is not None:
                items.extend(await document_converter_service.extract_archive(archive.filename, await archive.read()))
            if urls:
                try:
                    url_list = _json.loads(urls)
                    if not isinstance(url_list, list):
                        raise ValueError()
                except Exception:
                    raise HTTPException(status_code=400, detail="Invalid urls payload. Provide JSON array of strings.")
                items.extend(await document_converter_service.download_urls(url_list))
            result = await document_converter_service.batch_convert(items, target_format="pdf", allowed_sources=["rtf"])
            if result.status != 200:
                raise HTTPException(status_code=result.status, detail=result.message)
            return Response(content=result.data, media_type="application/zip", headers={"Content-Disposition": "attachment; filename=batch_rtf_to_pdf.zip"})

        if file is None or not file.filename.lower().endswith('.rtf'):
            raise HTTPException(status_code=400, detail="Provide a .rtf file or use files/archive/urls for batch")
        file_content = await file.read()
        result = await document_converter_service.convert_rtf_to_pdf(file_content)
        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)
        filename = file.filename.rsplit('.', 1)[0] + '.pdf'
        return Response(content=result.data, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename={filename}"})

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_rtf_to_pdf controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting document: {str(e)}"
        )

async def convert_rtf_to_docx(
    file: UploadFile = File(...),
) -> Response:
    """Convert RTF file to DOCX."""
    try:
        if not file.filename.lower().endswith('.rtf'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .rtf files are supported"
            )

        file_content = await file.read()
        result = await document_converter_service.convert_rtf_to_docx(file_buffer=file_content)

        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        filename = file.filename.rsplit('.', 1)[0] + '.docx'
        return Response(
            content=result.data,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_rtf_to_docx controller", error=str(e))
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


async def batch_convert_documents(
    target_format: str = Form(...),
    source_format: Optional[str] = Form(None),
    files: List[UploadFile] = File(None),
    archive: UploadFile = File(None),
    urls: Optional[str] = Form(None),
) -> Response:
    """Batch convert multiple inputs (files/zip/rar/urls) to target format.
    Returns a ZIP containing converted outputs and a manifest.json.
    """
    try:
        # Collect inputs as list of (filename, bytes)
        items: list[tuple[str, bytes]] = []

        # Files
        if files:
            for f in files:
                content = await f.read()
                items.append((f.filename, content))

        # Archive (zip/rar)
        if archive is not None:
            arch_name = archive.filename.lower()
            arch_bytes = await archive.read()
            extracted = await document_converter_service.extract_archive(arch_name, arch_bytes)
            items.extend(extracted)  # list of (filename, bytes)

        # URLs (JSON array string)
        if urls:
            try:
                url_list = _json.loads(urls)
                if not isinstance(url_list, list):
                    raise ValueError("urls must be a JSON array of strings")
            except Exception:
                raise HTTPException(status_code=400, detail="Invalid urls payload. Provide JSON array of strings.")
            downloaded = await document_converter_service.download_urls(url_list)
            items.extend(downloaded)

        if not items:
            raise HTTPException(status_code=400, detail="No inputs provided. Upload files, an archive, or provide urls.")

        # Perform batch conversion
        result = await document_converter_service.batch_convert(items, target_format=target_format, source_format=source_format)
        if result.status != 200:
            raise HTTPException(status_code=result.status, detail=result.message)

        # Return ZIP
        filename = "batch_results.zip"
        return Response(
            content=result.data,
            media_type="application/zip",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in batch_convert_documents controller", error=str(e))
        raise HTTPException(status_code=500, detail=f"Error performing batch conversion: {str(e)}")

