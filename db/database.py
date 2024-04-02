from typing import Generator
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from settings import SQLALCHEMY_DATABASE_URL

engine = create_async_engine(
    (SQLALCHEMY_DATABASE_URL),
    future=True,
    echo=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession) # type: ignore

async def get_db() -> Generator:
    """Dependency for getting async session"""
    try:
        db: AsyncSession = async_session()
        yield db
    finally:
        await db.close()