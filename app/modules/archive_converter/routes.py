"""
Archive converter routes.
Defines API endpoints for archive format conversions.
"""

from fastapi import APIRouter
from .controller import archive_converter_controller

router = APIRouter()

# ZIP conversions
router.add_api_route(
    "/zip-to-rar",
    archive_converter_controller.convert_zip_to_rar,
    methods=["POST"],
    summary="Convert ZIP to RAR",
    description="Upload a ZIP file and convert it to RAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/zip-to-7z",
    archive_converter_controller.convert_zip_to_7z,
    methods=["POST"],
    summary="Convert ZIP to 7Z",
    description="Upload a ZIP file and convert it to 7Z format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/zip-to-tar",
    archive_converter_controller.convert_zip_to_tar,
    methods=["POST"],
    summary="Convert ZIP to TAR",
    description="Upload a ZIP file and convert it to TAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/zip-to-gz",
    archive_converter_controller.convert_zip_to_gz,
    methods=["POST"],
    summary="Convert ZIP to GZ",
    description="Upload a ZIP file and convert it to GZ format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/zip-to-bz2",
    archive_converter_controller.convert_zip_to_bz2,
    methods=["POST"],
    summary="Convert ZIP to BZ2",
    description="Upload a ZIP file and convert it to BZ2 format",
    tags=["Archive Conversion"]
)

# RAR conversions
router.add_api_route(
    "/rar-to-zip",
    archive_converter_controller.convert_rar_to_zip,
    methods=["POST"],
    summary="Convert RAR to ZIP",
    description="Upload a RAR file and convert it to ZIP format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/rar-to-7z",
    archive_converter_controller.convert_rar_to_7z,
    methods=["POST"],
    summary="Convert RAR to 7Z",
    description="Upload a RAR file and convert it to 7Z format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/rar-to-tar",
    archive_converter_controller.convert_rar_to_tar,
    methods=["POST"],
    summary="Convert RAR to TAR",
    description="Upload a RAR file and convert it to TAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/rar-to-gz",
    archive_converter_controller.convert_rar_to_gz,
    methods=["POST"],
    summary="Convert RAR to GZ",
    description="Upload a RAR file and convert it to GZ format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/rar-to-bz2",
    archive_converter_controller.convert_rar_to_bz2,
    methods=["POST"],
    summary="Convert RAR to BZ2",
    description="Upload a RAR file and convert it to BZ2 format",
    tags=["Archive Conversion"]
)

# 7Z conversions
router.add_api_route(
    "/7z-to-zip",
    archive_converter_controller.convert_7z_to_zip,
    methods=["POST"],
    summary="Convert 7Z to ZIP",
    description="Upload a 7Z file and convert it to ZIP format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/7z-to-rar",
    archive_converter_controller.convert_7z_to_rar,
    methods=["POST"],
    summary="Convert 7Z to RAR",
    description="Upload a 7Z file and convert it to RAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/7z-to-tar",
    archive_converter_controller.convert_7z_to_tar,
    methods=["POST"],
    summary="Convert 7Z to TAR",
    description="Upload a 7Z file and convert it to TAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/7z-to-gz",
    archive_converter_controller.convert_7z_to_gz,
    methods=["POST"],
    summary="Convert 7Z to GZ",
    description="Upload a 7Z file and convert it to GZ format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/7z-to-bz2",
    archive_converter_controller.convert_7z_to_bz2,
    methods=["POST"],
    summary="Convert 7Z to BZ2",
    description="Upload a 7Z file and convert it to BZ2 format",
    tags=["Archive Conversion"]
)

# TAR conversions
router.add_api_route(
    "/tar-to-zip",
    archive_converter_controller.convert_tar_to_zip,
    methods=["POST"],
    summary="Convert TAR to ZIP",
    description="Upload a TAR file and convert it to ZIP format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/tar-to-rar",
    archive_converter_controller.convert_tar_to_rar,
    methods=["POST"],
    summary="Convert TAR to RAR",
    description="Upload a TAR file and convert it to RAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/tar-to-7z",
    archive_converter_controller.convert_tar_to_7z,
    methods=["POST"],
    summary="Convert TAR to 7Z",
    description="Upload a TAR file and convert it to 7Z format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/tar-to-gz",
    archive_converter_controller.convert_tar_to_gz,
    methods=["POST"],
    summary="Convert TAR to GZ",
    description="Upload a TAR file and convert it to GZ format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/tar-to-bz2",
    archive_converter_controller.convert_tar_to_bz2,
    methods=["POST"],
    summary="Convert TAR to BZ2",
    description="Upload a TAR file and convert it to BZ2 format",
    tags=["Archive Conversion"]
)

# GZ conversions
router.add_api_route(
    "/gz-to-zip",
    archive_converter_controller.convert_gz_to_zip,
    methods=["POST"],
    summary="Convert GZ to ZIP",
    description="Upload a GZ file and convert it to ZIP format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/gz-to-rar",
    archive_converter_controller.convert_gz_to_rar,
    methods=["POST"],
    summary="Convert GZ to RAR",
    description="Upload a GZ file and convert it to RAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/gz-to-7z",
    archive_converter_controller.convert_gz_to_7z,
    methods=["POST"],
    summary="Convert GZ to 7Z",
    description="Upload a GZ file and convert it to 7Z format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/gz-to-tar",
    archive_converter_controller.convert_gz_to_tar,
    methods=["POST"],
    summary="Convert GZ to TAR",
    description="Upload a GZ file and convert it to TAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/gz-to-bz2",
    archive_converter_controller.convert_gz_to_bz2,
    methods=["POST"],
    summary="Convert GZ to BZ2",
    description="Upload a GZ file and convert it to BZ2 format",
    tags=["Archive Conversion"]
)

# BZ2 conversions
router.add_api_route(
    "/bz2-to-zip",
    archive_converter_controller.convert_bz2_to_zip,
    methods=["POST"],
    summary="Convert BZ2 to ZIP",
    description="Upload a BZ2 file and convert it to ZIP format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/bz2-to-rar",
    archive_converter_controller.convert_bz2_to_rar,
    methods=["POST"],
    summary="Convert BZ2 to RAR",
    description="Upload a BZ2 file and convert it to RAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/bz2-to-7z",
    archive_converter_controller.convert_bz2_to_7z,
    methods=["POST"],
    summary="Convert BZ2 to 7Z",
    description="Upload a BZ2 file and convert it to 7Z format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/bz2-to-tar",
    archive_converter_controller.convert_bz2_to_tar,
    methods=["POST"],
    summary="Convert BZ2 to TAR",
    description="Upload a BZ2 file and convert it to TAR format",
    tags=["Archive Conversion"]
)

router.add_api_route(
    "/bz2-to-gz",
    archive_converter_controller.convert_bz2_to_gz,
    methods=["POST"],
    summary="Convert BZ2 to GZ",
    description="Upload a BZ2 file and convert it to GZ format",
    tags=["Archive Conversion"]
)

# Get supported conversions
router.add_api_route(
    "/supported-conversions",
    archive_converter_controller.get_supported_conversions,
    methods=["GET"],
    summary="Get supported archive conversions",
    description="Get list of all supported archive format conversions",
    tags=["Archive Conversion"]
)
