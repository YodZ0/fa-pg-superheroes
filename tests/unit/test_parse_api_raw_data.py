import pytest
from typing import Any

from src.apps.superheroes.services.superhero_api import parse_api_raw_data
from src.apps.superheroes.schemas.superheroes import SuperheroCreateSchema


class TestParseApiRawData:
    """
    parse_raw_data function tests.
    """

    def test_parse_valid_data(self):
        raw_data = {
            "name": "Superman",
            "powerstats": {
                "intelligence": "90",
                "strength": "100",
                "speed": "95",
                "durability": "100",
                "power": "100",
                "combat": "85",
            },
        }

        result = parse_api_raw_data(raw_data)

        assert isinstance(result, SuperheroCreateSchema)
        assert result.name == "Superman"
        assert result.intelligence == 90
        assert result.strength == 100
        assert result.speed == 95
        assert result.durability == 100
        assert result.power == 100
        assert result.combat == 85

    @pytest.mark.parametrize(
        "value,expected",
        [
            ("null", 0),
            ("NULL", 0),
            (None, 0),
            ("", 0),
            ("0", 0),
            ("42", 42),
        ],
    )
    def test_parse_edge_cases(self, value: Any, expected: int):
        raw_data = {
            "name": "Test Hero",
            "powerstats": {
                "intelligence": value,
                "strength": "0",
                "speed": "0",
                "durability": "0",
                "power": "0",
                "combat": "0",
            },
        }

        result = parse_api_raw_data(raw_data)
        assert result.intelligence == expected
