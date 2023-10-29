from sqlalchemy.ext.asyncio import create_async_engine

from parsing.core.config import settings


async_engine = create_async_engine(
    settings.db_url_asyncpg, future=True, echo=True
)
