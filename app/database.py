from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

sqlite_url = "sqlite:///./freelance_hub.db"

engine = create_engine(sqlite_url, echo=True)


class Base(DeclarativeBase):
    pass

