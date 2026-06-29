from dataclasses import dataclass
from typing import Any, Generic, Literal, TypeVar, overload

T = TypeVar("T")


@dataclass
class Success(Generic[T]):
    """
    A standardized container for successful service responses.
    """

    success: Literal[True]
    message: str
    data: T


@dataclass
class Failure:
    """
    A standardized container for failed service responses.
    """

    success: Literal[False]
    message: str
    data: Any = None


ServiceResult = Success[T] | Failure


class Service:
    """
    Base class for all services to provide consistent response formatting.
    """

    @staticmethod
    @overload
    def success(message: str) -> Success[None]: ...

    @staticmethod
    @overload
    def success(message: str, data: T) -> Success[T]: ...

    @staticmethod
    def success(message: str, data: Any = None) -> Success[Any]:
        return Success(success=True, message=message, data=data)

    @staticmethod
    def failure(message: str, data: Any = None) -> Failure:
        return Failure(success=False, message=message, data=data)
