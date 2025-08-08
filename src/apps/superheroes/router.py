import logging
from typing import List

from fastapi import APIRouter

from .schemas.superheroes import SuperheroReadSchema
from .depends import CreateSuperheroUseCase, ListSuperheroesUseCase

__all__ = ("router",)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/superheroes",
    tags=["SuperHeroes"],
)


@router.post("/hero")
async def add_hero(
    superhero_name: str,
    uc: CreateSuperheroUseCase,
) -> SuperheroReadSchema:
    """Add hero by name"""
    result = await uc.execute(superhero_name=superhero_name)
    return result


@router.get("/hero")
async def find_hero():
    """Get hero by name and stats"""
    return {}
