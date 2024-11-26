from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.db import get_db
from model.models import User
from repository.user import UserRepository
from schemas.user import UserSchema
from utils.auth import Auth
from utils.hash_password import Hash

security = HTTPBearer()


class AuthService:

    def __init__(self, db: AsyncSession, repository: UserRepository):
        self.db = db
        self.repository = repository

    @staticmethod
    async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: AsyncSession = Depends(get_db),
    ):
        token = credentials.credentials
        email = await Auth.get_current_user_with_token(token)
        user = await db.execute(select(User).filter(User.email == email))
        user_obj = user.scalar_one_or_none()
        return user_obj

    async def get_user_by_email(self, email: str):
        return await self.repository.get_one(email=email)

    async def signup(self, body: UserSchema):
        user = await self.get_user_by_email(email=body.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Account already exists"
            )
        body.password = await Hash.get_password_hash(body.password)
        user = User(**body.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, body: HTTPAuthorizationCredentials):
        user = await self.get_user_by_email(email=body.email)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email"
            )
        if not await Hash.verify_password(body.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password"
            )
        access_token = await Auth.create_access_token(data={"sub": user.email})
        return {
            "access_token": access_token,
        }
