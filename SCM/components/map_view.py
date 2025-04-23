import folium
import streamlit as st
from streamlit_folium import folium_static
import logging

logger = logging.getLogger(__name__)

def create_infrastructure_map(assessment_data):
    """Create a Folium map showing infrastructure points"""
    try:
        # Default center (US center)
        center_lat, center_lon = 39.8283, -98.5795
        
        # Get infrastructure points
        points = assessment_data.get('infrastructure_points', [])
        if points:
            # Center map on first point
            center_lat = points[0].get('latitude', center_lat)
            center_lon = points[0].get('longitude', center_lon)

        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=12,
            tiles="OpenStreetMap"
        )

        # Add points to map
        for point in points:
            # Calculate status color based on age and maintenance
            age = point.get('age', 0)
            maintenance_days = point.get('last_maintenance_days', 0)
            
            if age > 20 or maintenance_days > 365:
                color = 'red'
            elif age > 10 or maintenance_days > 180:
                color = 'orange'
            else:
                color = 'green'

            # Create popup content
            popup_html = f"""
            <div style='width: 200px'>
                <h4>{point.get('name', 'Unknown')}</h4>
                <p><b>Type:</b> {point.get('type', 'N/A')}</p>
                <p><b>Age:</b> {age} years</p>
                <p><b>Last Maintenance:</b> {maintenance_days} days ago</p>
                <p><b>Status:</b> <span style='color: {color}'>●</span></p>
            </div>
            """

            # Add marker
            folium.CircleMarker(
                location=[point.get('latitude'), point.get('longitude')],
                radius=8,
                popup=folium.Popup(popup_html, max_width=300),
                color=color,
                fill=True,
                fill_color=color
            ).add_to(m)

        return m
    except Exception as e:
        logger.error(f"Error creating map: {e}", exc_info=True)
        return None

def show_infrastructure_map(assessment_data):
    """Display infrastructure map in Streamlit"""
    try:
        map_obj = create_infrastructure_map(assessment_data)
        if map_obj:
            st.subheader("Infrastructure Map")
            folium_static(map_obj)
        else:
            st.warning("Could not create infrastructure map")
    except Exception as e:
        logger.error(f"Error displaying map: {e}", exc_info=True)
        st.error("Unable to display infrastructure map")
