import streamlit as st
from utils.db import get_db
from utils.auth import create_user
import pandas as pd
from datetime import datetime, timedelta
from components.org_tree import show_org_tree

def show():
    if not st.session_state.get("is_admin", False):
        st.error("Unauthorized access")
        return

    st.title("Admin Panel")

    # Create tabs for different admin sections
    tabs = st.tabs(["Organization Tree", "User Management", "Activity Timeline", "System Statistics"])

    with tabs[0]:
        show_org_tree()

    with tabs[1]:
        show_user_management()

    with tabs[2]:
        show_activity_timeline()

    with tabs[3]:
        show_system_statistics()

def show_user_management():
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

    # Get users with their project count and last activity
    c.execute("""
        SELECT 
            u.id,
            u.username,
            u.is_admin,
            COUNT(DISTINCT pm.project_id) as project_count,
            MAX(al.timestamp) as last_activity
        FROM users u
        LEFT JOIN project_members pm ON u.id = pm.user_id
        LEFT JOIN activity_log al ON u.id = al.user_id
        GROUP BY u.id, u.username, u.is_admin
    """)
    users = c.fetchall()

    if users:
        user_data = []
        for user in users:
            user_data.append({
                "Username": user["username"],
                "Admin": "Yes" if user["is_admin"] else "No",
                "Projects": user["project_count"],
                "Last Activity": user["last_activity"] or "Never"
            })

        st.dataframe(
            pd.DataFrame(user_data),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No users found")

def show_activity_timeline():
    st.header("Activity Timeline")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        days = st.slider("Show activities from last N days", 1, 30, 7)
    with col2:
        activity_type = st.multiselect(
            "Filter by activity type",
            ["assessment", "report", "update", "maintenance"],
            default=["assessment", "report", "update", "maintenance"]
        )

    # Get filtered activities
    db = get_db()
    c = db.cursor()
    c.execute("""
        SELECT 
            al.timestamp,
            u.username,
            p.name as project_name,
            al.action_type,
            al.action_details
        FROM activity_log al
        JOIN users u ON al.user_id = u.id
        JOIN projects p ON al.project_id = p.id
        WHERE al.timestamp > ?
        AND al.action_type IN ({})
        ORDER BY al.timestamp DESC
    """.format(','.join(['?']*len(activity_type))),
        [datetime.now() - timedelta(days=days)] + activity_type
    )
    activities = c.fetchall()

    if activities:
        for activity in activities:
            with st.expander(f"{activity['timestamp']} - {activity['username']}"):
                st.write(f"**Project:** {activity['project_name']}")
                st.write(f"**Action:** {activity['action_type']}")
                st.write(f"**Details:** {activity['action_details']}")
    else:
        st.info("No activities found for the selected filters")

def show_system_statistics():
    st.header("System Statistics")

    db = get_db()
    c = db.cursor()

    # Create a 3-column layout
    col1, col2, col3 = st.columns(3)

    with col1:
        c.execute("SELECT COUNT(*) as count FROM assessments")
        assessment_count = c.fetchone()["count"]
        st.metric("Total Assessments", assessment_count)

    with col2:
        c.execute("SELECT COUNT(*) as count FROM users")
        user_count = c.fetchone()["count"]
        st.metric("Total Users", user_count)

    with col3:
        c.execute("SELECT COUNT(*) as count FROM projects")
        project_count = c.fetchone()["count"]
        st.metric("Active Projects", project_count)

    # Activity trends
    st.subheader("Activity Trends")
    c.execute("""
        SELECT 
            DATE(timestamp) as date,
            COUNT(*) as count
        FROM activity_log
        GROUP BY DATE(timestamp)
        ORDER BY date DESC
        LIMIT 10
    """)
    activity_data = c.fetchall()
    if activity_data:
        chart_data = pd.DataFrame(activity_data)
        st.line_chart(chart_data.set_index('date'))