import pytest
from unittest.mock import AsyncMock

from src.core.exceptions.db_exceptions import ModelAlreadyExistsException
from src.apps.superheroes.services.superheroes import SuperheroesServiceImpl
from src.apps.superheroes.schemas.superheroes import (
    SuperheroCreateSchema,
    SuperheroReadSchema,
    SuperheroQueryFilterSchema,
)
from src.apps.superheroes.exceptions import (
    DBHeroNotFoundException,
    DBFilteredHeroesNotFoundException,
)


class FakeModel:
    pass


class TestSuperheroesServiceImpl:
    @pytest.fixture
    def repo(self) -> AsyncMock:
        return AsyncMock()

    @pytest.fixture
    def service(self, repo: AsyncMock) -> SuperheroesServiceImpl:
        return SuperheroesServiceImpl(repository=repo)

    @pytest.mark.asyncio
    async def test_create_hero_success(
        self,
        service: SuperheroesServiceImpl,
        repo: AsyncMock,
    ):
        schema = SuperheroCreateSchema(
            name="Batman",
            intelligence=100,
            strength=85,
            speed=65,
            durability=85,
            power=80,
            combat=90,
        )
        repo_return = SuperheroReadSchema(
            id=1,
            name="Batman",
            intelligence=100,
            strength=85,
            speed=65,
            durability=85,
            power=80,
            combat=90,
        )
        repo.create.return_value = repo_return

        result = await service.create_hero(schema)

        assert result == repo_return
        repo.create.assert_awaited_once_with(schema)

    @pytest.mark.asyncio
    async def test_create_hero_already_exists(
        self,
        service: SuperheroesServiceImpl,
        repo: AsyncMock,
    ):
        schema = SuperheroCreateSchema(
            name="Batman",
            intelligence=100,
            strength=85,
            speed=65,
            durability=85,
            power=80,
            combat=90,
        )
        repo.create.side_effect = ModelAlreadyExistsException(FakeModel, "duplicate")

        with pytest.raises(ModelAlreadyExistsException):
            await service.create_hero(schema)

        repo.create.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_find_hero_by_name_exists(
        self,
        service: SuperheroesServiceImpl,
        repo: AsyncMock,
    ):
        repo_return = SuperheroReadSchema(
            id=1,
            name="Batman",
            intelligence=100,
            strength=85,
            speed=65,
            durability=85,
            power=80,
            combat=90,
        )
        repo.get_by_name.return_value = repo_return

        result = await service.find_hero_by_name("Batman")

        assert result == repo_return
        repo.get_by_name.assert_awaited_once_with("Batman")

    @pytest.mark.asyncio
    async def test_find_hero_by_name_not_found(
        self,
        service: SuperheroesServiceImpl,
        repo: AsyncMock,
    ):
        repo.get_by_name.side_effect = DBHeroNotFoundException(FakeModel, "Unknown")

        result = await service.find_hero_by_name("Unknown")

        assert result is None
        repo.get_by_name.assert_awaited_once_with("Unknown")

    @pytest.mark.asyncio
    async def test_filter_heroes_success(
        self,
        service: SuperheroesServiceImpl,
        repo: AsyncMock,
    ):
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
        repo_return = [
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
        repo.filter_all.return_value = repo_return

        result = await service.filter_heroes(filters)

        assert result == repo_return
        repo.filter_all.assert_awaited_once_with(filters)

    @pytest.mark.asyncio
    async def test_filter_heroes_empty(
        self,
        service: SuperheroesServiceImpl,
        repo: AsyncMock,
    ):
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
            combat_le=50,
        )
        repo.filter_all.side_effect = DBFilteredHeroesNotFoundException(
            FakeModel,
            filters=filters.model_dump(),
        )

        result = await service.filter_heroes(filters)

        assert result is None
        repo.filter_all.assert_awaited_once_with(filters)
