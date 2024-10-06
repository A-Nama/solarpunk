import requests

# Function to fetch GLOBE data dynamically based on lat, lon, and protocols
def fetch_globe_data(lat, lon, start_date, end_date, protocol):
    """
    Fetch environmental data from the GLOBE API based on latitude, longitude, and date range.
    
    Parameters:
        lat (float): Latitude of the location.
        lon (float): Longitude of the location.
        start_date (str): Start date for data in the format YYYY-MM-DD.
        end_date (str): End date for data in the format YYYY-MM-DD.
        protocol (str): The protocol for which data is fetched ('air_temperature', 'precipitation', 'vegetation').

    Returns:
        dict: Environmental data fetched from the GLOBE API.
    """
    
    # Define the base URL
    base_url = f"https://api.globe.gov/search/v1/measurement/protocol/{protocol}/measureddates"
    
    # Set query parameters
    params = {
        'startdate': start_date,
        'enddate': end_date,
        'latitude': lat,
        'longitude': lon,
        'geojson': 'FALSE'
    }
    
    try:
        # Make the request to GLOBE API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()

        if 'results' in data and data['results']:
            # Extract relevant data points from the response, depending on the protocol
            if protocol == 'air_temperature':
                return {'air_temperature': [d['measurement']['airTemperature'] for d in data['results'] if 'measurement' in d and 'airTemperature' in d['measurement']]}
            elif protocol == 'precipitation':
                return {'precipitation': [d['measurement']['precipitation'] for d in data['results'] if 'measurement' in d and 'precipitation' in d['measurement']]}
            elif protocol == 'vegetation':
                return {'vegetation_cover': [d['measurement']['landCover'] for d in data['results'] if 'measurement' in d and 'landCover' in d['measurement']]}
        else:
            return {}
    except requests.RequestException as e:
        print(f"Error fetching data from GLOBE API: {e}")
        return {}