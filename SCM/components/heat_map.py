import streamlit as st
import folium
from streamlit_folium import folium_static
import json
from branca.colormap import LinearColormap

def create_risk_heat_map(assessment_data=None, center=[40.7128, -74.0060]):
    """
    Create an interactive heat map showing infrastructure risk levels
    Default center is New York City coordinates
    """
    # Create base map
    m = folium.Map(location=center, zoom_start=12)
    
    # Create color scale for risk levels
    colormap = LinearColormap(
        colors=['green', 'yellow', 'orange', 'red'],
        vmin=0,
        vmax=10,
        caption='Infrastructure Risk Level'
    )
    
    if assessment_data:
        # Extract risk levels from assessment data
        risk_levels = calculate_risk_levels(assessment_data)
        
        # Add markers for each infrastructure point
        for point in risk_levels:
            folium.CircleMarker(
                location=[point['lat'], point['lng']],
                radius=15,
                popup=f"""
                    <b>{point['name']}</b><br>
                    Risk Level: {point['risk_level']}/10<br>
                    Status: {point['status']}
                """,
                color=colormap(point['risk_level']),
                fill=True,
                fill_color=colormap(point['risk_level'])
            ).add_to(m)
    
    # Add the colormap to the map
    colormap.add_to(m)
    
    return m

def calculate_risk_levels(assessment_data):
    """Calculate risk levels from assessment data"""
    # Example risk calculation - this should be customized based on your needs
    points = []
    
    if 'infrastructure_points' in assessment_data:
        for point in assessment_data['infrastructure_points']:
            risk_level = calculate_point_risk(point, assessment_data)
            points.append({
                'lat': point['latitude'],
                'lng': point['longitude'],
                'name': point['name'],
                'risk_level': risk_level,
                'status': get_risk_status(risk_level)
            })
    
    return points

def calculate_point_risk(point, assessment_data):
    """Calculate risk level for a specific infrastructure point"""
    # Example risk calculation using assessment metrics
    risk_factors = {
        'condition': assessment_data['condition']['stormwaterHydraulicAssetCondition']['damageLevels'].get(point['type'], 'low'),
        'age': point.get('age', 0),
        'maintenance': point.get('last_maintenance_days', 365)
    }
    
    # Convert text-based damage levels to numbers
    damage_scores = {'low': 2, 'moderate': 5, 'high': 8}
    
    # Calculate base risk from condition
    risk = damage_scores[risk_factors['condition']]
    
    # Adjust for age (assume 50 years is maximum age)
    age_factor = min(risk_factors['age'] / 50, 1) * 2
    
    # Adjust for maintenance (assume 365 days without maintenance is maximum)
    maintenance_factor = min(risk_factors['maintenance'] / 365, 1) * 2
    
    final_risk = min((risk + age_factor + maintenance_factor) / 1.2, 10)
    return round(final_risk, 1)

def get_risk_status(risk_level):
    """Get text status based on risk level"""
    if risk_level >= 8:
        return "Critical - Immediate Action Required"
    elif risk_level >= 6:
        return "High Risk - Priority Maintenance"
    elif risk_level >= 4:
        return "Moderate Risk - Regular Monitoring"
    else:
        return "Low Risk - Routine Maintenance"
