from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str
    data: Optional[T] = None


class PaginatedResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str
    data: Optional[T] = None
    total: int = 0
    skip: int = 0
    limit: int = 100
