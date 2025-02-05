from fastapi import status

from ..users import CustomException


class LimitException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User has reached the borrowing limit"


class AvailableException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "No copies available"


class RebookNotFoundException(CustomException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Rebook record not found"


class RebookReturnException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Book has already been returned"
