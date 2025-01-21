from fastapi import HTTPException, status


class CustomException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=self.status_code,
            detail=self.detail,
            headers=self.headers
        )


class LoginException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Incorrect username or password"
    headers = {"WWW-Authenticate": "Bearer"}


class UserExistsException(CustomException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = "User with this username already exists"
    headers = {"WWW-Authenticate": "Bearer"}


class CredentialsException(CustomException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}
