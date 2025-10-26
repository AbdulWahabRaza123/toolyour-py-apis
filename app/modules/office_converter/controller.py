"""
Office converter controller.
"""

from fastapi import HTTPException, UploadFile, File, Form, status
from fastapi.responses import Response
import structlog

from .service import office_converter_service
from .types import OfficeConversionOptions

logger = structlog.get_logger(__name__)

# XLS conversions
async def convert_xls_to_xlsx(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_formatting: bool = Form(True)
) -> Response:
    """Convert XLS file to XLSX."""
    try:
        if not file.filename.lower().endswith('.xls'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xls files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            include_formatting=include_formatting
        )

        result = await office_converter_service.convert_xls_to_xlsx(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.xlsx'
        return Response(
            content=result.data,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_xls_to_xlsx controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_xls_to_csv(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    sheet_name: str = Form(None)
) -> Response:
    """Convert XLS file to CSV."""
    try:
        if not file.filename.lower().endswith('.xls'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xls files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            sheet_name=sheet_name
        )

        result = await office_converter_service.convert_xls_to_csv(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.csv'
        return Response(
            content=result.data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_xls_to_csv controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_xls_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    sheet_name: str = Form(None)
) -> Response:
    """Convert XLS file to TXT."""
    try:
        if not file.filename.lower().endswith('.xls'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xls files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            sheet_name=sheet_name
        )

        result = await office_converter_service.convert_xls_to_txt(file_content, options)

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
        logger.error("Error in convert_xls_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_xls_to_json(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    sheet_name: str = Form(None)
) -> Response:
    """Convert XLS file to JSON."""
    try:
        if not file.filename.lower().endswith('.xls'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xls files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            sheet_name=sheet_name
        )

        result = await office_converter_service.convert_xls_to_json(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.json'
        return Response(
            content=result.data,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_xls_to_json controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

# XLSX conversions
async def convert_xlsx_to_xls(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_formatting: bool = Form(True)
) -> Response:
    """Convert XLSX file to XLS."""
    try:
        if not file.filename.lower().endswith('.xlsx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xlsx files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            include_formatting=include_formatting
        )

        result = await office_converter_service.convert_xlsx_to_xls(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.xls'
        return Response(
            content=result.data,
            media_type="application/vnd.ms-excel",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_xlsx_to_xls controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_xlsx_to_csv(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    sheet_name: str = Form(None)
) -> Response:
    """Convert XLSX file to CSV."""
    try:
        if not file.filename.lower().endswith('.xlsx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xlsx files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            sheet_name=sheet_name
        )

        result = await office_converter_service.convert_xlsx_to_csv(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.csv'
        return Response(
            content=result.data,
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_xlsx_to_csv controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_xlsx_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    sheet_name: str = Form(None)
) -> Response:
    """Convert XLSX file to TXT."""
    try:
        if not file.filename.lower().endswith('.xlsx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xlsx files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            sheet_name=sheet_name
        )

        result = await office_converter_service.convert_xlsx_to_txt(file_content, options)

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
        logger.error("Error in convert_xlsx_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_xlsx_to_json(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    sheet_name: str = Form(None)
) -> Response:
    """Convert XLSX file to JSON."""
    try:
        if not file.filename.lower().endswith('.xlsx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xlsx files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            sheet_name=sheet_name
        )

        result = await office_converter_service.convert_xlsx_to_json(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.json'
        return Response(
            content=result.data,
            media_type="application/json",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_xlsx_to_json controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

# PPT conversions
async def convert_ppt_to_pptx(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    include_images: bool = Form(True)
) -> Response:
    """Convert PPT file to PPTX."""
    try:
        if not file.filename.lower().endswith('.ppt'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .ppt files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            include_images=include_images
        )

        result = await office_converter_service.convert_ppt_to_pptx(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.pptx'
        return Response(
            content=result.data,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_ppt_to_pptx controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_ppt_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert PPT file to TXT."""
    try:
        if not file.filename.lower().endswith('.ppt'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .ppt files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(encoding=encoding)

        result = await office_converter_service.convert_ppt_to_txt(file_content, options)

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
        logger.error("Error in convert_ppt_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

# PPTX conversions
async def convert_pptx_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    slide_number: int = Form(None)
) -> Response:
    """Convert PPTX file to TXT."""
    try:
        if not file.filename.lower().endswith('.pptx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .pptx files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            slide_number=slide_number
        )

        result = await office_converter_service.convert_pptx_to_txt(file_content, options)

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
        logger.error("Error in convert_pptx_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_pptx_to_html(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    slide_number: int = Form(None)
) -> Response:
    """Convert PPTX file to HTML."""
    try:
        if not file.filename.lower().endswith('.pptx'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .pptx files are supported"
            )

        file_content = await file.read()
        options = OfficeConversionOptions(
            encoding=encoding,
            slide_number=slide_number
        )

        result = await office_converter_service.convert_pptx_to_html(file_content, options)

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
        logger.error("Error in convert_pptx_to_html controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def get_supported_conversions():
    """Get list of supported office conversions."""
    return await office_converter_service.get_supported_conversions()
