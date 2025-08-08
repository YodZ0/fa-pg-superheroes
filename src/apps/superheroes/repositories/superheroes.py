from sqlalchemy import select

from src.core.models.superheroes import Superhero
from src.core.repositories.db_repository import (
    DatabaseRepositoryProtocol,
    DatabaseRepositoryImpl,
)
from ..schemas.superheroes import (
    SuperheroReadSchema,
    SuperheroCreateSchema,
    SuperheroUpdateSchema,
)
from ..exceptions import DBHeroNotFoundException

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
