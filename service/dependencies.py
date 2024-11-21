from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from database.db import get_db
from repository.pet import PetRepository
from repository.user import UserRepository
from service.pet import PetService
from service.user import UserService


async def get_pet_service(db: AsyncSession = Depends(get_db)):
    pet_repository = PetRepository(db)
    return PetService(db, pet_repository)


async def get_user_service(db: AsyncSession = Depends(get_db)):
    user_repository = UserRepository(db)
    return UserService(db, user_repository)
