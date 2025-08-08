from typing import List

from sqlalchemy import select
from sqlalchemy.sql.expression import and_

from src.core.models.superheroes import Superhero
from src.core.repositories.db_repository import (
    DatabaseRepositoryProtocol,
    DatabaseRepositoryImpl,
)
from ..schemas.superheroes import (
    SuperheroReadSchema,
    SuperheroCreateSchema,
    SuperheroUpdateSchema,
    SuperheroQueryFilterSchema,
)
from ..exceptions import (
    DBHeroNotFoundException,
    DBFilteredHeroesNotFoundException,
)


_ConcreteBaseRepositoryIml = DatabaseRepositoryImpl[
    Superhero,
    SuperheroReadSchema,
    SuperheroCreateSchema,
    SuperheroUpdateSchema,
]


class SuperheroesRepositoryProtocol(
    DatabaseRepositoryProtocol[
        Superhero,
        SuperheroReadSchema,
        SuperheroCreateSchema,
        SuperheroUpdateSchema,
    ],
):
    async def get_by_name(self, name: str) -> SuperheroReadSchema: ...

    async def filter_all(
        self,
        filters: SuperheroQueryFilterSchema,
    ) -> List[SuperheroReadSchema]: ...


class SuperheroesRepositoryImpl(_ConcreteBaseRepositoryIml):
    model_type = Superhero
    read_schema_type = SuperheroReadSchema

    async def get_by_name(self, name: str) -> SuperheroReadSchema:
        async with self._session as s:
            query = select(self.model_type).where(self.model_type.name == name)
            model = (await s.execute(query)).scalar_one_or_none()
            if model is None:
                raise DBHeroNotFoundException(self.model_type, name)
            return self.read_schema_type.model_validate(model, from_attributes=True)

    async def filter_all(
        self,
        filters: SuperheroQueryFilterSchema,
    ) -> List[SuperheroReadSchema]:
        async with self._session as s:
            query = select(self.model_type)
            conditions = []
            numeric_fields = [
                "intelligence",
                "strength",
                "speed",
                "durability",
                "power",
                "combat",
            ]

            for field in numeric_fields:
                eq_value = getattr(filters, field)
                ge_value = getattr(filters, f"{field}_ge")
                le_value = getattr(filters, f"{field}_le")

                if eq_value is not None:
                    conditions.append(getattr(self.model_type, field) == eq_value)
                else:
                    if ge_value is not None:
                        conditions.append(getattr(self.model_type, field) >= ge_value)
                    if le_value is not None:
                        conditions.append(getattr(self.model_type, field) <= le_value)

            if conditions:
                query = query.where(and_(*conditions))

            models = (await s.execute(query)).scalars().all()

            if not models:
                raise DBFilteredHeroesNotFoundException(
                    self.model_type,
                    filters.model_dump(exclude_none=True),
                )

            return [
                self.read_schema_type.model_validate(model, from_attributes=True)
                for model in models
            ]