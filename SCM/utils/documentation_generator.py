from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
import base64
from datetime import datetime
import streamlit as st
import os
import xml.etree.ElementTree as ET
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

def generate_user_manual():
    """Generate a comprehensive user manual PDF"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    title = Paragraph("Stormwater Infrastructure Assessment<br/>User Manual", title_style)
    story.append(title)
    story.append(Spacer(1, 20))

    # Document metadata
    metadata_style = ParagraphStyle(
        'Metadata',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray,
        alignment=1  # Center alignment
    )
    metadata = Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d')}<br/>Version 1.0", metadata_style)
    story.append(metadata)
    story.append(Spacer(1, 30))

    # Table of Contents header
    toc_header = Paragraph("Table of Contents", styles["Heading2"])
    story.append(toc_header)
    story.append(Spacer(1, 10))

    # Simple Table of Contents
    toc_data = [
        ["1. Introduction", "3"],
        ["2. Getting Started", "4"],
        ["3. User Interface Overview", "5"],
        ["4. Dashboard", "6"],
        ["5. Projects", "7"],
        ["6. Assessments", "8"],
        ["7. Reports", "10"],
        ["8. Administration", "12"],
        ["9. Technical Architecture", "14"],
        ["10. Troubleshooting", "15"]
    ]
    
    toc_table = Table(toc_data, colWidths=[400, 50])
    toc_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ]))
    story.append(toc_table)
    story.append(Spacer(1, 30))

    # 1. Introduction
    story.append(Paragraph("1. Introduction", styles["Heading1"]))
    intro_text = """
    The Stormwater Infrastructure Assessment application is a comprehensive tool designed for 
    municipalities, engineers, and infrastructure managers to evaluate, track, and plan maintenance 
    for stormwater control systems. This application provides a structured approach to assessing 
    infrastructure condition, functionality, cost-effectiveness, and environmental impact.
    
    Key features include:
    • Comprehensive assessment framework with five key categories
    • Interactive dashboards with data visualization
    • Project management capabilities for team collaboration
    • GIS integration for spatial visualization of infrastructure
    • Detailed reporting with 0-10 scoring system
    • Historical tracking of infrastructure performance
    """
    story.append(Paragraph(intro_text, styles["Normal"]))
    story.append(Spacer(1, 20))

    # 2. Getting Started
    story.append(Paragraph("2. Getting Started", styles["Heading1"]))
    story.append(Paragraph("2.1 System Access", styles["Heading2"]))
    
    login_text = """
    To access the system, navigate to the application URL in your web browser. You will be 
    presented with a login screen. Enter your credentials provided by your system administrator.
    
    Default users include:
    • Username: admin, Password: admin123 (Administrator access)
    • Username: john_engineer, Password: john123 (Standard user)
    
    For security purposes, it is recommended to change your password after first login.
    """
    story.append(Paragraph(login_text, styles["Normal"]))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("2.2 Navigation", styles["Heading2"]))
    nav_text = """
    After logging in, you will see the main dashboard. The application features a sidebar navigation 
    menu with the following options:
    
    • Dashboard: Overview of assessment data with visualizations
    • Projects: Manage and collaborate on infrastructure projects
    • Assessment: Create new infrastructure assessments
    • Documentation: Access help and guidelines
    • Admin: User management and system statistics (admin users only)
    
    You can navigate between these sections by clicking on the corresponding sidebar menu item.
    """
    story.append(Paragraph(nav_text, styles["Normal"]))
    story.append(Spacer(1, 20))

    # 3. User Interface Overview
    story.append(Paragraph("3. User Interface Overview", styles["Heading1"]))
    ui_text = """
    The application uses a consistent layout across all pages:
    
    • Left Sidebar: Navigation menu and user information
    • Main Content Area: Displays the selected view (dashboard, projects, etc.)
    • Top Section: Page title and context-specific actions
    
    Most pages use a card-based design with clear sections for different types of information. 
    Data visualizations include:
    
    • Charts (bar, line, radar, pie) for metric visualization
    • Maps showing infrastructure locations and status
    • Tables for detailed data representation
    • Forms for data input and assessment
    """
    story.append(Paragraph(ui_text, styles["Normal"]))
    story.append(Spacer(1, 20))

    # 4. Dashboard
    story.append(Paragraph("4. Dashboard", styles["Heading1"]))
    dashboard_text = """
    The dashboard provides an overview of assessment data with key metrics and visualizations.
    
    Key components include:
    
    • Project Overview: Shows total assessments, recent assessments, and last assessment date
    • Assessment Analysis: Visualizations of infrastructure condition data
    • Performance Metrics: Radar chart showing system performance indicators
    • Environmental Impact: Pie chart of environmental metrics
    • Infrastructure Map: Geographical representation of infrastructure points
    • Historical Analysis: Trend charts showing performance over time
    
    The dashboard uses a 0-10 scoring system to represent overall infrastructure health. This score is calculated 
    using a weighted average of all assessment categories:
    
    • Condition (30% weight): Physical state of infrastructure
    • Functionality (20% weight): Operational performance
    • Time Effectiveness (15% weight): Lifespan and maintenance timing
    • Cost Effectiveness (15% weight): Financial metrics
    • Environmental Impact (20% weight): Environmental and social benefits
    
    Each section of the dashboard can be interacted with for more detailed information.
    """
    story.append(Paragraph(dashboard_text, styles["Normal"]))
    story.append(Spacer(1, 20))

    # 5. Projects
    story.append(Paragraph("5. Projects", styles["Heading1"]))
    projects_text = """
    The Projects section allows you to manage and collaborate on infrastructure assessments.
    
    Key functionality includes:
    
    • Project Listing: View all projects you have access to
    • Project Details: Description, status, and your role in the project
    • Member Management: Add users to projects (admin role required)
    • Assessment History: View all assessments created for a project
    • Report Generation: Download PDF reports for assessments
    
    Projects are organized using tabs, with each tab representing a different project. Within each 
    project tab, assessments are displayed in a collapsible format showing assessment date and 
    assessor, with options to download detailed reports.
    
    Project administrators can add new members to projects using the "Manage Members" expander.
    """
    story.append(Paragraph(projects_text, styles["Normal"]))
    story.append(Spacer(1, 20))

    # 6. Assessments
    story.append(Paragraph("6. Assessments", styles["Heading1"]))
    assessment_text = """
    The Assessment section allows you to create new infrastructure assessments.
    
    Assessment Categories:
    
    1. Stormwater Condition Assessment
       • Evaluates the physical condition of infrastructure components
       • Includes damage levels for pipes, culverts, manholes, drainage inlets, and channels
       • Options include low, moderate, and high damage levels
    
    2. Functionality Assessment
       • Measures hydraulic and hydrological performance
       • Metrics include flow attenuation (%), volume reduction (%), CSO frequency, and drainage duration
    
    3. Time-Effectiveness Assessment
       • Tracks infrastructure lifespan (years)
       • Records maintenance lag time (days)
       • Monitors flood duration (hours)
    
    4. Cost-Effectiveness Assessment
       • Records operational costs ($)
       • Calculates return on investment (%)
       • Tracks construction and preliminary costs
    
    5. Environmental and Social Impact
       • Measures pollutant concentration reduction (%)
       • Records customer satisfaction scores (0-10)
       • Calculates pollution retention rates (%)
    
    Additionally, assessments include:
    
    • Infrastructure Points: Geographical locations with metadata
    • Project Context: Linking assessment to specific projects
    • Timestamp: Recording when assessment was performed
    
    After completing an assessment, the data is saved to the database and becomes available for 
    visualization in the dashboard and for report generation.
    """
    story.append(Paragraph(assessment_text, styles["Normal"]))
    story.append(Spacer(1, 20))

    # 7. Reports
    story.append(Paragraph("7. Reports", styles["Heading1"]))
    reports_text = """
    The application provides detailed PDF reports for assessments. Reports can be accessed from:
    
    • Project Page: Reports for each assessment in a project
    • Dashboard: Generate report for the latest assessment
    
    Report contents include:
    
    • Executive Summary: Overall infrastructure score (0-10) and assessment metadata
    • Infrastructure Analysis: Table of infrastructure points with condition details
    • Assessment Sections: Detailed breakdown of all assessment categories with individual scores
    • City-Specific Recommendations: Customized recommendations based on project location
    
    Reports are designed to be comprehensive yet concise, providing all the necessary information for 
    decision-making. Each assessment category receives individual scores that contribute to the 
    overall infrastructure score.
    
    To download a report:
    1. Navigate to the Projects page
    2. Select the project of interest
    3. Expand the assessment you want to report on
    4. Click the "Download Report" button
    
    Alternatively, from the Dashboard:
    1. Select the project from the dropdown
    2. Scroll to the "Export Options" section
    3. Click "Generate Assessment Report"
    4. Use the "Download Assessment Report" button that appears
    """
    story.append(Paragraph(reports_text, styles["Normal"]))
    story.append(Spacer(1, 20))

    # 8. Administration
    story.append(Paragraph("8. Administration", styles["Heading1"]))
    admin_text = """
    The Admin section is available only to users with administrator privileges. It provides 
    system-wide management capabilities.
    
    Key features include:
    
    • Organization Tree: Visual representation of users and their activities
    • User Management: Create and manage user accounts
    • Activity Timeline: Track system-wide activity
    • System Statistics: View usage metrics and trends
    
    User Management allows administrators to:
    • Create new users
    • Assign admin privileges
    • View user projects and activity
    
    The Activity Timeline provides a chronological view of all system activities with filters for:
    • Time range (1-30 days)
    • Activity types (assessment, report, update, maintenance)
    
    System Statistics show key metrics including:
    • Total assessments
    • Total users
    • Active projects
    • Activity trends over time
    """
    story.append(Paragraph(admin_text, styles["Normal"]))
    story.append(Spacer(1, 20))

    # 9. Technical Architecture
    story.append(Paragraph("9. Technical Architecture", styles["Heading1"]))
    architecture_text = """
    The Stormwater Infrastructure Assessment application is built with the following technologies:
    
    • Frontend: Streamlit (Python web framework)
    • Database: SQLite (local database for data persistence)
    • Visualization: Plotly and Folium for interactive charts and maps
    • Reporting: ReportLab for PDF generation
    • Authentication: Custom implementation with bcrypt for password hashing
    
    The application architecture follows a modular design:
    
    • app.py: Main application entry point and navigation
    • views/: Module containing all page views (dashboard, projects, etc.)
    • components/: Reusable UI components (charts, maps, forms)
    • utils/: Utility functions for database, authentication, and reporting
    
    Data flow:
    1. User input is collected through forms
    2. Data is processed and stored in the SQLite database
    3. Visualization components query the database and display the data
    4. Reports are generated using the same data sources
    
    The application uses a SQLite database with the following tables:
    • users: User accounts and authentication
    • projects: Project metadata
    • project_members: User-project relationships
    • assessments: Assessment data
    • activity_log: System activity tracking
    """
    story.append(Paragraph(architecture_text, styles["Normal"]))
    story.append(Spacer(1, 20))
    
    # Add architectural diagram
    try:
        # Convert SVG to ReportLab drawing
        svg_path = "doc_assets/system_architecture.svg"
        if os.path.exists(svg_path):
            story.append(Paragraph("System Architecture Diagram:", styles["Heading2"]))
            drawing = svg2rlg(svg_path)
            # Scale the drawing to fit the page
            drawing.width = 450
            drawing.height = 350
            drawing.scale(1, 1)
            story.append(drawing)
            story.append(Spacer(1, 10))
            story.append(Paragraph("The diagram above illustrates the layered architecture of the Stormwater Infrastructure Assessment system.", styles["Normal"]))
        else:
            story.append(Paragraph("* System architecture diagram not available *", styles["Normal"]))
    except Exception as e:
        # If there's an error loading the SVG, just continue without it
        story.append(Paragraph("* System architecture diagram not available *", styles["Normal"]))
        print(f"Error adding architecture diagram: {e}")
    
    story.append(Spacer(1, 20))

    # 10. Troubleshooting
    story.append(Paragraph("10. Troubleshooting", styles["Heading1"]))
    troubleshooting_text = """
    Common issues and their solutions:
    
    Issue: Unable to log in
    Solution:
    • Verify username and password
    • Check with an administrator if your account is active
    • Try resetting your password
    
    Issue: Assessment data not appearing in dashboard
    Solution:
    • Verify that the assessment was saved successfully
    • Check that you have selected the correct project
    • Refresh the page to reload data
    
    Issue: Report generation fails
    Solution:
    • Ensure the assessment has complete data in all categories
    • Try generating the report from the Projects page instead
    • Check that the assessment has infrastructure points data
    
    Issue: Map visualization not showing
    Solution:
    • Verify that the assessment includes infrastructure points with coordinates
    • Check that the coordinates are valid (latitude and longitude)
    • Refresh the page to reload the map
    
    For additional support:
    • Contact your system administrator
    • Check the documentation page for updates
    • Review the logs for more detailed error information (admin only)
    """
    story.append(Paragraph(troubleshooting_text, styles["Normal"]))

    # Build the PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def add_documentation_download():
    """Add a download button for the user manual in the documentation view"""
    with st.sidebar:
        st.markdown("---")
        st.subheader("Documentation")
        
        user_manual = generate_user_manual()
        st.download_button(
            label="📚 Download User Manual (PDF)",
            data=user_manual,
            file_name=f"stormwater_assessment_manual_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            help="Download a comprehensive user manual with detailed instructions and technical documentation",
            use_container_width=True
        )