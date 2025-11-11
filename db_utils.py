"""
Database utility functions for Paimon Discord Bot.

This module centralizes database operations to follow DRY principles.
It addresses:
- Code duplication in database session management
- Inconsistent error handling
- Better separation of concerns
"""

import os
import logging
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session as SQLSession
from models import Base

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration constants
DEFAULT_DB_URL = 'sqlite:///paimon_users.db'


class DatabaseManager:
    """
    Manages database connections and operations.
    Provides a centralized interface for database interactions.
    """
    
    def __init__(self, db_url: str = None):
        """
        Initialize database manager.
        
        Args:
            db_url: Database connection URL. If None, uses environment variable or default.
        """
        self.db_url = db_url or os.getenv('DATABASE_URL', DEFAULT_DB_URL)
        self.engine = create_engine(self.db_url, future=True)
        self.SessionLocal = sessionmaker(bind=self.engine, expire_on_commit=False)
        
    def init_database(self):
        """
        Initialize database tables if they don't exist.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            Base.metadata.create_all(self.engine)
            logger.info("✅ Database tables created successfully")
            return True
        except Exception as e:
            logger.error(f"❌ Error creating database tables: {e}")
            return False
    
    @contextmanager
    def get_session(self):
        """
        Context manager for database sessions.
        Automatically handles session cleanup and error rollback.
        
        Yields:
            SQLSession: Database session
            
        Example:
            with db_manager.get_session() as session:
                user = session.query(User).first()
        """
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            session.close()
    
    def create_tables_if_not_exist(self):
        """
        Create all tables defined in models if they don't exist.
        
        Returns:
            list: Names of tables created
        """
        try:
            Base.metadata.create_all(self.engine)
            table_names = list(Base.metadata.tables.keys())
            logger.info(f"✅ Database tables ready: {', '.join(table_names)}")
            return table_names
        except Exception as e:
            logger.error(f"❌ Error creating tables: {e}")
            return []
    
    def get_table_names(self):
        """
        Get list of all table names defined in the models.
        
        Returns:
            list: Table names
        """
        return list(Base.metadata.tables.keys())


def create_database_manager(db_url: str = None) -> DatabaseManager:
    """
    Factory function to create a DatabaseManager instance.
    
    Args:
        db_url: Database connection URL
        
    Returns:
        DatabaseManager: Configured database manager
    """
    return DatabaseManager(db_url)


def validate_database_connection(db_url: str = None) -> bool:
    """
    Validate that database connection can be established.
    
    Args:
        db_url: Database connection URL to test
        
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        test_engine = create_engine(
            db_url or os.getenv('DATABASE_URL', DEFAULT_DB_URL),
            future=True
        )
        # Try to connect
        with test_engine.connect() as conn:
            logger.info("✅ Database connection validated successfully")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False
    finally:
        if 'test_engine' in locals():
            test_engine.dispose()
