import pytest
from unittest.mock import AsyncMock

from src.apps.superheroes.use_cases.create import CreateSuperheroUseCaseImpl
from src.apps.superheroes.schemas.superheroes import (
    SuperheroCreateSchema,
    SuperheroReadSchema,
)
from src.apps.superheroes.exceptions import HeroNotFoundException


class TestCreateSuperheroUseCaseImpl:
    @pytest.fixture
    def superheroes_service(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def superhero_api_service(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def use_case(
        self,
        superheroes_service: AsyncMock,
        superhero_api_service: AsyncMock,
    ) -> CreateSuperheroUseCaseImpl:
        return CreateSuperheroUseCaseImpl(
            superheroes_service=superheroes_service,
            superhero_api_service=superhero_api_service,
        )

    @pytest.mark.asyncio
    async def test_execute_already_in_db(
        self,
        use_case: CreateSuperheroUseCaseImpl,
        superheroes_service: AsyncMock,
    ):
        db_hero = SuperheroReadSchema(
            id=1,
            name="Batman",
            intelligence=100,
            strength=85,
            speed=65,
            durability=85,
            power=80,
            combat=90,
        )
        superheroes_service.find_hero_by_name.return_value = db_hero

        result = await use_case.execute(superhero_name="Batman")

        assert result == db_hero
        superheroes_service.find_hero_by_name.assert_awaited_once_with(name="Batman")
        superheroes_service.create_hero.assert_not_awaited()
        use_case.superhero_api_service.get_hero_by_name.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_execute_not_in_db_found_in_api(
        self,
        use_case: CreateSuperheroUseCaseImpl,
        superheroes_service: AsyncMock,
        superhero_api_service: AsyncMock,
    ):
        superheroes_service.find_hero_by_name.return_value = None

        api_schema = SuperheroCreateSchema(
            name="Superman",
            intelligence=95,
            strength=100,
            speed=100,
            durability=95,
            power=100,
            combat=80,
        )
        superhero_api_service.get_hero_by_name.return_value = api_schema

        db_hero = SuperheroReadSchema(
            id=2,
            name="Superman",
            intelligence=95,
            strength=100,
            speed=100,
            durability=95,
            power=100,
            combat=80,
        )
        superheroes_service.create_hero.return_value = db_hero

        result = await use_case.execute(superhero_name="Superman")

        assert result == db_hero
        superheroes_service.find_hero_by_name.assert_awaited_once_with(name="Superman")
        superhero_api_service.get_hero_by_name.assert_awaited_once_with(name="Superman")
        superheroes_service.create_hero.assert_awaited_once_with(new_hero=api_schema)

    @pytest.mark.asyncio
    async def test_execute_not_found_anywhere(
        self,
        use_case: CreateSuperheroUseCaseImpl,
        superheroes_service: AsyncMock,
        superhero_api_service: AsyncMock,
    ):
        superheroes_service.find_hero_by_name.return_value = None
        superhero_api_service.get_hero_by_name.return_value = None

        with pytest.raises(HeroNotFoundException) as exc_info:
            await use_case.execute("Unknown")

        assert "Unknown" in str(exc_info.value)
        superheroes_service.find_hero_by_name.assert_awaited_once_with(name="Unknown")
        superhero_api_service.get_hero_by_name.assert_awaited_once_with(name="Unknown")
        superheroes_service.create_hero.assert_not_awaited()
