from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

class Base(DeclarativeBase):
    pass

Database_url = os.getenv("DATABASE_URL")

engine = create_async_engine(
    Database_url,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    pool_pre_ping=True
)


async_session_maker = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session():
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e