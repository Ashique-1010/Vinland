from fastapi import HTTPException, status

class CustomException(HTTPException):
    def __init__(
            self,
            status_code: int,
            detail: str = None,
            headers: dict = None,
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)

class CredentialsException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

class UserNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

class PostNotFoundException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found",
        )

class UnauthorizedException(CustomException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform this action",
        )

