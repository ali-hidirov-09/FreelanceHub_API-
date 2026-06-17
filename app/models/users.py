from sqlalchemy import String, text, ForeignKey
from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)