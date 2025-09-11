"""
Database initialization script for Paimon Discord Bot.
Creates the authorized_users table if it doesn't exist.
"""

import os
from sqlalchemy import create_engine
from models import Base

def create_database_tables():
    """Create all database tables defined in models."""
    # Get database URL from environment or use default SQLite
    db_url = os.getenv('DATABASE_URL', 'sqlite:///paimon_users.db')
    
    print(f"📁 Connecting to database: {db_url}")
    
    try:
        # Create engine
        engine = create_engine(db_url, future=True)
        
        # Create all tables
        Base.metadata.create_all(engine)
        
        print("✅ Successfully created database tables:")
        for table_name in Base.metadata.tables.keys():
            print(f"   📋 {table_name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False

def create_tables_sql_script():
    """Generate SQL script to create tables manually."""
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
    
    print("📄 SQL script to create tables manually:")
    print("=" * 60)
    print(sql_script)
    print("=" * 60)
    
    # Save to file
    with open('create_tables.sql', 'w') as f:
        f.write(sql_script)
    print("💾 SQL script saved to 'create_tables.sql'")

if __name__ == '__main__':
    print("🛠️  Paimon Database Initialization")
    print("=" * 50)
    
    # Create tables using SQLAlchemy
    success = create_database_tables()
    
    # Generate SQL script for manual creation
    print("\n")
    create_tables_sql_script()
    
    if success:
        print("\n✅ Database initialization completed successfully!")
        print("The 'authorized_users' table is now ready for Discord OAuth callbacks.")
    else:
        print("\n❌ Database initialization failed!")
        print("Please check the error messages above and try again.")