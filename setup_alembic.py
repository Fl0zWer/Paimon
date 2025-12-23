"""
Setup Alembic migrations for Paimon Discord Bot database.
Run this script to initialize Alembic migrations system.

Improvements:
- Better error handling and logging
- More informative output
- Cleaner code structure
"""

import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_alembic_installed() -> bool:
    """
    Check if Alembic is already installed.
    
    Returns:
        bool: True if Alembic is installed, False otherwise
    """
    try:
        import alembic
        logger.info("✅ Alembic is already installed")
        return True
    except ImportError:
        return False


def install_alembic() -> bool:
    """
    Install Alembic package.
    
    Returns:
        bool: True if successful, False otherwise
    """
    if check_alembic_installed():
        return True
    
    logger.info("📦 Installing Alembic...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "alembic"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info("✅ Alembic installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to install Alembic: {e}")
        return False


def initialize_alembic() -> bool:
    """
    Initialize Alembic configuration and create first migration.
    
    Returns:
        bool: True if successful, False otherwise
    """
    import os
    
    if os.path.exists("alembic"):
        logger.info("✅ Alembic is already initialized")
        return True
    
    logger.info("🔧 Initializing Alembic...")
    try:
        # Initialize Alembic
        subprocess.check_call(
            ["alembic", "init", "alembic"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info("✅ Alembic initialized successfully")
        
        # Create first migration
        logger.info("📝 Creating initial migration...")
        subprocess.check_call(
            [
                "alembic", "revision",
                "-m", "create_authorized_users_table",
                "--autogenerate"
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info("✅ Initial migration created")
        
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"❌ Failed to initialize Alembic: {e}")
        return False
    except FileNotFoundError:
        logger.error("❌ Alembic command not found. Is it installed correctly?")
        return False


def print_next_steps():
    """Print instructions for next steps after setup."""
    print("\n" + "=" * 60)
    print("✅ Alembic setup completed!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit alembic.ini to configure your database URL")
    print("2. Edit alembic/env.py to import your models")
    print("3. Run 'alembic upgrade head' to apply migrations")
    print("4. For future changes:")
    print("   - 'alembic revision --autogenerate -m \"description\"'")
    print("   - 'alembic upgrade head'")
    print("=" * 60)


def main() -> int:
    """
    Main entry point for Alembic setup.
    
    Returns:
        int: Exit code (0 for success, 1 for failure)
    """
    print("🛠️  Setting up Alembic Migrations for Paimon")
    print("=" * 50)
    
    # Install Alembic
    if not install_alembic():
        logger.error("Failed to install Alembic")
        return 1
    
    # Initialize Alembic
    if not initialize_alembic():
        logger.error("Failed to initialize Alembic")
        return 1
    
    # Print next steps
    print_next_steps()
    
    return 0


if __name__ == "__main__":
    sys.exit(main())