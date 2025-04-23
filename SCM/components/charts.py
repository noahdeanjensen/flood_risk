import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_radar_chart(assessment_data):
    """Create a radar chart showing different aspects of the infrastructure assessment"""
    try:
        categories = ['Condition', 'Functionality', 'Time-Effectiveness', 
                     'Cost-Effectiveness', 'Environmental']

        values = [
            assessment_data['condition']['stormwaterHydraulicAssetCondition']['damageLevels'].get('pipes', 'moderate'),
            assessment_data['functionality']['hydraulicPerformance']['flowAttenuation'],
            assessment_data['time_effectiveness']['lifespan'],
            100 - (assessment_data['cost_effectiveness']['operationalCosts'] / 1000),
            assessment_data['environmental_social']['pollutantConcentrationReduction']
        ]

        # Convert text values to numeric
        values = [100 if v == 'high' else 50 if v == 'moderate' else 0 if v == 'low' else float(v) 
                 for v in values]

        fig = go.Figure(data=go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line=dict(color='rgb(31, 119, 180)'),
            fillcolor='rgba(31, 119, 180, 0.5)'
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )),
            showlegend=False,
            title="Infrastructure Assessment Radar"
        )

        return fig
    except Exception as e:
        # Return a simple empty figure if there's an error
        return go.Figure()

def create_trend_chart(assessments):
    """Create a line chart showing assessment trends over time"""
    try:
        df = pd.DataFrame(assessments)
        fig = px.line(
            df,
            x='date',
            y='overall_score',
            title='Assessment Score Trends',
            labels={'date': 'Assessment Date', 'overall_score': 'Overall Score'},
            line_shape='linear'
        )

        fig.update_layout(
            yaxis=dict(range=[0, 10]),
            hovermode='x unified'
        )

        return fig
    except Exception as e:
        return go.Figure()

def create_component_trend_chart(assessments, component):
    """Create a trend chart for a specific component"""
    try:
        data = []
        for assessment in assessments:
            if component in assessment['data']:
                data.append({
                    'date': assessment['timestamp'],
                    'value': assessment['data'][component].get('score', 0)
                })

        df = pd.DataFrame(data)
        fig = px.line(
            df,
            x='date',
            y='value',
            title=f'{component.title()} Trend',
            labels={'date': 'Date', 'value': 'Score'}
        )

        return fig
    except Exception as e:
        return go.Figure()