"""
Archive conversion service.
Handles ZIP, RAR, 7Z, TAR, GZ, BZ2 conversions.
"""

import io
import zipfile
import tarfile
import gzip
import bz2
import lzma
from typing import Optional
import structlog
import py7zr
import rarfile

from .types import ArchiveServiceResponse, ArchiveConversionOptions

logger = structlog.get_logger(__name__)


class ArchiveConverterService:
    """Service for converting archive formats."""

    def __init__(self):
        self.supported_conversions = {
            'zip': ['rar', '7z', 'tar', 'gz', 'bz2'],
            'rar': ['zip', '7z', 'tar', 'gz', 'bz2'],
            '7z': ['zip', 'rar', 'tar', 'gz', 'bz2'],
            'tar': ['zip', 'rar', '7z', 'gz', 'bz2'],
            'gz': ['zip', 'rar', '7z', 'tar', 'bz2'],
            'bz2': ['zip', 'rar', '7z', 'tar', 'gz'],
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

    # ZIP conversions
    async def convert_zip_to_rar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert ZIP to RAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # For now, return a placeholder response
            # ZIP to RAR conversion requires additional libraries
            logger.warning("ZIP to RAR conversion requires additional libraries")
            return ArchiveServiceResponse(
                status=501,
                message="ZIP to RAR conversion requires additional libraries (rarfile/rar)",
                error="ZIP to RAR conversion not fully implemented"
            )

        except Exception as e:
            logger.error("ZIP to RAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting ZIP to RAR",
                error=str(e)
            )

    async def convert_zip_to_7z(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert ZIP to 7Z."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read ZIP file
            with zipfile.ZipFile(io.BytesIO(file_buffer), 'r') as zip_file:
                # Create 7Z file
                sevenz_buffer = io.BytesIO()
                with py7zr.SevenZipFile(sevenz_buffer, 'w', password=options.password) as sevenz_file:
                    for file_info in zip_file.filelist:
                        if not file_info.is_dir():
                            file_data = zip_file.read(file_info.filename)
                            sevenz_file.writestr(file_info.filename, file_data)

                sevenz_content = sevenz_buffer.getvalue()
                sevenz_buffer.close()

            logger.info("ZIP to 7Z conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="ZIP converted to 7Z successfully",
                data=sevenz_content,
                format="7z"
            )

        except Exception as e:
            logger.error("ZIP to 7Z conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting ZIP to 7Z",
                error=str(e)
            )

    async def convert_zip_to_tar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert ZIP to TAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read ZIP file
            with zipfile.ZipFile(io.BytesIO(file_buffer), 'r') as zip_file:
                # Create TAR file
                tar_buffer = io.BytesIO()
                with tarfile.open(fileobj=tar_buffer, mode='w') as tar_file:
                    for file_info in zip_file.filelist:
                        if not file_info.is_dir():
                            file_data = zip_file.read(file_info.filename)
                            tarinfo = tarfile.TarInfo(name=file_info.filename)
                            tarinfo.size = len(file_data)
                            tar_file.addfile(tarinfo, io.BytesIO(file_data))

                tar_content = tar_buffer.getvalue()
                tar_buffer.close()

            logger.info("ZIP to TAR conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="ZIP converted to TAR successfully",
                data=tar_content,
                format="tar"
            )

        except Exception as e:
            logger.error("ZIP to TAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting ZIP to TAR",
                error=str(e)
            )

    async def convert_zip_to_gz(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert ZIP to GZ."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read ZIP file and extract first file
            with zipfile.ZipFile(io.BytesIO(file_buffer), 'r') as zip_file:
                file_list = [f for f in zip_file.filelist if not f.is_dir()]
                if not file_list:
                    return ArchiveServiceResponse(
                        status=400,
                        message="ZIP file contains no files to compress",
                        error="No files found in ZIP archive"
                    )
                
                # Get the first file
                first_file = file_list[0]
                file_data = zip_file.read(first_file.filename)
                
                # Compress with gzip
                gz_buffer = io.BytesIO()
                with gzip.GzipFile(fileobj=gz_buffer, mode='wb', compresslevel=options.compression_level) as gz_file:
                    gz_file.write(file_data)
                
                gz_content = gz_buffer.getvalue()
                gz_buffer.close()

            logger.info("ZIP to GZ conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="ZIP converted to GZ successfully",
                data=gz_content,
                format="gz"
            )

        except Exception as e:
            logger.error("ZIP to GZ conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting ZIP to GZ",
                error=str(e)
            )

    async def convert_zip_to_bz2(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert ZIP to BZ2."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read ZIP file and extract first file
            with zipfile.ZipFile(io.BytesIO(file_buffer), 'r') as zip_file:
                file_list = [f for f in zip_file.filelist if not f.is_dir()]
                if not file_list:
                    return ArchiveServiceResponse(
                        status=400,
                        message="ZIP file contains no files to compress",
                        error="No files found in ZIP archive"
                    )
                
                # Get the first file
                first_file = file_list[0]
                file_data = zip_file.read(first_file.filename)
                
                # Compress with bz2
                bz2_content = bz2.compress(file_data, compresslevel=options.compression_level)

            logger.info("ZIP to BZ2 conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="ZIP converted to BZ2 successfully",
                data=bz2_content,
                format="bz2"
            )

        except Exception as e:
            logger.error("ZIP to BZ2 conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting ZIP to BZ2",
                error=str(e)
            )

    # RAR conversions
    async def convert_rar_to_zip(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert RAR to ZIP."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read RAR file
            with rarfile.RarFile(io.BytesIO(file_buffer), 'r', password=options.password) as rar_file:
                # Create ZIP file
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=options.compression_level) as zip_file:
                    for file_info in rar_file.infolist():
                        if not file_info.is_dir():
                            file_data = rar_file.read(file_info.filename)
                            zip_file.writestr(file_info.filename, file_data)

                zip_content = zip_buffer.getvalue()
                zip_buffer.close()

            logger.info("RAR to ZIP conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="RAR converted to ZIP successfully",
                data=zip_content,
                format="zip"
            )

        except Exception as e:
            logger.error("RAR to ZIP conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting RAR to ZIP",
                error=str(e)
            )

    async def convert_rar_to_7z(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert RAR to 7Z."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read RAR file
            with rarfile.RarFile(io.BytesIO(file_buffer), 'r', password=options.password) as rar_file:
                # Create 7Z file
                sevenz_buffer = io.BytesIO()
                with py7zr.SevenZipFile(sevenz_buffer, 'w', password=options.password) as sevenz_file:
                    for file_info in rar_file.infolist():
                        if not file_info.is_dir():
                            file_data = rar_file.read(file_info.filename)
                            sevenz_file.writestr(file_info.filename, file_data)

                sevenz_content = sevenz_buffer.getvalue()
                sevenz_buffer.close()

            logger.info("RAR to 7Z conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="RAR converted to 7Z successfully",
                data=sevenz_content,
                format="7z"
            )

        except Exception as e:
            logger.error("RAR to 7Z conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting RAR to 7Z",
                error=str(e)
            )

    async def convert_rar_to_tar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert RAR to TAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read RAR file
            with rarfile.RarFile(io.BytesIO(file_buffer), 'r', password=options.password) as rar_file:
                # Create TAR file
                tar_buffer = io.BytesIO()
                with tarfile.open(fileobj=tar_buffer, mode='w') as tar_file:
                    for file_info in rar_file.infolist():
                        if not file_info.is_dir():
                            file_data = rar_file.read(file_info.filename)
                            tarinfo = tarfile.TarInfo(name=file_info.filename)
                            tarinfo.size = len(file_data)
                            tar_file.addfile(tarinfo, io.BytesIO(file_data))

                tar_content = tar_buffer.getvalue()
                tar_buffer.close()

            logger.info("RAR to TAR conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="RAR converted to TAR successfully",
                data=tar_content,
                format="tar"
            )

        except Exception as e:
            logger.error("RAR to TAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting RAR to TAR",
                error=str(e)
            )

    async def convert_rar_to_gz(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert RAR to GZ."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read RAR file and extract first file
            with rarfile.RarFile(io.BytesIO(file_buffer), 'r', password=options.password) as rar_file:
                file_list = [f for f in rar_file.infolist() if not f.is_dir()]
                if not file_list:
                    return ArchiveServiceResponse(
                        status=400,
                        message="RAR file contains no files to compress",
                        error="No files found in RAR archive"
                    )
                
                # Get the first file
                first_file = file_list[0]
                file_data = rar_file.read(first_file.filename)
                
                # Compress with gzip
                gz_buffer = io.BytesIO()
                with gzip.GzipFile(fileobj=gz_buffer, mode='wb', compresslevel=options.compression_level) as gz_file:
                    gz_file.write(file_data)
                
                gz_content = gz_buffer.getvalue()
                gz_buffer.close()

            logger.info("RAR to GZ conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="RAR converted to GZ successfully",
                data=gz_content,
                format="gz"
            )

        except Exception as e:
            logger.error("RAR to GZ conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting RAR to GZ",
                error=str(e)
            )

    async def convert_rar_to_bz2(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert RAR to BZ2."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read RAR file and extract first file
            with rarfile.RarFile(io.BytesIO(file_buffer), 'r', password=options.password) as rar_file:
                file_list = [f for f in rar_file.infolist() if not f.is_dir()]
                if not file_list:
                    return ArchiveServiceResponse(
                        status=400,
                        message="RAR file contains no files to compress",
                        error="No files found in RAR archive"
                    )
                
                # Get the first file
                first_file = file_list[0]
                file_data = rar_file.read(first_file.filename)
                
                # Compress with bz2
                bz2_content = bz2.compress(file_data, compresslevel=options.compression_level)

            logger.info("RAR to BZ2 conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="RAR converted to BZ2 successfully",
                data=bz2_content,
                format="bz2"
            )

        except Exception as e:
            logger.error("RAR to BZ2 conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting RAR to BZ2",
                error=str(e)
            )

    # 7Z conversions
    async def convert_7z_to_zip(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert 7Z to ZIP."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read 7Z file
            with py7zr.SevenZipFile(io.BytesIO(file_buffer), 'r', password=options.password) as sevenz_file:
                # Create ZIP file
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=options.compression_level) as zip_file:
                    for file_info in sevenz_file.list():
                        if not file_info.is_directory:
                            file_data = sevenz_file.read(file_info.filename)
                            zip_file.writestr(file_info.filename, file_data)

                zip_content = zip_buffer.getvalue()
                zip_buffer.close()

            logger.info("7Z to ZIP conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="7Z converted to ZIP successfully",
                data=zip_content,
                format="zip"
            )

        except Exception as e:
            logger.error("7Z to ZIP conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting 7Z to ZIP",
                error=str(e)
            )

    async def convert_7z_to_rar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert 7Z to RAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # For now, return a placeholder response
            logger.warning("7Z to RAR conversion requires additional libraries")
            return ArchiveServiceResponse(
                status=501,
                message="7Z to RAR conversion requires additional libraries",
                error="7Z to RAR conversion not fully implemented"
            )

        except Exception as e:
            logger.error("7Z to RAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting 7Z to RAR",
                error=str(e)
            )

    async def convert_7z_to_tar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert 7Z to TAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read 7Z file
            with py7zr.SevenZipFile(io.BytesIO(file_buffer), 'r', password=options.password) as sevenz_file:
                # Create TAR file
                tar_buffer = io.BytesIO()
                with tarfile.open(fileobj=tar_buffer, mode='w') as tar_file:
                    for file_info in sevenz_file.list():
                        if not file_info.is_directory:
                            file_data = sevenz_file.read(file_info.filename)
                            tarinfo = tarfile.TarInfo(name=file_info.filename)
                            tarinfo.size = len(file_data)
                            tar_file.addfile(tarinfo, io.BytesIO(file_data))

                tar_content = tar_buffer.getvalue()
                tar_buffer.close()

            logger.info("7Z to TAR conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="7Z converted to TAR successfully",
                data=tar_content,
                format="tar"
            )

        except Exception as e:
            logger.error("7Z to TAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting 7Z to TAR",
                error=str(e)
            )

    async def convert_7z_to_gz(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert 7Z to GZ."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read 7Z file and extract first file
            with py7zr.SevenZipFile(io.BytesIO(file_buffer), 'r', password=options.password) as sevenz_file:
                file_list = [f for f in sevenz_file.list() if not f.is_directory]
                if not file_list:
                    return ArchiveServiceResponse(
                        status=400,
                        message="7Z file contains no files to compress",
                        error="No files found in 7Z archive"
                    )
                
                # Get the first file
                first_file = file_list[0]
                file_data = sevenz_file.read(first_file.filename)
                
                # Compress with gzip
                gz_buffer = io.BytesIO()
                with gzip.GzipFile(fileobj=gz_buffer, mode='wb', compresslevel=options.compression_level) as gz_file:
                    gz_file.write(file_data)
                
                gz_content = gz_buffer.getvalue()
                gz_buffer.close()

            logger.info("7Z to GZ conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="7Z converted to GZ successfully",
                data=gz_content,
                format="gz"
            )

        except Exception as e:
            logger.error("7Z to GZ conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting 7Z to GZ",
                error=str(e)
            )

    async def convert_7z_to_bz2(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert 7Z to BZ2."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read 7Z file and extract first file
            with py7zr.SevenZipFile(io.BytesIO(file_buffer), 'r', password=options.password) as sevenz_file:
                file_list = [f for f in sevenz_file.list() if not f.is_directory]
                if not file_list:
                    return ArchiveServiceResponse(
                        status=400,
                        message="7Z file contains no files to compress",
                        error="No files found in 7Z archive"
                    )
                
                # Get the first file
                first_file = file_list[0]
                file_data = sevenz_file.read(first_file.filename)
                
                # Compress with bz2
                bz2_content = bz2.compress(file_data, compresslevel=options.compression_level)

            logger.info("7Z to BZ2 conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="7Z converted to BZ2 successfully",
                data=bz2_content,
                format="bz2"
            )

        except Exception as e:
            logger.error("7Z to BZ2 conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting 7Z to BZ2",
                error=str(e)
            )

    # TAR conversions
    async def convert_tar_to_zip(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert TAR to ZIP."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read TAR file
            with tarfile.open(fileobj=io.BytesIO(file_buffer), mode='r') as tar_file:
                # Create ZIP file
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=options.compression_level) as zip_file:
                    for member in tar_file.getmembers():
                        if member.isfile():
                            file_data = tar_file.extractfile(member).read()
                            zip_file.writestr(member.name, file_data)

                zip_content = zip_buffer.getvalue()
                zip_buffer.close()

            logger.info("TAR to ZIP conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="TAR converted to ZIP successfully",
                data=zip_content,
                format="zip"
            )

        except Exception as e:
            logger.error("TAR to ZIP conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting TAR to ZIP",
                error=str(e)
            )

    async def convert_tar_to_rar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert TAR to RAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # For now, return a placeholder response
            logger.warning("TAR to RAR conversion requires additional libraries")
            return ArchiveServiceResponse(
                status=501,
                message="TAR to RAR conversion requires additional libraries",
                error="TAR to RAR conversion not fully implemented"
            )

        except Exception as e:
            logger.error("TAR to RAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting TAR to RAR",
                error=str(e)
            )

    async def convert_tar_to_7z(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert TAR to 7Z."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Read TAR file
            with tarfile.open(fileobj=io.BytesIO(file_buffer), mode='r') as tar_file:
                # Create 7Z file
                sevenz_buffer = io.BytesIO()
                with py7zr.SevenZipFile(sevenz_buffer, 'w', password=options.password) as sevenz_file:
                    for member in tar_file.getmembers():
                        if member.isfile():
                            file_data = tar_file.extractfile(member).read()
                            sevenz_file.writestr(member.name, file_data)

                sevenz_content = sevenz_buffer.getvalue()
                sevenz_buffer.close()

            logger.info("TAR to 7Z conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="TAR converted to 7Z successfully",
                data=sevenz_content,
                format="7z"
            )

        except Exception as e:
            logger.error("TAR to 7Z conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting TAR to 7Z",
                error=str(e)
            )

    async def convert_tar_to_gz(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert TAR to GZ."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Compress TAR with gzip
            gz_content = gzip.compress(file_buffer, compresslevel=options.compression_level)

            logger.info("TAR to GZ conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="TAR converted to GZ successfully",
                data=gz_content,
                format="gz"
            )

        except Exception as e:
            logger.error("TAR to GZ conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting TAR to GZ",
                error=str(e)
            )

    async def convert_tar_to_bz2(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert TAR to BZ2."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Compress TAR with bz2
            bz2_content = bz2.compress(file_buffer, compresslevel=options.compression_level)

            logger.info("TAR to BZ2 conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="TAR converted to BZ2 successfully",
                data=bz2_content,
                format="bz2"
            )

        except Exception as e:
            logger.error("TAR to BZ2 conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting TAR to BZ2",
                error=str(e)
            )

    # GZ conversions
    async def convert_gz_to_zip(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert GZ to ZIP."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Decompress GZ file
            decompressed_data = gzip.decompress(file_buffer)
            
            # Create ZIP file with the decompressed data
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=options.compression_level) as zip_file:
                zip_file.writestr("extracted_file", decompressed_data)

            zip_content = zip_buffer.getvalue()
            zip_buffer.close()

            logger.info("GZ to ZIP conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="GZ converted to ZIP successfully",
                data=zip_content,
                format="zip"
            )

        except Exception as e:
            logger.error("GZ to ZIP conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting GZ to ZIP",
                error=str(e)
            )

    async def convert_gz_to_rar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert GZ to RAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # For now, return a placeholder response
            logger.warning("GZ to RAR conversion requires additional libraries")
            return ArchiveServiceResponse(
                status=501,
                message="GZ to RAR conversion requires additional libraries",
                error="GZ to RAR conversion not fully implemented"
            )

        except Exception as e:
            logger.error("GZ to RAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting GZ to RAR",
                error=str(e)
            )

    async def convert_gz_to_7z(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert GZ to 7Z."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Decompress GZ file
            decompressed_data = gzip.decompress(file_buffer)
            
            # Create 7Z file with the decompressed data
            sevenz_buffer = io.BytesIO()
            with py7zr.SevenZipFile(sevenz_buffer, 'w', password=options.password) as sevenz_file:
                sevenz_file.writestr("extracted_file", decompressed_data)

            sevenz_content = sevenz_buffer.getvalue()
            sevenz_buffer.close()

            logger.info("GZ to 7Z conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="GZ converted to 7Z successfully",
                data=sevenz_content,
                format="7z"
            )

        except Exception as e:
            logger.error("GZ to 7Z conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting GZ to 7Z",
                error=str(e)
            )

    async def convert_gz_to_tar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert GZ to TAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Decompress GZ file
            tar_content = gzip.decompress(file_buffer)

            logger.info("GZ to TAR conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="GZ converted to TAR successfully",
                data=tar_content,
                format="tar"
            )

        except Exception as e:
            logger.error("GZ to TAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting GZ to TAR",
                error=str(e)
            )

    async def convert_gz_to_bz2(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert GZ to BZ2."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Decompress GZ file
            decompressed_data = gzip.decompress(file_buffer)
            
            # Compress with bz2
            bz2_content = bz2.compress(decompressed_data, compresslevel=options.compression_level)

            logger.info("GZ to BZ2 conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="GZ converted to BZ2 successfully",
                data=bz2_content,
                format="bz2"
            )

        except Exception as e:
            logger.error("GZ to BZ2 conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting GZ to BZ2",
                error=str(e)
            )

    # BZ2 conversions
    async def convert_bz2_to_zip(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert BZ2 to ZIP."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Decompress BZ2 file
            decompressed_data = bz2.decompress(file_buffer)
            
            # Create ZIP file with the decompressed data
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, compresslevel=options.compression_level) as zip_file:
                zip_file.writestr("extracted_file", decompressed_data)

            zip_content = zip_buffer.getvalue()
            zip_buffer.close()

            logger.info("BZ2 to ZIP conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="BZ2 converted to ZIP successfully",
                data=zip_content,
                format="zip"
            )

        except Exception as e:
            logger.error("BZ2 to ZIP conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting BZ2 to ZIP",
                error=str(e)
            )

    async def convert_bz2_to_rar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert BZ2 to RAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # For now, return a placeholder response
            logger.warning("BZ2 to RAR conversion requires additional libraries")
            return ArchiveServiceResponse(
                status=501,
                message="BZ2 to RAR conversion requires additional libraries",
                error="BZ2 to RAR conversion not fully implemented"
            )

        except Exception as e:
            logger.error("BZ2 to RAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting BZ2 to RAR",
                error=str(e)
            )

    async def convert_bz2_to_7z(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert BZ2 to 7Z."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Decompress BZ2 file
            decompressed_data = bz2.decompress(file_buffer)
            
            # Create 7Z file with the decompressed data
            sevenz_buffer = io.BytesIO()
            with py7zr.SevenZipFile(sevenz_buffer, 'w', password=options.password) as sevenz_file:
                sevenz_file.writestr("extracted_file", decompressed_data)

            sevenz_content = sevenz_buffer.getvalue()
            sevenz_buffer.close()

            logger.info("BZ2 to 7Z conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="BZ2 converted to 7Z successfully",
                data=sevenz_content,
                format="7z"
            )

        except Exception as e:
            logger.error("BZ2 to 7Z conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting BZ2 to 7Z",
                error=str(e)
            )

    async def convert_bz2_to_tar(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert BZ2 to TAR."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Decompress BZ2 file
            tar_content = bz2.decompress(file_buffer)

            logger.info("BZ2 to TAR conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="BZ2 converted to TAR successfully",
                data=tar_content,
                format="tar"
            )

        except Exception as e:
            logger.error("BZ2 to TAR conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting BZ2 to TAR",
                error=str(e)
            )

    async def convert_bz2_to_gz(
        self,
        file_buffer: bytes,
        options: Optional[ArchiveConversionOptions] = None
    ) -> ArchiveServiceResponse:
        """Convert BZ2 to GZ."""
        try:
            if options is None:
                options = ArchiveConversionOptions()

            # Decompress BZ2 file
            decompressed_data = bz2.decompress(file_buffer)
            
            # Compress with gzip
            gz_content = gzip.compress(decompressed_data, compresslevel=options.compression_level)

            logger.info("BZ2 to GZ conversion completed")
            return ArchiveServiceResponse(
                status=200,
                message="BZ2 converted to GZ successfully",
                data=gz_content,
                format="gz"
            )

        except Exception as e:
            logger.error("BZ2 to GZ conversion failed", error=str(e))
            return ArchiveServiceResponse(
                status=500,
                message="Error converting BZ2 to GZ",
                error=str(e)
            )

    async def get_supported_conversions(self):
        """Get list of supported archive conversions."""
        return {
            "supported_conversions": self.supported_conversions,
            "message": "List of supported archive format conversions"
        }


# Global instance
archive_converter_service = ArchiveConverterService()
