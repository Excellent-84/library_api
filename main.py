import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError

from app.authors import authors_router
from app.books import books_router
from app.config import settings
from app.exceptions import (
    integrity_error_handler,
    validation_exception_handler,
)
from app.rebooks import rebooks_router
from app.users import users_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("library_api")

app = FastAPI(
    title="Library Management API",
    description="""
    RESTful API для управления библиотечным каталогом:

    - Управление книгами, авторами и читателями
    - Выдача и возврат книг
    - Разделение прав пользователей: администратор и читатель
    """,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)

app.include_router(users_router)
app.include_router(authors_router)
app.include_router(books_router)
app.include_router(rebooks_router)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=settings.HOST, port=settings.PORT, reload=True
    )
