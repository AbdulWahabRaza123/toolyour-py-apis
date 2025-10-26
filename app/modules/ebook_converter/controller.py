"""
eBook converter controller.
"""

from fastapi import HTTPException, UploadFile, File, Form, status
from fastapi.responses import Response
import structlog

from .service import ebook_converter_service
from .types import EBookConversionOptions

logger = structlog.get_logger(__name__)

# EPUB conversions
async def convert_epub_to_mobi(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_images: bool = Form(True),
    include_metadata: bool = Form(True)
) -> Response:
    """Convert EPUB file to MOBI."""
    try:
        if not file.filename.lower().endswith('.epub'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .epub files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            include_images=include_images,
            include_metadata=include_metadata
        )

        result = await ebook_converter_service.convert_epub_to_mobi(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.mobi'
        return Response(
            content=result.data,
            media_type="application/x-mobipocket-ebook",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_epub_to_mobi controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_epub_to_azw(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_images: bool = Form(True),
    include_metadata: bool = Form(True)
) -> Response:
    """Convert EPUB file to AZW."""
    try:
        if not file.filename.lower().endswith('.epub'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .epub files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            include_images=include_images,
            include_metadata=include_metadata
        )

        result = await ebook_converter_service.convert_epub_to_azw(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.azw'
        return Response(
            content=result.data,
            media_type="application/vnd.amazon.ebook",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_epub_to_azw controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_epub_to_fb2(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_metadata: bool = Form(True)
) -> Response:
    """Convert EPUB file to FB2."""
    try:
        if not file.filename.lower().endswith('.epub'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .epub files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            include_metadata=include_metadata
        )

        result = await ebook_converter_service.convert_epub_to_fb2(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.fb2'
        return Response(
            content=result.data,
            media_type="application/x-fictionbook+xml",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_epub_to_fb2 controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_epub_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert EPUB file to TXT."""
    try:
        if not file.filename.lower().endswith('.epub'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .epub files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(encoding=encoding)

        result = await ebook_converter_service.convert_epub_to_txt(file_content, options)

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
        logger.error("Error in convert_epub_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_epub_to_html(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_images: bool = Form(True)
) -> Response:
    """Convert EPUB file to HTML."""
    try:
        if not file.filename.lower().endswith('.epub'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .epub files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            include_images=include_images
        )

        result = await ebook_converter_service.convert_epub_to_html(file_content, options)

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
        logger.error("Error in convert_epub_to_html controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_epub_to_pdf(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    quality: str = Form("high")
) -> Response:
    """Convert EPUB file to PDF."""
    try:
        if not file.filename.lower().endswith('.epub'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .epub files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            quality=quality
        )

        result = await ebook_converter_service.convert_epub_to_pdf(file_content, options)

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
        logger.error("Error in convert_epub_to_pdf controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_epub_to_docx(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_images: bool = Form(True)
) -> Response:
    """Convert EPUB file to DOCX."""
    try:
        if not file.filename.lower().endswith('.epub'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .epub files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            include_images=include_images
        )

        result = await ebook_converter_service.convert_epub_to_docx(file_content, options)

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
        logger.error("Error in convert_epub_to_docx controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

# MOBI conversions
async def convert_mobi_to_epub(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_images: bool = Form(True)
) -> Response:
    """Convert MOBI file to EPUB."""
    try:
        if not file.filename.lower().endswith('.mobi'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .mobi files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            include_images=include_images
        )

        result = await ebook_converter_service.convert_mobi_to_epub(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.epub'
        return Response(
            content=result.data,
            media_type="application/epub+zip",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_mobi_to_epub controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_mobi_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert MOBI file to TXT."""
    try:
        if not file.filename.lower().endswith('.mobi'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .mobi files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(encoding=encoding)

        result = await ebook_converter_service.convert_mobi_to_txt(file_content, options)

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
        logger.error("Error in convert_mobi_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_mobi_to_html(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert MOBI file to HTML."""
    try:
        if not file.filename.lower().endswith('.mobi'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .mobi files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(encoding=encoding)

        result = await ebook_converter_service.convert_mobi_to_html(file_content, options)

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
        logger.error("Error in convert_mobi_to_html controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_mobi_to_pdf(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    quality: str = Form("high")
) -> Response:
    """Convert MOBI file to PDF."""
    try:
        if not file.filename.lower().endswith('.mobi'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .mobi files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            quality=quality
        )

        result = await ebook_converter_service.convert_mobi_to_pdf(file_content, options)

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
        logger.error("Error in convert_mobi_to_pdf controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

# AZW conversions
async def convert_azw_to_epub(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_images: bool = Form(True)
) -> Response:
    """Convert AZW file to EPUB."""
    try:
        if not file.filename.lower().endswith('.azw'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .azw files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            include_images=include_images
        )

        result = await ebook_converter_service.convert_azw_to_epub(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.epub'
        return Response(
            content=result.data,
            media_type="application/epub+zip",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_azw_to_epub controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_azw_to_mobi(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert AZW file to MOBI."""
    try:
        if not file.filename.lower().endswith('.azw'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .azw files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(encoding=encoding)

        result = await ebook_converter_service.convert_azw_to_mobi(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.mobi'
        return Response(
            content=result.data,
            media_type="application/x-mobipocket-ebook",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_azw_to_mobi controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_azw_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert AZW file to TXT."""
    try:
        if not file.filename.lower().endswith('.azw'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .azw files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(encoding=encoding)

        result = await ebook_converter_service.convert_azw_to_txt(file_content, options)

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
        logger.error("Error in convert_azw_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_azw_to_html(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert AZW file to HTML."""
    try:
        if not file.filename.lower().endswith('.azw'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .azw files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(encoding=encoding)

        result = await ebook_converter_service.convert_azw_to_html(file_content, options)

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
        logger.error("Error in convert_azw_to_html controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_azw_to_pdf(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    quality: str = Form("high")
) -> Response:
    """Convert AZW file to PDF."""
    try:
        if not file.filename.lower().endswith('.azw'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .azw files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            quality=quality
        )

        result = await ebook_converter_service.convert_azw_to_pdf(file_content, options)

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
        logger.error("Error in convert_azw_to_pdf controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

# FB2 conversions
async def convert_fb2_to_epub(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_metadata: bool = Form(True)
) -> Response:
    """Convert FB2 file to EPUB."""
    try:
        if not file.filename.lower().endswith('.fb2'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .fb2 files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            include_metadata=include_metadata
        )

        result = await ebook_converter_service.convert_fb2_to_epub(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.epub'
        return Response(
            content=result.data,
            media_type="application/epub+zip",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_fb2_to_epub controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_fb2_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert FB2 file to TXT."""
    try:
        if not file.filename.lower().endswith('.fb2'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .fb2 files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(encoding=encoding)

        result = await ebook_converter_service.convert_fb2_to_txt(file_content, options)

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
        logger.error("Error in convert_fb2_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_fb2_to_html(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert FB2 file to HTML."""
    try:
        if not file.filename.lower().endswith('.fb2'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .fb2 files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(encoding=encoding)

        result = await ebook_converter_service.convert_fb2_to_html(file_content, options)

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
        logger.error("Error in convert_fb2_to_html controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_fb2_to_pdf(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    quality: str = Form("high")
) -> Response:
    """Convert FB2 file to PDF."""
    try:
        if not file.filename.lower().endswith('.fb2'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .fb2 files are supported"
            )

        file_content = await file.read()
        options = EBookConversionOptions(
            encoding=encoding,
            quality=quality
        )

        result = await ebook_converter_service.convert_fb2_to_pdf(file_content, options)

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
        logger.error("Error in convert_fb2_to_pdf controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def get_supported_conversions():
    """Get list of supported eBook conversions."""
    return await ebook_converter_service.get_supported_conversions()
