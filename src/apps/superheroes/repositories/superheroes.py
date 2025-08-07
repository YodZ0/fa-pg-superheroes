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


class SuperheroesRepositoryProtocol(
    DatabaseRepositoryProtocol[
        Superhero,
        SuperheroReadSchema,
        SuperheroCreateSchema,
        SuperheroUpdateSchema,
    ],
): ...


_ConcreteRepositoryBase = DatabaseRepositoryImpl[
    Superhero,
    SuperheroReadSchema,
    SuperheroCreateSchema,
    SuperheroUpdateSchema,
]


class SuperheroesRepositoryImpl(_ConcreteRepositoryBase):
    model_type = Superhero
    read_schema_type = SuperheroReadSchema
