from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status

from schemas.pet import PetResponse, PetSchema
from service.dependencies import get_pet_service
from service.pet import PetService

router = APIRouter(prefix="/pet", tags=["pet"])


@router.post("/", response_model=PetResponse, status_code=status.HTTP_201_CREATED)
async def create_pet(
    body: PetSchema, pet_service: PetService = Depends(get_pet_service)
):
    return await pet_service.create_pet(body)


@router.get("/", response_model=list[PetResponse])
async def get_many_pets(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    pet_service: PetService = Depends(get_pet_service),
):
    return await pet_service.get_all_pets(offset, limit)


@router.get("/{pet_id}", response_model=PetResponse)
async def get_one_pet(pet_id: UUID, pet_service: PetService = Depends(get_pet_service)):
    return await pet_service.get_one_pet(pet_id)

