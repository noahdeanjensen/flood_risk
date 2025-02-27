import os
from pymongo import MongoClient
import streamlit as st

@st.cache_resource
def init_database():
    client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017/"))
    return client

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
