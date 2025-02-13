import os
import json
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

class ArcGISCorrector:
    def __init__(self):
        # Configure with your ArcGIS credentials
        self.gis = GIS(
            url="https://www.arcgis.com",
            api_key=os.getenv('ARCGIS_API_KEY')  # Store in environment variables
        )
        self.stormwater_service_url = "https://services.arcgis.com/.../Stormwater_Assets/FeatureServer/0"

    def fetch_asset_data(self, asset_id=None, geometry=None):
        """
        Fetch stormwater asset data from ArcGIS feature service
        Returns data in Django model-compatible format
        """
        try:
            layer = FeatureLayer(self.stormwater_service_url)
            query = "1=1"  # Default query to get all features
            
            if asset_id:
                query = f"OBJECTID = {asset_id}"
            elif geometry:
                query += f" AND geometry intersects {geometry.wkt}"

            features = layer.query(where=query).features
            
            if features:
                return self._format_feature(features[0])
            
            return None
            
        except Exception as e:
            print(f"ArcGIS API Error: {str(e)}")
            return None

    def _format_feature(self, feature):
        """Convert ArcGIS feature to our model format"""
        attributes = feature.attributes
        geometry = feature.geometry
        
        return {
            'asset_id': attributes.get('OBJECTID'),
            'geometry': json.dumps(geometry),
            'pipe_diameter': attributes.get('DIAMETER'),
            'material': attributes.get('MATERIAL'),
            'condition': attributes.get('CONDITION_SCORE'),
            'last_inspected': attributes.get('LAST_INSP_DATE'),
            'risk_score': self._calculate_risk_score(attributes)
        }

    def _calculate_risk_score(self, attributes):
        """Simple risk scoring algorithm"""
        base_score = (
            (attributes.get('CONDITION_SCORE', 0) * 0.6) +
            (attributes.get('AGE', 0) * 0.3) +
            (attributes.get('FLOOD_HISTORY', 0) * 0.1)
        )
        return min(max(base_score, 0), 100)

# Example usage:
# corrector = ArcGISCorrector()
# asset_data = corrector.fetch_asset_data(asset_id=123)