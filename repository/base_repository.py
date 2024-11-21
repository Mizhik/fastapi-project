from typing import Optional, TypeVar
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeMeta
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=DeclarativeMeta)


class BaseRepository:
    def __init__(self, model: ModelType, db: AsyncSession):
        self._model = model
        self._db = db

    async def get_many(self, offset: Optional[int] = None, limit: Optional[int] = None):
        query = select(self._model)
        if offset is not None and limit is not None:
            query = query.offset(offset).limit(limit)
        result = await self._db.execute(query)
        return result.scalars().all()

    async def get_one(self, **params) -> ModelType:
        query = select(self._model).filter_by(**params)
        result = await self._db.execute(query)
        return result.scalar_one_or_none()

    async def create(self, body: dict) -> ModelType:
        result = self._model(**body)
        self._db.add(result)
        await self._db.commit()
        await self._db.refresh(result)
        return result
