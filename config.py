"""
Configuration management for Paimon Discord Bot.

This module centralizes configuration values to avoid magic strings
and hardcoded values scattered throughout the codebase.

Improvements:
- Centralized configuration constants
- Environment variable management
- Type-safe configuration access
- Better separation of concerns
"""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    url: str = os.getenv('DATABASE_URL', 'sqlite:///paimon_users.db')
    echo_sql: bool = os.getenv('DB_ECHO_SQL', 'false').lower() == 'true'
    pool_size: int = int(os.getenv('DB_POOL_SIZE', '5'))
    max_overflow: int = int(os.getenv('DB_MAX_OVERFLOW', '10'))


@dataclass
class DiscordConfig:
    """Discord OAuth configuration settings."""
    client_id: Optional[str] = os.getenv('DISCORD_CLIENT_ID')
    client_secret: Optional[str] = os.getenv('DISCORD_CLIENT_SECRET')
    redirect_uri: str = os.getenv('DISCORD_REDIRECT_URI', 'http://localhost:5000/callback')
    oauth_scopes: list[str] = None
    
    def __post_init__(self):
        """Initialize default OAuth scopes if not provided."""
        if self.oauth_scopes is None:
            scopes_str = os.getenv('DISCORD_OAUTH_SCOPES', 'identify')
            self.oauth_scopes = [s.strip() for s in scopes_str.split(',')]
    
    def get_oauth_url(self) -> str:
        """
        Generate Discord OAuth authorization URL.
        
        Returns:
            str: Complete OAuth URL
        """
        scopes = '+'.join(self.oauth_scopes)
        return (
            f"https://discord.com/oauth2/authorize"
            f"?client_id={self.client_id}"
            f"&redirect_uri={self.redirect_uri}"
            f"&response_type=code"
            f"&scope={scopes}"
        )


@dataclass
class FlaskConfig:
    """Flask web application configuration."""
    secret_key: str = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    debug: bool = os.getenv('FLASK_DEBUG', 'true').lower() == 'true'
    host: str = os.getenv('FLASK_HOST', '0.0.0.0')
    port: int = int(os.getenv('FLASK_PORT', '5000'))


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = os.getenv('LOG_LEVEL', 'INFO')
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format: str = '%Y-%m-%d %H:%M:%S'


class AppConfig:
    """
    Main application configuration aggregator.
    
    This class provides a single point of access to all configuration
    settings, making it easy to manage and update configuration.
    """
    
    def __init__(self):
        self.database = DatabaseConfig()
        self.discord = DiscordConfig()
        self.flask = FlaskConfig()
        self.logging = LoggingConfig()
    
    def validate(self) -> tuple[bool, list[str]]:
        """
        Validate configuration settings.
        
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []
        
        # Validate Discord configuration
        if not self.discord.client_id:
            errors.append("DISCORD_CLIENT_ID environment variable is required")
        
        if not self.discord.client_secret:
            errors.append("DISCORD_CLIENT_SECRET environment variable is required")
        
        # Validate Flask secret key in production
        if not self.flask.debug and self.flask.secret_key == 'your-secret-key-change-this':
            errors.append("SECRET_KEY must be set to a secure value in production")
        
        return len(errors) == 0, errors
    
    def print_config(self, mask_secrets: bool = True):
        """
        Print current configuration (for debugging).
        
        Args:
            mask_secrets: Whether to mask sensitive values
        """
        print("=" * 60)
        print("Paimon Configuration")
        print("=" * 60)
        
        print("\nDatabase:")
        # Mask database URL if it contains password
        db_url = self.database.url
        if mask_secrets and '@' in db_url:
            # Mask password in connection string
            parts = db_url.split('@')
            if len(parts) > 1:
                # Mask credentials before @
                protocol_and_creds = parts[0].split('//')
                if len(protocol_and_creds) > 1:
                    db_url = f"{protocol_and_creds[0]}//***:***@{parts[1]}"
        print(f"  URL: {db_url}")
        print(f"  Echo SQL: {self.database.echo_sql}")
        
        print("\nDiscord:")
        # Always mask sensitive data for security
        print(f"  Client ID: {'***' if mask_secrets else self.discord.client_id}")
        print(f"  Redirect URI: {self.discord.redirect_uri}")
        # OAuth scopes should always be masked as they can reveal permissions
        print(f"  OAuth Scopes: {'***' if mask_secrets else ', '.join(self.discord.oauth_scopes)}")
        
        print("\nFlask:")
        print(f"  Debug: {self.flask.debug}")
        print(f"  Host: {self.flask.host}")
        print(f"  Port: {self.flask.port}")
        # Secret key should never be fully logged
        print(f"  Secret Key: {'***' if mask_secrets else '*** (hidden for security)'}")
        
        print("\nLogging:")
        print(f"  Level: {self.logging.level}")
        
        print("=" * 60)


# Global configuration instance
config = AppConfig()
