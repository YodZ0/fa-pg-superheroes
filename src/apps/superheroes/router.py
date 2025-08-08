import logging
from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from .schemas.superheroes import SuperheroReadSchema, SuperheroQueryFilterSchema
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
    """
    Add hero by name
    """

    return await uc.execute(superhero_name=superhero_name)


def validate_filters_ranges(filters: SuperheroQueryFilterSchema) -> None:
    """
    Validate ranges set correctly.
    """

    fields = ("intelligence", "strength", "speed", "durability", "power", "combat")

    for field in fields:
        equal = getattr(filters, field)
        min_val = getattr(filters, f"{field}_ge")
        max_val = getattr(filters, f"{field}_le")

        if min_val is not None and max_val is not None and min_val > max_val:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{field}: min value ({min_val}) is greater than max value ({max_val})",
            )
        if equal is not None:
            if min_val is not None and equal < min_val:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field}: exact value ({equal}) is less than min ({min_val})",
                )
            if max_val is not None and equal > max_val:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"{field}: exact value ({equal}) is greater than max ({max_val})",
                )


@router.get("/hero")
async def find_hero(
    uc: ListSuperheroesUseCase,
    filters: SuperheroQueryFilterSchema = Depends(),
) -> List[SuperheroReadSchema]:
    """
    Get heroes by filters (name and powerstats).
    If exact value given, and it is in range ge < exact < le, heroes will be filtered only by exact value.
    In other cases, heroes will be filtered by range ge/le.
    """

    logger.debug("Received filters: %r", filters)
    validate_filters_ranges(filters)
    return await uc.execute(filters=filters)
