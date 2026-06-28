import enum
from sqlalchemy import String, text, Enum
from app.core.database import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from .job import Job

class Role(str, enum.Enum):
    FREELANCER = "freelancer"
    ADMIN = "admin"
    EMPLOYER = "employer"


class User(Base):
    __tablename__= "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String(100))
    role: Mapped[Role] = mapped_column(Enum(Role, native_enum=False), default=Role.EMPLOYER)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

    jobs: Mapped[list["Job"]] = relationship(back_populates="user")


    def __repr__(self):
        return f"""
        id: {self.id}
        email: {self.email}
        role: {self.role}
        is_active: {self.is_active}
        "created_at: {self.created_at}"""




