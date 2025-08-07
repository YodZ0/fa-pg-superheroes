import uuid
from pydantic import BaseModel, ConfigDict


class CreateBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UpdateBaseModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID | int