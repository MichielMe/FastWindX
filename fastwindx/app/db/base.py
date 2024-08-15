"""
Database configuration and session management for FastWindX.
"""

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import SQLModel, create_engine

from app.core.config import settings

# Ensure SQLALCHEMY_DATABASE_URI is a string
if settings.SQLALCHEMY_DATABASE_URI is None:
    raise ValueError("SQLALCHEMY_DATABASE_URI must be set")

# Create async engine
async_engine: AsyncEngine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, future=True)

# Create sync engine for Alembic migrations and database creation
sync_engine = create_engine(settings.SQLALCHEMY_DATABASE_URI.replace("+asyncpg", ""), echo=True, future=True)

# Export sync_engine as engine for compatibility
engine = sync_engine

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def create_db_if_not_exists() -> None:
    """
    Create the database if it doesn't exist using synchronous operations.
    """
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)


async def init_db() -> None:
    """
    Initialize the database by creating it if it doesn't exist and then creating all tables.
    """
    # Run the synchronous database creation in a separate thread
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, create_db_if_not_exists)

    # Now we can use the async engine to create tables
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Yield an async session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError:
            await session.rollback()
            raise
        finally:
            await session.close()


def get_sync_session() -> Session:
    """
    Function to get a synchronous SQLAlchemy session.
    This is mainly used for database migrations with Alembic.
    """
    return sessionmaker(bind=sync_engine, autocommit=False, autoflush=False)()
