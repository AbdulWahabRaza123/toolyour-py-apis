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

# DOCX to RTF conversion
router.add_api_route(
    "/docx-to-rtf",
    controller.convert_docx_to_rtf,
    methods=["POST"],
    summary="Convert DOCX to RTF",
    description="Upload a DOCX file and convert it to RTF format",
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

# DOCX to HTML conversion
router.add_api_route(
    "/docx-to-html",
    controller.convert_docx_to_html,
    methods=["POST"],
    summary="Convert DOCX to HTML",
    description="Upload a DOCX file and convert it to HTML format",
    tags=["Document Conversion"]
)

# PDF to TXT conversion
router.add_api_route(
    "/pdf-to-txt",
    controller.convert_pdf_to_txt,
    methods=["POST"],
    summary="Convert PDF to TXT",
    description="Upload a PDF file and convert it to plain text",
    tags=["Document Conversion"]
)

# TXT to DOCX conversion
router.add_api_route(
    "/txt-to-docx",
    controller.convert_txt_to_docx,
    methods=["POST"],
    summary="Convert TXT to DOCX",
    description="Upload a text file and convert it to DOCX format",
    tags=["Document Conversion"]
)

# TXT to RTF conversion
router.add_api_route(
    "/txt-to-rtf",
    controller.convert_txt_to_rtf,
    methods=["POST"],
    summary="Convert TXT to RTF",
    description="Upload a text file and convert it to RTF format",
    tags=["Document Conversion"]
)

# TXT to MD conversion
router.add_api_route(
    "/txt-to-md",
    controller.convert_txt_to_md,
    methods=["POST"],
    summary="Convert TXT to MD",
    description="Upload a text file and convert it to Markdown format",
    tags=["Document Conversion"]
)

# RTF to PDF conversion
router.add_api_route(
    "/rtf-to-pdf",
    controller.convert_rtf_to_pdf,
    methods=["POST"],
    summary="Convert RTF to PDF",
    description="Upload an RTF file and convert it to PDF format",
    tags=["Document Conversion"]
)

# RTF to DOCX conversion
router.add_api_route(
    "/rtf-to-docx",
    controller.convert_rtf_to_docx,
    methods=["POST"],
    summary="Convert RTF to DOCX",
    description="Upload an RTF file and convert it to DOCX format",
    tags=["Document Conversion"]
)

# PDF to DOCX conversion
router.add_api_route(
    "/pdf-to-docx",
    controller.convert_pdf_to_docx,
    methods=["POST"],
    summary="Convert PDF to DOCX",
    description="Upload a PDF file and convert it to DOCX format",
    tags=["Document Conversion"]
)

# PDF to RTF conversion
router.add_api_route(
    "/pdf-to-rtf",
    controller.convert_pdf_to_rtf,
    methods=["POST"],
    summary="Convert PDF to RTF",
    description="Upload a PDF file and convert it to RTF format",
    tags=["Document Conversion"]
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
    "/csv-to-xlsx",
    controller.convert_csv_to_xlsx,
    methods=["POST"],
    summary="Convert CSV to XLSX",
    description="Upload a CSV file and convert it to XLSX format",
    tags=["Office Conversion"]
)

# HTML conversions
router.add_api_route(
    "/html-to-pdf",
    controller.convert_html_to_pdf,
    methods=["POST"],
    summary="Convert HTML to PDF",
    description="Upload an HTML file and convert it to PDF format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/html-to-docx",
    controller.convert_html_to_docx,
    methods=["POST"],
    summary="Convert HTML to DOCX",
    description="Upload an HTML file and convert it to DOCX format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/html-to-txt",
    controller.convert_html_to_txt,
    methods=["POST"],
    summary="Convert HTML to TXT",
    description="Upload an HTML file and convert it to plain text",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/html-to-md",
    controller.convert_html_to_md,
    methods=["POST"],
    summary="Convert HTML to Markdown",
    description="Upload an HTML file and convert it to Markdown format",
    tags=["Web Conversion"]
)

# Markdown conversions
router.add_api_route(
    "/md-to-pdf",
    controller.convert_md_to_pdf,
    methods=["POST"],
    summary="Convert Markdown to PDF",
    description="Upload a Markdown file and convert it to PDF format",
    tags=["Document Conversion"]
)

router.add_api_route(
    "/md-to-docx",
    controller.convert_md_to_docx,
    methods=["POST"],
    summary="Convert Markdown to DOCX",
    description="Upload a Markdown file and convert it to DOCX format",
    tags=["Document Conversion"]
)

router.add_api_route(
    "/md-to-txt",
    controller.convert_md_to_txt,
    methods=["POST"],
    summary="Convert Markdown to TXT",
    description="Upload a Markdown file and convert it to plain text",
    tags=["Document Conversion"]
)

router.add_api_route(
    "/md-to-html",
    controller.convert_md_to_html,
    methods=["POST"],
    summary="Convert Markdown to HTML",
    description="Upload a Markdown file and convert it to HTML format",
    tags=["Document Conversion"]
)

# RTF to TXT conversion
router.add_api_route(
    "/rtf-to-txt",
    controller.convert_rtf_to_txt,
    methods=["POST"],
    summary="Convert RTF to TXT",
    description="Upload an RTF file and convert it to plain text",
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

# Batch conversion (files/zip/rar/urls) -> target format, returns ZIP
router.add_api_route(
    "/batch-convert",
    controller.batch_convert_documents,
    methods=["POST"],
    summary="Batch convert documents",
    description="Upload multiple files or a ZIP/RAR or provide URLs and convert to target format. Returns a ZIP of results.",
    tags=["Document Conversion"]
)

