import requests
from globe_data import fetch_globe_data  # Import the fetch_globe_data method

def initialize_ecosystem(plot_type):
    ecosystem = {
        'vegetation': 50,
        'water': 50,
        'energy': 50,
        'biodiversity': 50,
        'sustainability': 50
    }
    
    # Adjust initial parameters based on plot type
    if plot_type == "Forest Village":
        ecosystem['vegetation'] += 20
        ecosystem['water'] += 10
        ecosystem['energy'] -= 10
    elif plot_type == "Solar City":
        ecosystem['energy'] += 20
        ecosystem['water'] -= 10
        ecosystem['vegetation'] -= 10
    elif plot_type == "Urban Eco-Hub":
        ecosystem['sustainability'] += 15
        ecosystem['energy'] += 10
        ecosystem['water'] += 5
    
    return ecosystem

def simulate_solarpunk_ecosystem(ecosystem, globe_data):
    """
    Simulate the ecosystem changes based on real-time GLOBE data.
    
    Parameters:
        ecosystem (dict): Current state of the ecosystem.
        globe_data (dict): Environmental data fetched from the GLOBE API.
    
    Returns:
        dict: Updated ecosystem parameters.
    """
    # Check for valid globe_data input before processing
    if not globe_data:
        return ecosystem  # Return the current ecosystem if no globe data is provided

    # Extracting data for air temperature, precipitation, and vegetation cover from the GLOBE data
    air_temp_data = globe_data.get('air_temperature', {})
    precipitation_data = globe_data.get('precipitation', {})
    vegetation_data = globe_data.get('vegetation', {})

    # Adjust vegetation, water, and energy based on air temperature data
    if air_temp_data and 'measurements' in air_temp_data:
        air_temp = air_temp_data['measurements'][-1]  # Use the latest air temperature
        if air_temp > 35:
            ecosystem['vegetation'] -= 10
            ecosystem['water'] -= 5
            ecosystem['energy'] += 5
        elif air_temp < 15:
            ecosystem['vegetation'] -= 5
            ecosystem['water'] += 5
            ecosystem['energy'] -= 5
        else:
            ecosystem['vegetation'] += 5
            ecosystem['water'] += 2
            ecosystem['energy'] += 2

    # Adjust water and sustainability based on precipitation data
    if precipitation_data and 'measurements' in precipitation_data:
        precipitation = precipitation_data['measurements'][-1]  # Use the latest precipitation data
        if precipitation > 100:
            ecosystem['water'] += 20
            ecosystem['sustainability'] += 5
        elif precipitation < 20:
            ecosystem['water'] -= 10
            ecosystem['sustainability'] -= 5
        else:
            ecosystem['water'] += 5

    # Adjust vegetation based on vegetation cover data
    if vegetation_data and 'measurements' in vegetation_data:
        vegetation_cover = vegetation_data['measurements'][-1]  # Use the latest vegetation cover data
        if vegetation_cover < 30:
            ecosystem['vegetation'] -= 10
        elif vegetation_cover > 70:
            ecosystem['vegetation'] += 10
        else:
            ecosystem['vegetation'] += 5

    # Ensure ecosystem parameters stay within 0-100 range
    for key in ecosystem:
        ecosystem[key] = max(0, min(100, ecosystem[key]))
    
    return ecosystem


def perform_action(ecosystem, action):
    """
    Perform an action that modifies the ecosystem parameters.
    
    Parameters:
        ecosystem (dict): Current state of the ecosystem.
        action (str): The action to perform (e.g., "Plant Trees", "Install Solar Panels").
    
    Returns:
        dict: Updated ecosystem parameters after the action.
    """
    if action == "Plant Trees":
        ecosystem['vegetation'] += 10
    elif action == "Install Solar Panels":
        ecosystem['energy'] += 10
    elif action == "Build Rainwater Harvesting System":
        ecosystem['water'] += 10
    elif action == "Upgrade to Vertical Gardens":
        ecosystem['vegetation'] += 15
        ecosystem['sustainability'] += 5
    elif action == "Implement Wind Turbines":
        ecosystem['energy'] += 15
        ecosystem['sustainability'] += 5

    # Ensure parameters stay within 0-100 range after performing the action
    for key in ecosystem:
        ecosystem[key] = max(0, min(100, ecosystem[key]))

    return ecosystem

def calculate_score(ecosystem):
    """
    Calculate the score based on the current state of the ecosystem.
    
    Parameters:
        ecosystem (dict): Current state of the ecosystem.
    
    Returns:
        int: Score calculated based on ecosystem parameters.
    """
    score = (
        ecosystem['vegetation'] +
        ecosystem['water'] +
        ecosystem['energy'] +
        ecosystem['biodiversity'] +
        ecosystem['sustainability']
    ) // 5  # Average score
    return score

def get_ecosystem_status(ecosystem):
    """
    Get a textual status of the ecosystem based on its parameters.
    
    Parameters:
        ecosystem (dict): Current state of the ecosystem.
    
    Returns:
        str: Status message indicating the overall health of the ecosystem.
    """
    if ecosystem['sustainability'] > 80:
        return "Your ecosystem is thriving! 🌟"
    elif ecosystem['sustainability'] > 50:
        return "Your ecosystem is doing well. Keep it up! 👍"
    else:
        return "Your ecosystem needs attention! ⚠️"