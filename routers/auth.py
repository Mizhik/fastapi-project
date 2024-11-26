from fastapi import APIRouter, Depends, status

from schemas.auth import TokenSchema
from schemas.user import UserLogin, UserResponse, UserSchema
from service.auth import AuthService
from service.dependencies import get_auth_service


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
async def singup(body: UserSchema, auth_service=Depends(get_auth_service)):
    return await auth_service.signup(body)


@router.post("/login", response_model=TokenSchema)
async def login(body: UserLogin, auth_service=Depends(get_auth_service)):
    return await auth_service.login(body)


@router.get("/me", response_model=UserResponse)
async def user_me(current_user: UserResponse = Depends(AuthService.get_current_user)):
    return current_user
