from typing import Optional
from pydantic import BaseModel, Field

from src.core.schemas.http_schemas import ResponseSchema
from src.core.schemas.db_schemas import CreateBaseModel, UpdateBaseModel


class SuperheroReadSchema(ResponseSchema):
    id: int
    name: str
    intelligence: int
    strength: int
    speed: int
    durability: int
    power: int
    combat: int


class SuperheroCreateSchema(CreateBaseModel):
    name: str
    intelligence: int
    strength: int
    speed: int
    durability: int
    power: int
    combat: int


class SuperheroUpdateSchema(UpdateBaseModel):
    pass


class SuperheroQueryFilterSchema(BaseModel):
    name: Optional[str] = Field(None, description="Exact match for name")

    intelligence: Optional[int] = Field(
        None, ge=0, description="Exact match for intelligence"
    )
    intelligence_ge: Optional[int] = Field(None, ge=0)
    intelligence_le: Optional[int] = Field(None, ge=0)

    strength: Optional[int] = Field(None, ge=0, description="Exact match for strength")
    strength_ge: Optional[int] = Field(None, ge=0)
    strength_le: Optional[int] = Field(None, ge=0)

    speed: Optional[int] = Field(None, ge=0, description="Exact match for speed")
    speed_ge: Optional[int] = Field(None, ge=0)
    speed_le: Optional[int] = Field(None, ge=0)

    durability: Optional[int] = Field(
        None, ge=0, description="Exact match for durability"
    )
    durability_ge: Optional[int] = Field(None, ge=0)
    durability_le: Optional[int] = Field(None, ge=0)

    power: Optional[int] = Field(None, ge=0, description="Exact match for power")
    power_ge: Optional[int] = Field(None, ge=0)
    power_le: Optional[int] = Field(None, ge=0)

    combat: Optional[int] = Field(None, ge=0, description="Exact match for combat")
    combat_ge: Optional[int] = Field(None, ge=0)
    combat_le: Optional[int] = Field(None, ge=0)