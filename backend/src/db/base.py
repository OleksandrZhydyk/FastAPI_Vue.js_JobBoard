from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker

from core.config import Config

Base = declarative_base()

engine = create_async_engine(Config.DB_CONFIG, echo=True, future=True)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
