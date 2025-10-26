"""
Video converter routes.
Defines API endpoints for video format conversions.
"""

from fastapi import APIRouter
from .controller import video_converter_controller

router = APIRouter()

# MP4 conversions
router.add_api_route(
    "/mp4-to-avi",
    video_converter_controller.convert_mp4_to_avi,
    methods=["POST"],
    summary="Convert MP4 to AVI",
    description="Upload an MP4 file and convert it to AVI format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/mp4-to-mov",
    video_converter_controller.convert_mp4_to_mov,
    methods=["POST"],
    summary="Convert MP4 to MOV",
    description="Upload an MP4 file and convert it to MOV format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/mp4-to-mkv",
    video_converter_controller.convert_mp4_to_mkv,
    methods=["POST"],
    summary="Convert MP4 to MKV",
    description="Upload an MP4 file and convert it to MKV format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/mp4-to-webm",
    video_converter_controller.convert_mp4_to_webm,
    methods=["POST"],
    summary="Convert MP4 to WEBM",
    description="Upload an MP4 file and convert it to WEBM format",
    tags=["Video Conversion"]
)

# AVI conversions
router.add_api_route(
    "/avi-to-mp4",
    video_converter_controller.convert_avi_to_mp4,
    methods=["POST"],
    summary="Convert AVI to MP4",
    description="Upload an AVI file and convert it to MP4 format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/avi-to-mov",
    video_converter_controller.convert_avi_to_mov,
    methods=["POST"],
    summary="Convert AVI to MOV",
    description="Upload an AVI file and convert it to MOV format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/avi-to-mkv",
    video_converter_controller.convert_avi_to_mkv,
    methods=["POST"],
    summary="Convert AVI to MKV",
    description="Upload an AVI file and convert it to MKV format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/avi-to-webm",
    video_converter_controller.convert_avi_to_webm,
    methods=["POST"],
    summary="Convert AVI to WEBM",
    description="Upload an AVI file and convert it to WEBM format",
    tags=["Video Conversion"]
)

# MOV conversions
router.add_api_route(
    "/mov-to-mp4",
    video_converter_controller.convert_mov_to_mp4,
    methods=["POST"],
    summary="Convert MOV to MP4",
    description="Upload a MOV file and convert it to MP4 format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/mov-to-avi",
    video_converter_controller.convert_mov_to_avi,
    methods=["POST"],
    summary="Convert MOV to AVI",
    description="Upload a MOV file and convert it to AVI format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/mov-to-mkv",
    video_converter_controller.convert_mov_to_mkv,
    methods=["POST"],
    summary="Convert MOV to MKV",
    description="Upload a MOV file and convert it to MKV format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/mov-to-webm",
    video_converter_controller.convert_mov_to_webm,
    methods=["POST"],
    summary="Convert MOV to WEBM",
    description="Upload a MOV file and convert it to WEBM format",
    tags=["Video Conversion"]
)

# MKV conversions
router.add_api_route(
    "/mkv-to-mp4",
    video_converter_controller.convert_mkv_to_mp4,
    methods=["POST"],
    summary="Convert MKV to MP4",
    description="Upload an MKV file and convert it to MP4 format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/mkv-to-avi",
    video_converter_controller.convert_mkv_to_avi,
    methods=["POST"],
    summary="Convert MKV to AVI",
    description="Upload an MKV file and convert it to AVI format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/mkv-to-mov",
    video_converter_controller.convert_mkv_to_mov,
    methods=["POST"],
    summary="Convert MKV to MOV",
    description="Upload an MKV file and convert it to MOV format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/mkv-to-webm",
    video_converter_controller.convert_mkv_to_webm,
    methods=["POST"],
    summary="Convert MKV to WEBM",
    description="Upload an MKV file and convert it to WEBM format",
    tags=["Video Conversion"]
)

# WEBM conversions
router.add_api_route(
    "/webm-to-mp4",
    video_converter_controller.convert_webm_to_mp4,
    methods=["POST"],
    summary="Convert WEBM to MP4",
    description="Upload a WEBM file and convert it to MP4 format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/webm-to-avi",
    video_converter_controller.convert_webm_to_avi,
    methods=["POST"],
    summary="Convert WEBM to AVI",
    description="Upload a WEBM file and convert it to AVI format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/webm-to-mov",
    video_converter_controller.convert_webm_to_mov,
    methods=["POST"],
    summary="Convert WEBM to MOV",
    description="Upload a WEBM file and convert it to MOV format",
    tags=["Video Conversion"]
)

router.add_api_route(
    "/webm-to-mkv",
    video_converter_controller.convert_webm_to_mkv,
    methods=["POST"],
    summary="Convert WEBM to MKV",
    description="Upload a WEBM file and convert it to MKV format",
    tags=["Video Conversion"]
)

# Get supported conversions
router.add_api_route(
    "/supported-conversions",
    video_converter_controller.get_supported_conversions,
    methods=["GET"],
    summary="Get supported video conversions",
    description="Get list of all supported video format conversions",
    tags=["Video Conversion"]
)
