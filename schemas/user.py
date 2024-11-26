from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from model.enums import Gender


class UserSchema(BaseModel):
    fullname: str = Field(min_length=10, max_length=255)
    email: EmailStr
    password: str
    age: int
    sex: Gender


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    fullname: str
    email: EmailStr
    age: int
    sex: Gender

    class Config:
        from_attributes = True
