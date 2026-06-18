from app.database import Base
from sqlalchemy import String, text, Text, Numeric, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum
from decimal import Decimal


class JobStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    DRAFT = "draft"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100), index=True)
    salary: Mapped[Decimal] = mapped_column(Numeric(10,2))
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD")
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus, native_enum=False), default=JobStatus.OPEN)
    posted_by_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"),)
    deadline: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

