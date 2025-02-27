import os
from pymongo import MongoClient, errors
import streamlit as st
from urllib.parse import quote_plus
import certifi

@st.cache_resource
def init_database():
    try:
        # Get MongoDB URI from environment
        uri = os.getenv("MONGODB_URI")
        if not uri:
            raise ValueError("MongoDB URI not found in environment variables")

        # Configure MongoDB client with proper SSL settings
        client = MongoClient(
            uri,
            tls=True,
            tlsCAFile=certifi.where(),  # Use system CA certificates
            retryWrites=True,
            w='majority',
            connectTimeoutMS=30000,
            socketTimeoutMS=None,
            connect=True,
            maxPoolSize=1
        )

        # Test the connection
        client.admin.command('ping')
        return client
    except errors.ConnectionFailure as e:
        st.error(f"Failed to connect to MongoDB: Connection error - {str(e)}")
        raise e
    except errors.ServerSelectionTimeoutError as e:
        st.error(f"Failed to connect to MongoDB: Server selection timeout - {str(e)}")
        raise e
    except Exception as e:
        st.error(f"Failed to connect to MongoDB: {str(e)}")
        raise e

def get_db():
    client = init_database()
    return client.stormwater_assessment

def save_assessment(data):
    try:
        db = get_db()
        result = db.assessments.insert_one(data)
        return str(result.inserted_id)
    except Exception as e:
        st.error(f"Failed to save assessment: {str(e)}")
        raise e

def get_assessments(user_id=None):
    try:
        db = get_db()
        query = {"user_id": user_id} if user_id else {}
        return list(db.assessments.find(query))
    except Exception as e:
        st.error(f"Failed to retrieve assessments: {str(e)}")
        return []

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