from app.core.database import Base
from sqlalchemy import String, text, Text, Numeric, ForeignKey, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import enum
from decimal import Decimal


class JobStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    DRAFT = "draft"


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100), index=True)
    salary: Mapped[Decimal] = mapped_column(Numeric(10,2))
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD")
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus, native_enum=True), default=JobStatus.OPEN)
    posted_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    deadline: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=text("CURRENT_TIMESTAMP"))
    is_deleted: Mapped[bool] = mapped_column(default=False)
    user: Mapped["User"] = relationship(back_populates="jobs")

    def __repr__(self):
        return f"""
        id: {self.id},
        title: {self.title},
        deadline: {self.deadline},
        posted_by_id: {self.posted_by_id},
        category: {self.category},"""
