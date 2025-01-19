from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession, async_sessionmaker, create_async_engine
)
from sqlalchemy.orm import DeclarativeBase

from .config import settings

engine = create_async_engine(settings.async_database_url, echo=True)

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[Any, Any]:
    async with async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
