from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass
class ServiceResult(Generic[T]):
    """
    A standardized container for service responses.
    Mimics Go-style error handling: (result, error)
    """

    success: bool
    message: str
    data: T | None = None


class Service:
    """
    Base class for all services to provide consistent response formatting.
    """

    @staticmethod
    def success(message: str, data: T = None) -> ServiceResult[T]:
        return ServiceResult(success=True, message=message, data=data)

    @staticmethod
    def failure(message: str, data: Any = None) -> ServiceResult[Any]:
        return ServiceResult(success=False, message=message, data=data)
