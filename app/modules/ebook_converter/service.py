"""
eBook conversion service.
Handles EPUB, MOBI, AZW, FB2, LIT, PRC conversions.
"""

import io
import zipfile
import xml.etree.ElementTree as ET
from typing import Optional
import structlog
from ebooklib import epub
import markdown
from bs4 import BeautifulSoup

from .types import EBookServiceResponse, EBookConversionOptions

logger = structlog.get_logger(__name__)


class EBookConverterService:
    """Service for converting eBook formats."""

    def __init__(self):
        self.supported_conversions = {
            'epub': ['mobi', 'azw', 'fb2', 'txt', 'html', 'pdf', 'docx'],
            'mobi': ['epub', 'azw', 'txt', 'html', 'pdf'],
            'azw': ['epub', 'mobi', 'txt', 'html', 'pdf'],
            'fb2': ['epub', 'mobi', 'txt', 'html', 'pdf'],
            'lit': ['epub', 'mobi', 'txt', 'html', 'pdf'],
            'prc': ['epub', 'mobi', 'txt', 'html', 'pdf'],
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

    # EPUB conversions
    async def convert_epub_to_mobi(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert EPUB to MOBI."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Read EPUB file
            book = epub.read_epub(io.BytesIO(file_buffer))
            
            # For now, return a placeholder response
            # EPUB to MOBI conversion requires additional libraries like kindlegen
            logger.warning("EPUB to MOBI conversion requires kindlegen or calibre")
            return EBookServiceResponse(
                status=501,
                message="EPUB to MOBI conversion requires additional libraries (kindlegen/calibre)",
                error="EPUB to MOBI conversion not fully implemented"
            )

        except Exception as e:
            logger.error("EPUB to MOBI conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting EPUB to MOBI",
                error=str(e)
            )

    async def convert_epub_to_azw(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert EPUB to AZW."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("EPUB to AZW conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="EPUB to AZW conversion requires additional libraries (kindlegen/calibre)",
                error="EPUB to AZW conversion not fully implemented"
            )

        except Exception as e:
            logger.error("EPUB to AZW conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting EPUB to AZW",
                error=str(e)
            )

    async def convert_epub_to_fb2(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert EPUB to FB2."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Read EPUB file
            book = epub.read_epub(io.BytesIO(file_buffer))
            
            # Create FB2 structure
            fb2_content = self._create_fb2_from_epub(book, options)
            
            logger.info("EPUB to FB2 conversion completed")
            return EBookServiceResponse(
                status=200,
                message="EPUB converted to FB2 successfully",
                data=fb2_content.encode(options.encoding),
                format="fb2"
            )

        except Exception as e:
            logger.error("EPUB to FB2 conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting EPUB to FB2",
                error=str(e)
            )

    async def convert_epub_to_txt(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert EPUB to TXT."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Read EPUB file
            book = epub.read_epub(io.BytesIO(file_buffer))
            
            # Extract text content
            text_content = self._extract_text_from_epub(book)
            
            logger.info("EPUB to TXT conversion completed")
            return EBookServiceResponse(
                status=200,
                message="EPUB converted to TXT successfully",
                data=text_content.encode(options.encoding),
                format="txt"
            )

        except Exception as e:
            logger.error("EPUB to TXT conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting EPUB to TXT",
                error=str(e)
            )

    async def convert_epub_to_html(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert EPUB to HTML."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Read EPUB file
            book = epub.read_epub(io.BytesIO(file_buffer))
            
            # Convert to HTML
            html_content = self._convert_epub_to_html(book, options)
            
            logger.info("EPUB to HTML conversion completed")
            return EBookServiceResponse(
                status=200,
                message="EPUB converted to HTML successfully",
                data=html_content.encode(options.encoding),
                format="html"
            )

        except Exception as e:
            logger.error("EPUB to HTML conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting EPUB to HTML",
                error=str(e)
            )

    async def convert_epub_to_pdf(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert EPUB to PDF."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Read EPUB file
            book = epub.read_epub(io.BytesIO(file_buffer))
            
            # Convert to HTML first, then to PDF
            html_content = self._convert_epub_to_html(book, options)
            
            # For now, return HTML content as PDF conversion requires additional libraries
            logger.warning("EPUB to PDF conversion requires additional libraries (weasyprint/wkhtmltopdf)")
            return EBookServiceResponse(
                status=501,
                message="EPUB to PDF conversion requires additional libraries",
                error="EPUB to PDF conversion not fully implemented"
            )

        except Exception as e:
            logger.error("EPUB to PDF conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting EPUB to PDF",
                error=str(e)
            )

    async def convert_epub_to_docx(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert EPUB to DOCX."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Read EPUB file
            book = epub.read_epub(io.BytesIO(file_buffer))
            
            # Convert to HTML first, then to DOCX
            html_content = self._convert_epub_to_html(book, options)
            
            # For now, return HTML content as DOCX conversion requires additional libraries
            logger.warning("EPUB to DOCX conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="EPUB to DOCX conversion requires additional libraries",
                error="EPUB to DOCX conversion not fully implemented"
            )

        except Exception as e:
            logger.error("EPUB to DOCX conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting EPUB to DOCX",
                error=str(e)
            )

    # MOBI conversions
    async def convert_mobi_to_epub(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert MOBI to EPUB."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("MOBI to EPUB conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="MOBI to EPUB conversion requires additional libraries (calibre/mobidedrm)",
                error="MOBI to EPUB conversion not fully implemented"
            )

        except Exception as e:
            logger.error("MOBI to EPUB conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting MOBI to EPUB",
                error=str(e)
            )

    async def convert_mobi_to_txt(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert MOBI to TXT."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("MOBI to TXT conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="MOBI to TXT conversion requires additional libraries",
                error="MOBI to TXT conversion not fully implemented"
            )

        except Exception as e:
            logger.error("MOBI to TXT conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting MOBI to TXT",
                error=str(e)
            )

    async def convert_mobi_to_html(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert MOBI to HTML."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("MOBI to HTML conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="MOBI to HTML conversion requires additional libraries",
                error="MOBI to HTML conversion not fully implemented"
            )

        except Exception as e:
            logger.error("MOBI to HTML conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting MOBI to HTML",
                error=str(e)
            )

    async def convert_mobi_to_pdf(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert MOBI to PDF."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("MOBI to PDF conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="MOBI to PDF conversion requires additional libraries",
                error="MOBI to PDF conversion not fully implemented"
            )

        except Exception as e:
            logger.error("MOBI to PDF conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting MOBI to PDF",
                error=str(e)
            )

    # AZW conversions
    async def convert_azw_to_epub(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert AZW to EPUB."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("AZW to EPUB conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="AZW to EPUB conversion requires additional libraries (calibre/mobidedrm)",
                error="AZW to EPUB conversion not fully implemented"
            )

        except Exception as e:
            logger.error("AZW to EPUB conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting AZW to EPUB",
                error=str(e)
            )

    async def convert_azw_to_mobi(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert AZW to MOBI."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("AZW to MOBI conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="AZW to MOBI conversion requires additional libraries",
                error="AZW to MOBI conversion not fully implemented"
            )

        except Exception as e:
            logger.error("AZW to MOBI conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting AZW to MOBI",
                error=str(e)
            )

    async def convert_azw_to_txt(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert AZW to TXT."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("AZW to TXT conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="AZW to TXT conversion requires additional libraries",
                error="AZW to TXT conversion not fully implemented"
            )

        except Exception as e:
            logger.error("AZW to TXT conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting AZW to TXT",
                error=str(e)
            )

    async def convert_azw_to_html(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert AZW to HTML."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("AZW to HTML conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="AZW to HTML conversion requires additional libraries",
                error="AZW to HTML conversion not fully implemented"
            )

        except Exception as e:
            logger.error("AZW to HTML conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting AZW to HTML",
                error=str(e)
            )

    async def convert_azw_to_pdf(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert AZW to PDF."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # For now, return a placeholder response
            logger.warning("AZW to PDF conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="AZW to PDF conversion requires additional libraries",
                error="AZW to PDF conversion not fully implemented"
            )

        except Exception as e:
            logger.error("AZW to PDF conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting AZW to PDF",
                error=str(e)
            )

    # FB2 conversions
    async def convert_fb2_to_epub(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert FB2 to EPUB."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Parse FB2 file
            fb2_content = file_buffer.decode(options.encoding)
            root = ET.fromstring(fb2_content)
            
            # Create EPUB book
            book = epub.EpubBook()
            
            # Extract metadata
            title_elem = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}book-title')
            if title_elem is not None:
                book.set_title(title_elem.text or "Unknown Title")
            
            # Extract content
            body_elem = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}body')
            if body_elem is not None:
                content_html = self._fb2_body_to_html(body_elem)
                chapter = epub.EpubHtml(title="Chapter 1", file_name="chapter1.xhtml", lang="en")
                chapter.content = content_html
                book.add_item(chapter)
            
            # Create EPUB
            epub_buffer = io.BytesIO()
            epub.write_epub(epub_buffer, book, {})
            epub_content = epub_buffer.getvalue()
            epub_buffer.close()
            
            logger.info("FB2 to EPUB conversion completed")
            return EBookServiceResponse(
                status=200,
                message="FB2 converted to EPUB successfully",
                data=epub_content,
                format="epub"
            )

        except Exception as e:
            logger.error("FB2 to EPUB conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting FB2 to EPUB",
                error=str(e)
            )

    async def convert_fb2_to_txt(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert FB2 to TXT."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Parse FB2 file
            fb2_content = file_buffer.decode(options.encoding)
            root = ET.fromstring(fb2_content)
            
            # Extract text content
            text_content = self._extract_text_from_fb2(root)
            
            logger.info("FB2 to TXT conversion completed")
            return EBookServiceResponse(
                status=200,
                message="FB2 converted to TXT successfully",
                data=text_content.encode(options.encoding),
                format="txt"
            )

        except Exception as e:
            logger.error("FB2 to TXT conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting FB2 to TXT",
                error=str(e)
            )

    async def convert_fb2_to_html(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert FB2 to HTML."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Parse FB2 file
            fb2_content = file_buffer.decode(options.encoding)
            root = ET.fromstring(fb2_content)
            
            # Convert to HTML
            html_content = self._convert_fb2_to_html(root, options)
            
            logger.info("FB2 to HTML conversion completed")
            return EBookServiceResponse(
                status=200,
                message="FB2 converted to HTML successfully",
                data=html_content.encode(options.encoding),
                format="html"
            )

        except Exception as e:
            logger.error("FB2 to HTML conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting FB2 to HTML",
                error=str(e)
            )

    async def convert_fb2_to_pdf(
        self,
        file_buffer: bytes,
        options: Optional[EBookConversionOptions] = None
    ) -> EBookServiceResponse:
        """Convert FB2 to PDF."""
        try:
            if options is None:
                options = EBookConversionOptions()

            # Convert to HTML first
            fb2_content = file_buffer.decode(options.encoding)
            root = ET.fromstring(fb2_content)
            html_content = self._convert_fb2_to_html(root, options)
            
            # For now, return HTML content as PDF conversion requires additional libraries
            logger.warning("FB2 to PDF conversion requires additional libraries")
            return EBookServiceResponse(
                status=501,
                message="FB2 to PDF conversion requires additional libraries",
                error="FB2 to PDF conversion not fully implemented"
            )

        except Exception as e:
            logger.error("FB2 to PDF conversion failed", error=str(e))
            return EBookServiceResponse(
                status=500,
                message="Error converting FB2 to PDF",
                error=str(e)
            )

    # Helper methods
    def _extract_text_from_epub(self, book):
        """Extract text content from EPUB book."""
        text_content = []
        
        # Get title
        if book.get_metadata('DC', 'title'):
            text_content.append(f"Title: {book.get_metadata('DC', 'title')[0][0]}")
        
        # Get author
        if book.get_metadata('DC', 'creator'):
            text_content.append(f"Author: {book.get_metadata('DC', 'creator')[0][0]}")
        
        text_content.append("")
        
        # Extract text from all items
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text_content.append(soup.get_text())
        
        return "\n".join(text_content)

    def _convert_epub_to_html(self, book, options):
        """Convert EPUB book to HTML."""
        html_parts = []
        
        # Add metadata
        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html>")
        html_parts.append("<head>")
        html_parts.append(f'<meta charset="{options.encoding}">')
        
        if book.get_metadata('DC', 'title'):
            title = book.get_metadata('DC', 'title')[0][0]
            html_parts.append(f"<title>{title}</title>")
        
        html_parts.append("</head>")
        html_parts.append("<body>")
        
        # Add title and author
        if book.get_metadata('DC', 'title'):
            title = book.get_metadata('DC', 'title')[0][0]
            html_parts.append(f"<h1>{title}</h1>")
        
        if book.get_metadata('DC', 'creator'):
            author = book.get_metadata('DC', 'creator')[0][0]
            html_parts.append(f"<p><strong>Author:</strong> {author}</p>")
        
        # Add content
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                html_parts.append(str(soup))
        
        html_parts.append("</body>")
        html_parts.append("</html>")
        
        return "\n".join(html_parts)

    def _create_fb2_from_epub(self, book, options):
        """Create FB2 content from EPUB book."""
        # This is a simplified FB2 creation
        fb2_content = []
        fb2_content.append('<?xml version="1.0" encoding="UTF-8"?>')
        fb2_content.append('<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">')
        fb2_content.append('<description>')
        fb2_content.append('<title-info>')
        
        if book.get_metadata('DC', 'title'):
            title = book.get_metadata('DC', 'title')[0][0]
            fb2_content.append(f'<book-title>{title}</book-title>')
        
        if book.get_metadata('DC', 'creator'):
            author = book.get_metadata('DC', 'creator')[0][0]
            fb2_content.append('<author>')
            fb2_content.append(f'<first-name>{author}</first-name>')
            fb2_content.append('</author>')
        
        fb2_content.append('</title-info>')
        fb2_content.append('</description>')
        fb2_content.append('<body>')
        
        # Add content
        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                fb2_content.append(f'<p>{soup.get_text()}</p>')
        
        fb2_content.append('</body>')
        fb2_content.append('</FictionBook>')
        
        return "\n".join(fb2_content)

    def _extract_text_from_fb2(self, root):
        """Extract text content from FB2 XML."""
        text_content = []
        
        # Extract title
        title_elem = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}book-title')
        if title_elem is not None:
            text_content.append(f"Title: {title_elem.text}")
        
        # Extract author
        author_elem = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}author')
        if author_elem is not None:
            first_name = author_elem.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}first-name')
            last_name = author_elem.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}last-name')
            if first_name is not None and last_name is not None:
                text_content.append(f"Author: {first_name.text} {last_name.text}")
        
        text_content.append("")
        
        # Extract body content
        body_elem = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}body')
        if body_elem is not None:
            for p in body_elem.findall('.//{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
                if p.text:
                    text_content.append(p.text)
        
        return "\n".join(text_content)

    def _convert_fb2_to_html(self, root, options):
        """Convert FB2 XML to HTML."""
        html_parts = []
        html_parts.append("<!DOCTYPE html>")
        html_parts.append("<html>")
        html_parts.append("<head>")
        html_parts.append(f'<meta charset="{options.encoding}">')
        
        # Extract title
        title_elem = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}book-title')
        if title_elem is not None:
            html_parts.append(f"<title>{title_elem.text}</title>")
        
        html_parts.append("</head>")
        html_parts.append("<body>")
        
        # Add title
        if title_elem is not None:
            html_parts.append(f"<h1>{title_elem.text}</h1>")
        
        # Add author
        author_elem = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}author')
        if author_elem is not None:
            first_name = author_elem.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}first-name')
            last_name = author_elem.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}last-name')
            if first_name is not None and last_name is not None:
                html_parts.append(f"<p><strong>Author:</strong> {first_name.text} {last_name.text}</p>")
        
        # Add body content
        body_elem = root.find('.//{http://www.gribuser.ru/xml/fictionbook/2.0}body')
        if body_elem is not None:
            for p in body_elem.findall('.//{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
                if p.text:
                    html_parts.append(f"<p>{p.text}</p>")
        
        html_parts.append("</body>")
        html_parts.append("</html>")
        
        return "\n".join(html_parts)

    def _fb2_body_to_html(self, body_elem):
        """Convert FB2 body element to HTML."""
        html_parts = []
        for p in body_elem.findall('.//{http://www.gribuser.ru/xml/fictionbook/2.0}p'):
            if p.text:
                html_parts.append(f"<p>{p.text}</p>")
        return "\n".join(html_parts)

    async def get_supported_conversions(self):
        """Get list of supported eBook conversions."""
        return {
            "supported_conversions": self.supported_conversions,
            "message": "List of supported eBook format conversions"
        }


# Global instance
ebook_converter_service = EBookConverterService()
