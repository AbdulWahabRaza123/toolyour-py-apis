"""
Main API router.
"""

from fastapi import APIRouter

from app.modules.document_converter import router as document_router
from app.modules.web_converter import router as web_router
from app.modules.office_converter import router as office_router
from app.modules.ebook_converter import router as ebook_router
from app.modules.archive_converter import router as archive_router
from app.modules.audio_converter import router as audio_router
from app.modules.video_converter import router as video_router

api_router = APIRouter()

# Include document converter module
api_router.include_router(document_router, prefix="/documents", tags=["Document Conversion"])

# Include web converter module
api_router.include_router(web_router, prefix="/web", tags=["Web Conversion"])

# Include office converter module
api_router.include_router(office_router, prefix="/office", tags=["Office Conversion"])

# Include eBook converter module
api_router.include_router(ebook_router, prefix="/ebook", tags=["eBook Conversion"])

# Include archive converter module
api_router.include_router(archive_router, prefix="/archive", tags=["Archive Conversion"])

# Include audio converter module
api_router.include_router(audio_router, prefix="/audio", tags=["Audio Conversion"])

# Include video converter module
api_router.include_router(video_router, prefix="/video", tags=["Video Conversion"])

