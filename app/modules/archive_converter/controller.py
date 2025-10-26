"""
Archive converter controller.
Handles API request parsing and calls to the archive conversion service.
"""

from fastapi import HTTPException, status, UploadFile, File, Form
from fastapi.responses import Response
from typing import Optional
import structlog

from .service import archive_converter_service
from .types import ArchiveConversionOptions

logger = structlog.get_logger(__name__)


class ArchiveConverterController:
    """Controller for archive conversion endpoints."""

    def __init__(self):
        self.service = archive_converter_service

    # ZIP conversions
    async def convert_zip_to_rar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert ZIP to RAR."""
        try:
            if not file.filename.lower().endswith('.zip'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .zip files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_zip_to_rar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.rar'
            return Response(
                content=result.data,
                media_type="application/x-rar-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_zip_to_rar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_zip_to_7z(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert ZIP to 7Z."""
        try:
            if not file.filename.lower().endswith('.zip'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .zip files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_zip_to_7z(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.7z'
            return Response(
                content=result.data,
                media_type="application/x-7z-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_zip_to_7z controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_zip_to_tar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert ZIP to TAR."""
        try:
            if not file.filename.lower().endswith('.zip'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .zip files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_zip_to_tar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.tar'
            return Response(
                content=result.data,
                media_type="application/x-tar",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_zip_to_tar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_zip_to_gz(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert ZIP to GZ."""
        try:
            if not file.filename.lower().endswith('.zip'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .zip files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_zip_to_gz(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.gz'
            return Response(
                content=result.data,
                media_type="application/gzip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_zip_to_gz controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_zip_to_bz2(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert ZIP to BZ2."""
        try:
            if not file.filename.lower().endswith('.zip'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .zip files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_zip_to_bz2(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.bz2'
            return Response(
                content=result.data,
                media_type="application/x-bzip2",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_zip_to_bz2 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    # RAR conversions
    async def convert_rar_to_zip(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert RAR to ZIP."""
        try:
            if not file.filename.lower().endswith('.rar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .rar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_rar_to_zip(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.zip'
            return Response(
                content=result.data,
                media_type="application/zip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_rar_to_zip controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_rar_to_7z(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert RAR to 7Z."""
        try:
            if not file.filename.lower().endswith('.rar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .rar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_rar_to_7z(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.7z'
            return Response(
                content=result.data,
                media_type="application/x-7z-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_rar_to_7z controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_rar_to_tar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert RAR to TAR."""
        try:
            if not file.filename.lower().endswith('.rar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .rar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_rar_to_tar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.tar'
            return Response(
                content=result.data,
                media_type="application/x-tar",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_rar_to_tar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_rar_to_gz(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert RAR to GZ."""
        try:
            if not file.filename.lower().endswith('.rar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .rar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_rar_to_gz(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.gz'
            return Response(
                content=result.data,
                media_type="application/gzip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_rar_to_gz controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_rar_to_bz2(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert RAR to BZ2."""
        try:
            if not file.filename.lower().endswith('.rar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .rar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_rar_to_bz2(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.bz2'
            return Response(
                content=result.data,
                media_type="application/x-bzip2",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_rar_to_bz2 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    # 7Z conversions
    async def convert_7z_to_zip(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert 7Z to ZIP."""
        try:
            if not file.filename.lower().endswith('.7z'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .7z files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_7z_to_zip(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.zip'
            return Response(
                content=result.data,
                media_type="application/zip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_7z_to_zip controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_7z_to_rar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert 7Z to RAR."""
        try:
            if not file.filename.lower().endswith('.7z'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .7z files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_7z_to_rar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.rar'
            return Response(
                content=result.data,
                media_type="application/x-rar-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_7z_to_rar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_7z_to_tar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert 7Z to TAR."""
        try:
            if not file.filename.lower().endswith('.7z'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .7z files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_7z_to_tar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.tar'
            return Response(
                content=result.data,
                media_type="application/x-tar",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_7z_to_tar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_7z_to_gz(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert 7Z to GZ."""
        try:
            if not file.filename.lower().endswith('.7z'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .7z files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_7z_to_gz(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.gz'
            return Response(
                content=result.data,
                media_type="application/gzip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_7z_to_gz controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_7z_to_bz2(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert 7Z to BZ2."""
        try:
            if not file.filename.lower().endswith('.7z'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .7z files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_7z_to_bz2(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.bz2'
            return Response(
                content=result.data,
                media_type="application/x-bzip2",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_7z_to_bz2 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    # TAR conversions
    async def convert_tar_to_zip(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert TAR to ZIP."""
        try:
            if not file.filename.lower().endswith('.tar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .tar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_tar_to_zip(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.zip'
            return Response(
                content=result.data,
                media_type="application/zip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_tar_to_zip controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_tar_to_rar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert TAR to RAR."""
        try:
            if not file.filename.lower().endswith('.tar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .tar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_tar_to_rar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.rar'
            return Response(
                content=result.data,
                media_type="application/x-rar-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_tar_to_rar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_tar_to_7z(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert TAR to 7Z."""
        try:
            if not file.filename.lower().endswith('.tar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .tar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_tar_to_7z(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.7z'
            return Response(
                content=result.data,
                media_type="application/x-7z-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_tar_to_7z controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_tar_to_gz(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert TAR to GZ."""
        try:
            if not file.filename.lower().endswith('.tar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .tar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_tar_to_gz(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.gz'
            return Response(
                content=result.data,
                media_type="application/gzip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_tar_to_gz controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_tar_to_bz2(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert TAR to BZ2."""
        try:
            if not file.filename.lower().endswith('.tar'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .tar files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_tar_to_bz2(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.bz2'
            return Response(
                content=result.data,
                media_type="application/x-bzip2",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_tar_to_bz2 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    # GZ conversions
    async def convert_gz_to_zip(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert GZ to ZIP."""
        try:
            if not file.filename.lower().endswith('.gz'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .gz files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_gz_to_zip(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.zip'
            return Response(
                content=result.data,
                media_type="application/zip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_gz_to_zip controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_gz_to_rar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert GZ to RAR."""
        try:
            if not file.filename.lower().endswith('.gz'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .gz files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_gz_to_rar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.rar'
            return Response(
                content=result.data,
                media_type="application/x-rar-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_gz_to_rar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_gz_to_7z(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert GZ to 7Z."""
        try:
            if not file.filename.lower().endswith('.gz'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .gz files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_gz_to_7z(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.7z'
            return Response(
                content=result.data,
                media_type="application/x-7z-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_gz_to_7z controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_gz_to_tar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert GZ to TAR."""
        try:
            if not file.filename.lower().endswith('.gz'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .gz files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_gz_to_tar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.tar'
            return Response(
                content=result.data,
                media_type="application/x-tar",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_gz_to_tar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_gz_to_bz2(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert GZ to BZ2."""
        try:
            if not file.filename.lower().endswith('.gz'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .gz files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_gz_to_bz2(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.bz2'
            return Response(
                content=result.data,
                media_type="application/x-bzip2",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_gz_to_bz2 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    # BZ2 conversions
    async def convert_bz2_to_zip(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert BZ2 to ZIP."""
        try:
            if not file.filename.lower().endswith('.bz2'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .bz2 files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_bz2_to_zip(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.zip'
            return Response(
                content=result.data,
                media_type="application/zip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_bz2_to_zip controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_bz2_to_rar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert BZ2 to RAR."""
        try:
            if not file.filename.lower().endswith('.bz2'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .bz2 files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_bz2_to_rar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.rar'
            return Response(
                content=result.data,
                media_type="application/x-rar-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_bz2_to_rar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_bz2_to_7z(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert BZ2 to 7Z."""
        try:
            if not file.filename.lower().endswith('.bz2'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .bz2 files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_bz2_to_7z(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.7z'
            return Response(
                content=result.data,
                media_type="application/x-7z-compressed",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_bz2_to_7z controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_bz2_to_tar(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert BZ2 to TAR."""
        try:
            if not file.filename.lower().endswith('.bz2'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .bz2 files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_bz2_to_tar(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.tar'
            return Response(
                content=result.data,
                media_type="application/x-tar",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_bz2_to_tar controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def convert_bz2_to_gz(
        self,
        file: UploadFile = File(...),
        compression_level: int = Form(6),
        password: Optional[str] = Form(None),
        include_hidden: bool = Form(False),
        preserve_permissions: bool = Form(True),
        compression_method: str = Form("deflate")
    ) -> Response:
        """Convert BZ2 to GZ."""
        try:
            if not file.filename.lower().endswith('.bz2'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .bz2 files are supported"
                )

            file_content = await file.read()
            options = ArchiveConversionOptions(
                compression_level=compression_level,
                password=password,
                include_hidden=include_hidden,
                preserve_permissions=preserve_permissions,
                compression_method=compression_method
            )

            result = await self.service.convert_bz2_to_gz(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.gz'
            return Response(
                content=result.data,
                media_type="application/gzip",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_bz2_to_gz controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting archive: {str(e)}"
            )

    async def get_supported_conversions(self):
        """Get list of supported archive conversions."""
        return await self.service.get_supported_conversions()


# Global instance
archive_converter_controller = ArchiveConverterController()
