import streamlit as st
from utils.db import get_assessments
from components.charts import create_radar_chart, create_trend_chart

def show():
    st.title("Dashboard")
    
    # Get user's assessments
    assessments = get_assessments(st.session_state.user_id)
    
    if not assessments:
        st.warning("No assessments found. Please complete an assessment first.")
        return
    
    # Overview metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Assessments", len(assessments))
    
    with col2:
        avg_condition = sum(a['condition']['damage_levels']['Pipes'] 
                          for a in assessments) / len(assessments)
        st.metric("Average Condition", f"{avg_condition:.1f}/10")
    
    with col3:
        avg_satisfaction = sum(a['environmental_social']['satisfaction'] 
                             for a in assessments) / len(assessments)
        st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}/10")
    
    # Charts
    st.subheader("Latest Assessment Overview")
    latest = assessments[-1]
    radar_chart = create_radar_chart(latest)
    st.plotly_chart(radar_chart)
    
    st.subheader("Assessment Trends")
    trend_chart = create_trend_chart(assessments)
    st.plotly_chart(trend_chart)
