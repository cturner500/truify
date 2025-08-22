"""
auth.py - Simple authentication system

This module provides basic username/password authentication using a CSV file.

IMPORTANT: Session persistence has been disabled to require re-authentication 
on page refresh. Users must login again each time they refresh the page.
"""

import streamlit as st
import pandas as pd
import os
import json
import time
import hashlib
import csv
from datetime import datetime
import pytz
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def save_session_to_file(username):
    """Save session to file for persistence - DISABLED to force re-auth on refresh"""
    # Session persistence is disabled to require re-authentication on page refresh
    # This function is kept for compatibility but no longer saves sessions
    pass
    
    # Original implementation (commented out):
    # session_data = {
    #     'username': username,
    #     'timestamp': int(time.time()),
    #     'session_id': hashlib.sha256(f"{username}{time.time()}".encode()).hexdigest()
    # }
    # session_file = os.path.join(os.path.dirname(__file__), 'session.json')
    # try:
    #     with open(session_file, 'w') as f:
    #         json.dump(session_data, f)
    # except Exception as e:
    #     st.error(f"Error saving session: {e}")

def load_session_from_file():
    """Load session from file - DISABLED to force re-auth on refresh"""
    # Session persistence is disabled to require re-authentication on page refresh
    # This function is kept for compatibility but no longer loads sessions
    return None
    
    # Original implementation (commented out):
    # try:
    #     session_file = os.path.join(os.path.dirname(__file__), 'session_file')
    #     if os.path.exists(session_file):
    #         with open(session_file, 'r') as f:
    #             session_data = json.load(f)
    #         if time.time() - session_data['timestamp'] < 86400:  # 24 hours
    #             return session_data['username']
    #         else:
    #             os.remove(session_file)
    #     return None
    # except Exception as e:
    #     try:
    #         session_file = os.path.join(os.path.dirname(__file__), 'session_file')
    #         if os.path.exists(session_file):
    #             os.remove(session_file)
    #     except:
    #         pass
    #     return None

def clear_session_file():
    """Clear session file - DISABLED to force re-auth on refresh"""
    # Session persistence is disabled to require re-authentication on page refresh
    # This function is kept for compatibility but no longer clears sessions
    pass
    
    # Original implementation (commented out):
    # try:
    #     session_file = os.path.join(os.path.dirname(__file__), 'session.json')
    #     if os.path.exists(session_file):
    #         os.remove(session_file)
    # except Exception as e:
    #     st.error(f"Error clearing session: {e}")

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
        
        # Terms and Conditions checkbox
        st.markdown("""
        <style>
        .stCheckbox label {
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        terms_accepted = st.checkbox("I agree to TRUIFY.AI's Terms and Conditions", key="terms_checkbox")
        
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
        /* Terms and conditions checkbox styling */
        .stForm .stCheckbox {
            margin: 15px 0 !important;
            text-align: left !important;
        }
        .stForm .stCheckbox label {
            color: #cccccc !important;
            font-size: 14px !important;
        }
        .stForm .stCheckbox a {
            color: #87CEEB !important;
            text-decoration: underline !important;
        }
        .stForm .stCheckbox a:hover {
            color: #B0E0E6 !important;
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
        if not terms_accepted:
            st.error("You must accept the Terms and Conditions to proceed.")
        elif check_credentials(username, password):
            st.session_state['authenticated'] = True
            st.session_state['username'] = username
            save_session_to_file(username)
            
            # Send email notification
            send_email_notification(username)
            
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("User or Password do not match our records.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Terms and Conditions expander (at the bottom of the page)
    with st.expander("View Terms and Conditions", expanded=False):
        # Custom CSS for white text on black background
        st.markdown("""
        <style>
        .stExpander .stMarkdown {
            color: white !important;
        }
        .stExpander h3 {
            color: white !important;
        }
        .stExpander p {
            color: white !important;
        }
        .stExpander a {
            color: #87CEEB !important;
        }
        .stExpander strong {
            color: #ffeb3b !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Important Legal Disclaimer
        st.markdown("""
        **IMPORTANT LEGAL DISCLAIMER:** TRUIFY.AI is a data analysis and compliance assessment tool that provides informational guidance only. This tool does not constitute legal advice, does not make legal recommendations, and does not confirm that your data will be compliant with any applicable laws or regulations. TRUIFY.AI does not reduce or eliminate your legal or compliance risks. You should consult with qualified legal counsel to review and finalize any changes recommended by TRUIFY.AI before using data for any production workflows.
        """)
        
        # Section 1: Acceptance of Terms
        st.subheader("1. Acceptance of Terms")
        st.write("By accessing and using TRUIFY.AI (\"the Service\"), you accept and agree to be bound by the terms and provision of this agreement.")
        
        # Section 2: No Legal Advice
        st.subheader("2. No Legal Advice")
        st.markdown("""
        **CRITICAL:** TRUIFY.AI is not a law firm and does not provide legal services. The information, tools, and recommendations provided through the Service are for informational and educational purposes only.
        """)
        
        # Section 3: Compliance and Risk Disclaimer
        st.subheader("3. Compliance and Risk Disclaimer")
        st.markdown("""
        **COMPLIANCE RISK DISCLAIMER:** TRUIFY.AI does not guarantee compliance with any laws, regulations, or industry standards. Using the Service does not reduce, eliminate, or otherwise affect your legal or compliance risks.
        """)
        
        # Section 4: User Responsibilities
        st.subheader("4. User Responsibilities")
        st.write("Users are responsible for:")
        st.markdown("""
        • Consulting with qualified legal counsel before implementing any changes  
        • Having legal counsel review all recommendations before production use  
        • Understanding that compliance requirements vary by jurisdiction and industry  
        • Recognizing that laws and regulations change over time
        """)
        
        # Section 5: Contact Information
        st.subheader("5. Contact Information")
        st.markdown("""
        **For questions about these Terms and Conditions:**  
        Email: [info@truify.ai](mailto:info@truify.ai)  
        Website: [https://truify.ai](https://truify.ai)
        """)
        
        # Footer
        st.markdown("""
        ---
        *© 2024 TRUIFY.AI. All rights reserved.*
        """)

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

def detect_page_refresh():
    """Detect if this is a page refresh by checking session state initialization"""
    # Check if we have a session ID that persists across refreshes
    if 'session_id' not in st.session_state:
        # Generate a unique session ID for this browser session
        import secrets
        st.session_state['session_id'] = secrets.token_hex(16)
        return True  # This is likely a page refresh or new session
    
    # Check if we have a page load counter
    if 'page_load_count' not in st.session_state:
        st.session_state['page_load_count'] = 1
        return True  # First page load
    
    # Increment page load counter
    st.session_state['page_load_count'] += 1
    return False  # Not a refresh, just navigation within the app

def is_authenticated():
    """Check if user is authenticated"""
    # Check if this is a page refresh
    if detect_page_refresh():
        # This is likely a page refresh, clear any existing session
        if 'authenticated' in st.session_state:
            del st.session_state['authenticated']
        if 'username' in st.session_state:
            del st.session_state['username']
        clear_session_file()
        return False
    
    # Check if user is authenticated in current session
    if st.session_state.get('authenticated', False):
        return True
    
    # Don't load from persistent session file on page refresh
    # This forces users to login again after refreshing
    return False

def logout():
    """Logout the user"""
    if 'authenticated' in st.session_state:
        del st.session_state['authenticated']
    if 'username' in st.session_state:
        del st.session_state['username']
    clear_session_file()

def send_email_notification(username):
    """Send email notification when user logs in using Gmail SMTP"""
    try:
        # Read email addresses from email.csv
        email_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "email.csv")
        
        if not os.path.exists(email_file):
            return
        
        # Get current time in local and Pacific timezone
        local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pacific_tz = pytz.timezone('US/Pacific')
        pacific_time = datetime.now(pacific_tz).strftime("%Y-%m-%d %H:%M:%S %Z")
        
        # Read email addresses from CSV
        email_addresses = []
        with open(email_file, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                if len(row) >= 2:
                    email = row[1].strip()
                    if '@' in email:  # Basic email validation
                        email_addresses.append(email)
        
        if not email_addresses:
            return
        
        # Email content
        subject = "Successful TRUIFY.AI Login"
        body = f"{username} has logged in at {local_time} which is {pacific_time}"
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = os.getenv('GMAIL_USER', 'truify@localhost')
        msg['Subject'] = subject
        
        # Add body to email
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email to all addresses using Gmail SMTP
        try:
            # Get Gmail credentials from environment variables
            gmail_user = os.getenv('GMAIL_USER')
            gmail_password = os.getenv('GMAIL_APP_PASSWORD')
            
            if gmail_user and gmail_password:
                # Use Gmail SMTP
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(gmail_user, gmail_password)
                
                for email in email_addresses:
                    try:
                        msg['To'] = email
                        text = msg.as_string()
                        server.sendmail(gmail_user, email, text)
                    except Exception as e:
                        pass  # Silently handle email errors
                
                server.quit()
            
        except Exception as e:
            pass  # Silently handle SMTP errors
            
    except Exception as e:
        pass  # Silently handle any other errors

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
        

