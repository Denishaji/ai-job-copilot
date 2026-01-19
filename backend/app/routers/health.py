# app/routers/health.py
from fastapi import APIRouter
from app.config import settings


router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    """Simple health check endpoint."""
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "version": settings.app_version,
    }
