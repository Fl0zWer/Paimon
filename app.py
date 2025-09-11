"""
Paimon Discord Bot OAuth Web Application
Handles Discord OAuth callbacks and manages authorized users.
"""

import os
import time
from flask import Flask, request, redirect, session, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AuthorizedUser

# Configuration
DB_URL = os.getenv('DATABASE_URL', 'sqlite:///paimon_users.db')
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI', 'http://localhost:5000/callback')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Database setup
engine = create_engine(DB_URL, future=True)
Session = sessionmaker(bind=engine, expire_on_commit=False)

def init_database():
    """Initialize database tables if they don't exist."""
    try:
        Base.metadata.create_all(engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        raise

def upsert_authorized_user(discord_id, username, avatar, access_token, refresh_token, scope, expires_in):
    """
    Insert or update an authorized user in the database.
    
    Args:
        discord_id: Discord user ID
        username: Discord username
        avatar: Discord avatar URL
        access_token: OAuth access token
        refresh_token: OAuth refresh token  
        scope: OAuth scope
        expires_in: Token expiration time in seconds
    """
    expires_at = int(time.time()) + int(expires_in) if expires_in else None
    
    try:
        with Session() as s:
            row = s.query(AuthorizedUser).filter_by(discord_id=str(discord_id)).one_or_none()
            if row is None:
                # Create new user
                row = AuthorizedUser(
                    discord_id=str(discord_id),
                    username=username,
                    avatar=avatar,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    scope=scope,
                    expires_at=expires_at,
                )
                s.add(row)
                print(f"✅ Created new authorized user: {username} ({discord_id})")
            else:
                # Update existing user
                row.username = username
                row.avatar = avatar
                row.access_token = access_token
                row.refresh_token = refresh_token
                row.scope = scope
                row.expires_at = expires_at
                print(f"✅ Updated authorized user: {username} ({discord_id})")
            
            s.commit()
            return True
    except Exception as e:
        print(f"❌ Error in upsert_authorized_user: {e}")
        return False

@app.route('/')
def index():
    """Home page with Discord login link."""
    return f'''
    <html>
        <head><title>Paimon Discord OAuth</title></head>
        <body>
            <h1>Paimon Discord Bot OAuth</h1>
            <p>Welcome to the Paimon Discord Bot OAuth system.</p>
            <a href="https://discord.com/oauth2/authorize?client_id={DISCORD_CLIENT_ID}&redirect_uri={DISCORD_REDIRECT_URI}&response_type=code&scope=identify">
                Login with Discord
            </a>
        </body>
    </html>
    '''

@app.route('/callback')
def discord_callback():
    """Handle Discord OAuth callback."""
    try:
        # Get authorization code from Discord
        code = request.args.get('code')
        if not code:
            return "❌ Error: No authorization code received", 400

        # In a real implementation, you would:
        # 1. Exchange the code for access token with Discord API
        # 2. Get user info from Discord API
        # 3. Store the user data
        
        # For now, this is a placeholder that prevents the "no such table" error
        # by ensuring the table exists when the callback is called
        
        # Mock user data (replace with actual Discord API calls)
        mock_user_data = {
            'discord_id': '123456789012345678',
            'username': 'TestUser',
            'avatar': 'https://cdn.discordapp.com/avatars/123456789012345678/abcdef.png',
            'access_token': 'mock_access_token',
            'refresh_token': 'mock_refresh_token',
            'scope': 'identify',
            'expires_in': 3600
        }
        
        # Upsert user data - this is where the "authorized_users" table is accessed
        success = upsert_authorized_user(
            discord_id=mock_user_data['discord_id'],
            username=mock_user_data['username'],
            avatar=mock_user_data['avatar'],
            access_token=mock_user_data['access_token'],
            refresh_token=mock_user_data['refresh_token'],
            scope=mock_user_data['scope'],
            expires_in=mock_user_data['expires_in']
        )
        
        if success:
            return '''
            <html>
                <head><title>OAuth Success</title></head>
                <body>
                    <h1>✅ Discord OAuth Successful</h1>
                    <p>You have been successfully authorized!</p>
                    <p>The authorized_users table has been accessed successfully.</p>
                </body>
            </html>
            '''
        else:
            return "❌ Error saving user data", 500
            
    except Exception as e:
        error_msg = f"Error en callback: {str(e)}"
        print(error_msg)
        return f"❌ {error_msg}", 500

@app.route('/users')
def list_users():
    """List all authorized users (for testing)."""
    try:
        with Session() as s:
            users = s.query(AuthorizedUser).all()
            user_list = []
            for user in users:
                user_list.append({
                    'id': user.id,
                    'discord_id': user.discord_id,
                    'username': user.username,
                    'created_at': str(user.created_at),
                    'updated_at': str(user.updated_at)
                })
            return jsonify(user_list)
    except Exception as e:
        return f"❌ Error: {str(e)}", 500

if __name__ == '__main__':
    print("🚀 Starting Paimon Discord OAuth server...")
    
    # Initialize database on startup
    init_database()
    
    # Start Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)