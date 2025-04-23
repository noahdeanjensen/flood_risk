import plotly.graph_objects as go
import pandas as pd
import streamlit as st
from utils.db import get_db
from datetime import datetime, timedelta

def create_org_tree():
    """Create an organizational tree showing users and their current work"""
    try:
        db = get_db()
        c = db.cursor()
        
        # Get all active users and their projects
        c.execute("""
            SELECT 
                u.username,
                p.name as project_name,
                pm.role,
                al.action_type,
                al.action_details,
                al.timestamp
            FROM users u
            LEFT JOIN project_members pm ON u.id = pm.user_id
            LEFT JOIN projects p ON pm.project_id = p.id
            LEFT JOIN activity_log al ON (u.id = al.user_id AND pm.project_id = al.project_id)
            WHERE al.timestamp >= datetime('now', '-30 days')
            OR al.timestamp IS NULL
            ORDER BY al.timestamp DESC
        """)
        
        activities = c.fetchall()
        
        # Process data for tree visualization
        nodes = ["Stormwater<br>Assessment<br>System"]  # Root node
        node_parents = [""]  # Root has no parent
        node_text = [""]  # Root has no additional text
        node_colors = ["#1f77b4"]  # Root color
        
        # Add users and their activities
        users_added = set()
        for activity in activities:
            username = activity['username']
            
            # Add user if not already added
            if username not in users_added:
                nodes.append(username)
                node_parents.append("Stormwater<br>Assessment<br>System")
                node_text.append(f"Role: {activity['role']}")
                node_colors.append("#2ca02c")  # Green for users
                users_added.add(username)
            
            # Add project node
            if activity['project_name']:
                project_node = f"{activity['project_name']}"
                if project_node not in nodes:
                    nodes.append(project_node)
                    node_parents.append(username)
                    node_text.append("")
                    node_colors.append("#ff7f0e")  # Orange for projects
                
                # Add activity node
                if activity['action_type']:
                    activity_text = f"{activity['action_type']}: {activity['action_details']}"
                    timestamp = datetime.fromisoformat(activity['timestamp'])
                    nodes.append(f"{activity_text}<br>{timestamp.strftime('%Y-%m-%d %H:%M')}")
                    node_parents.append(project_node)
                    node_text.append("")
                    node_colors.append("#d62728")  # Red for activities
        
        # Create the tree visualization
        fig = go.Figure(go.Treemap(
            labels=nodes,
            parents=node_parents,
            text=node_text,
            marker=dict(colors=node_colors),
            textinfo="label",
            hovertext=node_text,
            hoverinfo="text"
        ))
        
        fig.update_layout(
            title="Organization Activity Tree",
            width=1000,
            height=800,
            showlegend=False
        )
        
        return fig
        
    except Exception as e:
        st.error(f"Failed to create organization tree: {str(e)}")
        return None

def show_org_tree():
    """Display the organizational tree in the admin panel"""
    st.header("Organization Activity Tree")
    
    # Add filters
    col1, col2 = st.columns(2)
    with col1:
        view_type = st.selectbox(
            "View Type",
            ["All Activities", "Recent Activities", "Current Projects"]
        )
    
    with col2:
        time_range = st.slider(
            "Time Range (days)",
            min_value=1,
            max_value=30,
            value=7
        )
    
    # Create and display the tree
    tree = create_org_tree()
    if tree:
        st.plotly_chart(tree, use_container_width=True)
    else:
        st.warning("Could not generate organization tree")
