from typing import Protocol, List

from ..services.superheroes import SuperheroesServiceProtocol
from ..schemas.superheroes import SuperheroReadSchema, SuperheroQueryFilterSchema
from ..exceptions import HeroNotFoundException, FilteredHeroesNotFoundException


class ListSuperheroesUseCaseProtocol(Protocol):
    async def execute(
        self,
        filters: SuperheroQueryFilterSchema,
    ) -> List[SuperheroReadSchema]: ...


class ListSuperheroesUseCaseImpl:
    def __init__(self, superheroes_service: SuperheroesServiceProtocol) -> None:
        self.superheroes_service = superheroes_service

    async def execute(
        self,
        filters: SuperheroQueryFilterSchema,
    ) -> List[SuperheroReadSchema]:
        if filters.name:
            superhero = await self.superheroes_service.find_hero_by_name(name=filters.name)
            if superhero is None:
                raise HeroNotFoundException(hero_name=filters.name)
            return [superhero]

        superheroes = await self.superheroes_service.filter_heroes(filters=filters)
        if superheroes is None:
            raise FilteredHeroesNotFoundException(filters=filters.model_dump(exclude_none=True))

        return superheroes
