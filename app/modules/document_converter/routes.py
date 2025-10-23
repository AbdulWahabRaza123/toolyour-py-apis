"""
Document conversion routes.
"""

from fastapi import APIRouter

from . import controller

router = APIRouter()

# DOCX to PDF conversion
router.add_api_route(
    "/docx-to-pdf",
    controller.convert_docx_to_pdf,
    methods=["POST"],
    summary="Convert DOCX to PDF",
    description="Upload a DOCX file and convert it to PDF format",
    tags=["Document Conversion"]
)

# DOCX to TXT conversion
router.add_api_route(
    "/docx-to-txt",
    controller.convert_docx_to_txt,
    methods=["POST"],
    summary="Convert DOCX to TXT",
    description="Upload a DOCX file and convert it to plain text",
    tags=["Document Conversion"]
)

# TXT to PDF conversion
router.add_api_route(
    "/txt-to-pdf",
    controller.convert_txt_to_pdf,
    methods=["POST"],
    summary="Convert TXT to PDF",
    description="Upload a text file and convert it to PDF format",
    tags=["Document Conversion"]
)

# Get supported conversions
router.add_api_route(
    "/supported-conversions",
    controller.get_supported_conversions,
    methods=["GET"],
    summary="Get supported conversions",
    description="Get list of all supported document format conversions",
    tags=["Document Conversion"]
)

