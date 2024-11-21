from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from repository.user import UserRepository
from schemas.user import UserResponse, UserSchema


class UserService:
    def __init__(self, db: AsyncSession, repository: UserRepository):
        self.db = db
        self.repository = repository

    async def create_user(self, body: UserSchema) -> UserResponse:
        body_dict = body.model_dump()
        return await self.repository.create(body_dict)

    async def get_one_user(self, user_id: UUID) -> UserResponse:
        return await self.repository.get_one(id=user_id)

    async def get_all_users(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ):
        return await self.repository.get_many(offset, limit)
