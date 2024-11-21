from pydantic import BaseModel, Field
from uuid import UUID
from model.enums import Gender


class UserSchema(BaseModel):
    fullname: str = Field(min_length=10, max_length=255)
    age: int
    sex: Gender


class UserResponse(BaseModel):
    id: UUID
    fullname: str
    age: int
    sex: Gender

    class Config:
        from_attributes = True
