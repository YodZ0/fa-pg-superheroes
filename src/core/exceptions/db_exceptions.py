from typing import TypeVar

from src.core.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class ModelNotFoundException(Exception):
    """
    Model not found exception
    """

    def __init__(
        self,
        model_type: ModelType,
        object_id: int,
        *args: object,
    ) -> None:
        model_name = model_type.__name__
        message = f"Model '{model_name}' with id = {object_id} not found."
        super().__init__(message, *args)
        self.model_type = model_type
        self.object_id = object_id


class ModelAlreadyExistsException(Exception):
    """
    Model with an existing unique field exception.
    """

    def __init__(
        self,
        model_type: ModelType,
        field_name: str,
        *args: object,
    ) -> None:
        model_name = model_type.__name__
        message = (
            f"Model '{model_name}' already exists with a unique field '{field_name}'."
        )
        super().__init__(message, *args)
        self.model_type = model_type
        self.field_name = field_name