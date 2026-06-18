from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent

PROJECT_ROOT = BASE_DIR.parent

DB_PATH = PROJECT_ROOT / "freelance_hub.db"

sqlite_url = f"sqlite:///{DB_PATH}"

engine = create_engine(sqlite_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

