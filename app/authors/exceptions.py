from fastapi import status

from ..users import CustomException


class AuthorExistsException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Author with this name already exists"


class AuthorNotFoundException(CustomException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Author not found"
