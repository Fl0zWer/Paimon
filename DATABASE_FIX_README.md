# Paimon Discord Bot - OAuth Database Fix

This repository contains the fix for the "no such table: authorized_users" error in the Discord OAuth callback system.

## Problem Solved

The error occurred when the Discord OAuth callback tried to access the `authorized_users` table, but it didn't exist in the database. This implementation provides:

✅ **SQLAlchemy model** for the `authorized_users` table  
✅ **Automatic table creation** on application startup  
✅ **Upsert functionality** for user authorization data  
✅ **Flask web application** with OAuth callback handling  
✅ **Database initialization scripts**  
✅ **Optional Alembic migration support**  

## Files Added

- `models.py` - SQLAlchemy model for AuthorizedUser
- `app.py` - Flask web application with OAuth callback
- `init_db.py` - Database initialization script
- `setup_alembic.py` - Optional Alembic migration setup
- `create_tables.sql` - SQL script for manual table creation
- Updated `requirements.txt` - Added SQLAlchemy and Flask dependencies

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
# Option A: Using SQLAlchemy (recommended)
python init_db.py

# Option B: Using SQL directly
sqlite3 paimon_users.db < create_tables.sql
```

### 3. Run the OAuth Application
```bash
python app.py
```

The server will start on `http://localhost:5000` with:
- `/` - Home page with Discord login link
- `/callback` - Discord OAuth callback handler
- `/users` - List authorized users (for testing)

## Environment Variables

Set these environment variables for production:

```bash
# Database
DATABASE_URL=sqlite:///paimon_users.db

# Discord OAuth
DISCORD_CLIENT_ID=your_discord_client_id
DISCORD_CLIENT_SECRET=your_discord_client_secret
DISCORD_REDIRECT_URI=http://localhost:5000/callback

# Security
SECRET_KEY=your-secret-key-here
```

## Database Schema

The `authorized_users` table contains:

| Column | Type | Description |
|--------|------|-------------|
| `id` | INTEGER | Primary key |
| `discord_id` | TEXT | Discord user ID (unique) |
| `username` | TEXT | Discord username |
| `avatar` | TEXT | Discord avatar URL |
| `access_token` | TEXT | OAuth access token |
| `refresh_token` | TEXT | OAuth refresh token |
| `scope` | TEXT | OAuth scope |
| `expires_at` | INTEGER | Token expiration (epoch seconds) |
| `created_at` | DATETIME | Record creation time |
| `updated_at` | DATETIME | Last update time |

## Usage in Your Application

### Import and Use the Model

```python
from models import AuthorizedUser, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup database
engine = create_engine('sqlite:///paimon_users.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
```

### Upsert User Data

```python
from app import upsert_authorized_user

# In your Discord OAuth callback
success = upsert_authorized_user(
    discord_id=user_data['id'],
    username=user_data['username'],
    avatar=user_data['avatar'],
    access_token=token_data['access_token'],
    refresh_token=token_data['refresh_token'],
    scope=token_data['scope'],
    expires_in=token_data['expires_in']
)
```

## Migration to Alembic (Optional)

For production use, set up database migrations:

```bash
# Install and setup Alembic
python setup_alembic.py

# Apply migrations
alembic upgrade head

# Create new migrations when models change
alembic revision --autogenerate -m "description of changes"
alembic upgrade head
```

## Testing

The implementation includes a test callback that demonstrates the fix:

```bash
# Test the callback endpoint
curl "http://localhost:5000/callback?code=test_code"

# Check stored users
curl "http://localhost:5000/users"
```

## Integration with Existing Code

If you have existing Discord OAuth callback code, simply:

1. Import the upsert function: `from app import upsert_authorized_user`
2. Call it in your callback with the user data from Discord API
3. The table will be created automatically on first run

## Error Resolution

This implementation specifically resolves:
- ❌ `Error en callback: no such table: authorized_users`
- ✅ Creates the table automatically
- ✅ Provides proper database schema
- ✅ Handles user data upserts correctly

## Production Notes

- Replace the mock data in `app.py` with actual Discord API calls
- Set proper environment variables
- Use a production WSGI server instead of Flask's development server
- Consider using PostgreSQL instead of SQLite for production
- Implement proper error handling and logging