"""
Pydantic-схемы для работы с пользователями:

- Валидации данных пользователей (создание, обновление).
- Формирования ответа API с информацией о пользователях.
- Обработки запросов для входа и работы с токенами.
"""

from typing import Annotated, Optional

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from .enums import UserRole


class UserBase(BaseModel):
    """
    Базовая схема для создания и обновления данных пользователя.
    """

    email: EmailStr = Field(
        ...,
        title="Email пользователя",
        description="Должен быть валидным адресом электронной почты.",
        json_schema_extra={"example": "example@example.com"},
    )


class UserCreate(UserBase):
    """
    Схема для создания пользователя.
    """

    username: Annotated[str, MinLen(3), MaxLen(20)] = Field(
        ...,
        title="Имя пользователя",
        description="Имя пользователя должно содержать от 3 до 20 символов.",
        json_schema_extra={"example": "example_user"},
    )
    password: Annotated[str, MinLen(8), MaxLen(16)] = Field(
        ...,
        title="Пароль",
        description="Пароль должен содержать от 8 до 16 символов.",
        json_schema_extra={"example": "example_password"},
    )
    role: str = Field(
        default=UserRole.READER.value,
        title="Роль пользователя",
        description="Роль нового пользователя. По умолчанию - 'reader'.",
        json_schema_extra={"example": UserRole.READER.value},
    )


class UserUpdate(BaseModel):
    """
    Схема для обновления данных пользователя.
    Оба поля являются необязательными.
    """

    username: Optional[Annotated[str, MinLen(3), MaxLen(20)]] = Field(
        None,
        title="Новое имя пользователя",
        description="Имя пользователя должно содержать от 3 до 20 символов.",
        json_schema_extra={"example": "updated_user"},
    )
    password: Optional[Annotated[str, MinLen(8), MaxLen(16)]] = Field(
        None,
        title="Новый пароль",
        description="Пароль должен содержать от 8 до 16 символов.",
        json_schema_extra={"example": "updated_password"},
    )


class UserResponse(UserBase):
    """
    Схема для ответа с данными пользователя.
    """

    id: int = Field(
        ...,
        title="ID пользователя",
        description="Уникальный идентификатор пользователя.",
        json_schema_extra={"example": 1},
    )
    username: str = Field(
        ...,
        title="Имя пользователя",
        description="Имя пользователя, указанное при регистрации.",
        json_schema_extra={"example": "example_user"},
    )
    is_active: bool = Field(
        ...,
        title="Статус активности",
        description="Показывает, активен ли пользователь.",
        json_schema_extra={"example": True},
    )
    role: str = Field(
        ...,
        title="Роль пользователя",
        description="Роль пользователя (например, 'reader' или 'admin').",
        json_schema_extra={"example": UserRole.READER.value},
    )

    model_config = ConfigDict(from_attributes=True)


class UserRebookResponse(UserResponse):
    """
    Схема для ответа с данными пользователя и выданных ему книгах (rebooks).
    """

    rebooks: Optional[list] = Field(
        None,
        title="Книги пользователя",
        description="Список книг, взятых пользователем.",
        json_schema_extra={
            "example": [{"id": 1, "title": "Book", "author": "Author Name"}]
        },
    )

    model_config = ConfigDict(from_attributes=True)

    def set_rebooks(self, rebooks_data):
        from ..rebooks import RebookResponse

        self.rebooks = [RebookResponse.model_validate(r) for r in rebooks_data]


class LoginRequest(BaseModel):
    """
    Схема для запроса на вход пользователя.
    """

    email: EmailStr = Field(
        ...,
        title="Email",
        description="Электронная почта пользователя.",
        json_schema_extra={"example": "example@example.com"},
    )
    password: Annotated[str, MinLen(8), MaxLen(16)] = Field(
        ...,
        title="Пароль",
        description="Пароль пользователя.",
        json_schema_extra={"example": "example_password"},
    )


class Token(BaseModel):
    """
    Схема для токена.
    """

    access_token: str = Field(
        ...,
        title="Токен доступа",
        description="JWT токен, используемый для авторизации.",
        json_schema_extra={"example": "eyJhbGciOiJIUzI1NiIsInR5cCI6Ik..."},
    )
    token_type: str = Field(
        default="bearer",
        title="Тип токена",
        description="Тип токена. Обычно 'bearer'.",
        json_schema_extra={"example": "bearer"},
    )


class RoleUpdate(BaseModel):
    """
    Схема для обновления роли пользователя.
    """

    new_role: str = Field(
        ...,
        title="Новая роль",
        description="Роль, которую нужно установить для пользователя.",
        json_schema_extra={"example": UserRole.ADMIN.value},
    )
