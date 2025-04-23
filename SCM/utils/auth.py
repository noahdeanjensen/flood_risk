import streamlit as st
from utils.db import get_db
import bcrypt

def init_auth():
    """Initialize authentication state"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False
    if "user_id" not in st.session_state:
        st.session_state.user_id = None

def check_auth():
    """Handle user authentication"""
    # Remove the title as we already have it in the image
    
    # Create a card-like container for the login
    with st.container():
        # Add enhanced styling for the login form similar to Replit
        st.markdown("""
        <style>
        /* Main button styling - Replit style */
        div[data-testid="stButton"] > button {
            background-color: #0079F2;
            color: white !important;
            font-weight: 500;
            border: none;
            padding: 0.7rem 1.2rem;
            border-radius: 0.375rem;
            transition: all 0.15s ease;
            width: 100%;
            margin-top: 1.5rem;
            font-size: 0.9rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            cursor: pointer;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #0066CC;
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        div[data-testid="stButton"] > button:active {
            transform: translateY(0);
        }
        
        /* Input field styling - Replit style */
        div[data-baseweb="input"] {
            border-radius: 0.375rem;
            border: 1px solid #e2e8f0;
            background-color: #f8fafc;
            transition: all 0.15s ease;
        }
        div[data-baseweb="input"]:focus-within {
            border-color: #0079F2;
            box-shadow: 0 0 0 3px rgba(0, 121, 242, 0.1);
        }
        
        /* Label styling */
        p, label {
            font-weight: 500;
            color: #334155;
            font-size: 0.9rem;
        }
        
        /* Error message styling - Replit style */
        div[data-testid="stAlert"] {
            border-radius: 0.375rem;
            border: none;
            padding: 0.8rem 1rem;
            margin: 1rem 0;
            background-color: #FEE2E2;
            color: #B91C1C;
        }
        
        /* Remove button focus outline */
        button:focus {
            outline: none !important;
            box-shadow: 0 0 0 3px rgba(0, 121, 242, 0.1);
        }
        
        /* Form container styling - card-like */
        .stForm {
            background-color: white;
            border-radius: 0.5rem;
            padding: 1.5rem !important;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Add centered welcome header - Replit style
        st.markdown("<h3 style='text-align: center; margin-bottom: 1rem; color: #0f172a; font-weight: 600; font-size: 1.5rem;'>Log in to continue</h3>", unsafe_allow_html=True)
        
        # Add container with card-like styling for form elements
        with st.container():
            # Add a more subtle white background for form
            st.markdown("""
            <div style="
                background-color: white; 
                padding: 1.5rem; 
                border-radius: 0.5rem; 
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                border: 1px solid #f1f5f9;
            ">
            </div>
            """, unsafe_allow_html=True)
            
            # Login form with placeholders
            username = st.text_input(
                "Username", 
                key="login_username",
                placeholder="Enter your username"
            )
            
            password = st.text_input(
                "Password", 
                type="password", 
                key="login_password",
                placeholder="Enter your password"
            )
            
            # Add space before button
            st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
            
            # Login button
            if st.button("Sign In", use_container_width=True):
                try:
                    db = get_db()
                    c = db.cursor()
                    c.execute("SELECT * FROM users WHERE username = ?", (username,))
                    user = c.fetchone()

                    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                        st.session_state.authenticated = True
                        st.session_state.is_admin = bool(user['is_admin'])
                        st.session_state.user_id = user['id']
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Please check your username and password.")
                except Exception as e:
                    st.error(f"Login failed: {str(e)}")
        
        # Footer text with Replit-style
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; color: #475569; font-size: 0.875rem;'>Stormwater Infrastructure Assessment System</p>", unsafe_allow_html=True)
        
        # Help text with light gray and smaller font
        st.markdown("""
        <div style="text-align: center; margin-top: 0.75rem;">
            <span style="font-size: 0.75rem; color: #94a3b8; display: inline-block; border-radius: 0.25rem; padding: 0.25rem 0.5rem; background-color: #f8fafc;">
                Default login: admin / admin123
            </span>
        </div>
        """, unsafe_allow_html=True)
            

def create_user(username, password, is_admin=False):
    """Create a new user"""
    try:
        db = get_db()
        c = db.cursor()

        # Check if username exists
        c.execute("SELECT id FROM users WHERE username = ?", (username,))
        if c.fetchone():
            raise ValueError("Username already exists")

        # Create new user with bcrypt hashed password
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        c.execute(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            (username, hashed, is_admin)
        )
        db.commit()
        return c.lastrowid
    except Exception as e:
        st.error(f"Failed to create user: {str(e)}")
        raise e