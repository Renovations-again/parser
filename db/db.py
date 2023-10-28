from sqlalchemy.ext.asyncio import create_async_engine

from parsing.core.config import Settings


async_engine = create_async_engine(
    Settings.db_url_asyncpg, future=True, echo=True
)
