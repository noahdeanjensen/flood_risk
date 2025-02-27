import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_radar_chart(assessment_data):
    categories = ['Condition', 'Functionality', 'Time-Effectiveness', 
                 'Cost-Effectiveness', 'Environmental']
    
    values = [
        assessment_data['condition']['damage_levels']['Pipes'],
        assessment_data['functionality']['flow_attenuation'],
        assessment_data['time_effectiveness']['lifespan'],
        100 - (assessment_data['cost_effectiveness']['operational'] / 1000),
        assessment_data['environmental_social']['pollutant_reduction']
    ]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=False
    )
    
    return fig

def create_trend_chart(assessments):
    df = pd.DataFrame(assessments)
    fig = px.line(df, x='date', y='overall_score', title='Assessment Trends')
    return fig
