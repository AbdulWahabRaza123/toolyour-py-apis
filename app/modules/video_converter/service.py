"""
Video conversion service.
Handles MP4, AVI, MOV, MKV, WEBM conversions with security limits.
"""

import io
import os
import tempfile
from typing import Optional
import structlog
from pydub import AudioSegment
from pydub.utils import which

# Note: moviepy import is commented out due to dependency issues
# from moviepy.editor import VideoFileClip

from .types import VideoServiceResponse, VideoConversionOptions

logger = structlog.get_logger(__name__)


class VideoConverterService:
    """Service for converting video formats with security restrictions."""

    def __init__(self):
        self.supported_conversions = {
            'mp4': ['avi', 'mov', 'mkv', 'webm', 'wmv', 'flv'],
            'avi': ['mp4', 'mov', 'mkv', 'webm', 'wmv', 'flv'],
            'mov': ['mp4', 'avi', 'mkv', 'webm', 'wmv', 'flv'],
            'mkv': ['mp4', 'avi', 'mov', 'webm', 'wmv', 'flv'],
            'webm': ['mp4', 'avi', 'mov', 'mkv', 'wmv', 'flv'],
            'wmv': ['mp4', 'avi', 'mov', 'mkv', 'webm', 'flv'],
            'flv': ['mp4', 'avi', 'mov', 'mkv', 'webm', 'wmv'],
        }
        
        # Security limits
        self.MAX_DURATION = 300  # 5 minutes
        self.MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
        self.ABSOLUTE_MAX_DURATION = 600  # 10 minutes
        self.ABSOLUTE_MAX_FILE_SIZE = 500 * 1024 * 1024  # 500MB

    def can_convert(self, source_format: str, target_format: str) -> bool:
        """Check if conversion is supported."""
        source_format = source_format.lower().replace('.', '')
        target_format = target_format.lower().replace('.', '')
        
        return target_format in self.supported_conversions.get(source_format, [])

    def get_supported_formats(self, source_format: str) -> list:
        """Get supported target formats for a source format."""
        source_format = source_format.lower().replace('.', '')
        return self.supported_conversions.get(source_format, [])

    def _validate_file_limits(self, file_buffer: bytes, options: VideoConversionOptions) -> tuple[bool, str]:
        """Validate file size and estimated duration limits."""
        file_size = len(file_buffer)
        
        # Check file size
        if file_size > options.max_file_size:
            return False, f"File size ({file_size / (1024*1024):.1f}MB) exceeds maximum allowed size ({options.max_file_size / (1024*1024):.1f}MB)"
        
        if file_size > self.ABSOLUTE_MAX_FILE_SIZE:
            return False, f"File size ({file_size / (1024*1024):.1f}MB) exceeds absolute maximum size ({self.ABSOLUTE_MAX_FILE_SIZE / (1024*1024):.1f}MB)"
        
        # For now, we'll do basic validation
        # In a real implementation, you'd use ffprobe to get actual duration
        return True, "File validation passed"

    def _get_ffmpeg_params(self, target_format: str, options: VideoConversionOptions) -> str:
        """Get FFmpeg parameters for video conversion."""
        params = []
        
        # Video codec and quality
        if target_format in ['mp4', 'mov']:
            params.append('-c:v libx264')
        elif target_format == 'webm':
            params.append('-c:v libvpx-vp9')
        elif target_format == 'mkv':
            params.append('-c:v libx264')
        elif target_format == 'avi':
            params.append('-c:v libx264')
        elif target_format == 'wmv':
            params.append('-c:v wmv2')
        elif target_format == 'flv':
            params.append('-c:v libx264')
        
        # Audio codec
        params.append(f'-c:a {options.audio_codec}')
        
        # Bitrate
        params.append(f'-b:v {options.bitrate}')
        params.append(f'-b:a {options.audio_bitrate}')
        
        # Resolution
        if options.resolution == '480p':
            params.append('-s 854x480')
        elif options.resolution == '720p':
            params.append('-s 1280x720')
        elif options.resolution == '1080p':
            params.append('-s 1920x1080')
        elif options.resolution == '4k':
            params.append('-s 3840x2160')
        
        # FPS
        params.append(f'-r {options.fps}')
        
        # Duration limit
        params.append(f'-t {options.max_duration}')
        
        # Speed adjustment
        if options.speed != 1.0:
            params.append(f'-filter:v "setpts={1/options.speed}*PTS"')
            params.append(f'-filter:a "atempo={options.speed}"')
        
        # Volume adjustment
        if options.volume != 1.0:
            params.append(f'-filter:a "volume={options.volume}"')
        
        return ' '.join(params)

    def _convert_with_ffmpeg(self, input_buffer: bytes, target_format: str, options: VideoConversionOptions) -> bytes:
        """Convert video using FFmpeg command line."""
        import subprocess
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(suffix=f'.{target_format}', delete=False) as output_file:
            with tempfile.NamedTemporaryFile(delete=False) as input_file:
                input_file.write(input_buffer)
                input_file.flush()
                
                # Build FFmpeg command
                ffmpeg_cmd = [
                    'ffmpeg',
                    '-i', input_file.name,
                    '-y',  # Overwrite output file
                ]
                
                # Add conversion parameters
                ffmpeg_params = self._get_ffmpeg_params(target_format, options)
                ffmpeg_cmd.extend(ffmpeg_params.split())
                ffmpeg_cmd.append(output_file.name)
                
                try:
                    # Run FFmpeg
                    result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, timeout=300)
                    
                    if result.returncode != 0:
                        raise Exception(f"FFmpeg error: {result.stderr}")
                    
                    # Read output file
                    with open(output_file.name, 'rb') as f:
                        output_data = f.read()
                    
                    # Clean up
                    os.unlink(input_file.name)
                    os.unlink(output_file.name)
                    
                    return output_data
                    
                except subprocess.TimeoutExpired:
                    # Clean up on timeout
                    try:
                        os.unlink(input_file.name)
                        os.unlink(output_file.name)
                    except:
                        pass
                    raise Exception("Video conversion timed out (5 minutes limit)")
                except Exception as e:
                    # Clean up on error
                    try:
                        os.unlink(input_file.name)
                        os.unlink(output_file.name)
                    except:
                        pass
                    raise e

    # MP4 conversions
    async def convert_mp4_to_avi(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MP4 to AVI."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            avi_content = self._convert_with_ffmpeg(file_buffer, 'avi', options)

            logger.info("MP4 to AVI conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MP4 converted to AVI successfully",
                data=avi_content,
                format="avi",
                file_size=len(avi_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MP4 to AVI conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MP4 to AVI",
                error=str(e)
            )

    async def convert_mp4_to_mov(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MP4 to MOV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mov_content = self._convert_with_ffmpeg(file_buffer, 'mov', options)

            logger.info("MP4 to MOV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MP4 converted to MOV successfully",
                data=mov_content,
                format="mov",
                file_size=len(mov_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MP4 to MOV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MP4 to MOV",
                error=str(e)
            )

    async def convert_mp4_to_mkv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MP4 to MKV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mkv_content = self._convert_with_ffmpeg(file_buffer, 'mkv', options)

            logger.info("MP4 to MKV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MP4 converted to MKV successfully",
                data=mkv_content,
                format="mkv",
                file_size=len(mkv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MP4 to MKV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MP4 to MKV",
                error=str(e)
            )

    async def convert_mp4_to_webm(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MP4 to WEBM."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            webm_content = self._convert_with_ffmpeg(file_buffer, 'webm', options)

            logger.info("MP4 to WEBM conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MP4 converted to WEBM successfully",
                data=webm_content,
                format="webm",
                file_size=len(webm_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MP4 to WEBM conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MP4 to WEBM",
                error=str(e)
            )

    async def convert_mp4_to_wmv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MP4 to WMV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            wmv_content = self._convert_with_ffmpeg(file_buffer, 'wmv', options)

            logger.info("MP4 to WMV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MP4 converted to WMV successfully",
                data=wmv_content,
                format="wmv",
                file_size=len(wmv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MP4 to WMV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MP4 to WMV",
                error=str(e)
            )

    async def convert_mp4_to_flv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MP4 to FLV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            flv_content = self._convert_with_ffmpeg(file_buffer, 'flv', options)

            logger.info("MP4 to FLV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MP4 converted to FLV successfully",
                data=flv_content,
                format="flv",
                file_size=len(flv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MP4 to FLV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MP4 to FLV",
                error=str(e)
            )

    # AVI conversions
    async def convert_avi_to_mp4(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert AVI to MP4."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mp4_content = self._convert_with_ffmpeg(file_buffer, 'mp4', options)

            logger.info("AVI to MP4 conversion completed")
            return VideoServiceResponse(
                status=200,
                message="AVI converted to MP4 successfully",
                data=mp4_content,
                format="mp4",
                file_size=len(mp4_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("AVI to MP4 conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting AVI to MP4",
                error=str(e)
            )

    async def convert_avi_to_mov(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert AVI to MOV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mov_content = self._convert_with_ffmpeg(file_buffer, 'mov', options)

            logger.info("AVI to MOV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="AVI converted to MOV successfully",
                data=mov_content,
                format="mov",
                file_size=len(mov_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("AVI to MOV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting AVI to MOV",
                error=str(e)
            )

    async def convert_avi_to_mkv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert AVI to MKV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mkv_content = self._convert_with_ffmpeg(file_buffer, 'mkv', options)

            logger.info("AVI to MKV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="AVI converted to MKV successfully",
                data=mkv_content,
                format="mkv",
                file_size=len(mkv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("AVI to MKV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting AVI to MKV",
                error=str(e)
            )

    async def convert_avi_to_webm(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert AVI to WEBM."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            webm_content = self._convert_with_ffmpeg(file_buffer, 'webm', options)

            logger.info("AVI to WEBM conversion completed")
            return VideoServiceResponse(
                status=200,
                message="AVI converted to WEBM successfully",
                data=webm_content,
                format="webm",
                file_size=len(webm_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("AVI to WEBM conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting AVI to WEBM",
                error=str(e)
            )

    async def convert_avi_to_wmv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert AVI to WMV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            wmv_content = self._convert_with_ffmpeg(file_buffer, 'wmv', options)

            logger.info("AVI to WMV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="AVI converted to WMV successfully",
                data=wmv_content,
                format="wmv",
                file_size=len(wmv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("AVI to WMV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting AVI to WMV",
                error=str(e)
            )

    async def convert_avi_to_flv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert AVI to FLV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            flv_content = self._convert_with_ffmpeg(file_buffer, 'flv', options)

            logger.info("AVI to FLV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="AVI converted to FLV successfully",
                data=flv_content,
                format="flv",
                file_size=len(flv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("AVI to FLV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting AVI to FLV",
                error=str(e)
            )

    # MOV conversions
    async def convert_mov_to_mp4(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MOV to MP4."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mp4_content = self._convert_with_ffmpeg(file_buffer, 'mp4', options)

            logger.info("MOV to MP4 conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MOV converted to MP4 successfully",
                data=mp4_content,
                format="mp4",
                file_size=len(mp4_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MOV to MP4 conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MOV to MP4",
                error=str(e)
            )

    async def convert_mov_to_avi(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MOV to AVI."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            avi_content = self._convert_with_ffmpeg(file_buffer, 'avi', options)

            logger.info("MOV to AVI conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MOV converted to AVI successfully",
                data=avi_content,
                format="avi",
                file_size=len(avi_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MOV to AVI conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MOV to AVI",
                error=str(e)
            )

    async def convert_mov_to_mkv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MOV to MKV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mkv_content = self._convert_with_ffmpeg(file_buffer, 'mkv', options)

            logger.info("MOV to MKV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MOV converted to MKV successfully",
                data=mkv_content,
                format="mkv",
                file_size=len(mkv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MOV to MKV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MOV to MKV",
                error=str(e)
            )

    async def convert_mov_to_webm(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MOV to WEBM."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            webm_content = self._convert_with_ffmpeg(file_buffer, 'webm', options)

            logger.info("MOV to WEBM conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MOV converted to WEBM successfully",
                data=webm_content,
                format="webm",
                file_size=len(webm_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MOV to WEBM conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MOV to WEBM",
                error=str(e)
            )

    async def convert_mov_to_wmv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MOV to WMV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            wmv_content = self._convert_with_ffmpeg(file_buffer, 'wmv', options)

            logger.info("MOV to WMV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MOV converted to WMV successfully",
                data=wmv_content,
                format="wmv",
                file_size=len(wmv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MOV to WMV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MOV to WMV",
                error=str(e)
            )

    async def convert_mov_to_flv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MOV to FLV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            flv_content = self._convert_with_ffmpeg(file_buffer, 'flv', options)

            logger.info("MOV to FLV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MOV converted to FLV successfully",
                data=flv_content,
                format="flv",
                file_size=len(flv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MOV to FLV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MOV to FLV",
                error=str(e)
            )

    # MKV conversions
    async def convert_mkv_to_mp4(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MKV to MP4."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mp4_content = self._convert_with_ffmpeg(file_buffer, 'mp4', options)

            logger.info("MKV to MP4 conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MKV converted to MP4 successfully",
                data=mp4_content,
                format="mp4",
                file_size=len(mp4_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MKV to MP4 conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MKV to MP4",
                error=str(e)
            )

    async def convert_mkv_to_avi(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MKV to AVI."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            avi_content = self._convert_with_ffmpeg(file_buffer, 'avi', options)

            logger.info("MKV to AVI conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MKV converted to AVI successfully",
                data=avi_content,
                format="avi",
                file_size=len(avi_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MKV to AVI conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MKV to AVI",
                error=str(e)
            )

    async def convert_mkv_to_mov(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MKV to MOV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mov_content = self._convert_with_ffmpeg(file_buffer, 'mov', options)

            logger.info("MKV to MOV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MKV converted to MOV successfully",
                data=mov_content,
                format="mov",
                file_size=len(mov_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MKV to MOV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MKV to MOV",
                error=str(e)
            )

    async def convert_mkv_to_webm(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MKV to WEBM."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            webm_content = self._convert_with_ffmpeg(file_buffer, 'webm', options)

            logger.info("MKV to WEBM conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MKV converted to WEBM successfully",
                data=webm_content,
                format="webm",
                file_size=len(webm_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MKV to WEBM conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MKV to WEBM",
                error=str(e)
            )

    async def convert_mkv_to_wmv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MKV to WMV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            wmv_content = self._convert_with_ffmpeg(file_buffer, 'wmv', options)

            logger.info("MKV to WMV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MKV converted to WMV successfully",
                data=wmv_content,
                format="wmv",
                file_size=len(wmv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MKV to WMV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MKV to WMV",
                error=str(e)
            )

    async def convert_mkv_to_flv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert MKV to FLV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            flv_content = self._convert_with_ffmpeg(file_buffer, 'flv', options)

            logger.info("MKV to FLV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="MKV converted to FLV successfully",
                data=flv_content,
                format="flv",
                file_size=len(flv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("MKV to FLV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting MKV to FLV",
                error=str(e)
            )

    # WEBM conversions
    async def convert_webm_to_mp4(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert WEBM to MP4."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mp4_content = self._convert_with_ffmpeg(file_buffer, 'mp4', options)

            logger.info("WEBM to MP4 conversion completed")
            return VideoServiceResponse(
                status=200,
                message="WEBM converted to MP4 successfully",
                data=mp4_content,
                format="mp4",
                file_size=len(mp4_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("WEBM to MP4 conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting WEBM to MP4",
                error=str(e)
            )

    async def convert_webm_to_avi(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert WEBM to AVI."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            avi_content = self._convert_with_ffmpeg(file_buffer, 'avi', options)

            logger.info("WEBM to AVI conversion completed")
            return VideoServiceResponse(
                status=200,
                message="WEBM converted to AVI successfully",
                data=avi_content,
                format="avi",
                file_size=len(avi_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("WEBM to AVI conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting WEBM to AVI",
                error=str(e)
            )

    async def convert_webm_to_mov(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert WEBM to MOV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mov_content = self._convert_with_ffmpeg(file_buffer, 'mov', options)

            logger.info("WEBM to MOV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="WEBM converted to MOV successfully",
                data=mov_content,
                format="mov",
                file_size=len(mov_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("WEBM to MOV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting WEBM to MOV",
                error=str(e)
            )

    async def convert_webm_to_mkv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert WEBM to MKV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            mkv_content = self._convert_with_ffmpeg(file_buffer, 'mkv', options)

            logger.info("WEBM to MKV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="WEBM converted to MKV successfully",
                data=mkv_content,
                format="mkv",
                file_size=len(mkv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("WEBM to MKV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting WEBM to MKV",
                error=str(e)
            )

    async def convert_webm_to_wmv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert WEBM to WMV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            wmv_content = self._convert_with_ffmpeg(file_buffer, 'wmv', options)

            logger.info("WEBM to WMV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="WEBM converted to WMV successfully",
                data=wmv_content,
                format="wmv",
                file_size=len(wmv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("WEBM to WMV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting WEBM to WMV",
                error=str(e)
            )

    async def convert_webm_to_flv(
        self,
        file_buffer: bytes,
        options: Optional[VideoConversionOptions] = None
    ) -> VideoServiceResponse:
        """Convert WEBM to FLV."""
        try:
            if options is None:
                options = VideoConversionOptions()

            # Validate file limits
            is_valid, message = self._validate_file_limits(file_buffer, options)
            if not is_valid:
                return VideoServiceResponse(
                    status=400,
                    message=message,
                    error="File validation failed"
                )

            # Convert using FFmpeg
            flv_content = self._convert_with_ffmpeg(file_buffer, 'flv', options)

            logger.info("WEBM to FLV conversion completed")
            return VideoServiceResponse(
                status=200,
                message="WEBM converted to FLV successfully",
                data=flv_content,
                format="flv",
                file_size=len(flv_content),
                resolution=options.resolution,
                bitrate=options.bitrate,
                fps=options.fps
            )

        except Exception as e:
            logger.error("WEBM to FLV conversion failed", error=str(e))
            return VideoServiceResponse(
                status=500,
                message="Error converting WEBM to FLV",
                error=str(e)
            )

    async def get_supported_conversions(self):
        """Get list of supported video conversions."""
        return {
            "supported_conversions": self.supported_conversions,
            "message": "List of supported video format conversions",
            "limits": {
                "max_duration_seconds": self.MAX_DURATION,
                "max_file_size_mb": self.MAX_FILE_SIZE / (1024 * 1024),
                "absolute_max_duration_seconds": self.ABSOLUTE_MAX_DURATION,
                "absolute_max_file_size_mb": self.ABSOLUTE_MAX_FILE_SIZE / (1024 * 1024)
            }
        }


# Global instance
video_converter_service = VideoConverterService()
