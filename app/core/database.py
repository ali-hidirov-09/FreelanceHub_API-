from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

Database_url = os.getenv("DATABASE_URL")

engine = create_async_engine(
    Database_url,
    echo=True,
    pool_size=10,       # soniyasiga 2000-3000 ta ish bajara oladi
    max_overflow=20,    # qo'shimcha ishchilar agar bular ham qo'shilsa soniyasiga 6000-9000 gacha query bajara oladi
    pool_recycle=3600   # har soatda ishchilarni yangilab turadi
)

class Base(DeclarativeBase):
    pass

async_session_maker = async_sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session():
    async with async_session_maker() as session:
        yield session