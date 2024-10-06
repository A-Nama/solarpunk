import requests

# Function to fetch GLOBE data dynamically based on protocol, country code, and date
def fetch_globe_data(start_date, end_date, country_code, protocol):
    """
    Fetch environmental data from the GLOBE API based on the date range and country code.
    
    Parameters:
        start_date (str): Start date for data in the format YYYY-MM-DD.
        end_date (str): End date for data in the format YYYY-MM-DD.
        country_code (str): The country code for which data is fetched.
        protocol (str): The protocol for which data is fetched ('air_temp_dailies', 'precipitations', 'vegetation_covers').

    Returns:
        dict: Environmental data fetched from the GLOBE API.
    """
    
    # Define the base URL
    base_url = f"https://api.globe.gov/search/v1/measurement/protocol/measureddate/country/"
    
    # Set query parameters
    params = {
        'protocols': protocol,
        'startdate': start_date,
        'enddate': end_date,
        'countrycode': country_code,
        'geojson': 'FALSE',
        'sample': 'TRUE'  # Add the sample parameter
    }
    
    try:
        # Make the request to GLOBE API
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        data = response.json()

        if 'results' in data and data['results']:
            if protocol == 'air_temps':
                return {'air_temperature': [d['data']['airtempsCurrentTemp'] for d in data['results'] if 'data' in d and 'airtempsCurrentTemp' in d['data']]}
            elif protocol == 'precipitation_monthlies':
                return {'precipitation': [d['data']['precipitationmonthliesLiquidAccumulationMm'] for d in data['results'] if 'data' in d and 'precipitationmonthliesLiquidAccumulationMm' in d['data']]}
            elif protocol == 'soil_phs':
                return {'soil_ph': [d['data']['soilphsPh'] for d in data['results'] if 'data' in d and 'soilphsPh' in d['data']]}
        else:
            return {}
    except requests.RequestException as e:
        print(f"Error fetching data from GLOBE API: {e}")
        return {}

