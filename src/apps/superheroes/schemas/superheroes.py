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