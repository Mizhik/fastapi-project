from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from repository.pet import PetRepository
from schemas.pet import PetResponse, PetSchema


class PetService:
    def __init__(self, db: AsyncSession, repository: PetRepository):
        self.db = db
        self.repository = repository

    async def create_pet(self, body: PetSchema) -> PetResponse:
        body_dict = body.model_dump()
        return await self.repository.create(body_dict)

    async def get_one_pet(self, pet_id: UUID) -> PetResponse:
        return await self.repository.get_one(id=pet_id)

    async def get_all_pets(
        self, offset: Optional[int] = None, limit: Optional[int] = None
    ) -> list[PetResponse]:
        return await self.repository.get_many(offset, limit)

    # async def update_pet(self, pet_id:UUID, body:PetSchema) -> PetResponse:
    #     body_dict = body.model_dump()
