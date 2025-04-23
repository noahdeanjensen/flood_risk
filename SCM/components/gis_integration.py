import geopandas as gpd
import folium
from shapely.geometry import Point, Polygon
import streamlit as st
from streamlit_folium import folium_static
import json
from typing import List, Dict, Any

class GISManager:
    def __init__(self):
        self.infrastructure_layers = {}
        
    def add_infrastructure_points(self, points_data: List[Dict[Any, Any]], layer_name: str = "Infrastructure"):
        """Convert infrastructure points to GeoDataFrame"""
        geometry = [Point(p['longitude'], p['latitude']) for p in points_data]
        gdf = gpd.GeoDataFrame(points_data, geometry=geometry)
        self.infrastructure_layers[layer_name] = gdf
        return gdf

    def create_infrastructure_map(self, center_lat: float = 39.8283, center_lon: float = -98.5795, zoom: int = 4):
        """Create a Folium map with infrastructure layers"""
        m = folium.Map(location=[center_lat, center_lon], zoom_start=zoom)
        
        # Add base layers
        folium.TileLayer('openstreetmap').add_to(m)
        folium.TileLayer('cartodbpositron', name='Light Mode').add_to(m)
        folium.TileLayer('cartodbdark_matter', name='Dark Mode').add_to(m)
        
        # Add infrastructure layers
        for layer_name, gdf in self.infrastructure_layers.items():
            feature_group = folium.FeatureGroup(name=layer_name)
            
            for idx, row in gdf.iterrows():
                # Create popup content
                popup_content = f"""
                <div style='width: 200px'>
                    <h4>{row['name']}</h4>
                    <p><b>Type:</b> {row['type']}</p>
                    <p><b>Age:</b> {row['age']} years</p>
                    <p><b>Last Maintenance:</b> {row['last_maintenance_days']} days ago</p>
                </div>
                """
                
                # Add marker with custom icon based on type
                icon_color = self._get_status_color(row['age'], row['last_maintenance_days'])
                folium.CircleMarker(
                    location=[row['latitude'], row['longitude']],
                    radius=8,
                    popup=folium.Popup(popup_content, max_width=300),
                    color=icon_color,
                    fill=True,
                    fill_color=icon_color
                ).add_to(feature_group)
            
            feature_group.add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        return m

    def _get_status_color(self, age: int, last_maintenance_days: int) -> str:
        """Determine infrastructure point status color based on age and maintenance"""
        if age > 20 or last_maintenance_days > 365:
            return 'red'
        elif age > 10 or last_maintenance_days > 180:
            return 'orange'
        return 'green'

    def export_geojson(self, layer_name: str) -> dict:
        """Export a layer as GeoJSON"""
        if layer_name in self.infrastructure_layers:
            return json.loads(self.infrastructure_layers[layer_name].to_json())
        return {}

def show_gis_dashboard(assessment_data: dict):
    """Display GIS dashboard with infrastructure data"""
    st.subheader("Infrastructure GIS View")
    
    # Initialize GIS manager
    gis_manager = GISManager()
    
    if 'infrastructure_points' in assessment_data:
        # Add infrastructure points to GIS manager
        gis_manager.add_infrastructure_points(assessment_data['infrastructure_points'])
        
        # Create map centered on first point
        first_point = assessment_data['infrastructure_points'][0]
        map_center = [first_point['latitude'], first_point['longitude']]
        
        # Create and display map
        infrastructure_map = gis_manager.create_infrastructure_map(
            center_lat=map_center[0],
            center_lon=map_center[1],
            zoom=12
        )
        
        # Display map in Streamlit
        folium_static(infrastructure_map)
        
        # Add export option
        if st.button("Export Infrastructure Data as GeoJSON"):
            geojson_data = gis_manager.export_geojson("Infrastructure")
            st.download_button(
                "Download GeoJSON",
                data=json.dumps(geojson_data, indent=2),
                file_name="infrastructure.geojson",
                mime="application/json"
            )
    else:
        st.info("No infrastructure points available for GIS visualization")
