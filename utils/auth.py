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
                user = db.users.find_one({"username": username})

                if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                    st.session_state.authenticated = True
                    st.session_state.is_admin = user.get('is_admin', False)
                    st.session_state.user_id = str(user['_id'])
                    st.experimental_rerun()
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
        if db.users.find_one({"username": username}):
            raise ValueError("Username already exists")

        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {
            "username": username,
            "password": hashed,
            "is_admin": is_admin
        }

        result = db.users.insert_one(user)
        return str(result.inserted_id)
    except Exception as e:
        st.error(f"Failed to create user: {str(e)}")
        raise e