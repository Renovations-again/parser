from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession
)

from parsing.core.config import settings


async_engine = create_async_engine(
    settings.db_url_asyncpg, future=True, echo=True
)
async_session_maker = async_sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

# Пока не понятно зачем вообще использовать этот AsyncGenerator
# async def get_async_session() -> AsyncGenerator:
#     '''Get sqlalchemy async session.

#     yield:
#         object: sqlalchemy async session
#     '''
#     async_session = async_sessionmaker(
#         bind=async_engine,
#         expire_on_commit=False,
#     )
#     async with async_session() as session:
#         yield session
