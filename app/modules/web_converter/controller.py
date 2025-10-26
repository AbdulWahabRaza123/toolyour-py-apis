"""
Web converter controller.
"""

from fastapi import HTTPException, UploadFile, File, Form, status
from fastapi.responses import Response
import structlog

from .service import web_converter_service
from .types import WebConversionOptions

logger = structlog.get_logger(__name__)

# HTML conversions
async def convert_html_to_xml(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    pretty_print: bool = Form(True)
) -> Response:
    """Convert HTML file to XML."""
    try:
        if not file.filename.lower().endswith('.html'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .html files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(
            encoding=encoding,
            pretty_print=pretty_print
        )

        result = await web_converter_service.convert_html_to_xml(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.xml'
        return Response(
            content=result.data,
            media_type="application/xml",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_html_to_xml controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_html_to_json(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    pretty_print: bool = Form(True)
) -> Response:
    """Convert HTML file to JSON."""
    try:
        if not file.filename.lower().endswith('.html'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .html files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(
            encoding=encoding,
            pretty_print=pretty_print
        )

        result = await web_converter_service.convert_html_to_json(file_content, options)

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
        logger.error("Error in convert_html_to_json controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

# XML conversions
async def convert_xml_to_html(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert XML file to HTML."""
    try:
        if not file.filename.lower().endswith('.xml'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xml files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(encoding=encoding)

        result = await web_converter_service.convert_xml_to_html(file_content, options)

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
        logger.error("Error in convert_xml_to_html controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_xml_to_json(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    pretty_print: bool = Form(True)
) -> Response:
    """Convert XML file to JSON."""
    try:
        if not file.filename.lower().endswith('.xml'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xml files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(
            encoding=encoding,
            pretty_print=pretty_print
        )

        result = await web_converter_service.convert_xml_to_json(file_content, options)

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
        logger.error("Error in convert_xml_to_json controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_xml_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert XML file to TXT."""
    try:
        if not file.filename.lower().endswith('.xml'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xml files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(encoding=encoding)

        result = await web_converter_service.convert_xml_to_txt(file_content, options)

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
        logger.error("Error in convert_xml_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_xml_to_csv(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    delimiter: str = Form(","),
    include_headers: bool = Form(True)
) -> Response:
    """Convert XML file to CSV."""
    try:
        if not file.filename.lower().endswith('.xml'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .xml files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(
            encoding=encoding,
            delimiter=delimiter,
            include_headers=include_headers
        )

        result = await web_converter_service.convert_xml_to_csv(file_content, options)

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
        logger.error("Error in convert_xml_to_csv controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

# JSON conversions
async def convert_json_to_html(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert JSON file to HTML."""
    try:
        if not file.filename.lower().endswith('.json'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .json files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(encoding=encoding)

        result = await web_converter_service.convert_json_to_html(file_content, options)

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
        logger.error("Error in convert_json_to_html controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_json_to_xml(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert JSON file to XML."""
    try:
        if not file.filename.lower().endswith('.json'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .json files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(encoding=encoding)

        result = await web_converter_service.convert_json_to_xml(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.xml'
        return Response(
            content=result.data,
            media_type="application/xml",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_json_to_xml controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_json_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8")
) -> Response:
    """Convert JSON file to TXT."""
    try:
        if not file.filename.lower().endswith('.json'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .json files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(encoding=encoding)

        result = await web_converter_service.convert_json_to_txt(file_content, options)

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
        logger.error("Error in convert_json_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_json_to_csv(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    delimiter: str = Form(","),
    include_headers: bool = Form(True)
) -> Response:
    """Convert JSON file to CSV."""
    try:
        if not file.filename.lower().endswith('.json'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .json files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(
            encoding=encoding,
            delimiter=delimiter,
            include_headers=include_headers
        )

        result = await web_converter_service.convert_json_to_csv(file_content, options)

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
        logger.error("Error in convert_json_to_csv controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

# CSV conversions
async def convert_csv_to_html(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    delimiter: str = Form(","),
    include_headers: bool = Form(True)
) -> Response:
    """Convert CSV file to HTML."""
    try:
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .csv files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(
            encoding=encoding,
            delimiter=delimiter,
            include_headers=include_headers
        )

        result = await web_converter_service.convert_csv_to_html(file_content, options)

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
        logger.error("Error in convert_csv_to_html controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_csv_to_xml(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    delimiter: str = Form(",")
) -> Response:
    """Convert CSV file to XML."""
    try:
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .csv files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(
            encoding=encoding,
            delimiter=delimiter
        )

        result = await web_converter_service.convert_csv_to_xml(file_content, options)

        if result.status != 200:
            raise HTTPException(
                status_code=result.status,
                detail=result.message
            )

        filename = file.filename.rsplit('.', 1)[0] + '.xml'
        return Response(
            content=result.data,
            media_type="application/xml",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error in convert_csv_to_xml controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_csv_to_json(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    delimiter: str = Form(","),
    pretty_print: bool = Form(True)
) -> Response:
    """Convert CSV file to JSON."""
    try:
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .csv files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(
            encoding=encoding,
            delimiter=delimiter,
            pretty_print=pretty_print
        )

        result = await web_converter_service.convert_csv_to_json(file_content, options)

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
        logger.error("Error in convert_csv_to_json controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def convert_csv_to_txt(
    file: UploadFile = File(...),
    encoding: str = Form("utf-8"),
    delimiter: str = Form(","),
    include_headers: bool = Form(True)
) -> Response:
    """Convert CSV file to TXT."""
    try:
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only .csv files are supported"
            )

        file_content = await file.read()
        options = WebConversionOptions(
            encoding=encoding,
            delimiter=delimiter,
            include_headers=include_headers
        )

        result = await web_converter_service.convert_csv_to_txt(file_content, options)

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
        logger.error("Error in convert_csv_to_txt controller", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error converting file: {str(e)}"
        )

async def get_supported_conversions():
    """Get list of supported web conversions."""
    return await web_converter_service.get_supported_conversions()
