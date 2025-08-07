import logging

from fastapi import APIRouter

__all__ = ("router",)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/superheroes",
    tags=["SuperHeroes"],
)


@router.post("/hero")
async def add_hero(name: str):
    """Add hero by name"""
    return {}


@router.get("/hero")
async def find_hero():
    """Get hero by name and stats"""
    return {}
