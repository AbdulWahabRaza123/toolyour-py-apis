"""
Video converter controller.
Handles API request parsing and calls to the video conversion service.
"""

from fastapi import HTTPException, status, UploadFile, File, Form
from fastapi.responses import Response
from typing import Optional
import structlog

from .service import video_converter_service
from .types import VideoConversionOptions

logger = structlog.get_logger(__name__)


class VideoConverterController:
    """Controller for video conversion endpoints."""

    def __init__(self):
        self.service = video_converter_service

    # MP4 conversions
    async def convert_mp4_to_avi(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert MP4 to AVI."""
        try:
            if not file.filename.lower().endswith('.mp4'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mp4 files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mp4_to_avi(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.avi'
            return Response(
                content=result.data,
                media_type="video/x-msvideo",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mp4_to_avi controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_mp4_to_mov(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert MP4 to MOV."""
        try:
            if not file.filename.lower().endswith('.mp4'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mp4 files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mp4_to_mov(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mov'
            return Response(
                content=result.data,
                media_type="video/quicktime",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mp4_to_mov controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_mp4_to_mkv(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert MP4 to MKV."""
        try:
            if not file.filename.lower().endswith('.mp4'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mp4 files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mp4_to_mkv(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mkv'
            return Response(
                content=result.data,
                media_type="video/x-matroska",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mp4_to_mkv controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_mp4_to_webm(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("vp9")
    ) -> Response:
        """Convert MP4 to WEBM."""
        try:
            if not file.filename.lower().endswith('.mp4'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mp4 files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mp4_to_webm(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.webm'
            return Response(
                content=result.data,
                media_type="video/webm",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mp4_to_webm controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    # AVI conversions
    async def convert_avi_to_mp4(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert AVI to MP4."""
        try:
            if not file.filename.lower().endswith('.avi'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .avi files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_avi_to_mp4(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mp4'
            return Response(
                content=result.data,
                media_type="video/mp4",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_avi_to_mp4 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_avi_to_mov(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert AVI to MOV."""
        try:
            if not file.filename.lower().endswith('.avi'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .avi files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_avi_to_mov(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mov'
            return Response(
                content=result.data,
                media_type="video/quicktime",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_avi_to_mov controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_avi_to_mkv(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert AVI to MKV."""
        try:
            if not file.filename.lower().endswith('.avi'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .avi files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_avi_to_mkv(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mkv'
            return Response(
                content=result.data,
                media_type="video/x-matroska",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_avi_to_mkv controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_avi_to_webm(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("vp9")
    ) -> Response:
        """Convert AVI to WEBM."""
        try:
            if not file.filename.lower().endswith('.avi'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .avi files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_avi_to_webm(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.webm'
            return Response(
                content=result.data,
                media_type="video/webm",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_avi_to_webm controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    # MOV conversions
    async def convert_mov_to_mp4(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert MOV to MP4."""
        try:
            if not file.filename.lower().endswith('.mov'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mov files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mov_to_mp4(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mp4'
            return Response(
                content=result.data,
                media_type="video/mp4",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mov_to_mp4 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_mov_to_avi(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert MOV to AVI."""
        try:
            if not file.filename.lower().endswith('.mov'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mov files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mov_to_avi(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.avi'
            return Response(
                content=result.data,
                media_type="video/x-msvideo",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mov_to_avi controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_mov_to_mkv(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert MOV to MKV."""
        try:
            if not file.filename.lower().endswith('.mov'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mov files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mov_to_mkv(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mkv'
            return Response(
                content=result.data,
                media_type="video/x-matroska",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mov_to_mkv controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_mov_to_webm(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("vp9")
    ) -> Response:
        """Convert MOV to WEBM."""
        try:
            if not file.filename.lower().endswith('.mov'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mov files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mov_to_webm(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.webm'
            return Response(
                content=result.data,
                media_type="video/webm",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mov_to_webm controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    # MKV conversions
    async def convert_mkv_to_mp4(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert MKV to MP4."""
        try:
            if not file.filename.lower().endswith('.mkv'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mkv files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mkv_to_mp4(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mp4'
            return Response(
                content=result.data,
                media_type="video/mp4",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mkv_to_mp4 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_mkv_to_avi(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert MKV to AVI."""
        try:
            if not file.filename.lower().endswith('.mkv'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mkv files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mkv_to_avi(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.avi'
            return Response(
                content=result.data,
                media_type="video/x-msvideo",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mkv_to_avi controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_mkv_to_mov(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert MKV to MOV."""
        try:
            if not file.filename.lower().endswith('.mkv'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mkv files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mkv_to_mov(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mov'
            return Response(
                content=result.data,
                media_type="video/quicktime",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mkv_to_mov controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_mkv_to_webm(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("vp9")
    ) -> Response:
        """Convert MKV to WEBM."""
        try:
            if not file.filename.lower().endswith('.mkv'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mkv files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_mkv_to_webm(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.webm'
            return Response(
                content=result.data,
                media_type="video/webm",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mkv_to_webm controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    # WEBM conversions
    async def convert_webm_to_mp4(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert WEBM to MP4."""
        try:
            if not file.filename.lower().endswith('.webm'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .webm files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_webm_to_mp4(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mp4'
            return Response(
                content=result.data,
                media_type="video/mp4",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_webm_to_mp4 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_webm_to_avi(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert WEBM to AVI."""
        try:
            if not file.filename.lower().endswith('.webm'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .webm files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_webm_to_avi(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.avi'
            return Response(
                content=result.data,
                media_type="video/x-msvideo",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_webm_to_avi controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_webm_to_mov(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert WEBM to MOV."""
        try:
            if not file.filename.lower().endswith('.webm'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .webm files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_webm_to_mov(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mov'
            return Response(
                content=result.data,
                media_type="video/quicktime",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_webm_to_mov controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def convert_webm_to_mkv(
        self,
        file: UploadFile = File(...),
        resolution: str = Form("1920x1080"),
        bitrate: int = Form(2000),
        fps: int = Form(30),
        codec: str = Form("h264")
    ) -> Response:
        """Convert WEBM to MKV."""
        try:
            if not file.filename.lower().endswith('.webm'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .webm files are supported"
                )

            file_content = await file.read()
            options = VideoConversionOptions(
                resolution=resolution,
                bitrate=bitrate,
                fps=fps,
                codec=codec
            )

            result = await self.service.convert_webm_to_mkv(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mkv'
            return Response(
                content=result.data,
                media_type="video/x-matroska",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_webm_to_mkv controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting video: {str(e)}"
            )

    async def get_supported_conversions(self):
        """Get list of supported video conversions."""
        return await self.service.get_supported_conversions()


# Global instance
video_converter_controller = VideoConverterController()
