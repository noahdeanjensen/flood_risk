import os
import sqlite3
import json
import streamlit as st
import bcrypt
from datetime import datetime

def dict_factory(cursor, row):
    """Convert SQL rows to dictionaries"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@st.cache_resource
def init_database():
    """Initialize SQLite database with required tables"""
    try:
        # Create database file if it doesn't exist
        conn = sqlite3.connect('stormwater_assessment.db', check_same_thread=False)
        conn.row_factory = dict_factory
        c = conn.cursor()

        # Create users table
        c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )
        ''')

        # Create assessments table
        c.execute('''
        CREATE TABLE IF NOT EXISTS assessments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            timestamp DATETIME NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
        ''')

        conn.commit()
        return conn
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        raise e

def get_db():
    """Get database connection"""
    if 'db' not in st.session_state:
        st.session_state.db = init_database()
    return st.session_state.db

def save_assessment(data):
    """Save assessment data"""
    try:
        db = get_db()
        c = db.cursor()

        c.execute(
            "INSERT INTO assessments (user_id, timestamp, data) VALUES (?, ?, ?)",
            (
                int(data['user_id']),
                datetime.utcnow().isoformat(),
                json.dumps(data)
            )
        )
        db.commit()
        return c.lastrowid
    except Exception as e:
        st.error(f"Failed to save assessment: {str(e)}")
        raise e

def get_assessments(user_id=None):
    """Get assessments for a user"""
    try:
        db = get_db()
        c = db.cursor()

        if user_id:
            c.execute("SELECT * FROM assessments WHERE user_id = ? ORDER BY timestamp DESC", (int(user_id),))
        else:
            c.execute("SELECT * FROM assessments ORDER BY timestamp DESC")

        rows = c.fetchall()

        # Parse JSON data
        for row in rows:
            row['data'] = json.loads(row['data'])

        return rows
    except Exception as e:
        st.error(f"Failed to retrieve assessments: {str(e)}")
        return []

def init_admin():
    """Initialize admin user if not exists"""
    try:
        db = get_db()
        c = db.cursor()

        # Check if admin exists
        c.execute("SELECT id FROM users WHERE username = ?", ("admin",))
        admin = c.fetchone()

        if not admin:
            # Create admin user with bcrypt hashed password
            password = "admin123"
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            try:
                c.execute(
                    "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                    ("admin", hashed, True)
                )
                db.commit()
                st.success("Admin user created successfully!")
                st.info("Username: admin, Password: admin123")
            except sqlite3.IntegrityError:
                # If another process created the admin user in the meantime
                pass
    except Exception as e:
        st.error(f"Failed to initialize admin user: {str(e)}")