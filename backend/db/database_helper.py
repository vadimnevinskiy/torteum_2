from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from ..config import settings
from ..models import Base


class DatabaseHelper:
    def __init__(self, url: str, echo: bool = False):
        self.engine = create_async_engine(url=url, echo=echo)
        self.session = async_sessionmaker(bind=self.engine, expire_on_commit=False, autoflush=False)

    async def get_db(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session() as db:
            yield db

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)


db_helper = DatabaseHelper(url=settings.database_async_url, echo=True)
