from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from ..database import Base
from .enums import UserRole


class BaseModel(Base):
    """
    Абстрактная базовая модель.

    Содержит общие для всех моделей поля:
    - id: Уникальный идентификатор записи
    - created_at: Дата и время создания записи
    - updated_at: Дата и время последнего обновления записи
    """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class User(BaseModel):
    """
    Модель пользователя.

    Содержит информацию о пользователе:
    - username: Имя пользователя
    - email: Электронная почта (уникальное поле)
    - hashed_password: Хешированный пароль
    - is_active: Статус активности пользователя
    - role: Роль пользователя (по умолчанию - "reader")
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    role: Mapped[str] = mapped_column(default=UserRole.READER.value)
