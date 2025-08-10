from typing import Protocol

from ..services.superheroes import SuperheroesServiceProtocol
from ..services.superhero_api import SuperHeroApiServiceProtocol
from ..schemas.superheroes import SuperheroReadSchema
from ..exceptions import HeroNotFoundException


class CreateSuperheroUseCaseProtocol(Protocol):
    async def execute(self, superhero_name: str) -> SuperheroReadSchema:
        """
        Checks if superhero already exists in DB.
        If not found tries to get it from API and saves in DB.
        """
        ...


class CreateSuperheroUseCaseImpl:
    def __init__(
        self,
        superheroes_service: SuperheroesServiceProtocol,
        superhero_api_service: SuperHeroApiServiceProtocol,
    ) -> None:
        self.superheroes_service = superheroes_service
        self.superhero_api_service = superhero_api_service

    async def execute(self, superhero_name: str) -> SuperheroReadSchema:
        """
        Checks if superhero already exists in DB.
        If not found tries to get it from API and saves in DB.
        """
        # Try to get object from DB
        db_superhero = await self.superheroes_service.find_hero_by_name(
            name=superhero_name
        )
        if db_superhero:
            return db_superhero

        # Send request to get superhero by name
        response = await self.superhero_api_service.get_hero_by_name(name=superhero_name)
        if not response:
            raise HeroNotFoundException(hero_name=superhero_name)

        # Save new superhero in DB
        new_superhero = await self.superheroes_service.create_hero(new_hero=response)

        return new_superhero