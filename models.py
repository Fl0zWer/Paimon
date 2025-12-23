"""
SQLAlchemy models for Paimon Discord Bot OAuth system.

Improvements:
- Better type hints and documentation
- More explicit field definitions
- Improved maintainability
"""

from typing import Optional
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func, Text

Base = declarative_base()


class AuthorizedUser(Base):
    """
    Model for storing Discord OAuth authorized users.
    
    This table stores users who have authorized the bot via Discord OAuth,
    including their access tokens and profile information.
    
    Attributes:
        id: Primary key auto-increment integer
        discord_id: Unique Discord user ID (snowflake as string)
        username: Discord username
        avatar: Discord avatar URL
        access_token: OAuth2 access token for API calls
        refresh_token: OAuth2 refresh token for token renewal
        scope: OAuth2 scope permissions granted
        expires_at: Unix timestamp when access_token expires
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    __tablename__ = "authorized_users"

    # Primary key
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        comment="Auto-increment primary key"
    )
    
    # Discord user identifier (required, unique)
    discord_id: Mapped[str] = mapped_column(
        String(32),
        unique=True,
        nullable=False,
        index=True,
        comment="Discord user ID (snowflake)"
    )
    
    # User profile information (optional)
    username: Mapped[Optional[str]] = mapped_column(
        String(100),
        comment="Discord username"
    )
    
    avatar: Mapped[Optional[str]] = mapped_column(
        Text,
        comment="Discord avatar URL"
    )
    
    # OAuth tokens (access_token required)
    access_token: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        comment="OAuth2 access token"
    )
    
    refresh_token: Mapped[Optional[str]] = mapped_column(
        Text,
        comment="OAuth2 refresh token"
    )
    
    # OAuth metadata
    scope: Mapped[Optional[str]] = mapped_column(
        Text,
        comment="OAuth2 scope permissions"
    )
    
    expires_at: Mapped[Optional[int]] = mapped_column(
        Integer,
        comment="Token expiration timestamp (Unix epoch seconds)"
    )
    
    # Audit timestamps
    created_at: Mapped[str] = mapped_column(
        DateTime,
        server_default=func.now(),
        comment="Record creation timestamp"
    )
    
    updated_at: Mapped[str] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Record last update timestamp"
    )
    
    def __repr__(self) -> str:
        """String representation of AuthorizedUser."""
        return (
            f"<AuthorizedUser(id={self.id}, "
            f"discord_id='{self.discord_id}', "
            f"username='{self.username}')>"
        )
    
    def is_token_expired(self) -> bool:
        """
        Check if the access token has expired.
        
        Returns:
            bool: True if token is expired or expiry not set, False otherwise
        """
        if self.expires_at is None:
            return True
        
        import time
        return time.time() >= self.expires_at