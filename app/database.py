from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

sqlite_url = "sqlite:///./freelance_hub.db"

engine = create_engine(sqlite_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

