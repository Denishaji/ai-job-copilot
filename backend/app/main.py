# app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import health, jobs, profile


def create_app() -> FastAPI:
    """Application factory function."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
    )

    origins = [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,        # or ["*"] for local dev only
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(jobs.router)
    app.include_router(profile.router)

    return app


app = create_app()
