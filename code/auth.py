"""
auth.py - Simple authentication system

This module provides basic username/password authentication using a CSV file.
"""

import streamlit as st
import pandas as pd
import os

def load_users():
    """Load users from users.csv file"""
    try:
        users_df = pd.read_csv('users.csv')
        return users_df
    except Exception as e:
        st.error(f"Error loading users: {e}")
        return pd.DataFrame(columns=['username', 'password'])

def check_credentials(username, password):
    """Check if username and password match any user in users.csv"""
    users_df = load_users()
    
    # Check if the username and password combination exists
    for _, user in users_df.iterrows():
        if user['username'] == username and user['password'] == password:
            return True
    return False

def login_page():
    """Display the login page with logo and login form"""
    
    # Set black background
    st.markdown("""
    <style>
    .main {
        background-color: black !important;
    }
    .stApp {
        background-color: black !important;
    }
    .block-container {
        background-color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Center the logo
    st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 2rem;">
        <img src="data:image/png;base64,{}" style="max-width: 900px; height: auto;">
    </div>
    """.format(get_logo_base64()), unsafe_allow_html=True)
    
    # Create login form with custom CSS
    st.markdown("""
    <style>
    /* Center everything on the page */
    .main {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        min-height: 100vh !important;
    }
    .block-container {
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        width: 100% !important;
        max-width: 100% !important;
        padding: 0 !important;
    }
    .login-form-container {
        width: 300px !important;
        margin: 0 auto !important;
        text-align: center !important;
    }
    .login-form-container .stForm {
        width: 100% !important;
        margin: 0 auto !important;
    }
    .stForm {
        width: 300px !important;
        max-width: 300px !important;
        margin: 0 auto !important;
        text-align: center !important;
    }
    .stForm > div {
        width: 100% !important;
        max-width: 100% !important;
        text-align: center !important;
    }
    .stForm input {
        width: 100% !important;
        max-width: 100% !important;
        text-align: left !important;
    }
    /* Fix password input and show password icon positioning */
    .stForm [data-testid="stTextInput"] {
        width: 100% !important;
        max-width: 100% !important;
    }
    .stForm [data-testid="stTextInput"] > div {
        width: 100% !important;
        max-width: 100% !important;
        position: relative !important;
    }
    .stForm [data-testid="stTextInput"] input {
        width: 100% !important;
        max-width: 100% !important;
        padding-right: 40px !important;
    }
    .stForm [data-testid="stTextInput"] button {
        position: absolute !important;
        right: 8px !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        width: auto !important;
        max-width: none !important;
        background: none !important;
        border: none !important;
        padding: 4px !important;
    }
    /* Only target submit buttons, not input field buttons */
    .stForm .stButton {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
    }
    .stForm .stButton > button {
        width: 50% !important;
        max-width: 50% !important;
        margin: 0 auto !important;
    }
    /* Text color styling for better readability on black background */
    .stForm h3 {
        color: #cccccc !important;
    }
    .stForm label {
        color: #cccccc !important;
    }
    /* Light blue button styling - target all submit buttons in form */
    .stForm .stButton > button {
        background-color: #87CEEB !important;
        color: #000000 !important;
        border: none !important;
        background-image: none !important;
    }
    .stForm .stButton > button:hover {
        background-color: #B0E0E6 !important;
        background-image: none !important;
    }
    /* Additional targeting for submit buttons */
    .stForm button[type="submit"] {
        background-color: #87CEEB !important;
        color: #000000 !important;
        border: none !important;
        background-image: none !important;
    }
    .stForm button[type="submit"]:hover {
        background-color: #B0E0E6 !important;
        background-image: none !important;
    }
    </style>
    <div class="login-form-container">
    """, unsafe_allow_html=True)
    
    # Login form
    with st.form("login_form"):
        #st.markdown("### Login")
        
        username = st.text_input("Username", key="username_input")
        password = st.text_input("Password", type="password", key="password_input")
        
        # Create custom styled submit button
        st.markdown("""
        <style>
        /* Target submit button with multiple selectors */
        .stForm button[type="submit"],
        .stForm .stButton > button,
        .stForm button[data-testid="baseButton-secondary"],
        .stForm button[data-testid="baseButton-primary"] {
            background-color: #87CEEB !important;
            color: #000000 !important;
            border: none !important;
            padding: 10px 20px !important;
            border-radius: 4px !important;
            cursor: pointer !important;
            font-size: 16px !important;
            width: 50% !important;
            max-width: 50% !important;
            font-weight: bold !important;
        }
        .stForm button[type="submit"]:hover,
        .stForm .stButton > button:hover,
        .stForm button[data-testid="baseButton-secondary"]:hover,
        .stForm button[data-testid="baseButton-primary"]:hover {
            background-color: #B0E0E6 !important;
        }
        /* Force width override */
        .stForm .stButton {
            width: 50% !important;
            max-width: 50% !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create button with inline styling
        st.markdown("""
        <style>
        /* Target only the submit button specifically */
        .stForm .stButton > button {
            width: 50% !important;
            max-width: 50% !important;
            min-width: 50% !important;
            background-color: #87CEEB !important;
            color: #000000 !important;
            border: none !important;
        }
        /* Target the button container */
        .stForm .stButton {
            width: 50% !important;
            max-width: 50% !important;
            display: flex !important;
            justify-content: center !important;
        }
        /* Hover state - blue instead of red */
        .stForm .stButton > button:hover {
            background-color: #B0E0E6 !important;
            color: #000000 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create the login button
        submit_button = st.form_submit_button("Login")
    
    # Handle login outside the form
    if submit_button:
        if check_credentials(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("User or Password do not match our records.")
    
    st.markdown("</div>", unsafe_allow_html=True)

def get_logo_base64():
    """Get the TruifyBanner2.png as base64 string"""
    try:
        import base64
        logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "images/TruifyBanner2.png")
        if os.path.exists(logo_path):
            with open(logo_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                return encoded_string
        else:
            # Fallback if logo doesn't exist
            return ""
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        return ""

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def logout():
    """Logout the user"""
    if 'authenticated' in st.session_state:
        del st.session_state['authenticated']
    if 'username' in st.session_state:
        del st.session_state['username']

def display_user_info():
    """Display user info in sidebar"""
    if is_authenticated():
        username = st.session_state.get('username', 'Unknown')
        st.sidebar.markdown(f"<span style='color: white;'>**Logged in as:** {username}</span>", unsafe_allow_html=True)

def display_logout_button():
    """Display logout button in sidebar"""
    if is_authenticated():
        if st.sidebar.button("Logout"):
            logout()
            st.rerun()
