import pytest
from aioresponses import aioresponses

from src.apps.superheroes.services.superhero_api import SuperHeroApiServiceImpl
from src.apps.superheroes.schemas.superheroes import SuperheroCreateSchema


class TestSuperHeroApiServiceImpl:
    @pytest.fixture
    def service(self):
        return SuperHeroApiServiceImpl()

    @pytest.mark.asyncio
    async def test_get_hero_by_name_success(
        self,
        service: SuperHeroApiServiceImpl,
        mock_superhero_response: dict,
    ):
        mock_superhero_response["response"] = "success"
        url = service._search_url + "Batman"

        with aioresponses() as m:
            m.get(url, payload=mock_superhero_response)

            result = await service.get_hero_by_name("Batman")

        assert isinstance(result, SuperheroCreateSchema)
        assert result.name == "Batman"
        assert result.intelligence == 100
        assert result.strength == 85

    @pytest.mark.asyncio
    async def test_get_hero_by_name_not_found(
        self,
        service: SuperHeroApiServiceImpl,
        mock_not_found_response: dict,
    ):
        url = service._search_url + "Unknown Hero"

        with aioresponses() as m:
            m.get(url, payload=mock_not_found_response)

            result = await service.get_hero_by_name("Unknown Hero")

        assert result is None

    @pytest.mark.asyncio
    async def test_get_hero_with_null_values(
        self,
        service: SuperHeroApiServiceImpl,
        mock_null_values_response: dict,
    ):
        mock_null_values_response["response"] = "success"
        url = service._search_url + "Test Hero"

        with aioresponses() as m:
            m.get(url, payload=mock_null_values_response)

            result = await service.get_hero_by_name("Test Hero")

        assert result is not None
        assert result.name == "Test Hero"
        assert result.intelligence == 0
        assert result.strength == 0
        assert result.speed == 0
        assert result.durability == 50
        assert result.power == 75
        assert result.combat == 25