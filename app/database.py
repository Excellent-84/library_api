"""
Модуль для настройки асинхронной базы данных.

- `engine`: Асинхронный движок SQLAlchemy для работы с PostgreSQL.
- `async_session`: Фабрика сессий для работы с базой данных.
- `Base`: Базовый класс для всех моделей ORM.
"""

import logging
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from .config import settings

logger = logging.getLogger("database")

try:
    engine = create_async_engine(settings.async_database_url, echo=True)
except Exception as e:
    raise RuntimeError(f"Error initializing database engine: {e}")

async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[Any, Any]:
    logger.info("Starting database session")
    async with async_session() as session:
        yield session
    logger.info("Database session closed")


class Base(DeclarativeBase):
    pass
