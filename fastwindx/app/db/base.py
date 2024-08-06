"""
Database configuration and session management for FastWindX.
"""

import asyncio
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

# Create async engine
async_engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, future=True)

# Create sync engine for Alembic migrations and database creation
sync_engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI.replace("+asyncpg", ""), echo=True, future=True
)

# Export sync_engine as engine for compatibility
engine = sync_engine

async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


def create_db_if_not_exists():
    """
    Create the database if it doesn't exist using synchronous operations.
    """
    if not database_exists(sync_engine.url):
        create_database(sync_engine.url)


async def init_db():
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
async def get_session():
    """Yield an async session."""
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_session():
    """
    Function to get a synchronous SQLAlchemy session.
    This is mainly used for database migrations with Alembic.
    """
    return Session(sync_engine)
