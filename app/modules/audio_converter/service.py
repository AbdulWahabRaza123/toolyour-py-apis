"""
Audio conversion service.
Handles MP3, WAV, FLAC, AAC, OGG, M4A, WMA conversions.
"""

import io
from typing import Optional
import structlog
from pydub import AudioSegment
from pydub.utils import which

from .types import AudioServiceResponse, AudioConversionOptions

logger = structlog.get_logger(__name__)


class AudioConverterService:
    """Service for converting audio formats."""

    def __init__(self):
        self.supported_conversions = {
            'mp3': ['wav', 'flac', 'aac', 'ogg', 'm4a', 'wma'],
            'wav': ['mp3', 'flac', 'aac', 'ogg', 'm4a', 'wma'],
            'flac': ['mp3', 'wav', 'aac', 'ogg', 'm4a', 'wma'],
            'aac': ['mp3', 'wav', 'flac', 'ogg', 'm4a', 'wma'],
            'ogg': ['mp3', 'wav', 'flac', 'aac', 'm4a', 'wma'],
            'm4a': ['mp3', 'wav', 'flac', 'aac', 'ogg', 'wma'],
            'wma': ['mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a'],
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

    def _apply_audio_processing(self, audio: AudioSegment, options: AudioConversionOptions) -> AudioSegment:
        """Apply audio processing options."""
        # Trim audio if specified
        if options.trim_start > 0 or options.trim_end is not None:
            start_ms = int(options.trim_start * 1000)
            end_ms = int(options.trim_end * 1000) if options.trim_end else len(audio)
            audio = audio[start_ms:end_ms]

        # Apply fade in/out
        if options.fade_in > 0:
            audio = audio.fade_in(int(options.fade_in * 1000))
        if options.fade_out > 0:
            audio = audio.fade_out(int(options.fade_out * 1000))

        # Normalize audio if requested
        if options.normalize:
            audio = audio.normalize()

        return audio

    def _get_export_params(self, target_format: str, options: AudioConversionOptions) -> dict:
        """Get export parameters for target format."""
        params = {
            "format": target_format,
            "bitrate": options.bitrate,
        }

        if target_format in ["wav", "flac"]:
            params["parameters"] = f"-ar {options.sample_rate} -ac {options.channels}"
        elif target_format == "mp3":
            params["parameters"] = f"-ar {options.sample_rate} -ac {options.channels} -b:a {options.bitrate}"
        elif target_format == "aac":
            params["parameters"] = f"-ar {options.sample_rate} -ac {options.channels} -b:a {options.bitrate}"
        elif target_format == "ogg":
            params["parameters"] = f"-ar {options.sample_rate} -ac {options.channels} -b:a {options.bitrate}"

        return params

    # MP3 conversions
    async def convert_mp3_to_wav(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert MP3 to WAV."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load MP3 audio
            audio = AudioSegment.from_mp3(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WAV
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wav_content = wav_buffer.getvalue()
            wav_buffer.close()

            logger.info("MP3 to WAV conversion completed")
            return AudioServiceResponse(
                status=200,
                message="MP3 converted to WAV successfully",
                data=wav_content,
                format="wav",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("MP3 to WAV conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting MP3 to WAV",
                error=str(e)
            )

    async def convert_mp3_to_flac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert MP3 to FLAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load MP3 audio
            audio = AudioSegment.from_mp3(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to FLAC
            flac_buffer = io.BytesIO()
            audio.export(flac_buffer, format="flac", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            flac_content = flac_buffer.getvalue()
            flac_buffer.close()

            logger.info("MP3 to FLAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="MP3 converted to FLAC successfully",
                data=flac_content,
                format="flac",
                duration=len(audio) / 1000.0,
                bitrate="lossless",
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("MP3 to FLAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting MP3 to FLAC",
                error=str(e)
            )

    async def convert_mp3_to_aac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert MP3 to AAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load MP3 audio
            audio = AudioSegment.from_mp3(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to AAC
            aac_buffer = io.BytesIO()
            audio.export(aac_buffer, format="aac", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            aac_content = aac_buffer.getvalue()
            aac_buffer.close()

            logger.info("MP3 to AAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="MP3 converted to AAC successfully",
                data=aac_content,
                format="aac",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("MP3 to AAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting MP3 to AAC",
                error=str(e)
            )

    async def convert_mp3_to_ogg(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert MP3 to OGG."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load MP3 audio
            audio = AudioSegment.from_mp3(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to OGG
            ogg_buffer = io.BytesIO()
            audio.export(ogg_buffer, format="ogg", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            ogg_content = ogg_buffer.getvalue()
            ogg_buffer.close()

            logger.info("MP3 to OGG conversion completed")
            return AudioServiceResponse(
                status=200,
                message="MP3 converted to OGG successfully",
                data=ogg_content,
                format="ogg",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("MP3 to OGG conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting MP3 to OGG",
                error=str(e)
            )

    async def convert_mp3_to_m4a(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert MP3 to M4A."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load MP3 audio
            audio = AudioSegment.from_mp3(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to M4A
            m4a_buffer = io.BytesIO()
            audio.export(m4a_buffer, format="mp4", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            m4a_content = m4a_buffer.getvalue()
            m4a_buffer.close()

            logger.info("MP3 to M4A conversion completed")
            return AudioServiceResponse(
                status=200,
                message="MP3 converted to M4A successfully",
                data=m4a_content,
                format="m4a",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("MP3 to M4A conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting MP3 to M4A",
                error=str(e)
            )

    async def convert_mp3_to_wma(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert MP3 to WMA."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load MP3 audio
            audio = AudioSegment.from_mp3(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WMA
            wma_buffer = io.BytesIO()
            audio.export(wma_buffer, format="wma", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wma_content = wma_buffer.getvalue()
            wma_buffer.close()

            logger.info("MP3 to WMA conversion completed")
            return AudioServiceResponse(
                status=200,
                message="MP3 converted to WMA successfully",
                data=wma_content,
                format="wma",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("MP3 to WMA conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting MP3 to WMA",
                error=str(e)
            )

    # WAV conversions
    async def convert_wav_to_mp3(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WAV to MP3."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WAV audio
            audio = AudioSegment.from_wav(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to MP3
            mp3_buffer = io.BytesIO()
            audio.export(mp3_buffer, format="mp3", bitrate=options.bitrate)
            mp3_content = mp3_buffer.getvalue()
            mp3_buffer.close()

            logger.info("WAV to MP3 conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WAV converted to MP3 successfully",
                data=mp3_content,
                format="mp3",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WAV to MP3 conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WAV to MP3",
                error=str(e)
            )

    async def convert_wav_to_flac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WAV to FLAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WAV audio
            audio = AudioSegment.from_wav(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to FLAC
            flac_buffer = io.BytesIO()
            audio.export(flac_buffer, format="flac", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            flac_content = flac_buffer.getvalue()
            flac_buffer.close()

            logger.info("WAV to FLAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WAV converted to FLAC successfully",
                data=flac_content,
                format="flac",
                duration=len(audio) / 1000.0,
                bitrate="lossless",
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WAV to FLAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WAV to FLAC",
                error=str(e)
            )

    async def convert_wav_to_aac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WAV to AAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WAV audio
            audio = AudioSegment.from_wav(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to AAC
            aac_buffer = io.BytesIO()
            audio.export(aac_buffer, format="aac", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            aac_content = aac_buffer.getvalue()
            aac_buffer.close()

            logger.info("WAV to AAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WAV converted to AAC successfully",
                data=aac_content,
                format="aac",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WAV to AAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WAV to AAC",
                error=str(e)
            )

    async def convert_wav_to_ogg(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WAV to OGG."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WAV audio
            audio = AudioSegment.from_wav(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to OGG
            ogg_buffer = io.BytesIO()
            audio.export(ogg_buffer, format="ogg", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            ogg_content = ogg_buffer.getvalue()
            ogg_buffer.close()

            logger.info("WAV to OGG conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WAV converted to OGG successfully",
                data=ogg_content,
                format="ogg",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WAV to OGG conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WAV to OGG",
                error=str(e)
            )

    async def convert_wav_to_m4a(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WAV to M4A."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WAV audio
            audio = AudioSegment.from_wav(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to M4A
            m4a_buffer = io.BytesIO()
            audio.export(m4a_buffer, format="mp4", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            m4a_content = m4a_buffer.getvalue()
            m4a_buffer.close()

            logger.info("WAV to M4A conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WAV converted to M4A successfully",
                data=m4a_content,
                format="m4a",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WAV to M4A conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WAV to M4A",
                error=str(e)
            )

    async def convert_wav_to_wma(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WAV to WMA."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WAV audio
            audio = AudioSegment.from_wav(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WMA
            wma_buffer = io.BytesIO()
            audio.export(wma_buffer, format="wma", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wma_content = wma_buffer.getvalue()
            wma_buffer.close()

            logger.info("WAV to WMA conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WAV converted to WMA successfully",
                data=wma_content,
                format="wma",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WAV to WMA conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WAV to WMA",
                error=str(e)
            )

    # FLAC conversions
    async def convert_flac_to_mp3(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert FLAC to MP3."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load FLAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="flac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to MP3
            mp3_buffer = io.BytesIO()
            audio.export(mp3_buffer, format="mp3", bitrate=options.bitrate)
            mp3_content = mp3_buffer.getvalue()
            mp3_buffer.close()

            logger.info("FLAC to MP3 conversion completed")
            return AudioServiceResponse(
                status=200,
                message="FLAC converted to MP3 successfully",
                data=mp3_content,
                format="mp3",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("FLAC to MP3 conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting FLAC to MP3",
                error=str(e)
            )

    async def convert_flac_to_wav(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert FLAC to WAV."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load FLAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="flac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WAV
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wav_content = wav_buffer.getvalue()
            wav_buffer.close()

            logger.info("FLAC to WAV conversion completed")
            return AudioServiceResponse(
                status=200,
                message="FLAC converted to WAV successfully",
                data=wav_content,
                format="wav",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("FLAC to WAV conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting FLAC to WAV",
                error=str(e)
            )

    async def convert_flac_to_aac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert FLAC to AAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load FLAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="flac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to AAC
            aac_buffer = io.BytesIO()
            audio.export(aac_buffer, format="aac", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            aac_content = aac_buffer.getvalue()
            aac_buffer.close()

            logger.info("FLAC to AAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="FLAC converted to AAC successfully",
                data=aac_content,
                format="aac",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("FLAC to AAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting FLAC to AAC",
                error=str(e)
            )

    async def convert_flac_to_ogg(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert FLAC to OGG."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load FLAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="flac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to OGG
            ogg_buffer = io.BytesIO()
            audio.export(ogg_buffer, format="ogg", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            ogg_content = ogg_buffer.getvalue()
            ogg_buffer.close()

            logger.info("FLAC to OGG conversion completed")
            return AudioServiceResponse(
                status=200,
                message="FLAC converted to OGG successfully",
                data=ogg_content,
                format="ogg",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("FLAC to OGG conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting FLAC to OGG",
                error=str(e)
            )

    async def convert_flac_to_m4a(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert FLAC to M4A."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load FLAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="flac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to M4A
            m4a_buffer = io.BytesIO()
            audio.export(m4a_buffer, format="mp4", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            m4a_content = m4a_buffer.getvalue()
            m4a_buffer.close()

            logger.info("FLAC to M4A conversion completed")
            return AudioServiceResponse(
                status=200,
                message="FLAC converted to M4A successfully",
                data=m4a_content,
                format="m4a",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("FLAC to M4A conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting FLAC to M4A",
                error=str(e)
            )

    async def convert_flac_to_wma(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert FLAC to WMA."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load FLAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="flac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WMA
            wma_buffer = io.BytesIO()
            audio.export(wma_buffer, format="wma", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wma_content = wma_buffer.getvalue()
            wma_buffer.close()

            logger.info("FLAC to WMA conversion completed")
            return AudioServiceResponse(
                status=200,
                message="FLAC converted to WMA successfully",
                data=wma_content,
                format="wma",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("FLAC to WMA conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting FLAC to WMA",
                error=str(e)
            )

    # AAC conversions
    async def convert_aac_to_mp3(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert AAC to MP3."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load AAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="aac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to MP3
            mp3_buffer = io.BytesIO()
            audio.export(mp3_buffer, format="mp3", bitrate=options.bitrate)
            mp3_content = mp3_buffer.getvalue()
            mp3_buffer.close()

            logger.info("AAC to MP3 conversion completed")
            return AudioServiceResponse(
                status=200,
                message="AAC converted to MP3 successfully",
                data=mp3_content,
                format="mp3",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("AAC to MP3 conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting AAC to MP3",
                error=str(e)
            )

    async def convert_aac_to_wav(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert AAC to WAV."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load AAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="aac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WAV
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wav_content = wav_buffer.getvalue()
            wav_buffer.close()

            logger.info("AAC to WAV conversion completed")
            return AudioServiceResponse(
                status=200,
                message="AAC converted to WAV successfully",
                data=wav_content,
                format="wav",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("AAC to WAV conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting AAC to WAV",
                error=str(e)
            )

    async def convert_aac_to_flac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert AAC to FLAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load AAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="aac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to FLAC
            flac_buffer = io.BytesIO()
            audio.export(flac_buffer, format="flac", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            flac_content = flac_buffer.getvalue()
            flac_buffer.close()

            logger.info("AAC to FLAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="AAC converted to FLAC successfully",
                data=flac_content,
                format="flac",
                duration=len(audio) / 1000.0,
                bitrate="lossless",
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("AAC to FLAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting AAC to FLAC",
                error=str(e)
            )

    async def convert_aac_to_ogg(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert AAC to OGG."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load AAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="aac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to OGG
            ogg_buffer = io.BytesIO()
            audio.export(ogg_buffer, format="ogg", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            ogg_content = ogg_buffer.getvalue()
            ogg_buffer.close()

            logger.info("AAC to OGG conversion completed")
            return AudioServiceResponse(
                status=200,
                message="AAC converted to OGG successfully",
                data=ogg_content,
                format="ogg",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("AAC to OGG conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting AAC to OGG",
                error=str(e)
            )

    async def convert_aac_to_m4a(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert AAC to M4A."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load AAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="aac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to M4A
            m4a_buffer = io.BytesIO()
            audio.export(m4a_buffer, format="mp4", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            m4a_content = m4a_buffer.getvalue()
            m4a_buffer.close()

            logger.info("AAC to M4A conversion completed")
            return AudioServiceResponse(
                status=200,
                message="AAC converted to M4A successfully",
                data=m4a_content,
                format="m4a",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("AAC to M4A conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting AAC to M4A",
                error=str(e)
            )

    async def convert_aac_to_wma(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert AAC to WMA."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load AAC audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="aac")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WMA
            wma_buffer = io.BytesIO()
            audio.export(wma_buffer, format="wma", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wma_content = wma_buffer.getvalue()
            wma_buffer.close()

            logger.info("AAC to WMA conversion completed")
            return AudioServiceResponse(
                status=200,
                message="AAC converted to WMA successfully",
                data=wma_content,
                format="wma",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("AAC to WMA conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting AAC to WMA",
                error=str(e)
            )

    # OGG conversions
    async def convert_ogg_to_mp3(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert OGG to MP3."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load OGG audio
            audio = AudioSegment.from_ogg(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to MP3
            mp3_buffer = io.BytesIO()
            audio.export(mp3_buffer, format="mp3", bitrate=options.bitrate)
            mp3_content = mp3_buffer.getvalue()
            mp3_buffer.close()

            logger.info("OGG to MP3 conversion completed")
            return AudioServiceResponse(
                status=200,
                message="OGG converted to MP3 successfully",
                data=mp3_content,
                format="mp3",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("OGG to MP3 conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting OGG to MP3",
                error=str(e)
            )

    async def convert_ogg_to_wav(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert OGG to WAV."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load OGG audio
            audio = AudioSegment.from_ogg(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WAV
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wav_content = wav_buffer.getvalue()
            wav_buffer.close()

            logger.info("OGG to WAV conversion completed")
            return AudioServiceResponse(
                status=200,
                message="OGG converted to WAV successfully",
                data=wav_content,
                format="wav",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("OGG to WAV conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting OGG to WAV",
                error=str(e)
            )

    async def convert_ogg_to_flac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert OGG to FLAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load OGG audio
            audio = AudioSegment.from_ogg(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to FLAC
            flac_buffer = io.BytesIO()
            audio.export(flac_buffer, format="flac", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            flac_content = flac_buffer.getvalue()
            flac_buffer.close()

            logger.info("OGG to FLAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="OGG converted to FLAC successfully",
                data=flac_content,
                format="flac",
                duration=len(audio) / 1000.0,
                bitrate="lossless",
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("OGG to FLAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting OGG to FLAC",
                error=str(e)
            )

    async def convert_ogg_to_aac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert OGG to AAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load OGG audio
            audio = AudioSegment.from_ogg(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to AAC
            aac_buffer = io.BytesIO()
            audio.export(aac_buffer, format="aac", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            aac_content = aac_buffer.getvalue()
            aac_buffer.close()

            logger.info("OGG to AAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="OGG converted to AAC successfully",
                data=aac_content,
                format="aac",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("OGG to AAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting OGG to AAC",
                error=str(e)
            )

    async def convert_ogg_to_m4a(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert OGG to M4A."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load OGG audio
            audio = AudioSegment.from_ogg(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to M4A
            m4a_buffer = io.BytesIO()
            audio.export(m4a_buffer, format="mp4", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            m4a_content = m4a_buffer.getvalue()
            m4a_buffer.close()

            logger.info("OGG to M4A conversion completed")
            return AudioServiceResponse(
                status=200,
                message="OGG converted to M4A successfully",
                data=m4a_content,
                format="m4a",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("OGG to M4A conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting OGG to M4A",
                error=str(e)
            )

    async def convert_ogg_to_wma(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert OGG to WMA."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load OGG audio
            audio = AudioSegment.from_ogg(io.BytesIO(file_buffer))
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WMA
            wma_buffer = io.BytesIO()
            audio.export(wma_buffer, format="wma", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wma_content = wma_buffer.getvalue()
            wma_buffer.close()

            logger.info("OGG to WMA conversion completed")
            return AudioServiceResponse(
                status=200,
                message="OGG converted to WMA successfully",
                data=wma_content,
                format="wma",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("OGG to WMA conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting OGG to WMA",
                error=str(e)
            )

    # M4A conversions
    async def convert_m4a_to_mp3(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert M4A to MP3."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load M4A audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="mp4")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to MP3
            mp3_buffer = io.BytesIO()
            audio.export(mp3_buffer, format="mp3", bitrate=options.bitrate)
            mp3_content = mp3_buffer.getvalue()
            mp3_buffer.close()

            logger.info("M4A to MP3 conversion completed")
            return AudioServiceResponse(
                status=200,
                message="M4A converted to MP3 successfully",
                data=mp3_content,
                format="mp3",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("M4A to MP3 conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting M4A to MP3",
                error=str(e)
            )

    async def convert_m4a_to_wav(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert M4A to WAV."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load M4A audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="mp4")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WAV
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wav_content = wav_buffer.getvalue()
            wav_buffer.close()

            logger.info("M4A to WAV conversion completed")
            return AudioServiceResponse(
                status=200,
                message="M4A converted to WAV successfully",
                data=wav_content,
                format="wav",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("M4A to WAV conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting M4A to WAV",
                error=str(e)
            )

    async def convert_m4a_to_flac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert M4A to FLAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load M4A audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="mp4")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to FLAC
            flac_buffer = io.BytesIO()
            audio.export(flac_buffer, format="flac", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            flac_content = flac_buffer.getvalue()
            flac_buffer.close()

            logger.info("M4A to FLAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="M4A converted to FLAC successfully",
                data=flac_content,
                format="flac",
                duration=len(audio) / 1000.0,
                bitrate="lossless",
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("M4A to FLAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting M4A to FLAC",
                error=str(e)
            )

    async def convert_m4a_to_aac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert M4A to AAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load M4A audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="mp4")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to AAC
            aac_buffer = io.BytesIO()
            audio.export(aac_buffer, format="aac", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            aac_content = aac_buffer.getvalue()
            aac_buffer.close()

            logger.info("M4A to AAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="M4A converted to AAC successfully",
                data=aac_content,
                format="aac",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("M4A to AAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting M4A to AAC",
                error=str(e)
            )

    async def convert_m4a_to_ogg(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert M4A to OGG."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load M4A audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="mp4")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to OGG
            ogg_buffer = io.BytesIO()
            audio.export(ogg_buffer, format="ogg", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            ogg_content = ogg_buffer.getvalue()
            ogg_buffer.close()

            logger.info("M4A to OGG conversion completed")
            return AudioServiceResponse(
                status=200,
                message="M4A converted to OGG successfully",
                data=ogg_content,
                format="ogg",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("M4A to OGG conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting M4A to OGG",
                error=str(e)
            )

    async def convert_m4a_to_wma(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert M4A to WMA."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load M4A audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="mp4")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WMA
            wma_buffer = io.BytesIO()
            audio.export(wma_buffer, format="wma", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wma_content = wma_buffer.getvalue()
            wma_buffer.close()

            logger.info("M4A to WMA conversion completed")
            return AudioServiceResponse(
                status=200,
                message="M4A converted to WMA successfully",
                data=wma_content,
                format="wma",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("M4A to WMA conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting M4A to WMA",
                error=str(e)
            )

    # WMA conversions
    async def convert_wma_to_mp3(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WMA to MP3."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WMA audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="wma")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to MP3
            mp3_buffer = io.BytesIO()
            audio.export(mp3_buffer, format="mp3", bitrate=options.bitrate)
            mp3_content = mp3_buffer.getvalue()
            mp3_buffer.close()

            logger.info("WMA to MP3 conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WMA converted to MP3 successfully",
                data=mp3_content,
                format="mp3",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WMA to MP3 conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WMA to MP3",
                error=str(e)
            )

    async def convert_wma_to_wav(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WMA to WAV."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WMA audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="wma")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to WAV
            wav_buffer = io.BytesIO()
            audio.export(wav_buffer, format="wav", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            wav_content = wav_buffer.getvalue()
            wav_buffer.close()

            logger.info("WMA to WAV conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WMA converted to WAV successfully",
                data=wav_content,
                format="wav",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WMA to WAV conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WMA to WAV",
                error=str(e)
            )

    async def convert_wma_to_flac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WMA to FLAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WMA audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="wma")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to FLAC
            flac_buffer = io.BytesIO()
            audio.export(flac_buffer, format="flac", parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            flac_content = flac_buffer.getvalue()
            flac_buffer.close()

            logger.info("WMA to FLAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WMA converted to FLAC successfully",
                data=flac_content,
                format="flac",
                duration=len(audio) / 1000.0,
                bitrate="lossless",
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WMA to FLAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WMA to FLAC",
                error=str(e)
            )

    async def convert_wma_to_aac(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WMA to AAC."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WMA audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="wma")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to AAC
            aac_buffer = io.BytesIO()
            audio.export(aac_buffer, format="aac", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            aac_content = aac_buffer.getvalue()
            aac_buffer.close()

            logger.info("WMA to AAC conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WMA converted to AAC successfully",
                data=aac_content,
                format="aac",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WMA to AAC conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WMA to AAC",
                error=str(e)
            )

    async def convert_wma_to_ogg(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WMA to OGG."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WMA audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="wma")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to OGG
            ogg_buffer = io.BytesIO()
            audio.export(ogg_buffer, format="ogg", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            ogg_content = ogg_buffer.getvalue()
            ogg_buffer.close()

            logger.info("WMA to OGG conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WMA converted to OGG successfully",
                data=ogg_content,
                format="ogg",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WMA to OGG conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WMA to OGG",
                error=str(e)
            )

    async def convert_wma_to_m4a(
        self,
        file_buffer: bytes,
        options: Optional[AudioConversionOptions] = None
    ) -> AudioServiceResponse:
        """Convert WMA to M4A."""
        try:
            if options is None:
                options = AudioConversionOptions()

            # Load WMA audio
            audio = AudioSegment.from_file(io.BytesIO(file_buffer), format="wma")
            
            # Apply processing
            audio = self._apply_audio_processing(audio, options)
            
            # Export to M4A
            m4a_buffer = io.BytesIO()
            audio.export(m4a_buffer, format="mp4", bitrate=options.bitrate, parameters=f"-ar {options.sample_rate} -ac {options.channels}")
            m4a_content = m4a_buffer.getvalue()
            m4a_buffer.close()

            logger.info("WMA to M4A conversion completed")
            return AudioServiceResponse(
                status=200,
                message="WMA converted to M4A successfully",
                data=m4a_content,
                format="m4a",
                duration=len(audio) / 1000.0,
                bitrate=options.bitrate,
                sample_rate=options.sample_rate,
                channels=options.channels
            )

        except Exception as e:
            logger.error("WMA to M4A conversion failed", error=str(e))
            return AudioServiceResponse(
                status=500,
                message="Error converting WMA to M4A",
                error=str(e)
            )

    async def get_supported_conversions(self):
        """Get list of supported audio conversions."""
        return {
            "supported_conversions": self.supported_conversions,
            "message": "List of supported audio format conversions"
        }


# Global instance
audio_converter_service = AudioConverterService()
