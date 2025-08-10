import logging
from typing import Protocol, Optional, Dict, Any

from aiohttp.client import ClientSession

from src.settings import settings

from ..schemas.superheroes import SuperheroCreateSchema

logger = logging.getLogger(__name__)


def parse_api_raw_data(raw_data: Dict[str, Any]) -> SuperheroCreateSchema:
    def _int(value: Any) -> int:
        try:
            return int(value) if str(value).lower() != "null" else 0
        except (ValueError, TypeError):
            return 0

    name = raw_data.get("name")
    powerstats = raw_data.get("powerstats", {})

    return SuperheroCreateSchema(
        name=name,
        intelligence=_int(powerstats.get("intelligence")),
        strength=_int(powerstats.get("strength")),
        speed=_int(powerstats.get("speed")),
        durability=_int(powerstats.get("durability")),
        power=_int(powerstats.get("power")),
        combat=_int(powerstats.get("combat")),
    )


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
            logger.debug("SuperHero API was found: %r", raw_data)
            superhero = parse_api_raw_data(raw_data)
            return superhero
