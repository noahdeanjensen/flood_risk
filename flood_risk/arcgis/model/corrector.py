import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import joblib
from arcgis.gis import GIS
from arcgis.geocoding import geocode

# Initialize ArcGIS
gis = GIS()

# Step 1: Web Scraping Functions
def search_web(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
    if results:
        return results[0].get_text()
    else:
        return None

def extract_numerical_value(text):
    numbers = re.findall(r'\d+\.?\d*', text)
    if numbers:
        return float(numbers[0])
    else:
        return None

# Step 2: ArcGIS Search Function
def search_arcgis(query):
    geocode_result = geocode(query)
    if geocode_result:
        return geocode_result[0]['attributes']
    else:
        return None

# Step 3: Gather Data for a City
def gather_city_data(city):
    data = {}

    # Pipe Diameter
    query = f"standard pipe diameter for stormwater drainage in {city}"
    pipe_diameter_text = search_web(query)
    if not pipe_diameter_text:
        pipe_diameter_text = search_arcgis(query)
    data['pipe_diameter'] = extract_numerical_value(pipe_diameter_text)

    # Inspection Frequency
    query = f"routine inspection frequency for stormwater systems in {city}"
    inspection_frequency_text = search_web(query)
    if not inspection_frequency_text:
        inspection_frequency_text = search_arcgis(query)
    data['inspection_frequency'] = extract_numerical_value(inspection_frequency_text)

    # Damage Level (assume a scale of 1-3)
    query = f"stormwater infrastructure damage level in {city}"
    damage_level_text = search_web(query)
    if not damage_level_text:
        damage_level_text = search_arcgis(query)
    data['damage_level'] = extract_numerical_value(damage_level_text)

    # Flow Attenuation
    query = f"flow attenuation for stormwater systems in {city}"
    flow_attenuation_text = search_web(query)
    if not flow_attenuation_text:
        flow_attenuation_text = search_arcgis(query)
    data['flow_attenuation'] = extract_numerical_value(flow_attenuation_text)

    # Lifespan
    query = f"average lifespan of stormwater systems in {city}"
    lifespan_text = search_web(query)
    if not lifespan_text:
        lifespan_text = search_arcgis(query)
    data['lifespan'] = extract_numerical_value(lifespan_text)

    # Cost
    query = f"cost of stormwater system construction in {city}"
    cost_text = search_web(query)
    if not cost_text:
        cost_text = search_arcgis(query)
    data['cost'] = extract_numerical_value(cost_text)

    # Pollutant Concentration
    query = f"pollutant concentration in stormwater in {city}"
    pollutant_concentration_text = search_web(query)
    if not pollutant_concentration_text:
        pollutant_concentration_text = search_arcgis(query)
    data['pollutant_concentration'] = extract_numerical_value(pollutant_concentration_text)

    return data

# Step 4: Load the Model
def load_model():
    model = joblib.load('scm_model.pkl')
    scaler = joblib.load('scaler.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    return model, scaler, label_encoder

# Step 5: Prepare Input Data
def prepare_input_data(city_data):
    user_data = pd.DataFrame([city_data])
    user_data = scaler.transform(user_data)
    return user_data

# Step 6: Assess SCM
def assess_scm(user_data):
    prediction = model.predict(user_data)
    rating = label_encoder.inverse_transform(prediction)
    return rating[0]

# Step 7: Save Results to CSV
def save_to_csv(city_data, rating, filename='scm_ratings.csv'):
    city_data['rating'] = rating
    results_df = pd.DataFrame([city_data])
    results_df.to_csv(filename, index=False)
    print(f"Results saved to '{filename}'")

# Step 8: Main Workflow
if __name__ == '__main__':
    # Load the model
    model, scaler, label_encoder = load_model()

    # Get user input
    city = input("Enter the city name: ")

    # Gather data for the city
    city_data = gather_city_data(city)

    # Prepare input data
    user_data = prepare_input_data(city_data)

    # Generate rating
    rating = assess_scm(user_data)

    # Save results to CSV
    save_to_csv(city_data, rating)