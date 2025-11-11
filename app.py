"""
Paimon Discord Bot OAuth Web Application
Handles Discord OAuth callbacks and manages authorized users.

Improvements:
- Uses centralized DatabaseManager for better code organization
- Improved error handling and logging
- Better separation of concerns
- More consistent validation
"""

import os
import time
import logging
from flask import Flask, request, jsonify
from models import AuthorizedUser
from db_utils import DatabaseManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration constants
DISCORD_CLIENT_ID = os.getenv('DISCORD_CLIENT_ID')
DISCORD_CLIENT_SECRET = os.getenv('DISCORD_CLIENT_SECRET')
DISCORD_REDIRECT_URI = os.getenv('DISCORD_REDIRECT_URI', 'http://localhost:5000/callback')
SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')

# Initialize Flask app
app = Flask(__name__)
app.secret_key = SECRET_KEY

# Initialize database manager
db_manager = DatabaseManager()


def validate_user_data(user_data: dict) -> tuple[bool, str]:
    """
    Validate user data before database operations.
    
    Args:
        user_data: Dictionary containing user information
        
    Returns:
        tuple: (is_valid, error_message)
    """
    required_fields = ['discord_id', 'username', 'access_token']
    
    for field in required_fields:
        if field not in user_data or not user_data[field]:
            return False, f"Missing required field: {field}"
    
    return True, ""


def calculate_token_expiry(expires_in):
    """
    Calculate token expiration timestamp.
    
    Args:
        expires_in: Expiration time in seconds or None
        
    Returns:
        int or None: Unix timestamp of expiration
    """
    if expires_in:
        try:
            return int(time.time()) + int(expires_in)
        except (ValueError, TypeError):
            logger.warning(f"Invalid expires_in value: {expires_in}")
            return None
    return None


def upsert_authorized_user(discord_id: str, username: str, avatar: str = None,
                          access_token: str = None, refresh_token: str = None,
                          scope: str = None, expires_in: int = None) -> bool:
    """
    Insert or update an authorized user in the database.
    
    Args:
        discord_id: Discord user ID
        username: Discord username
        avatar: Discord avatar URL (optional)
        access_token: OAuth access token
        refresh_token: OAuth refresh token (optional)
        scope: OAuth scope (optional)
        expires_in: Token expiration time in seconds (optional)
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Validate required fields
    user_data = {
        'discord_id': discord_id,
        'username': username,
        'access_token': access_token
    }
    is_valid, error_msg = validate_user_data(user_data)
    if not is_valid:
        logger.error(f"Validation error: {error_msg}")
        return False
    
    expires_at = calculate_token_expiry(expires_in)
    
    try:
        with db_manager.get_session() as session:
            # Check if user exists
            existing_user = session.query(AuthorizedUser).filter_by(
                discord_id=str(discord_id)
            ).one_or_none()
            
            if existing_user is None:
                # Create new user
                new_user = AuthorizedUser(
                    discord_id=str(discord_id),
                    username=username,
                    avatar=avatar,
                    access_token=access_token,
                    refresh_token=refresh_token,
                    scope=scope,
                    expires_at=expires_at,
                )
                session.add(new_user)
                logger.info(f"✅ Created new authorized user: {username} ({discord_id})")
            else:
                # Update existing user
                existing_user.username = username
                existing_user.avatar = avatar
                existing_user.access_token = access_token
                existing_user.refresh_token = refresh_token
                existing_user.scope = scope
                existing_user.expires_at = expires_at
                logger.info(f"✅ Updated authorized user: {username} ({discord_id})")
            
            return True
    except Exception as e:
        logger.error(f"❌ Error in upsert_authorized_user: {e}")
        return False


@app.route('/')
def index():
    """Home page with Discord login link."""
    if not DISCORD_CLIENT_ID:
        return """
        <html>
            <head><title>Configuration Error</title></head>
            <body>
                <h1>⚠️ Configuration Error</h1>
                <p>DISCORD_CLIENT_ID is not configured. Please set environment variables.</p>
            </body>
        </html>
        """, 500
    
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
            logger.warning("OAuth callback received without code")
            return "❌ Error: No authorization code received", 400

        # TODO: In production, replace with actual Discord API calls:
        # 1. Exchange the code for access token with Discord API
        # 2. Get user info from Discord API
        # 3. Store the user data
        
        # Mock user data (placeholder for development)
        mock_user_data = {
            'discord_id': '123456789012345678',
            'username': 'TestUser',
            'avatar': 'https://cdn.discordapp.com/avatars/123456789012345678/abcdef.png',
            'access_token': 'mock_access_token',
            'refresh_token': 'mock_refresh_token',
            'scope': 'identify',
            'expires_in': 3600
        }
        
        # Upsert user data
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
        error_msg = f"Error in callback: {str(e)}"
        logger.error(error_msg)
        return f"❌ {error_msg}", 500


@app.route('/users')
def list_users():
    """List all authorized users (for testing/admin purposes)."""
    try:
        with db_manager.get_session() as session:
            users = session.query(AuthorizedUser).all()
            user_list = [
                {
                    'id': user.id,
                    'discord_id': user.discord_id,
                    'username': user.username,
                    'created_at': str(user.created_at),
                    'updated_at': str(user.updated_at)
                }
                for user in users
            ]
            return jsonify(user_list)
    except Exception as e:
        logger.error(f"Error listing users: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    try:
        # Check database connection
        with db_manager.get_session() as session:
            session.execute("SELECT 1")
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected'
        })
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500


if __name__ == '__main__':
    logger.info("🚀 Starting Paimon Discord OAuth server...")
    
    # Initialize database on startup
    if not db_manager.init_database():
        logger.error("Failed to initialize database. Exiting.")
        exit(1)
    
    # Start Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)