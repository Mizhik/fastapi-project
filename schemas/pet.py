from pydantic import BaseModel, Field
from uuid import UUID
from model.enums import Gender


class PetSchema(BaseModel):
    nickname: str = Field(min_length=10, max_length=255)
    age: int
    sex: Gender
    owner_id: UUID


class PetResponse(BaseModel):
    id: UUID
    nickname: str
    age: int
    sex: Gender
    owner_id: UUID

    class Config:
        from_attributes = True
