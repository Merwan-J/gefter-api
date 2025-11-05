from fastapi import HTTPException
from typing import Optional


class BaseAPIException(HTTPException):
    def __init__(self, status_code: int, detail: str, headers: Optional[dict] = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class NotFoundError(BaseAPIException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)


class UnauthorizedError(BaseAPIException):
    def __init__(self, detail: str = "Not authorized to access this resource"):
        super().__init__(status_code=403, detail=detail)


class BadRequestError(BaseAPIException):
    def __init__(self, detail: str):
        super().__init__(status_code=400, detail=detail)


class InternalServerError(BaseAPIException):
    def __init__(self, detail: str = "An unexpected error occurred"):
        super().__init__(status_code=500, detail=detail)
