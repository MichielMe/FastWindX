"""
FastWindX: A SPA framework using FastAPI and HTMX.
"""

__version__ = "0.1.0"

from fastwindx.core.config import settings
from fastwindx.core.exceptions import FastWindXException

__all__ = ["settings", "FastWindXException"]
