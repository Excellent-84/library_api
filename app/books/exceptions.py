from fastapi import status

from ..users import CustomException


class NotEnoughCopiesException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Not enough available copies of the book"


class BookNotFoundException(CustomException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Book not found"
