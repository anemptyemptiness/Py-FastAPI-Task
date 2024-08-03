from fastapi import HTTPException, status


class UnAuthedUserException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid username or password"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyRegisteredException(HTTPException):
    status_code = status.HTTP_409_CONFLICT
    detail = "User already registered"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserNotFoundException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "User not found"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class InvalidTokenException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Invalid token error"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)