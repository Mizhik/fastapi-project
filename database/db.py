import contextlib
from core.settings import config
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker

class DatabaseSessionManager:
    def __init__(self, url: str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker = async_sessionmaker(
            autocommit=False, autoflush=False, bind=self._engine, expire_on_commit=False
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception("Session is not initialized")
        session = self._session_maker()
        try:
            yield session
        except Exception as error:
            print(error)
            await session.rollback()
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(config.ASYNC_DATABASE_URL)


async def get_db():
    async with sessionmanager.session() as session:
        yield session
