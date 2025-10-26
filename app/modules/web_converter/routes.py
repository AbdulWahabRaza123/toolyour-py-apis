"""
Web converter routes.
"""

from fastapi import APIRouter

from . import controller

router = APIRouter()

# HTML conversions
router.add_api_route(
    "/html-to-xml",
    controller.convert_html_to_xml,
    methods=["POST"],
    summary="Convert HTML to XML",
    description="Upload an HTML file and convert it to XML format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/html-to-json",
    controller.convert_html_to_json,
    methods=["POST"],
    summary="Convert HTML to JSON",
    description="Upload an HTML file and convert it to JSON format",
    tags=["Web Conversion"]
)

# XML conversions
router.add_api_route(
    "/xml-to-html",
    controller.convert_xml_to_html,
    methods=["POST"],
    summary="Convert XML to HTML",
    description="Upload an XML file and convert it to HTML format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/xml-to-json",
    controller.convert_xml_to_json,
    methods=["POST"],
    summary="Convert XML to JSON",
    description="Upload an XML file and convert it to JSON format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/xml-to-txt",
    controller.convert_xml_to_txt,
    methods=["POST"],
    summary="Convert XML to TXT",
    description="Upload an XML file and convert it to plain text",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/xml-to-csv",
    controller.convert_xml_to_csv,
    methods=["POST"],
    summary="Convert XML to CSV",
    description="Upload an XML file and convert it to CSV format",
    tags=["Web Conversion"]
)

# JSON conversions
router.add_api_route(
    "/json-to-html",
    controller.convert_json_to_html,
    methods=["POST"],
    summary="Convert JSON to HTML",
    description="Upload a JSON file and convert it to HTML format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/json-to-xml",
    controller.convert_json_to_xml,
    methods=["POST"],
    summary="Convert JSON to XML",
    description="Upload a JSON file and convert it to XML format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/json-to-txt",
    controller.convert_json_to_txt,
    methods=["POST"],
    summary="Convert JSON to TXT",
    description="Upload a JSON file and convert it to plain text",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/json-to-csv",
    controller.convert_json_to_csv,
    methods=["POST"],
    summary="Convert JSON to CSV",
    description="Upload a JSON file and convert it to CSV format",
    tags=["Web Conversion"]
)

# CSV conversions
router.add_api_route(
    "/csv-to-html",
    controller.convert_csv_to_html,
    methods=["POST"],
    summary="Convert CSV to HTML",
    description="Upload a CSV file and convert it to HTML format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/csv-to-xml",
    controller.convert_csv_to_xml,
    methods=["POST"],
    summary="Convert CSV to XML",
    description="Upload a CSV file and convert it to XML format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/csv-to-json",
    controller.convert_csv_to_json,
    methods=["POST"],
    summary="Convert CSV to JSON",
    description="Upload a CSV file and convert it to JSON format",
    tags=["Web Conversion"]
)

router.add_api_route(
    "/csv-to-txt",
    controller.convert_csv_to_txt,
    methods=["POST"],
    summary="Convert CSV to TXT",
    description="Upload a CSV file and convert it to plain text",
    tags=["Web Conversion"]
)

# Get supported conversions
router.add_api_route(
    "/supported-conversions",
    controller.get_supported_conversions,
    methods=["GET"],
    summary="Get supported web conversions",
    description="Get list of all supported web format conversions",
    tags=["Web Conversion"]
)
