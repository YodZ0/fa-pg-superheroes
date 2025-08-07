from src.core.schemas.http_schemas import ResponseSchema
from src.core.schemas.db_schemas import CreateBaseModel, UpdateBaseModel


class SuperheroReadSchema(ResponseSchema):
    pass


class SuperheroCreateSchema(CreateBaseModel):
    pass


class SuperheroUpdateSchema(UpdateBaseModel):
    pass