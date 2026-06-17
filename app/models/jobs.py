from app.database import Base
from sqlalchemy import String, text, Text, Numeric, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
import enum
import uuid
from decimal import Decimal


class JobStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    DRAFT = "draft"

class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("gen_random_uuid()"))
    title: Mapped[str] = mapped_column(String(200), index=True)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(100), index=True)
    salary: Mapped[Decimal] = mapped_column(Numeric(10,2))
    salary_currency: Mapped[str] = mapped_column(String(3), default="USD")
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus), default=JobStatus.OPEN, native_enum=False)

    # bu degani clasdan python koddan emas tayyor bazadan shu jadvalni topib unga ulab qo'y degani va biz bu yerda teble name ni yozamiz
    posted_by_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False)
    deadline: Mapped[datetime | None] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))

