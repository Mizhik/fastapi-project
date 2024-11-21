from typing import Optional
from uuid import UUID
from fastapi import APIRouter, Depends, status

from schemas.user import UserResponse, UserSchema
from service.dependencies import get_user_service
from service.user import UserService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    body: UserSchema, user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    return await user_service.create_user(body)


@router.get("/", response_model=list[UserResponse])
async def get_many_users(
    offset: Optional[int] = None,
    limit: Optional[int] = None,
    user_service: UserService = Depends(get_user_service),
):
    return await user_service.get_all_users(offset, limit)


@router.get("/{user_id}", response_model=UserResponse)
async def get_one_user(
    user_id: UUID, user_service: UserService = Depends(get_user_service)
):
    return await user_service.get_one_user(user_id)
