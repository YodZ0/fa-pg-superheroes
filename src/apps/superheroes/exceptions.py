from typing import Any, TypeVar, Dict, Optional
from fastapi import HTTPException, status

from src.core.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class HeroNotFoundException(HTTPException):
    """Hero not found HTTP exception."""

    def __init__(
        self,
        hero_name: str,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find hero with name '{hero_name}'.",
            headers=headers,
        )


class FilteredHeroesNotFoundException(HTTPException):
    """Heroes with passed filters not found HTTP exception."""

    def __init__(
        self,
        filters: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Unable to find heroes with filters '{filters}'.",
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


class DBFilteredHeroesNotFoundException(Exception):
    """
    Models with passed filters not found exception
    """

    def __init__(
        self,
        model_type: ModelType,
        filters: Dict[str, Any],
        *args: object,
    ) -> None:
        model_name = model_type.__name__
        message = f"Models '{model_name}' with filters '{filters}' not found."
        super().__init__(message, *args)
        self.model_type = model_type
        self.filters = filters
