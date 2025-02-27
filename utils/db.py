import os
from pymongo import MongoClient
import streamlit as st
from urllib.parse import quote_plus

@st.cache_resource
def init_database():
    try:
        # Get MongoDB URI from environment
        uri = os.getenv("MONGODB_URI")

        # Configure MongoDB client with proper SSL settings
        client = MongoClient(
            uri,
            tls=True,
            tlsAllowInvalidCertificates=True  # For development only
        )

        # Test the connection
        client.admin.command('ping')
        return client
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {str(e)}")
        raise e

def get_db():
    client = init_database()
    return client.stormwater_assessment

def save_assessment(data):
    db = get_db()
    db.assessments.insert_one(data)

def get_assessments(user_id=None):
    db = get_db()
    query = {"user_id": user_id} if user_id else {}
    return list(db.assessments.find(query))

def init_admin():
    """Initialize admin user if not exists"""
    try:
        db = get_db()
        admin_exists = db.users.find_one({"username": "admin"})
        if not admin_exists:
            from utils.auth import create_user
            create_user("admin", "admin123", is_admin=True)
            st.success("Admin user created successfully!")
            st.info("Username: admin, Password: admin123")
    except Exception as e:
        st.error(f"Failed to initialize admin user: {str(e)}")