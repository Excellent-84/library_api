import logging

from fastapi import status
from fastapi.responses import JSONResponse

logger = logging.getLogger("library_api")


async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc.errors()}")
    error_messages = [error["msg"] for error in exc.errors()]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": error_messages},
    )


async def integrity_error_handler(request, exc):
    logger.error(f"Integrity error: {str(exc)}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Database integrity error."},
    )
