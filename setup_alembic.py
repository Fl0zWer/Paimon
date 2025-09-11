"""
Setup Alembic migrations for Paimon Discord Bot database.
Run this script to initialize Alembic migrations system.
"""

import os
import subprocess
import sys

def install_alembic():
    """Install Alembic if not already installed."""
    try:
        import alembic
        print("✅ Alembic is already installed")
        return True
    except ImportError:
        print("📦 Installing Alembic...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "alembic"])
            print("✅ Alembic installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Alembic: {e}")
            return False

def init_alembic():
    """Initialize Alembic configuration."""
    if not os.path.exists("alembic"):
        print("🔧 Initializing Alembic...")
        try:
            subprocess.check_call(["alembic", "init", "alembic"])
            print("✅ Alembic initialized successfully")
            
            # Create first migration
            print("📝 Creating initial migration...")
            subprocess.check_call(["alembic", "revision", "-m", "create_authorized_users_table", "--autogenerate"])
            print("✅ Initial migration created")
            
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize Alembic: {e}")
            return False
    else:
        print("✅ Alembic is already initialized")
        return True

def main():
    print("🛠️  Setting up Alembic Migrations for Paimon")
    print("=" * 50)
    
    # Install Alembic
    if not install_alembic():
        return 1
    
    # Initialize Alembic
    if not init_alembic():
        return 1
    
    print("\n✅ Alembic setup completed!")
    print("\nNext steps:")
    print("1. Edit alembic.ini to configure your database URL")
    print("2. Edit alembic/env.py to import your models")
    print("3. Run 'alembic upgrade head' to apply migrations")
    print("4. For future changes: 'alembic revision --autogenerate -m \"description\"'")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())