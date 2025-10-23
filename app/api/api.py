"""
Main API router.
"""

from fastapi import APIRouter

from app.modules.document_converter import router as document_router

api_router = APIRouter()

# Include document converter module
api_router.include_router(document_router, prefix="/documents", tags=["Document Conversion"])

