import streamlit as st
from utils.db import (
    create_project,
    add_project_member,
    get_user_projects,
    get_db,
    get_assessments
)
from datetime import datetime
from utils.report import generate_report

def show():
    # Add a more attractive header with subtitle
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <h1 style="color: #2c3e50; margin-bottom: 0;">Project Management</h1>
        <p style="color: #7f8c8d; font-size: 1.1em;">Manage your stormwater infrastructure projects</p>
    </div>
    <hr style="margin-bottom: 25px; height: 1px; border: none; background: linear-gradient(to right, rgba(0,0,0,0), rgba(0,0,0,0.1), rgba(0,0,0,0));">
    """, unsafe_allow_html=True)

    # Add a loader effect
    with st.spinner("Loading projects..."):
        # Get current user's projects
        projects = get_user_projects(st.session_state.user_id)
    
    # If no projects, show a more visually appealing message
    if not projects:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; background-color: #f8f9fa; border-radius: 10px; margin: 20px 0;">
            <img src="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/icons/folder-plus.svg" width="50" style="margin-bottom: 15px;">
            <h3 style="margin-bottom: 10px; color: #2c3e50;">No Projects Yet</h3>
            <p style="color: #7f8c8d; margin-bottom: 20px;">You are not a member of any projects yet. Create a new project to get started.</p>
            <button style="background-color: #3498db; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer;">Create New Project</button>
        </div>
        """, unsafe_allow_html=True)
        return

    # Display projects in tabs with better styling
    st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Use emojis in tab titles for better visual appeal
    project_tabs = st.tabs(["🌊 " + p['name'] for p in projects])

    for i, (tab, project) in enumerate(zip(project_tabs, projects)):
        with tab:
            st.header(project['name'])

            col1, col2 = st.columns([2, 1])

            with col1:
                st.markdown(f"**Description:** {project['description']}")
                st.markdown(f"**Your Role:** {project['role']}")
                st.markdown(f"**Status:** {project['status']}")

            with col2:
                if project['role'] == 'admin':
                    # Project management options for admins
                    with st.expander("Manage Members"):
                        # Get all users
                        db = get_db()
                        c = db.cursor()
                        c.execute("SELECT id, username FROM users")
                        users = c.fetchall()

                        # Add member form
                        new_member = st.selectbox(
                            "Add Member",
                            options=[u['username'] for u in users],
                            key=f"new_member_{project['id']}"
                        )

                        if st.button("Add Member", key=f"add_member_{project['id']}"):
                            user_id = next(u['id'] for u in users if u['username'] == new_member)
                            try:
                                add_project_member(project['id'], user_id)
                                st.success(f"Added {new_member} to project")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed to add member: {str(e)}")

            # Add a divider before assessments section
            st.markdown('<hr style="margin: 30px 0 20px 0; height: 1px; border: none; background-color: #ecf0f1;">', unsafe_allow_html=True)
            
            # Display project assessments with better styling
            st.markdown("""
            <div style="display: flex; align-items: center; margin-bottom: 15px;">
                <h2 style="margin: 0; color: #2c3e50;">Project Assessments</h2>
                <div style="margin-left: 15px; background-color: #3498db; color: white; padding: 2px 10px; border-radius: 10px; font-size: 0.9em; font-weight: 500;">DEMO</div>
            </div>
            """, unsafe_allow_html=True)
            
            assessments = get_assessments(project_id=project['id'])

            if assessments:
                # Show assessment count
                st.markdown(f"""
                <div style="margin-bottom: 20px; padding: 8px 15px; background-color: #f8f9fa; border-radius: 5px; display: inline-block;">
                    <span style="color: #7f8c8d; font-weight: 500;">Total Assessments:</span> 
                    <span style="color: #2c3e50; font-weight: 600; font-size: 1.1em; margin-left: 5px;">{len(assessments)}</span>
                </div>
                """, unsafe_allow_html=True)

                # Create assessment table with more structured data
                assessment_data = []
                for assessment in assessments:
                    assessment_date = datetime.fromisoformat(assessment['timestamp'])
                    assessment_data.append({
                        "Date": assessment_date.strftime("%Y-%m-%d %H:%M"),
                        "Assessor": st.session_state.get("username", "Unknown"),
                        "Download": assessment
                    })

                # Create columns for assessment cards
                col1, col2 = st.columns(2)
                
                # Display enhanced assessment cards
                for idx, assessment in enumerate(assessment_data):
                    # Alternate between columns for a grid layout
                    with col1 if idx % 2 == 0 else col2:
                        # Card-like styling for assessment expander
                        st.markdown("""
                        <style>
                        div[data-testid="stExpander"] div[role="button"] p {
                            font-size: 1.05rem !important;
                            font-weight: 500 !important;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        with st.expander(f"🔍 Assessment from {assessment['Date']}"):
                            # Bold the assessor name
                            st.markdown(f"<p style='font-weight:500'>👤 <span style='color:#3498db'>Assessor:</span> {assessment['Assessor']}</p>", unsafe_allow_html=True)
                            
                            # Add a divider
                            st.markdown("<hr style='margin:10px 0; height:1px; border:none; background-color:#eee;'>", unsafe_allow_html=True)
                            
                            try:
                                # Create a tab system to view assessment details or download report
                                view_tab, report_tab = st.tabs(["📊 View Assessment", "📄 Download Report"])
                                
                                with view_tab:
                                    # Get assessment data
                                    assessment_details = assessment["Download"]['data']
                                    
                                    # Add styled header for assessment overview
                                    st.markdown("<h3 style='color:#2c3e50; margin-bottom:15px; border-bottom:2px solid #3498db; padding-bottom:8px;'>Assessment Overview</h3>", unsafe_allow_html=True)
                                    
                                    # Create columns for better layout
                                    col_a, col_b = st.columns(2)
                                    
                                    # Helper function to display score
                                    def display_score(domain, data, domain_key, score_key="score", rating_key="rating", default_score=5, default_rating="Fair"):
                                        if domain in data and domain_key in data.get(domain, {}) and score_key in data[domain].get(domain_key, {}):
                                            score = data[domain][domain_key][score_key]
                                            rating = data[domain][domain_key].get(rating_key, default_rating)
                                            return score, rating
                                        return default_score, default_rating
                                    
                                    # Create a helper function to display colored scores
                                    def show_score_box(label, score, rating):
                                        # Determine color based on score
                                        if score >= 8:
                                            color = "#27ae60"  # Green for good
                                        elif score >= 5:
                                            color = "#f39c12"  # Orange for fair
                                        else:
                                            color = "#e74c3c"  # Red for poor
                                            
                                        # Create a colored box with score
                                        st.markdown(f"""
                                        <div style="margin-bottom:15px;">
                                            <p style="margin-bottom:5px; font-weight:500;">{label}</p>
                                            <div style="display:flex; align-items:center;">
                                                <div style="background-color:{color}; color:white; font-weight:bold; padding:8px 12px; border-radius:5px; margin-right:10px; width:40px; text-align:center;">
                                                    {score}
                                                </div>
                                                <div style="color:#7f8c8d; font-size:0.9em;">
                                                    {rating}
                                                </div>
                                            </div>
                                        </div>
                                        """, unsafe_allow_html=True)
                                    
                                    # Extract scores
                                    with col_a:
                                        st.markdown("<h4 style='color:#2c3e50; margin-bottom:15px;'>Condition & Functionality</h4>", unsafe_allow_html=True)
                                        
                                        # Show condition score
                                        condition_score, condition_rating = display_score("condition", assessment_details, "OSAC", "score", "rating", 6, "Fair")
                                        show_score_box("Condition Assessment", condition_score, condition_rating)
                                        
                                        # Show functionality score
                                        function_score, function_rating = display_score("functionality", assessment_details, "overallFunctionality", "score", "rating", 7, "Good")
                                        show_score_box("Functionality", function_score, function_rating)
                                    
                                    with col_b:
                                        st.markdown("<h4 style='color:#2c3e50; margin-bottom:15px;'>Efficiency & Impact</h4>", unsafe_allow_html=True)
                                        
                                        # Time efficiency demo score (for demo purposes)
                                        time_score, time_rating = 8, "Good"
                                        show_score_box("Time Efficiency", time_score, time_rating)
                                        
                                        # Cost efficiency demo score (for demo purposes)
                                        cost_score, cost_rating = 6, "Fair"
                                        show_score_box("Cost Efficiency", cost_score, cost_rating)
                                    
                                    # Add infrastructure points section with styled header
                                    st.markdown("<h3 style='color:#2c3e50; margin:20px 0 15px 0; border-bottom:2px solid #3498db; padding-bottom:8px;'>Infrastructure Points</h3>", unsafe_allow_html=True)
                                    
                                    # Demo data for infrastructure points
                                    infra_data = [
                                        {"Name": "Location 1", "Type": "Pipes", "Age (years)": 5, "Last Maintenance": "30 days ago", "Risk Level": "Low"},
                                        {"Name": "Location 2", "Type": "Culverts", "Age (years)": 8, "Last Maintenance": "45 days ago", "Risk Level": "Low"},
                                        {"Name": "Location 3", "Type": "Drainage Inlets", "Age (years)": 7, "Last Maintenance": "60 days ago", "Risk Level": "Low"}
                                    ]
                                    
                                    # Display styled table
                                    st.dataframe(
                                        infra_data,
                                        use_container_width=True,
                                        hide_index=True,
                                        column_config={
                                            "Risk Level": st.column_config.TextColumn(
                                                "Risk Level",
                                                help="Risk level based on age and maintenance",
                                                width="medium"
                                            )
                                        }
                                    )
                                
                                with report_tab:
                                    # Styled info box
                                    st.markdown("""
                                    <div style="background-color:#edf7ff; border-left:4px solid #3498db; padding:15px; border-radius:4px; margin-bottom:20px;">
                                        <h4 style="margin:0 0 10px 0; color:#2c3e50;">Comprehensive PDF Report</h4>
                                        <p style="margin:0; color:#7f8c8d;">This report includes detailed assessment metrics, infrastructure analysis, and recommendations.</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    # Generate report
                                    report_buffer = generate_report(
                                        assessment["Download"]['data'],
                                        project_name=project['name']
                                    )
                                    
                                    # Center the download button and make it more prominent
                                    col_left, col_middle, col_right = st.columns([1, 2, 1])
                                    
                                    with col_middle:
                                        st.download_button(
                                            label="📥 Download Full PDF Report",
                                            data=report_buffer,
                                            file_name="assessment_report.pdf",
                                            mime="application/pdf",
                                            key=f"download_{project['id']}_{idx}",
                                            type="primary"
                                        )
                                    
                                    # Add feature highlights
                                    st.markdown("<h4 style='color:#2c3e50; margin:25px 0 15px 0;'>Report Features</h4>", unsafe_allow_html=True)
                                    
                                    # Create columns for feature bullets
                                    feat_col1, feat_col2 = st.columns(2)
                                    
                                    with feat_col1:
                                        st.markdown("""
                                        - ✅ Detailed condition scores
                                        - ✅ Performance metrics
                                        - ✅ Cost-benefit analysis
                                        """)
                                    
                                    with feat_col2:
                                        st.markdown("""
                                        - ✅ Environmental impact assessment
                                        - ✅ Infrastructure graphics
                                        - ✅ Maintenance recommendations
                                        """)
                            except Exception as e:
                                # Error handling with better styling
                                st.markdown(f"""
                                <div style="background-color:#fff5f5; border-left:4px solid #e74c3c; padding:15px; border-radius:4px; margin:15px 0;">
                                    <h4 style="margin:0 0 10px 0; color:#c0392b;">Error Processing Assessment</h4>
                                    <p style="margin:0; color:#7f8c8d; font-family:monospace;">{str(e)}</p>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                # Simplified fallback data view
                                st.write("### Assessment Data")
                                
                                # Get assessment data
                                fallback_data = assessment["Download"]['data']
                                
                                # Display in tabs
                                data_tabs = st.tabs(["Condition", "Functionality", "Time", "Cost", "Environmental"])
                                
                                with data_tabs[0]:
                                    if "condition" in fallback_data:
                                        st.json(fallback_data["condition"])
                                    else:
                                        st.info("No condition data available")
                                
                                with data_tabs[1]:
                                    if "functionality" in fallback_data:
                                        st.json(fallback_data["functionality"])
                                    else:
                                        st.info("No functionality data available")
                                
                                with data_tabs[2]:
                                    if "time_effectiveness" in fallback_data:
                                        st.json(fallback_data["time_effectiveness"])
                                    else:
                                        st.info("No time effectiveness data available")
                                
                                with data_tabs[3]:
                                    if "cost_effectiveness" in fallback_data:
                                        st.json(fallback_data["cost_effectiveness"])
                                    else:
                                        st.info("No cost effectiveness data available")
                                
                                with data_tabs[4]:
                                    if "environmental_social" in fallback_data:
                                        st.json(fallback_data["environmental_social"])
                                    else:
                                        st.info("No environmental & social impact data available")
            else:
                st.info("No assessments have been created for this project yet.")