from typing import Any, TypeVar
from fastapi import HTTPException, status

from src.core.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class HeroNotFoundException(HTTPException):
    """Hero not found HTTP exception."""

    def __init__(
        self,
        hero_name: str,
        headers: dict[str, Any] | None = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find hero with name '{hero_name}'.",
            headers=headers,
        )


class DBHeroNotFoundException(Exception):
    """
    Model not found exception
    """

    def __init__(
        self,
        model_type: ModelType,
        name: str,
        *args: object,
    ) -> None:
        model_name = model_type.__name__
        message = f"Model '{model_name}' with name '{name}' not found."
        super().__init__(message, *args)
        self.model_type = model_type
        self.name = name