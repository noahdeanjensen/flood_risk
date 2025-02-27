import streamlit as st

def show():
    st.title("Stormwater Infrastructure Assessment")
    
    st.markdown("""
    Welcome to the Stormwater Infrastructure Assessment System. This platform helps you:
    
    * Evaluate stormwater control infrastructure
    * Generate comprehensive assessment reports
    * Track and monitor infrastructure performance
    * Make data-driven decisions
    
    ### Getting Started
    
    1. Navigate to the Assessment section to start a new evaluation
    2. Use the Dashboard to view analytics and trends
    3. Check the Documentation for detailed guidance
    """)
    
    st.info("Please use the sidebar navigation to access different sections of the application.")
