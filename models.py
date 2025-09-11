"""
SQLAlchemy models for Paimon Discord Bot OAuth system.
"""

from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func, Text

Base = declarative_base()

class AuthorizedUser(Base):
    """Model for storing Discord OAuth authorized users."""
    __tablename__ = "authorized_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    discord_id: Mapped[str] = mapped_column(String(32), unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(100))
    avatar: Mapped[str | None] = mapped_column(Text)
    access_token: Mapped[str] = mapped_column(Text, nullable=False)
    refresh_token: Mapped[str | None] = mapped_column(Text)
    scope: Mapped[str | None] = mapped_column(Text)
    expires_at: Mapped[int | None] = mapped_column(Integer)   # epoch seconds
    created_at: Mapped[str] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[str] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())