import streamlit as st
from utils.db import get_assessments
from components.charts import create_radar_chart, create_trend_chart
import json

def calculate_overall_score(assessment_data):
    """Calculate overall infrastructure score (0-10)"""
    try:
        scores = {
            'condition': {
                'weight': 0.3,
                'value': sum(1 if v == "low" else 2 if v == "moderate" else 3 
                           for v in assessment_data['condition']['stormwaterHydraulicAssetCondition']['damageLevels'].values()) / (3 * len(assessment_data['condition']['stormwaterHydraulicAssetCondition']['damageLevels']))
            },
            'functionality': {
                'weight': 0.2,
                'value': (assessment_data['functionality']['hydraulicPerformance']['flowAttenuation'] + 
                         assessment_data['functionality']['hydraulicPerformance']['volumeReduction']) / 200
            },
            'time_effectiveness': {
                'weight': 0.15,
                'value': min(assessment_data['time_effectiveness']['lifespan'] / 50, 1.0)
            },
            'cost_effectiveness': {
                'weight': 0.15,
                'value': min((assessment_data['cost_effectiveness']['roi'] + 100) / 200, 1.0)
            },
            'environmental_social': {
                'weight': 0.2,
                'value': (assessment_data['environmental_social']['pollutantConcentrationReduction'] + 
                         assessment_data['environmental_social']['customerSatisfaction'] * 10) / 200
            }
        }

        overall_score = sum(score['weight'] * score['value'] * 10 for score in scores.values())
        return round(overall_score, 1)
    except Exception:
        return 5.0  # Default score if calculation fails

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
        try:
            latest_assessment = json.loads(assessments[0]['data'])
            latest_score = calculate_overall_score(latest_assessment)
            st.metric("Latest Infrastructure Score", f"{latest_score}/10")
        except Exception as e:
            st.metric("Latest Infrastructure Score", "N/A")

    with col3:
        try:
            avg_satisfaction = sum(float(a['data']['environmental_social']['customerSatisfaction']) 
                                 for a in assessments) / len(assessments)
            st.metric("Avg Satisfaction", f"{avg_satisfaction:.1f}/10")
        except Exception:
            st.metric("Avg Satisfaction", "N/A")

    # Charts
    st.subheader("Latest Assessment Overview")
    try:
        latest = json.loads(assessments[0]['data'])
        radar_chart = create_radar_chart(latest)
        st.plotly_chart(radar_chart)
    except Exception as e:
        st.error("Could not create radar chart for latest assessment")

    st.subheader("Assessment Trends")
    try:
        trend_data = [{
            'date': a['timestamp'],
            'overall_score': calculate_overall_score(json.loads(a['data']))
        } for a in assessments]
        trend_chart = create_trend_chart(trend_data)
        st.plotly_chart(trend_chart)
    except Exception as e:
        st.error("Could not create trend chart")