import logging
from typing import Protocol, Optional, List

from src.core.exceptions.db_exceptions import ModelAlreadyExistsException

from ..repositories.superheroes import SuperheroesRepositoryProtocol
from ..schemas.superheroes import (
    SuperheroReadSchema,
    SuperheroCreateSchema,
    SuperheroQueryFilterSchema,
)
from ..exceptions import DBHeroNotFoundException, DBFilteredHeroesNotFoundException

logger = logging.getLogger(__name__)


class SuperheroesServiceProtocol(Protocol):
    async def create_hero(
        self,
        new_hero: SuperheroCreateSchema,
    ) -> SuperheroReadSchema:
        """
        Create new hero in DB.
        """
        ...

    async def find_hero_by_name(
        self,
        name: str,
    ) -> Optional[SuperheroReadSchema]:
        """
        Find hero in DB by name. Return None if not found.
        """
        ...

    async def filter_heroes(
        self,
        filters: SuperheroQueryFilterSchema,
    ) -> List[SuperheroReadSchema] | None:
        """
        Filter heroes with passed filters.
        """
        ...


class SuperheroesServiceImpl:
    def __init__(self, repository: SuperheroesRepositoryProtocol) -> None:
        self.repository = repository

    async def create_hero(
        self,
        new_hero: SuperheroCreateSchema,
    ) -> SuperheroReadSchema:
        """
        Create new hero in DB.
        """
        try:
            superhero = await self.repository.create(new_hero)
            logger.debug("New superhero has been created: %r", superhero)
            return superhero
        except ModelAlreadyExistsException as e:
            logger.exception("Failed to create new superhero. Error:", exc_info=e)
            raise

    async def find_hero_by_name(
        self,
        name: str,
    ) -> Optional[SuperheroReadSchema]:
        """
        Find hero in DB by name. Return None if not found.
        """
        try:
            superhero = await self.repository.get_by_name(name)
            logger.debug("Superhero has been found: %r", superhero)
            return superhero
        except DBHeroNotFoundException:
            logger.warning(
                "Unable to find superhero with name %r in Database.",
                name,
            )
            return None

    async def filter_heroes(
        self,
        filters: SuperheroQueryFilterSchema,
    ) -> List[SuperheroReadSchema] | None:
        """
        Filter heroes with passed filters.
        """
        try:
            superheroes = await self.repository.filter_all(filters)
            logger.debug(
                "Filtered (%r) Superheroes: %r",
                filters.model_dump(exclude_none=True),
                superheroes,
            )
            return superheroes
        except DBFilteredHeroesNotFoundException:
            logger.warning(
                "Unable to find superheroes with filters %r in Database.",
                filters.model_dump(exclude_none=True),
            )
            return None
