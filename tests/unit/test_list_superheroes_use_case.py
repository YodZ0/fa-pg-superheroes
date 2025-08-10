import pytest
from unittest.mock import AsyncMock

from src.apps.superheroes.use_cases.list import ListSuperheroesUseCaseImpl
from src.apps.superheroes.schemas.superheroes import (
    SuperheroReadSchema,
    SuperheroQueryFilterSchema,
)
from src.apps.superheroes.exceptions import (
    HeroNotFoundException,
    FilteredHeroesNotFoundException,
)


class TestListSuperheroesUseCaseImpl:
    @pytest.fixture
    def service(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def use_case(self, service: AsyncMock) -> ListSuperheroesUseCaseImpl:
        return ListSuperheroesUseCaseImpl(superheroes_service=service)

    @pytest.mark.asyncio
    async def test_execute_by_name_found(
        self,
        use_case: ListSuperheroesUseCaseImpl,
        service: AsyncMock,
    ):
        hero = SuperheroReadSchema(
            id=1,
            name="Batman",
            intelligence=100,
            strength=85,
            speed=65,
            durability=85,
            power=80,
            combat=90,
        )
        service.find_hero_by_name.return_value = hero

        filters = SuperheroQueryFilterSchema(
            name="Batman",
            intelligence=None,
            intelligence_ge=None,
            intelligence_le=None,
            strength=None,
            strength_ge=None,
            strength_le=None,
            speed=None,
            speed_ge=None,
            speed_le=None,
            durability=None,
            durability_ge=None,
            durability_le=None,
            power=None,
            power_ge=None,
            power_le=None,
            combat=None,
            combat_ge=None,
            combat_le=None,
        )
        result = await use_case.execute(filters)

        assert result == [hero]
        service.find_hero_by_name.assert_awaited_once_with(name="Batman")
        service.filter_heroes.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_execute_by_name_not_found(
        self,
        use_case: ListSuperheroesUseCaseImpl,
        service: AsyncMock,
    ):
        service.find_hero_by_name.return_value = None

        filters = SuperheroQueryFilterSchema(
            name="Unknown",
            intelligence=None,
            intelligence_ge=None,
            intelligence_le=None,
            strength=None,
            strength_ge=None,
            strength_le=None,
            speed=None,
            speed_ge=None,
            speed_le=None,
            durability=None,
            durability_ge=None,
            durability_le=None,
            power=None,
            power_ge=None,
            power_le=None,
            combat=None,
            combat_ge=None,
            combat_le=None,
        )

        with pytest.raises(HeroNotFoundException) as exc:
            await use_case.execute(filters)

        assert "Unknown" in str(exc.value)
        service.find_hero_by_name.assert_awaited_once_with(name="Unknown")
        service.filter_heroes.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_execute_filter_found(
        self,
        use_case: ListSuperheroesUseCaseImpl,
        service: AsyncMock,
    ):
        heroes = [
            SuperheroReadSchema(
                id=1,
                name="Batman",
                intelligence=100,
                strength=85,
                speed=65,
                durability=85,
                power=80,
                combat=90,
            ),
            SuperheroReadSchema(
                id=2,
                name="Superman",
                intelligence=95,
                strength=100,
                speed=100,
                durability=95,
                power=100,
                combat=80,
            ),
        ]
        service.filter_heroes.return_value = heroes

        filters = SuperheroQueryFilterSchema(
            name=None,
            intelligence=None,
            intelligence_ge=90,
            intelligence_le=None,
            strength=None,
            strength_ge=None,
            strength_le=None,
            speed=None,
            speed_ge=None,
            speed_le=None,
            durability=None,
            durability_ge=None,
            durability_le=None,
            power=None,
            power_ge=None,
            power_le=None,
            combat=None,
            combat_ge=None,
            combat_le=None,
        )
        result = await use_case.execute(filters)

        assert result == heroes
        service.filter_heroes.assert_awaited_once_with(filters=filters)
        service.find_hero_by_name.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_execute_filter_empty(
        self,
        use_case: ListSuperheroesUseCaseImpl,
        service: AsyncMock,
    ):
        service.filter_heroes.return_value = None

        filters = SuperheroQueryFilterSchema(
            name=None,
            intelligence=None,
            intelligence_ge=None,
            intelligence_le=None,
            strength=None,
            strength_ge=None,
            strength_le=10,
            speed=None,
            speed_ge=None,
            speed_le=None,
            durability=None,
            durability_ge=None,
            durability_le=None,
            power=None,
            power_ge=None,
            power_le=None,
            combat=None,
            combat_ge=None,
            combat_le=None,
        )

        with pytest.raises(FilteredHeroesNotFoundException) as exc:
            await use_case.execute(filters)

        assert "strength_le" in str(exc.value)
        service.filter_heroes.assert_awaited_once_with(filters=filters)
        service.find_hero_by_name.assert_not_awaited()
