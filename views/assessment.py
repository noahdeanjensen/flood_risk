import streamlit as st
from components.forms import (
    condition_assessment_form,
    functionality_assessment_form,
    time_effectiveness_form,
    cost_effectiveness_form,
    environmental_social_form,
    infrastructure_location_form
)
from components.heat_map import create_risk_heat_map
from utils.db import save_assessment
from utils.report import generate_report
from datetime import datetime
from streamlit_folium import folium_static


def show():
    st.title("Infrastructure Assessment")

    # Create tabs for different assessment categories
    tabs = st.tabs([
        "Infrastructure Points",
        "Condition",
        "Functionality",
        "Time-Effectiveness",
        "Cost-Effectiveness",
        "Environmental/Social",
        "Risk Map"
    ])

    with tabs[0]:
        infrastructure_data = infrastructure_location_form()

    with tabs[1]:
        condition_data = condition_assessment_form()

    with tabs[2]:
        functionality_data = functionality_assessment_form()

    with tabs[3]:
        time_data = time_effectiveness_form()

    with tabs[4]:
        cost_data = cost_effectiveness_form()

    with tabs[5]:
        env_social_data = environmental_social_form()

    with tabs[6]:
        st.subheader("Infrastructure Risk Heat Map")
        current_assessment = {
            'infrastructure_points': st.session_state.get('infrastructure_points', []),
            'condition': condition_data,
            'functionality': functionality_data,
            'time_effectiveness': time_data,
            'cost_effectiveness': cost_data,
            'environmental_social': env_social_data
        }
        if current_assessment['infrastructure_points']:
            risk_map = create_risk_heat_map(current_assessment)
            folium_static(risk_map)
        else:
            st.info("Add infrastructure points in the 'Infrastructure Points' tab to view the risk heat map")

    if st.button("Save Assessment"):
        assessment_data = {
            "user_id": st.session_state.user_id,
            "timestamp": datetime.utcnow(),
            "infrastructure_points": infrastructure_data['infrastructure_points'],
            "condition": condition_data,
            "functionality": functionality_data,
            "time_effectiveness": time_data,
            "cost_effectiveness": cost_data,
            "environmental_social": env_social_data
        }

        try:
            assessment_id = save_assessment(assessment_data)
            st.success("Assessment saved successfully!")

            report_buffer = generate_report(assessment_data)

            st.download_button(
                label="Download Assessment Report",
                data=report_buffer,
                file_name=f"assessment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Failed to save assessment: {str(e)}")