"""
Main router for the API v1.
"""

from fastapi import APIRouter

from fastwindx.api.v1.endpoints import users

api_router = APIRouter()

api_router.include_router(users.router, prefix="/users", tags=["users"])

# Add more routers here as you create them
# For example:
# from fastwindx.api.v1.endpoints import items
# api_router.include_router(items.router, prefix="/items", tags=["items"])
