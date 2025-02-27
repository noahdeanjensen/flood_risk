import streamlit as st
from utils.db import get_db
import bcrypt

def init_auth():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "is_admin" not in st.session_state:
        st.session_state.is_admin = False

def check_auth():
    st.title("Login")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Login"):
            db = get_db()
            user = db.users.find_one({"username": username})
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
                st.session_state.authenticated = True
                st.session_state.is_admin = user.get('is_admin', False)
                st.session_state.user_id = str(user['_id'])
                st.experimental_rerun()
            else:
                st.error("Invalid credentials")

def create_user(username, password, is_admin=False):
    db = get_db()
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    user = {
        "username": username,
        "password": hashed,
        "is_admin": is_admin
    }
    
    db.users.insert_one(user)
