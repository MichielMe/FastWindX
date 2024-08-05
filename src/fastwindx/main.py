"""
Main application module for FastWindX.
"""

import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from fastwindx.api.v1.api import api_router
from fastwindx.core.config import settings
from fastwindx.db.base import init_db
from fastwindx.views.main import router as main_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI app.
    """
    logger.info("Initializing database connection.")
    await init_db()
    logger.info("Database connection initialized.")
    logger.info("App started.")
    yield
    logger.info("App shutting down.")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Mount static files
app.mount("/static", StaticFiles(directory=Path(__file__).parent / "static"), name="static")

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

app.include_router(main_router)


@app.get("/health")
async def health():
    """
    Health check endpoint.
    """
    return {"status": "ok"}
