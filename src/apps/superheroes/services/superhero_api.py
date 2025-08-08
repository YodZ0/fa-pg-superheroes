import logging
from typing import Protocol, Optional

from aiohttp.client import ClientSession

from src.settings import settings

from ..schemas.superheroes import SuperheroCreateSchema

logger = logging.getLogger(__name__)


class SuperHeroApiServiceProtocol(Protocol):
    async def get_hero_by_name(self, name: str) -> Optional[SuperheroCreateSchema]:
        """
        Send request to SuperHero API to get hero by name.
        Returns None if hero was not found.
        """
        ...


class SuperHeroApiServiceImpl:
    def __init__(self) -> None:
        self._search_url = f"{settings.sh_api.url}/search/"

    async def get_hero_by_name(self, name: str) -> Optional[SuperheroCreateSchema]:
        """
        Send request to SuperHero API to get hero by name.
        Returns None if hero was not found.
        """

        req_url = self._search_url + name
        async with ClientSession() as session:
            async with session.get(url=req_url) as response:
                result = await response.json()

        if result["response"] == "error":
            logger.warning("Unable to find superhero with name %r from API.", name)
            return None

        if result["response"] == "success":
            raw_data = result["results"][0]
            superhero = SuperheroCreateSchema(
                name=raw_data["name"],
                intelligence=int(raw_data["powerstats"]["intelligence"]),
                strength=int(raw_data["powerstats"]["strength"]),
                speed=int(raw_data["powerstats"]["speed"]),
                durability=int(raw_data["powerstats"]["durability"]),
                power=int(raw_data["powerstats"]["power"]),
                combat=int(raw_data["powerstats"]["combat"]),
            )
            logger.debug("Superhero was found: %r", superhero)
            return superhero
