"""
Audio converter controller.
Handles API request parsing and calls to the audio conversion service.
"""

from fastapi import HTTPException, status, UploadFile, File, Form
from fastapi.responses import Response
from typing import Optional
import structlog

from .service import audio_converter_service
from .types import AudioConversionOptions

logger = structlog.get_logger(__name__)


class AudioConverterController:
    """Controller for audio conversion endpoints."""

    def __init__(self):
        self.service = audio_converter_service

    # MP3 conversions
    async def convert_mp3_to_wav(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert MP3 to WAV."""
        try:
            if not file.filename.lower().endswith('.mp3'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mp3 files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_mp3_to_wav(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.wav'
            return Response(
                content=result.data,
                media_type="audio/wav",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mp3_to_wav controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_mp3_to_flac(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert MP3 to FLAC."""
        try:
            if not file.filename.lower().endswith('.mp3'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mp3 files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_mp3_to_flac(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.flac'
            return Response(
                content=result.data,
                media_type="audio/flac",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mp3_to_flac controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_mp3_to_aac(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert MP3 to AAC."""
        try:
            if not file.filename.lower().endswith('.mp3'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mp3 files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_mp3_to_aac(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.aac'
            return Response(
                content=result.data,
                media_type="audio/aac",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mp3_to_aac controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_mp3_to_ogg(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert MP3 to OGG."""
        try:
            if not file.filename.lower().endswith('.mp3'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .mp3 files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_mp3_to_ogg(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.ogg'
            return Response(
                content=result.data,
                media_type="audio/ogg",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_mp3_to_ogg controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    # WAV conversions
    async def convert_wav_to_mp3(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert WAV to MP3."""
        try:
            if not file.filename.lower().endswith('.wav'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .wav files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_wav_to_mp3(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mp3'
            return Response(
                content=result.data,
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_wav_to_mp3 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_wav_to_flac(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert WAV to FLAC."""
        try:
            if not file.filename.lower().endswith('.wav'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .wav files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_wav_to_flac(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.flac'
            return Response(
                content=result.data,
                media_type="audio/flac",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_wav_to_flac controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_wav_to_aac(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert WAV to AAC."""
        try:
            if not file.filename.lower().endswith('.wav'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .wav files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_wav_to_aac(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.aac'
            return Response(
                content=result.data,
                media_type="audio/aac",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_wav_to_aac controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_wav_to_ogg(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert WAV to OGG."""
        try:
            if not file.filename.lower().endswith('.wav'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .wav files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_wav_to_ogg(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.ogg'
            return Response(
                content=result.data,
                media_type="audio/ogg",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_wav_to_ogg controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    # FLAC conversions
    async def convert_flac_to_mp3(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert FLAC to MP3."""
        try:
            if not file.filename.lower().endswith('.flac'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .flac files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_flac_to_mp3(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mp3'
            return Response(
                content=result.data,
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_flac_to_mp3 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_flac_to_wav(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert FLAC to WAV."""
        try:
            if not file.filename.lower().endswith('.flac'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .flac files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_flac_to_wav(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.wav'
            return Response(
                content=result.data,
                media_type="audio/wav",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_flac_to_wav controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_flac_to_aac(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert FLAC to AAC."""
        try:
            if not file.filename.lower().endswith('.flac'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .flac files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_flac_to_aac(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.aac'
            return Response(
                content=result.data,
                media_type="audio/aac",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_flac_to_aac controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_flac_to_ogg(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert FLAC to OGG."""
        try:
            if not file.filename.lower().endswith('.flac'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .flac files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_flac_to_ogg(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.ogg'
            return Response(
                content=result.data,
                media_type="audio/ogg",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_flac_to_ogg controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    # AAC conversions
    async def convert_aac_to_mp3(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert AAC to MP3."""
        try:
            if not file.filename.lower().endswith('.aac'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .aac files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_aac_to_mp3(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mp3'
            return Response(
                content=result.data,
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_aac_to_mp3 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_aac_to_wav(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert AAC to WAV."""
        try:
            if not file.filename.lower().endswith('.aac'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .aac files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_aac_to_wav(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.wav'
            return Response(
                content=result.data,
                media_type="audio/wav",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_aac_to_wav controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_aac_to_flac(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert AAC to FLAC."""
        try:
            if not file.filename.lower().endswith('.aac'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .aac files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_aac_to_flac(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.flac'
            return Response(
                content=result.data,
                media_type="audio/flac",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_aac_to_flac controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_aac_to_ogg(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert AAC to OGG."""
        try:
            if not file.filename.lower().endswith('.aac'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .aac files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_aac_to_ogg(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.ogg'
            return Response(
                content=result.data,
                media_type="audio/ogg",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_aac_to_ogg controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    # OGG conversions
    async def convert_ogg_to_mp3(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert OGG to MP3."""
        try:
            if not file.filename.lower().endswith('.ogg'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .ogg files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_ogg_to_mp3(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.mp3'
            return Response(
                content=result.data,
                media_type="audio/mpeg",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_ogg_to_mp3 controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_ogg_to_wav(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert OGG to WAV."""
        try:
            if not file.filename.lower().endswith('.ogg'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .ogg files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_ogg_to_wav(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.wav'
            return Response(
                content=result.data,
                media_type="audio/wav",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_ogg_to_wav controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_ogg_to_flac(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert OGG to FLAC."""
        try:
            if not file.filename.lower().endswith('.ogg'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .ogg files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_ogg_to_flac(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.flac'
            return Response(
                content=result.data,
                media_type="audio/flac",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_ogg_to_flac controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def convert_ogg_to_aac(
        self,
        file: UploadFile = File(...),
        sample_rate: int = Form(44100),
        channels: int = Form(2),
        bit_depth: int = Form(16)
    ) -> Response:
        """Convert OGG to AAC."""
        try:
            if not file.filename.lower().endswith('.ogg'):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Only .ogg files are supported"
                )

            file_content = await file.read()
            options = AudioConversionOptions(
                sample_rate=sample_rate,
                channels=channels,
                bit_depth=bit_depth
            )

            result = await self.service.convert_ogg_to_aac(file_content, options)

            if result.status != 200:
                raise HTTPException(
                    status_code=result.status,
                    detail=result.message
                )

            filename = file.filename.rsplit('.', 1)[0] + '.aac'
            return Response(
                content=result.data,
                media_type="audio/aac",
                headers={"Content-Disposition": f"attachment; filename={filename}"}
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error("Error in convert_ogg_to_aac controller", error=str(e))
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error converting audio: {str(e)}"
            )

    async def get_supported_conversions(self):
        """Get list of supported audio conversions."""
        return await self.service.get_supported_conversions()


# Global instance
audio_converter_controller = AudioConverterController()
