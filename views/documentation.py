import streamlit as st

def show():
    st.title("Documentation")
    
    st.markdown("""
    ### Assessment Categories
    
    #### 1. Stormwater Condition Assessment
    - Evaluates physical condition of infrastructure
    - Includes SHAC, STAC, and SASC metrics
    - Damage levels are rated from 0-10
    
    #### 2. Functionality Assessment
    - Measures hydraulic and hydrological performance
    - Key metrics include flow attenuation and volume reduction
    - CSO monitoring and pumping station performance
    
    #### 3. Time-Effectiveness Assessment
    - Tracks lifespan and maintenance timing
    - Evaluates long-term effectiveness
    - Monitors response times and maintenance intervals
    
    #### 4. Cost-Effectiveness Assessment
    - Tracks all associated costs
    - Evaluates return on investment
    - Includes preliminary, construction, and operational costs
    
    #### 5. Environmental and Social Impact
    - Measures environmental benefits
    - Tracks community satisfaction
    - Monitors safety metrics
    
    ### Using the System
    
    1. Complete assessments regularly
    2. Review dashboard metrics
    3. Generate and save reports
    4. Track trends over time
    
    ### Best Practices
    
    - Conduct assessments at consistent intervals
    - Document all observations
    - Include photos when possible
    - Follow up on maintenance needs
    """)
