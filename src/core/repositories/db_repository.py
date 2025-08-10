import uuid
import logging
from typing import Protocol, TypeVar

from pydantic import BaseModel

from sqlalchemy import insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from src.core.models.base import Base
from src.core.exceptions.db_exceptions import (
    ModelNotFoundException,
    ModelAlreadyExistsException,
)
from src.core.schemas.db_schemas import CreateBaseModel, UpdateBaseModel


logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Base, covariant=True)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=CreateBaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=UpdateBaseModel)


class DatabaseRepositoryProtocol(
    Protocol[
        ModelType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    """
    Base Database CRUD repository interface.
    """

    async def create(self, create_object: CreateSchemaType) -> ReadSchemaType: ...

    async def update(self, update_object: UpdateSchemaType) -> ReadSchemaType: ...

    async def delete(self, object_id: uuid.UUID | int) -> bool: ...


class DatabaseRepositoryImpl(
    DatabaseRepositoryProtocol[
        ModelType,
        ReadSchemaType,
        CreateSchemaType,
        UpdateSchemaType,
    ],
):
    """
    Base Database CRUD repository implementation.
    """

    model_type: type[ModelType]
    read_schema_type: type[ReadSchemaType]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, create_object: CreateSchemaType) -> ReadSchemaType:
        async with self._session as s, s.begin():
            statement = (
                insert(self.model_type)
                .values(**create_object.model_dump(exclude={"id"}))
                .returning(self.model_type)
            )
            try:
                model = (await s.execute(statement)).scalar_one()
            except IntegrityError as e:
                logger.exception("Failed to create a new object. Error: %s", exc_info=e)
                raise ModelAlreadyExistsException(self.model_type, "some field")
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def update(self, update_object: UpdateSchemaType) -> ReadSchemaType:
        async with self._session as s, s.begin():
            pk = update_object.id
            statement = (
                update(self.model_type)
                .where(self.model_type.id == pk)
                .values(update_object.model_dump(exclude={"id"}, exclude_unset=True))
                .returning(self.model_type)
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, update_object.id)
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def delete(self, object_id: uuid.UUID | int) -> bool:
        async with self._session as s, s.begin():
            statement = delete(self.model_type).where(self.model_type.id == object_id)
            await s.execute(statement)
            return True
