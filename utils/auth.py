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
    st.title("Login")

    col1, col2 = st.columns([1, 2])

    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            try:
                db = get_db()
                c = db.cursor()
                c.execute("SELECT * FROM users WHERE username = ?", (username,))
                user = c.fetchone()

                if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                    st.session_state.authenticated = True
                    st.session_state.is_admin = bool(user['is_admin'])
                    st.session_state.user_id = user['id']
                    st.rerun()  # Updated from experimental_rerun
                else:
                    st.error("Invalid credentials")
            except Exception as e:
                st.error(f"Login failed: {str(e)}")

    with col2:
        st.info("""
        Welcome to the Stormwater Infrastructure Assessment System

        Default admin credentials:
        - Username: admin
        - Password: admin123
        """)

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