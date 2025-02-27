import streamlit as st
from components.forms import (
    condition_assessment_form,
    functionality_assessment_form,
    time_effectiveness_form,
    cost_effectiveness_form,
    environmental_social_form
)
from utils.db import save_assessment
from utils.report import generate_report
from datetime import datetime

def show():
    st.title("Infrastructure Assessment")

    # Create tabs for different assessment categories
    tabs = st.tabs([
        "Condition",
        "Functionality",
        "Time-Effectiveness",
        "Cost-Effectiveness",
        "Environmental/Social"
    ])

    with tabs[0]:
        condition_data = condition_assessment_form()

    with tabs[1]:
        functionality_data = functionality_assessment_form()

    with tabs[2]:
        time_data = time_effectiveness_form()

    with tabs[3]:
        cost_data = cost_effectiveness_form()

    with tabs[4]:
        env_social_data = environmental_social_form()

    if st.button("Save Assessment"):
        assessment_data = {
            "user_id": st.session_state.user_id,
            "timestamp": datetime.utcnow(),
            "condition": condition_data,
            "functionality": functionality_data,
            "time_effectiveness": time_data,
            "cost_effectiveness": cost_data,
            "environmental_social": env_social_data
        }

        try:
            # Save to database
            assessment_id = save_assessment(assessment_data)
            st.success("Assessment saved successfully!")

            # Generate report
            report_buffer = generate_report(assessment_data)

            # Offer report download
            st.download_button(
                label="Download Assessment Report",
                data=report_buffer,
                file_name=f"assessment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf"
            )
        except Exception as e:
            st.error(f"Failed to save assessment: {str(e)}")