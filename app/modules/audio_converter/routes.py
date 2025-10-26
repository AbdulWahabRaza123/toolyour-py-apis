"""
Audio converter routes.
Defines API endpoints for audio format conversions.
"""

from fastapi import APIRouter
from .controller import audio_converter_controller

router = APIRouter()

# MP3 conversions
router.add_api_route(
    "/mp3-to-wav",
    audio_converter_controller.convert_mp3_to_wav,
    methods=["POST"],
    summary="Convert MP3 to WAV",
    description="Upload an MP3 file and convert it to WAV format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/mp3-to-flac",
    audio_converter_controller.convert_mp3_to_flac,
    methods=["POST"],
    summary="Convert MP3 to FLAC",
    description="Upload an MP3 file and convert it to FLAC format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/mp3-to-aac",
    audio_converter_controller.convert_mp3_to_aac,
    methods=["POST"],
    summary="Convert MP3 to AAC",
    description="Upload an MP3 file and convert it to AAC format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/mp3-to-ogg",
    audio_converter_controller.convert_mp3_to_ogg,
    methods=["POST"],
    summary="Convert MP3 to OGG",
    description="Upload an MP3 file and convert it to OGG format",
    tags=["Audio Conversion"]
)

# WAV conversions
router.add_api_route(
    "/wav-to-mp3",
    audio_converter_controller.convert_wav_to_mp3,
    methods=["POST"],
    summary="Convert WAV to MP3",
    description="Upload a WAV file and convert it to MP3 format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/wav-to-flac",
    audio_converter_controller.convert_wav_to_flac,
    methods=["POST"],
    summary="Convert WAV to FLAC",
    description="Upload a WAV file and convert it to FLAC format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/wav-to-aac",
    audio_converter_controller.convert_wav_to_aac,
    methods=["POST"],
    summary="Convert WAV to AAC",
    description="Upload a WAV file and convert it to AAC format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/wav-to-ogg",
    audio_converter_controller.convert_wav_to_ogg,
    methods=["POST"],
    summary="Convert WAV to OGG",
    description="Upload a WAV file and convert it to OGG format",
    tags=["Audio Conversion"]
)

# FLAC conversions
router.add_api_route(
    "/flac-to-mp3",
    audio_converter_controller.convert_flac_to_mp3,
    methods=["POST"],
    summary="Convert FLAC to MP3",
    description="Upload a FLAC file and convert it to MP3 format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/flac-to-wav",
    audio_converter_controller.convert_flac_to_wav,
    methods=["POST"],
    summary="Convert FLAC to WAV",
    description="Upload a FLAC file and convert it to WAV format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/flac-to-aac",
    audio_converter_controller.convert_flac_to_aac,
    methods=["POST"],
    summary="Convert FLAC to AAC",
    description="Upload a FLAC file and convert it to AAC format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/flac-to-ogg",
    audio_converter_controller.convert_flac_to_ogg,
    methods=["POST"],
    summary="Convert FLAC to OGG",
    description="Upload a FLAC file and convert it to OGG format",
    tags=["Audio Conversion"]
)

# AAC conversions
router.add_api_route(
    "/aac-to-mp3",
    audio_converter_controller.convert_aac_to_mp3,
    methods=["POST"],
    summary="Convert AAC to MP3",
    description="Upload an AAC file and convert it to MP3 format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/aac-to-wav",
    audio_converter_controller.convert_aac_to_wav,
    methods=["POST"],
    summary="Convert AAC to WAV",
    description="Upload an AAC file and convert it to WAV format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/aac-to-flac",
    audio_converter_controller.convert_aac_to_flac,
    methods=["POST"],
    summary="Convert AAC to FLAC",
    description="Upload an AAC file and convert it to FLAC format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/aac-to-ogg",
    audio_converter_controller.convert_aac_to_ogg,
    methods=["POST"],
    summary="Convert AAC to OGG",
    description="Upload an AAC file and convert it to OGG format",
    tags=["Audio Conversion"]
)

# OGG conversions
router.add_api_route(
    "/ogg-to-mp3",
    audio_converter_controller.convert_ogg_to_mp3,
    methods=["POST"],
    summary="Convert OGG to MP3",
    description="Upload an OGG file and convert it to MP3 format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/ogg-to-wav",
    audio_converter_controller.convert_ogg_to_wav,
    methods=["POST"],
    summary="Convert OGG to WAV",
    description="Upload an OGG file and convert it to WAV format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/ogg-to-flac",
    audio_converter_controller.convert_ogg_to_flac,
    methods=["POST"],
    summary="Convert OGG to FLAC",
    description="Upload an OGG file and convert it to FLAC format",
    tags=["Audio Conversion"]
)

router.add_api_route(
    "/ogg-to-aac",
    audio_converter_controller.convert_ogg_to_aac,
    methods=["POST"],
    summary="Convert OGG to AAC",
    description="Upload an OGG file and convert it to AAC format",
    tags=["Audio Conversion"]
)

# Get supported conversions
router.add_api_route(
    "/supported-conversions",
    audio_converter_controller.get_supported_conversions,
    methods=["GET"],
    summary="Get supported audio conversions",
    description="Get list of all supported audio format conversions",
    tags=["Audio Conversion"]
)
