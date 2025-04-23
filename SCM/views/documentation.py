import streamlit as st
from utils.documentation_generator import generate_user_manual
from datetime import datetime

def show():
    st.title("Documentation")
    
    # Add a download button for the comprehensive user manual
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.markdown("### User Manual")
        user_manual = generate_user_manual()
        st.download_button(
            label="📚 Download Complete Manual",
            data=user_manual,
            file_name=f"stormwater_assessment_manual_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            help="Download a comprehensive user manual with detailed instructions and technical documentation",
            use_container_width=True
        )
        
        st.markdown("Download the complete user manual for detailed instructions, technical architecture documentation, and troubleshooting guides.")
    
    with col1:
        st.markdown("### Quick Reference Guide")
        
        st.markdown("""
        #### Assessment Categories
        
        ##### 1. Stormwater Condition Assessment
        - Evaluates physical condition of infrastructure
        - Includes SHAC, STAC, and SASC metrics
        - Damage levels are rated from 0-10
        
        ##### 2. Functionality Assessment
        - Measures hydraulic and hydrological performance
        - Key metrics include flow attenuation and volume reduction
        - CSO monitoring and pumping station performance
        
        ##### 3. Time-Effectiveness Assessment
        - Tracks lifespan and maintenance timing
        - Evaluates long-term effectiveness
        - Monitors response times and maintenance intervals
        
        ##### 4. Cost-Effectiveness Assessment
        - Tracks all associated costs
        - Evaluates return on investment
        - Includes preliminary, construction, and operational costs
        
        ##### 5. Environmental and Social Impact
        - Measures environmental benefits
        - Tracks community satisfaction
        - Monitors safety metrics
        """)
    
    st.markdown("---")
    
    st.markdown("### System Usage Overview")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Using the System
        
        1. Complete assessments regularly
        2. Review dashboard metrics
        3. Generate and save reports
        4. Track trends over time
        """)
    
    with col2:
        st.markdown("""
        #### Best Practices
        
        - Conduct assessments at consistent intervals
        - Document all observations
        - Include photos when possible
        - Follow up on maintenance needs
        """)
    
    st.markdown("---")
    
    st.markdown("### Presentation Materials")
    
    st.markdown("""
    #### Project Overview Presentation
    
    Key components covered in the stormwater infrastructure assessment system:
    
    1. Assessment Framework
       - Condition Assessment (SHAC, STAC, SASC metrics)
       - Functionality Assessment
       - Time-Effectiveness Assessment
       - Cost-Effectiveness Assessment
       - Environmental Impact Assessment
    
    2. Technical Implementation
       - Streamlit-based web interface
       - SQLite database for data persistence
       - PDF report generation
       - GIS integration
       - Multi-user support with role-based access
    
    3. Key Features
       - Interactive dashboards
       - Comprehensive assessment forms
       - Automated report generation
       - City-specific recommendations
       - Historical data tracking
    
    4. Future Development Areas
       - AI/ML integration for predictive maintenance
       - Enhanced GIS capabilities
       - Mobile app development
       - Integration with IoT sensors
       - Advanced analytics dashboard
    """)
    
    st.info("For comprehensive information including technical architecture, scoring methodology, and troubleshooting, please download the complete user manual.")