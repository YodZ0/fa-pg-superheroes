import logging
from typing import Protocol, Optional

from src.core.exceptions.db_exceptions import ModelAlreadyExistsException

from ..repositories.superheroes import SuperheroesRepositoryProtocol
from ..schemas.superheroes import SuperheroReadSchema, SuperheroCreateSchema
from ..exceptions import DBHeroNotFoundException

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
