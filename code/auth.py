import streamlit as st
import requests
from urllib.parse import urlencode
import json
import os
from datetime import datetime, timedelta
import base64
import hashlib
import secrets

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv not installed, use system environment variables

# Google OAuth configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'your-google-client-id')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'your-google-client-secret')
GOOGLE_REDIRECT_URI = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8501')

# Check if credentials are properly configured
def check_oauth_config():
    """Check if OAuth credentials are properly configured"""
    if GOOGLE_CLIENT_ID == 'your-google-client-id' or GOOGLE_CLIENT_SECRET == 'your-google-client-secret':
        return False, "OAuth credentials not configured. Please set GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET environment variables."
    return True, None

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

def generate_state():
    """Generate a random state parameter for OAuth security"""
    return secrets.token_urlsafe(32)

def get_google_auth_url():
    """Generate Google OAuth authorization URL"""
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'scope': 'openid email profile',
        'response_type': 'code',
        'state': st.session_state.get('oauth_state', generate_state()),
        'access_type': 'offline',
        'prompt': 'consent'
    }
    return f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    data = {
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'code': code,
        'grant_type': 'authorization_code',
        'redirect_uri': GOOGLE_REDIRECT_URI
    }
    
    response = requests.post(GOOGLE_TOKEN_URL, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Token exchange failed: {response.text}")
        return None

def get_user_info(access_token):
    """Get user information from Google"""
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Failed to get user info: {response.text}")
        return None

def is_authenticated():
    """Check if user is authenticated"""
    return 'user_info' in st.session_state and st.session_state['user_info'] is not None

def login_page():
    """Display login page"""
    # Center the logo
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.image("images/TruifyLogo.png", width=300)
    
    st.markdown("---")
    
    # Check OAuth configuration
    config_valid, error_message = check_oauth_config()
    if not config_valid:
        st.error("🔧 OAuth Configuration Error")
        st.error(error_message)
        st.markdown("""
        ### Setup Instructions:
        1. **Create Google Cloud Project**: Go to [Google Cloud Console](https://console.cloud.google.com/)
        2. **Enable Google+ API**: In APIs & Services > Library
        3. **Create OAuth Credentials**: In APIs & Services > Credentials
        4. **Set Environment Variables**: Create a `.env` file with:
           ```
           GOOGLE_CLIENT_ID=your-actual-client-id
           GOOGLE_CLIENT_SECRET=your-actual-client-secret
           GOOGLE_REDIRECT_URI=http://localhost:8501
           ```
        5. **Restart the application**
        
        See `GOOGLE_OAUTH_SETUP.md` for detailed instructions.
        """)
        return
    
    # Center the login content
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div style="text-align: center; padding: 2rem;">
            <h2>Sign in to continue</h2>
            <p style="color: #666; margin-bottom: 2rem;">
                Please authenticate with your Google account to access Truify.AI
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Google Sign-in button
        auth_url = get_google_auth_url()
        st.markdown(f"""
        <div style="text-align: center;">
            <a href="{auth_url}" target="_self">
                <button style="
                    background-color: #4285f4;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    border-radius: 4px;
                    font-size: 16px;
                    font-weight: 500;
                    cursor: pointer;
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                ">
                    <svg width="18" height="18" viewBox="0 0 24 24">
                        <path fill="white" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="white" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="white" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path fill="white" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                    </svg>
                    Sign in with Google
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="text-align: center; margin-top: 2rem;">
            <p style="color: #999; font-size: 14px;">
                By signing in, you agree to our Terms of Service and Privacy Policy
            </p>
        </div>
        """, unsafe_allow_html=True)

def handle_oauth_callback():
    """Handle OAuth callback and token exchange"""
    # Get URL parameters using the new query_params API
    if 'code' in st.query_params and 'state' in st.query_params:
        code = st.query_params['code']
        state = st.query_params['state']
        
        # Verify state parameter
        if state != st.session_state.get('oauth_state'):
            st.error("Invalid state parameter. Please try again.")
            return False
        
        # Exchange code for token
        token_data = exchange_code_for_token(code)
        if token_data and 'access_token' in token_data:
            # Get user information
            user_info = get_user_info(token_data['access_token'])
            if user_info:
                # Store user info in session state
                st.session_state['user_info'] = user_info
                st.session_state['access_token'] = token_data['access_token']
                st.session_state['token_expires_at'] = datetime.now() + timedelta(hours=1)
                
                # Clear URL parameters
                st.query_params.clear()
                return True
        
        st.error("Authentication failed. Please try again.")
        return False
    
    return False

def logout():
    """Logout user and clear session state"""
    keys_to_remove = ['user_info', 'access_token', 'token_expires_at', 'oauth_state']
    for key in keys_to_remove:
        if key in st.session_state:
            del st.session_state[key]
    
    # Clear all other session state except visited_pages
    visited_pages = st.session_state.get('visited_pages', set())
    st.session_state.clear()
    st.session_state['visited_pages'] = visited_pages

def check_token_expiry():
    """Check if access token has expired"""
    if 'token_expires_at' in st.session_state:
        if datetime.now() > st.session_state['token_expires_at']:
            st.warning("Your session has expired. Please log in again.")
            logout()
            return False
    return True

def display_user_info():
    """Display user information in sidebar"""
    if is_authenticated():
        user_info = st.session_state['user_info']
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 👤 User Info")
        
        # Display user avatar and name
        if 'picture' in user_info:
            st.sidebar.image(user_info['picture'], width=50)
        
        st.sidebar.markdown(f"**{user_info.get('name', 'Unknown')}**")
        st.sidebar.markdown(f"*{user_info.get('email', 'No email')}*")
        
        # Logout button
        if st.sidebar.button("🚪 Logout"):
            logout()
            st.rerun()
        
        st.sidebar.markdown("---")

def require_auth():
    """Decorator to require authentication for pages"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_authenticated():
                login_page()
                return
            elif not check_token_expiry():
                login_page()
                return
            else:
                return func(*args, **kwargs)
        return wrapper
    return decorator 