import streamlit as st
from utils.db import get_db
from utils.auth import create_user

def show():
    if not st.session_state.get("is_admin", False):
        st.error("Unauthorized access")
        return

    st.title("Admin Panel")

    # User Management
    st.header("User Management")

    # Create new user
    with st.expander("Create New User"):
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type="password")
        is_admin = st.checkbox("Admin privileges")

        if st.button("Create User"):
            if new_username and new_password:
                create_user(new_username, new_password, is_admin)
                st.success("User created successfully")
            else:
                st.error("Please fill all fields")

    # View users
    st.subheader("Existing Users")
    db = get_db()
    c = db.cursor()
    c.execute("SELECT id, username, is_admin FROM users")
    users = c.fetchall()

    if users:
        user_data = []
        for user in users:
            user_data.append({
                "Username": user["username"],
                "Admin": "Yes" if user["is_admin"] else "No"
            })

        st.table(user_data)
    else:
        st.info("No users found")

    # System Statistics
    st.header("System Statistics")

    col1, col2 = st.columns(2)

    with col1:
        c.execute("SELECT COUNT(*) as count FROM assessments")
        assessment_count = c.fetchone()["count"]
        st.metric("Total Assessments", assessment_count)

    with col2:
        c.execute("SELECT COUNT(*) as count FROM users")
        user_count = c.fetchone()["count"]
        st.metric("Total Users", user_count)