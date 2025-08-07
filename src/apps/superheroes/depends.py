from typing import Annotated
from fastapi import Depends

from src.core.database.db_provider import SessionDep

from .repositories.superheroes import (
    SuperheroesRepositoryProtocol,
    SuperheroesRepositoryImpl,
)

from .services.superheroes import SuperheroesServiceProtocol, SuperheroesServiceImpl
from .services.superhero_api import SuperHeroApiServiceProtocol, SuperHeroApiServiceImpl
from .use_cases.create import CreateSuperheroUseCaseProtocol, CreateSuperheroUseCaseImpl
from .use_cases.list import ListSuperheroesUseCaseProtocol, ListSuperheroesUseCaseImpl


__all__ = (
    "CreateSuperheroUseCase",
    "ListSuperheroesUseCase",
)


# ======= REPOSITORIES =======
def get_superheroes_repository(
    session: SessionDep,
) -> SuperheroesRepositoryProtocol:
    return SuperheroesRepositoryImpl(session=session)


SuperheroesRepository = Annotated[
    SuperheroesRepositoryProtocol,
    Depends(get_superheroes_repository),
]


# ======= SERVICES =======
def get_superheroes_service(
    repository: SuperheroesRepository,
) -> SuperheroesServiceProtocol:
    return SuperheroesServiceImpl(repository=repository)


def get_sh_api_service() -> SuperHeroApiServiceProtocol:
    return SuperHeroApiServiceImpl()


SuperheroesService = Annotated[
    SuperheroesServiceProtocol,
    Depends(get_superheroes_service),
]
SuperHeroAPI = Annotated[
    SuperHeroApiServiceProtocol,
    Depends(get_sh_api_service),
]


# ======= USE CASES =======
def get_superheroes_create_use_case(
    superheroes_service: SuperheroesService,
    superhero_api_service: SuperHeroAPI,
) -> CreateSuperheroUseCaseProtocol:
    return CreateSuperheroUseCaseImpl(
        superheroes_service=superheroes_service,
        superhero_api_service=superhero_api_service,
    )


def get_list_superheroes_use_case(
    superheroes_service: SuperheroesService,
) -> ListSuperheroesUseCaseProtocol:
    return ListSuperheroesUseCaseImpl(superheroes_service=superheroes_service)


CreateSuperheroUseCase = Annotated[
    CreateSuperheroUseCaseProtocol,
    Depends(get_superheroes_create_use_case),
]

ListSuperheroesUseCase = Annotated[
    ListSuperheroesUseCaseProtocol,
    Depends(get_list_superheroes_use_case),
]