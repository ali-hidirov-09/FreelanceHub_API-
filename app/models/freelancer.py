from app.core.database import Base
from sqlalchemy import String, text, Text, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from decimal import Decimal
from sqlalchemy.dialects.postgresql import ARRAY


class FreelancerProfiles(Base):
    __tablename__ = "freelancer_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    bio: Mapped[str] = mapped_column(Text, nullable=True)
    skills: Mapped[list[str]] = mapped_column(ARRAY(String))
    hourly_rate: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=True)
    avatar_url: Mapped[str] = mapped_column(String, nullable=True)
    resume_url: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"))