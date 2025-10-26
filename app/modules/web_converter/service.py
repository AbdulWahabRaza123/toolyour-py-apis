"""
Web conversion service.
Handles HTML, XML, JSON, CSV conversions.
"""

import io
import json
import csv
import xml.etree.ElementTree as ET
from typing import Optional
from bs4 import BeautifulSoup
import structlog

from .types import WebServiceResponse, WebConversionOptions

logger = structlog.get_logger(__name__)


class WebConverterService:
    """Service for converting web formats."""

    def __init__(self):
        self.supported_conversions = {
            'html': ['pdf', 'docx', 'txt', 'md', 'xml', 'json'],
            'xml': ['html', 'json', 'txt', 'csv'],
            'json': ['html', 'xml', 'txt', 'csv'],
            'csv': ['html', 'xml', 'json', 'xlsx', 'txt'],
        }

    def can_convert(self, source_format: str, target_format: str) -> bool:
        """Check if conversion is supported."""
        source_format = source_format.lower().replace('.', '')
        target_format = target_format.lower().replace('.', '')
        
        return target_format in self.supported_conversions.get(source_format, [])

    def get_supported_formats(self, source_format: str) -> list:
        """Get supported target formats for a source format."""
        source_format = source_format.lower().replace('.', '')
        return self.supported_conversions.get(source_format, [])

    # HTML conversions
    async def convert_html_to_xml(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert HTML to XML."""
        try:
            if options is None:
                options = WebConversionOptions()

            html_content = file_buffer.decode(options.encoding)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Convert to XML-like structure
            xml_content = f'<?xml version="1.0" encoding="{options.encoding}"?>\n'
            xml_content += '<html>\n'
            
            for element in soup.find_all():
                if element.name:
                    xml_content += f'  <{element.name}>'
                    if element.string:
                        xml_content += element.string
                    xml_content += f'</{element.name}>\n'

            xml_content += '</html>'

            logger.info("HTML to XML conversion completed")
            return WebServiceResponse(
                status=200,
                message="HTML converted to XML successfully",
                data=xml_content.encode(options.encoding),
                format="xml"
            )

        except Exception as e:
            logger.error("HTML to XML conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting HTML to XML",
                error=str(e)
            )

    async def convert_html_to_json(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert HTML to JSON."""
        try:
            if options is None:
                options = WebConversionOptions()

            html_content = file_buffer.decode(options.encoding)
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Convert to JSON structure
            json_data = {
                "title": soup.title.string if soup.title else "",
                "head": {},
                "body": {}
            }
            
            # Extract head elements
            for meta in soup.find_all('meta'):
                if meta.get('name'):
                    json_data["head"][meta.get('name')] = meta.get('content', '')
            
            # Extract body content
            body_content = []
            for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'div']):
                if element.get_text().strip():
                    body_content.append({
                        "tag": element.name,
                        "text": element.get_text().strip()
                    })
            
            json_data["body"]["content"] = body_content

            json_str = json.dumps(json_data, indent=2 if options.pretty_print else None)
            
            logger.info("HTML to JSON conversion completed")
            return WebServiceResponse(
                status=200,
                message="HTML converted to JSON successfully",
                data=json_str.encode(options.encoding),
                format="json"
            )

        except Exception as e:
            logger.error("HTML to JSON conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting HTML to JSON",
                error=str(e)
            )

    # XML conversions
    async def convert_xml_to_html(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert XML to HTML."""
        try:
            if options is None:
                options = WebConversionOptions()

            xml_content = file_buffer.decode(options.encoding)
            root = ET.fromstring(xml_content)
            
            # Convert XML to HTML
            html_content = f'<!DOCTYPE html>\n<html>\n<head>\n<meta charset="{options.encoding}">\n</head>\n<body>\n'
            
            def xml_to_html(element, indent=""):
                html = f"{indent}<{element.tag}>"
                if element.text and element.text.strip():
                    html += element.text.strip()
                for child in element:
                    html += "\n" + xml_to_html(child, indent + "  ")
                if element.tail:
                    html += element.tail
                html += f"</{element.tag}>\n"
                return html
            
            html_content += xml_to_html(root, "  ")
            html_content += "</body>\n</html>"

            logger.info("XML to HTML conversion completed")
            return WebServiceResponse(
                status=200,
                message="XML converted to HTML successfully",
                data=html_content.encode(options.encoding),
                format="html"
            )

        except Exception as e:
            logger.error("XML to HTML conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting XML to HTML",
                error=str(e)
            )

    async def convert_xml_to_json(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert XML to JSON."""
        try:
            if options is None:
                options = WebConversionOptions()

            xml_content = file_buffer.decode(options.encoding)
            root = ET.fromstring(xml_content)
            
            def xml_to_dict(element):
                result = {}
                if element.text and element.text.strip():
                    result['text'] = element.text.strip()
                
                if element.attrib:
                    result['attributes'] = element.attrib
                
                children = {}
                for child in element:
                    if child.tag in children:
                        if not isinstance(children[child.tag], list):
                            children[child.tag] = [children[child.tag]]
                        children[child.tag].append(xml_to_dict(child))
                    else:
                        children[child.tag] = xml_to_dict(child)
                
                if children:
                    result.update(children)
                
                return result

            json_data = {root.tag: xml_to_dict(root)}
            json_str = json.dumps(json_data, indent=2 if options.pretty_print else None)
            
            logger.info("XML to JSON conversion completed")
            return WebServiceResponse(
                status=200,
                message="XML converted to JSON successfully",
                data=json_str.encode(options.encoding),
                format="json"
            )

        except Exception as e:
            logger.error("XML to JSON conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting XML to JSON",
                error=str(e)
            )

    async def convert_xml_to_txt(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert XML to TXT."""
        try:
            if options is None:
                options = WebConversionOptions()

            xml_content = file_buffer.decode(options.encoding)
            root = ET.fromstring(xml_content)
            
            def xml_to_text(element):
                text = ""
                if element.text and element.text.strip():
                    text += element.text.strip() + "\n"
                for child in element:
                    text += xml_to_text(child)
                return text
            
            text_content = xml_to_text(root)
            
            logger.info("XML to TXT conversion completed")
            return WebServiceResponse(
                status=200,
                message="XML converted to TXT successfully",
                data=text_content.encode(options.encoding),
                format="txt"
            )

        except Exception as e:
            logger.error("XML to TXT conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting XML to TXT",
                error=str(e)
            )

    async def convert_xml_to_csv(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert XML to CSV."""
        try:
            if options is None:
                options = WebConversionOptions()

            xml_content = file_buffer.decode(options.encoding)
            root = ET.fromstring(xml_content)
            
            # Find all elements with the same tag (assuming tabular data)
            elements = root.findall('.//*')
            if not elements:
                elements = [root]
            
            # Extract data
            rows = []
            headers = set()
            
            for element in elements:
                row = {}
                if element.text and element.text.strip():
                    row['text'] = element.text.strip()
                row.update(element.attrib)
                if row:
                    rows.append(row)
                    headers.update(row.keys())
            
            if not rows:
                return WebServiceResponse(
                    status=400,
                    message="No data found in XML",
                    error="XML contains no extractable data"
                )
            
            # Convert to CSV
            csv_content = io.StringIO()
            writer = csv.DictWriter(
                csv_content,
                fieldnames=list(headers),
                delimiter=options.delimiter,
                quotechar=options.quote_char,
                escapechar=options.escape_char
            )
            
            if options.include_headers:
                writer.writeheader()
            writer.writerows(rows)
            
            logger.info("XML to CSV conversion completed")
            return WebServiceResponse(
                status=200,
                message="XML converted to CSV successfully",
                data=csv_content.getvalue().encode(options.encoding),
                format="csv"
            )

        except Exception as e:
            logger.error("XML to CSV conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting XML to CSV",
                error=str(e)
            )

    # JSON conversions
    async def convert_json_to_html(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert JSON to HTML."""
        try:
            if options is None:
                options = WebConversionOptions()

            json_content = file_buffer.decode(options.encoding)
            data = json.loads(json_content)
            
            def json_to_html(obj, level=0):
                if isinstance(obj, dict):
                    html = "<ul>\n"
                    for key, value in obj.items():
                        html += f"<li><strong>{key}:</strong> {json_to_html(value, level+1)}</li>\n"
                    html += "</ul>"
                    return html
                elif isinstance(obj, list):
                    html = "<ol>\n"
                    for item in obj:
                        html += f"<li>{json_to_html(item, level+1)}</li>\n"
                    html += "</ol>"
                    return html
                else:
                    return str(obj)
            
            html_content = f'<!DOCTYPE html>\n<html>\n<head>\n<meta charset="{options.encoding}">\n<title>JSON to HTML</title>\n</head>\n<body>\n'
            html_content += json_to_html(data)
            html_content += "\n</body>\n</html>"
            
            logger.info("JSON to HTML conversion completed")
            return WebServiceResponse(
                status=200,
                message="JSON converted to HTML successfully",
                data=html_content.encode(options.encoding),
                format="html"
            )

        except Exception as e:
            logger.error("JSON to HTML conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting JSON to HTML",
                error=str(e)
            )

    async def convert_json_to_xml(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert JSON to XML."""
        try:
            if options is None:
                options = WebConversionOptions()

            json_content = file_buffer.decode(options.encoding)
            data = json.loads(json_content)
            
            def json_to_xml(obj, root_name="root"):
                if isinstance(obj, dict):
                    xml = f"<{root_name}>\n"
                    for key, value in obj.items():
                        xml += json_to_xml(value, key)
                    xml += f"</{root_name}>\n"
                    return xml
                elif isinstance(obj, list):
                    xml = ""
                    for i, item in enumerate(obj):
                        xml += json_to_xml(item, f"item_{i}")
                    return xml
                else:
                    return f"<{root_name}>{obj}</{root_name}>\n"
            
            xml_content = f'<?xml version="1.0" encoding="{options.encoding}"?>\n'
            xml_content += json_to_xml(data, "root")
            
            logger.info("JSON to XML conversion completed")
            return WebServiceResponse(
                status=200,
                message="JSON converted to XML successfully",
                data=xml_content.encode(options.encoding),
                format="xml"
            )

        except Exception as e:
            logger.error("JSON to XML conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting JSON to XML",
                error=str(e)
            )

    async def convert_json_to_txt(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert JSON to TXT."""
        try:
            if options is None:
                options = WebConversionOptions()

            json_content = file_buffer.decode(options.encoding)
            data = json.loads(json_content)
            
            def json_to_text(obj, level=0):
                indent = "  " * level
                if isinstance(obj, dict):
                    text = ""
                    for key, value in obj.items():
                        text += f"{indent}{key}: {json_to_text(value, level+1)}\n"
                    return text
                elif isinstance(obj, list):
                    text = ""
                    for i, item in enumerate(obj):
                        text += f"{indent}[{i}]: {json_to_text(item, level+1)}\n"
                    return text
                else:
                    return str(obj)
            
            text_content = json_to_text(data)
            
            logger.info("JSON to TXT conversion completed")
            return WebServiceResponse(
                status=200,
                message="JSON converted to TXT successfully",
                data=text_content.encode(options.encoding),
                format="txt"
            )

        except Exception as e:
            logger.error("JSON to TXT conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting JSON to TXT",
                error=str(e)
            )

    async def convert_json_to_csv(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert JSON to CSV."""
        try:
            if options is None:
                options = WebConversionOptions()

            json_content = file_buffer.decode(options.encoding)
            data = json.loads(json_content)
            
            # Handle different JSON structures
            if isinstance(data, list):
                # Array of objects
                if data and isinstance(data[0], dict):
                    csv_content = io.StringIO()
                    writer = csv.DictWriter(
                        csv_content,
                        fieldnames=data[0].keys(),
                        delimiter=options.delimiter,
                        quotechar=options.quote_char,
                        escapechar=options.escape_char
                    )
                    
                    if options.include_headers:
                        writer.writeheader()
                    writer.writerows(data)
                    
                    csv_text = csv_content.getvalue()
                else:
                    # Array of primitives
                    csv_text = "\n".join(str(item) for item in data)
            elif isinstance(data, dict):
                # Single object - convert to single row
                csv_content = io.StringIO()
                writer = csv.DictWriter(
                    csv_content,
                    fieldnames=data.keys(),
                    delimiter=options.delimiter,
                    quotechar=options.quote_char,
                    escapechar=options.escape_char
                )
                
                if options.include_headers:
                    writer.writeheader()
                writer.writerow(data)
                
                csv_text = csv_content.getvalue()
            else:
                # Primitive value
                csv_text = str(data)
            
            logger.info("JSON to CSV conversion completed")
            return WebServiceResponse(
                status=200,
                message="JSON converted to CSV successfully",
                data=csv_text.encode(options.encoding),
                format="csv"
            )

        except Exception as e:
            logger.error("JSON to CSV conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting JSON to CSV",
                error=str(e)
            )

    # CSV conversions
    async def convert_csv_to_html(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert CSV to HTML."""
        try:
            if options is None:
                options = WebConversionOptions()

            csv_content = file_buffer.decode(options.encoding)
            csv_reader = csv.DictReader(
                io.StringIO(csv_content),
                delimiter=options.delimiter,
                quotechar=options.quote_char,
                escapechar=options.escape_char
            )
            
            rows = list(csv_reader)
            if not rows:
                return WebServiceResponse(
                    status=400,
                    message="No data found in CSV",
                    error="CSV contains no data"
                )
            
            # Convert to HTML table
            html_content = f'<!DOCTYPE html>\n<html>\n<head>\n<meta charset="{options.encoding}">\n<title>CSV to HTML</title>\n</head>\n<body>\n'
            html_content += "<table border='1'>\n"
            
            # Headers
            if options.include_headers and rows:
                html_content += "<thead>\n<tr>\n"
                for header in rows[0].keys():
                    html_content += f"<th>{header}</th>\n"
                html_content += "</tr>\n</thead>\n"
            
            # Rows
            html_content += "<tbody>\n"
            for row in rows:
                html_content += "<tr>\n"
                for value in row.values():
                    html_content += f"<td>{value}</td>\n"
                html_content += "</tr>\n"
            html_content += "</tbody>\n"
            html_content += "</table>\n</body>\n</html>"
            
            logger.info("CSV to HTML conversion completed")
            return WebServiceResponse(
                status=200,
                message="CSV converted to HTML successfully",
                data=html_content.encode(options.encoding),
                format="html"
            )

        except Exception as e:
            logger.error("CSV to HTML conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting CSV to HTML",
                error=str(e)
            )

    async def convert_csv_to_xml(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert CSV to XML."""
        try:
            if options is None:
                options = WebConversionOptions()

            csv_content = file_buffer.decode(options.encoding)
            csv_reader = csv.DictReader(
                io.StringIO(csv_content),
                delimiter=options.delimiter,
                quotechar=options.quote_char,
                escapechar=options.escape_char
            )
            
            rows = list(csv_reader)
            if not rows:
                return WebServiceResponse(
                    status=400,
                    message="No data found in CSV",
                    error="CSV contains no data"
                )
            
            # Convert to XML
            xml_content = f'<?xml version="1.0" encoding="{options.encoding}"?>\n'
            xml_content += "<data>\n"
            
            for i, row in enumerate(rows):
                xml_content += f"  <row id=\"{i}\">\n"
                for key, value in row.items():
                    xml_content += f"    <{key}>{value}</{key}>\n"
                xml_content += "  </row>\n"
            
            xml_content += "</data>"
            
            logger.info("CSV to XML conversion completed")
            return WebServiceResponse(
                status=200,
                message="CSV converted to XML successfully",
                data=xml_content.encode(options.encoding),
                format="xml"
            )

        except Exception as e:
            logger.error("CSV to XML conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting CSV to XML",
                error=str(e)
            )

    async def convert_csv_to_json(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert CSV to JSON."""
        try:
            if options is None:
                options = WebConversionOptions()

            csv_content = file_buffer.decode(options.encoding)
            csv_reader = csv.DictReader(
                io.StringIO(csv_content),
                delimiter=options.delimiter,
                quotechar=options.quote_char,
                escapechar=options.escape_char
            )
            
            rows = list(csv_reader)
            if not rows:
                return WebServiceResponse(
                    status=400,
                    message="No data found in CSV",
                    error="CSV contains no data"
                )
            
            # Convert to JSON
            json_data = {"data": rows}
            json_str = json.dumps(json_data, indent=2 if options.pretty_print else None)
            
            logger.info("CSV to JSON conversion completed")
            return WebServiceResponse(
                status=200,
                message="CSV converted to JSON successfully",
                data=json_str.encode(options.encoding),
                format="json"
            )

        except Exception as e:
            logger.error("CSV to JSON conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting CSV to JSON",
                error=str(e)
            )

    async def convert_csv_to_txt(
        self,
        file_buffer: bytes,
        options: Optional[WebConversionOptions] = None
    ) -> WebServiceResponse:
        """Convert CSV to TXT."""
        try:
            if options is None:
                options = WebConversionOptions()

            csv_content = file_buffer.decode(options.encoding)
            csv_reader = csv.reader(
                io.StringIO(csv_content),
                delimiter=options.delimiter,
                quotechar=options.quote_char,
                escapechar=options.escape_char
            )
            
            rows = list(csv_reader)
            if not rows:
                return WebServiceResponse(
                    status=400,
                    message="No data found in CSV",
                    error="CSV contains no data"
                )
            
            # Convert to formatted text
            text_lines = []
            for i, row in enumerate(rows):
                if i == 0 and options.include_headers:
                    text_lines.append(" | ".join(row))
                    text_lines.append("-" * len(" | ".join(row)))
                else:
                    text_lines.append(" | ".join(row))
            
            text_content = "\n".join(text_lines)
            
            logger.info("CSV to TXT conversion completed")
            return WebServiceResponse(
                status=200,
                message="CSV converted to TXT successfully",
                data=text_content.encode(options.encoding),
                format="txt"
            )

        except Exception as e:
            logger.error("CSV to TXT conversion failed", error=str(e))
            return WebServiceResponse(
                status=500,
                message="Error converting CSV to TXT",
                error=str(e)
            )

    async def get_supported_conversions(self):
        """Get list of supported web conversions."""
        return {
            "supported_conversions": self.supported_conversions,
            "message": "List of supported web format conversions"
        }


# Global instance
web_converter_service = WebConverterService()
