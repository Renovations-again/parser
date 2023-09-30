from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from core.config import settings

async_engine = create_async_engine(
    settings.db_url_asyncpg, future=True, echo=True
)


async def get_async_session() -> AsyncGenerator:
    """Get sqlalchemy async session.

    yield:
        object: sqlalchemy async session
    """
    async_session = async_sessionmaker(
        bind=async_engine, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
