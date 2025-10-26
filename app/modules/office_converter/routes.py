"""
Office converter routes.
"""

from fastapi import APIRouter

from . import controller

router = APIRouter()

# XLS conversions
router.add_api_route(
    "/xls-to-xlsx",
    controller.convert_xls_to_xlsx,
    methods=["POST"],
    summary="Convert XLS to XLSX",
    description="Upload an XLS file and convert it to XLSX format",
    tags=["Office Conversion"]
)

router.add_api_route(
    "/xls-to-csv",
    controller.convert_xls_to_csv,
    methods=["POST"],
    summary="Convert XLS to CSV",
    description="Upload an XLS file and convert it to CSV format",
    tags=["Office Conversion"]
)

router.add_api_route(
    "/xls-to-txt",
    controller.convert_xls_to_txt,
    methods=["POST"],
    summary="Convert XLS to TXT",
    description="Upload an XLS file and convert it to plain text",
    tags=["Office Conversion"]
)

router.add_api_route(
    "/xls-to-json",
    controller.convert_xls_to_json,
    methods=["POST"],
    summary="Convert XLS to JSON",
    description="Upload an XLS file and convert it to JSON format",
    tags=["Office Conversion"]
)

# XLSX conversions
router.add_api_route(
    "/xlsx-to-xls",
    controller.convert_xlsx_to_xls,
    methods=["POST"],
    summary="Convert XLSX to XLS",
    description="Upload an XLSX file and convert it to XLS format",
    tags=["Office Conversion"]
)

router.add_api_route(
    "/xlsx-to-csv",
    controller.convert_xlsx_to_csv,
    methods=["POST"],
    summary="Convert XLSX to CSV",
    description="Upload an XLSX file and convert it to CSV format",
    tags=["Office Conversion"]
)

router.add_api_route(
    "/xlsx-to-txt",
    controller.convert_xlsx_to_txt,
    methods=["POST"],
    summary="Convert XLSX to TXT",
    description="Upload an XLSX file and convert it to plain text",
    tags=["Office Conversion"]
)

router.add_api_route(
    "/xlsx-to-json",
    controller.convert_xlsx_to_json,
    methods=["POST"],
    summary="Convert XLSX to JSON",
    description="Upload an XLSX file and convert it to JSON format",
    tags=["Office Conversion"]
)

# PPT conversions
router.add_api_route(
    "/ppt-to-pptx",
    controller.convert_ppt_to_pptx,
    methods=["POST"],
    summary="Convert PPT to PPTX",
    description="Upload a PPT file and convert it to PPTX format",
    tags=["Office Conversion"]
)

router.add_api_route(
    "/ppt-to-txt",
    controller.convert_ppt_to_txt,
    methods=["POST"],
    summary="Convert PPT to TXT",
    description="Upload a PPT file and convert it to plain text",
    tags=["Office Conversion"]
)

# PPTX conversions
router.add_api_route(
    "/pptx-to-txt",
    controller.convert_pptx_to_txt,
    methods=["POST"],
    summary="Convert PPTX to TXT",
    description="Upload a PPTX file and convert it to plain text",
    tags=["Office Conversion"]
)

router.add_api_route(
    "/pptx-to-html",
    controller.convert_pptx_to_html,
    methods=["POST"],
    summary="Convert PPTX to HTML",
    description="Upload a PPTX file and convert it to HTML format",
    tags=["Office Conversion"]
)

# Get supported conversions
router.add_api_route(
    "/supported-conversions",
    controller.get_supported_conversions,
    methods=["GET"],
    summary="Get supported office conversions",
    description="Get list of all supported office format conversions",
    tags=["Office Conversion"]
)
