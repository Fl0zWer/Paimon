"""
Database initialization script for Paimon Discord Bot.
Creates the authorized_users table if it doesn't exist.

Improvements:
- Uses centralized DatabaseManager
- Better error handling
- More maintainable code structure
"""

import sys
from db_utils import DatabaseManager, validate_database_connection


def create_database_tables():
    """
    Create all database tables defined in models.
    
    Returns:
        bool: True if successful, False otherwise
    """
    print("📁 Initializing Paimon database...")
    
    # Validate connection first
    if not validate_database_connection():
        print("❌ Cannot establish database connection")
        return False
    
    # Create database manager
    db_manager = DatabaseManager()
    
    # Create tables
    table_names = db_manager.create_tables_if_not_exist()
    
    if table_names:
        print("✅ Successfully created database tables:")
        for table_name in table_names:
            print(f"   📋 {table_name}")
        return True
    else:
        print("❌ Failed to create database tables")
        return False


def generate_sql_script():
    """
    Generate SQL script to create tables manually.
    Useful for manual database setup or reference.
    """
    sql_script = '''
-- SQL script to create authorized_users table manually
-- Use this if you want to create the table directly in your database

CREATE TABLE IF NOT EXISTS authorized_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discord_id TEXT NOT NULL UNIQUE,
    username TEXT,
    avatar TEXT,
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    scope TEXT,
    expires_at INTEGER,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_authorized_users_discord_id ON authorized_users(discord_id);
'''
    
    print("\n📄 SQL script to create tables manually:")
    print("=" * 60)
    print(sql_script)
    print("=" * 60)
    
    # Save to file
    try:
        with open('create_tables.sql', 'w') as f:
            f.write(sql_script)
        print("💾 SQL script saved to 'create_tables.sql'")
    except IOError as e:
        print(f"⚠️  Could not save SQL script to file: {e}")


def main():
    """Main entry point for database initialization."""
    print("🛠️  Paimon Database Initialization")
    print("=" * 50)
    
    # Create tables using SQLAlchemy
    success = create_database_tables()
    
    # Generate SQL script for manual creation
    print("\n")
    generate_sql_script()
    
    if success:
        print("\n✅ Database initialization completed successfully!")
        print("The 'authorized_users' table is now ready for Discord OAuth callbacks.")
        return 0
    else:
        print("\n❌ Database initialization failed!")
        print("Please check the error messages above and try again.")
        return 1


if __name__ == '__main__':
    sys.exit(main())