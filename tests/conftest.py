import pytest
from typing import Dict, Any

from src.settings import settings


@pytest.fixture
def mock_superhero_response() -> Dict[str, Any]:
    """
    Mock API success response.
    """
    return {
        "response": "success",
        "results": [
            {
                "name": "Batman",
                "powerstats": {
                    "intelligence": "100",
                    "strength": "85",
                    "speed": "65",
                    "durability": "85",
                    "power": "80",
                    "combat": "90",
                },
            }
        ],
    }


@pytest.fixture
def mock_not_found_response() -> Dict[str, Any]:
    """
    Mock API hero not found response.
    """
    return {"response": "error", "error": "superhero not found"}


@pytest.fixture
def mock_null_values_response() -> Dict[str, Any]:
    """
    Mock API response with null values.
    """
    return {
        "response": "success",
        "results": [
            {
                "name": "Test Hero",
                "powerstats": {
                    "intelligence": "null",
                    "strength": "null",
                    "speed": "null",
                    "durability": "50",
                    "power": "75",
                    "combat": "25",
                },
            }
        ],
    }


@pytest.fixture(autouse=True)
def test_settings(monkeypatch):
    """
    Test settings.
    """
    monkeypatch.setattr(settings.sh_api, "access_token", "test-key")