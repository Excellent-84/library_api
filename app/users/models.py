from datetime import datetime

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from ..database import Base
from .enums import UserRole


class BaseModel(Base):
    """Абстрактная базовая модель. Содержит общие для всех моделей поля."""

    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, doc="Уникальный идентификатор"
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), doc="Дата и время создания записи"
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        doc="Дата и время последнего обновления записи",
    )


class User(BaseModel):
    """Модель пользователя."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(20), nullable=False, doc="Имя пользователя"
    )
    email: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        doc="Электронная почта",
    )
    hashed_password: Mapped[str] = mapped_column(
        String(255), nullable=False, doc="Хешированный пароль"
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, doc="Статус активности пользователя"
    )
    role: Mapped[str] = mapped_column(
        String(20),
        default=UserRole.READER.value,
        doc="Роль пользователя (по умолчанию - 'reader')",
    )
