import requests

# GLOBE API endpoint for fetching environmental data
GLOBE_API_URL = "https://api.globe.gov/search/v1/measurements"

# Function to fetch GLOBE data based on user location or specific parameters
def fetch_globe_data(lat=None, lon=None, start_date=None, end_date=None):
    """
    Fetch GLOBE data from the GLOBE API based on the user's location and date range.
    
    Parameters:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        start_date (str): Start date for the query (YYYY-MM-DD).
        end_date (str): End date for the query (YYYY-MM-DD).
        
    Returns:
        dict: Dictionary of relevant environmental data (air_temperature, precipitation, cloud_coverage).
    """
    
    # Set up parameters for the API request
    params = {
        'latitude': lat,           # Optional: Latitude for the player's location
        'longitude': lon,          # Optional: Longitude for the player's location
        'startdate': start_date,   # Optional: Start date for the data range
        'enddate': end_date,       # Optional: End date for the data range
        'offset': 0,               # Start from the first record
        'limit': 10,               # Limit the data to a manageable size
        'geojson': 'false'         # We're not interested in geojson, just the raw data
    }

    try:
        # Send request to the GLOBE API
        response = requests.get(GLOBE_API_URL, params=params)
        response.raise_for_status()  # Raise an exception for any HTTP errors
        data = response.json()       # Parse the JSON response

        # Example structure of the returned data:
        measurements = data.get("results", [])

        # Extract relevant data fields for ecosystem simulation
        relevant_data = {
            'air_temperature': [],
            'precipitation': [],
            'cloud_coverage': [],
        }

        # Iterate over the results and extract important environmental data
        for measurement in measurements:
            if 'airTemperature' in measurement:
                relevant_data['air_temperature'].append(measurement['airTemperature'])
            if 'precipitation' in measurement:
                relevant_data['precipitation'].append(measurement['precipitation'])
            if 'cloudCover' in measurement:
                relevant_data['cloud_coverage'].append(measurement['cloudCover'])

        # Return the extracted data as a dictionary
        return relevant_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching GLOBE data: {e}")
        return None
