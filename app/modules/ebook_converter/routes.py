"""
eBook converter routes.
"""

from fastapi import APIRouter

from . import controller

router = APIRouter()

# EPUB conversions
router.add_api_route(
    "/epub-to-mobi",
    controller.convert_epub_to_mobi,
    methods=["POST"],
    summary="Convert EPUB to MOBI",
    description="Upload an EPUB file and convert it to MOBI format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/epub-to-azw",
    controller.convert_epub_to_azw,
    methods=["POST"],
    summary="Convert EPUB to AZW",
    description="Upload an EPUB file and convert it to AZW format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/epub-to-fb2",
    controller.convert_epub_to_fb2,
    methods=["POST"],
    summary="Convert EPUB to FB2",
    description="Upload an EPUB file and convert it to FB2 format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/epub-to-txt",
    controller.convert_epub_to_txt,
    methods=["POST"],
    summary="Convert EPUB to TXT",
    description="Upload an EPUB file and convert it to plain text",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/epub-to-html",
    controller.convert_epub_to_html,
    methods=["POST"],
    summary="Convert EPUB to HTML",
    description="Upload an EPUB file and convert it to HTML format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/epub-to-pdf",
    controller.convert_epub_to_pdf,
    methods=["POST"],
    summary="Convert EPUB to PDF",
    description="Upload an EPUB file and convert it to PDF format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/epub-to-docx",
    controller.convert_epub_to_docx,
    methods=["POST"],
    summary="Convert EPUB to DOCX",
    description="Upload an EPUB file and convert it to DOCX format",
    tags=["eBook Conversion"]
)

# MOBI conversions
router.add_api_route(
    "/mobi-to-epub",
    controller.convert_mobi_to_epub,
    methods=["POST"],
    summary="Convert MOBI to EPUB",
    description="Upload a MOBI file and convert it to EPUB format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/mobi-to-txt",
    controller.convert_mobi_to_txt,
    methods=["POST"],
    summary="Convert MOBI to TXT",
    description="Upload a MOBI file and convert it to plain text",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/mobi-to-html",
    controller.convert_mobi_to_html,
    methods=["POST"],
    summary="Convert MOBI to HTML",
    description="Upload a MOBI file and convert it to HTML format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/mobi-to-pdf",
    controller.convert_mobi_to_pdf,
    methods=["POST"],
    summary="Convert MOBI to PDF",
    description="Upload a MOBI file and convert it to PDF format",
    tags=["eBook Conversion"]
)

# AZW conversions
router.add_api_route(
    "/azw-to-epub",
    controller.convert_azw_to_epub,
    methods=["POST"],
    summary="Convert AZW to EPUB",
    description="Upload an AZW file and convert it to EPUB format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/azw-to-mobi",
    controller.convert_azw_to_mobi,
    methods=["POST"],
    summary="Convert AZW to MOBI",
    description="Upload an AZW file and convert it to MOBI format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/azw-to-txt",
    controller.convert_azw_to_txt,
    methods=["POST"],
    summary="Convert AZW to TXT",
    description="Upload an AZW file and convert it to plain text",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/azw-to-html",
    controller.convert_azw_to_html,
    methods=["POST"],
    summary="Convert AZW to HTML",
    description="Upload an AZW file and convert it to HTML format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/azw-to-pdf",
    controller.convert_azw_to_pdf,
    methods=["POST"],
    summary="Convert AZW to PDF",
    description="Upload an AZW file and convert it to PDF format",
    tags=["eBook Conversion"]
)

# FB2 conversions
router.add_api_route(
    "/fb2-to-epub",
    controller.convert_fb2_to_epub,
    methods=["POST"],
    summary="Convert FB2 to EPUB",
    description="Upload an FB2 file and convert it to EPUB format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/fb2-to-txt",
    controller.convert_fb2_to_txt,
    methods=["POST"],
    summary="Convert FB2 to TXT",
    description="Upload an FB2 file and convert it to plain text",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/fb2-to-html",
    controller.convert_fb2_to_html,
    methods=["POST"],
    summary="Convert FB2 to HTML",
    description="Upload an FB2 file and convert it to HTML format",
    tags=["eBook Conversion"]
)

router.add_api_route(
    "/fb2-to-pdf",
    controller.convert_fb2_to_pdf,
    methods=["POST"],
    summary="Convert FB2 to PDF",
    description="Upload an FB2 file and convert it to PDF format",
    tags=["eBook Conversion"]
)

# Get supported conversions
router.add_api_route(
    "/supported-conversions",
    controller.get_supported_conversions,
    methods=["GET"],
    summary="Get supported eBook conversions",
    description="Get list of all supported eBook format conversions",
    tags=["eBook Conversion"]
)
