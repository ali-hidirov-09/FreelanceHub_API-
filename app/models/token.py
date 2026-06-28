from sqlalchemy import String, ForeignKey, text, DateTime
from app.core.database import Base

from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    token_hash: Mapped[str] = mapped_column(String(1000))
    jti: Mapped[str] = mapped_column(index=True)
    expires_at: Mapped[datetime] = mapped_column((DateTime(timezone=True)))
    created_at: Mapped[datetime] = mapped_column((DateTime(timezone=True)), server_default=text("CURRENT_TIMESTAMP"))
