# game_logic.py

def initialize_ecosystem(plot_type):
    """
    Initialize the ecosystem parameters based on the selected plot type.
    
    Parameters:
        plot_type (str): The type of eco-community selected by the player.
    
    Returns:
        dict: A dictionary containing initial ecosystem parameters.
    """
    # Base values for all communities
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
        globe_data (dict): Real-time environmental data fetched from GLOBE API.
    
    Returns:
        dict: Updated ecosystem parameters.
    """
    # Example: Adjust vegetation and water based on air temperature
    if globe_data and 'air_temperature' in globe_data and globe_data['air_temperature']:
        # Use the latest air temperature data
        air_temp = globe_data['air_temperature'][-1]  # Assuming latest is last
        if air_temp > 35:
            ecosystem['vegetation'] -= 10  # High temperature reduces vegetation
            ecosystem['water'] -= 5       # Increased evaporation
            ecosystem['energy'] += 5      # More energy needed for cooling
        elif air_temp < 15:
            ecosystem['vegetation'] -= 5   # Cold affects plant growth
            ecosystem['water'] += 5        # Less evaporation
            ecosystem['energy'] -= 5       # Less energy needed for cooling
        else:
            ecosystem['vegetation'] += 5   # Favorable temperatures boost vegetation
            ecosystem['water'] += 2        # Normal evaporation
            ecosystem['energy'] += 2       # Normal energy usage
    
    # Adjust based on precipitation data
    if globe_data and 'precipitation' in globe_data and globe_data['precipitation']:
        precipitation = globe_data['precipitation'][-1]  # Latest precipitation
        if precipitation > 100:
            ecosystem['water'] += 20    # Abundant water
            ecosystem['sustainability'] += 5  # Improved water management
        elif precipitation < 20:
            ecosystem['water'] -= 10    # Water scarcity
            ecosystem['sustainability'] -= 5  # Strain on resources
        else:
            ecosystem['water'] += 5     # Moderate precipitation
    
    # Adjust based on cloud coverage
    if globe_data and 'cloud_coverage' in globe_data and globe_data['cloud_coverage']:
        cloud_cover = globe_data['cloud_coverage'][-1]  # Latest cloud cover
        if cloud_cover > 80:
            ecosystem['energy'] -= 10  # Less solar energy
            ecosystem['sustainability'] -= 5
        elif cloud_cover < 20:
            ecosystem['energy'] += 10  # More solar energy
            ecosystem['sustainability'] += 5
        else:
            ecosystem['energy'] += 2    # Slight variation in energy
    
    # Ensure parameters stay within 0-100 range
    for key in ecosystem:
        ecosystem[key] = max(0, min(100, ecosystem[key]))
    
    return ecosystem

def perform_action(ecosystem, action):
    """
    Update the ecosystem based on the player's action.
    
    Parameters:
        ecosystem (dict): Current state of the ecosystem.
        action (str): The action performed by the player.
    
    Returns:
        dict: Updated ecosystem parameters.
    """
    if action == "Plant Trees":
        ecosystem['vegetation'] += 10
        ecosystem['biodiversity'] += 5
        ecosystem['sustainability'] += 5
    elif action == "Install Solar Panels":
        ecosystem['energy'] += 15
        ecosystem['sustainability'] += 10
    elif action == "Build Rainwater Harvesting System":
        ecosystem['water'] += 15
        ecosystem['sustainability'] += 10
    elif action == "Upgrade to Vertical Gardens":
        ecosystem['vegetation'] += 15
        ecosystem['biodiversity'] += 10
        ecosystem['sustainability'] += 10
    elif action == "Implement Wind Turbines":
        ecosystem['energy'] += 20
        ecosystem['sustainability'] += 15
    elif action == "Establish Community Gardens":
        ecosystem['vegetation'] += 10
        ecosystem['biodiversity'] += 5
        ecosystem['sustainability'] += 5
    # Add more actions as needed
    
    # Ensure parameters stay within 0-100 range
    for key in ecosystem:
        ecosystem[key] = max(0, min(100, ecosystem[key]))
    
    return ecosystem

def calculate_score(ecosystem):
    """
    Calculate the player's score based on the current state of the ecosystem.
    
    Parameters:
        ecosystem (dict): Current state of the ecosystem.
    
    Returns:
        int: Calculated score.
    """
    # Example scoring: Sum of all parameters
    score = ecosystem['vegetation'] + ecosystem['water'] + ecosystem['energy'] + ecosystem['biodiversity'] + ecosystem['sustainability']
    return score

def get_ecosystem_status(ecosystem):
    """
    Provide a status report of the ecosystem based on its parameters.
    
    Parameters:
        ecosystem (dict): Current state of the ecosystem.
    
    Returns:
        str: Status message.
    """
    status = []
    if ecosystem['vegetation'] > 70:
        status.append("Thriving vegetation")
    elif ecosystem['vegetation'] < 30:
        status.append("Vegetation struggling")
    else:
        status.append("Vegetation stable")
    
    if ecosystem['water'] > 70:
        status.append("Water resources abundant")
    elif ecosystem['water'] < 30:
        status.append("Water resources scarce")
    else:
        status.append("Water resources stable")
    
    if ecosystem['energy'] > 70:
        status.append("High renewable energy production")
    elif ecosystem['energy'] < 30:
        status.append("Low renewable energy production")
    else:
        status.append("Renewable energy production stable")
    
    if ecosystem['biodiversity'] > 70:
        status.append("Rich biodiversity")
    elif ecosystem['biodiversity'] < 30:
        status.append("Biodiversity declining")
    else:
        status.append("Biodiversity stable")
    
    if ecosystem['sustainability'] > 70:
        status.append("Highly sustainable")
    elif ecosystem['sustainability'] < 30:
        status.append("Sustainability efforts needed")
    else:
        status.append("Sustainability efforts stable")
    
    return ", ".join(status)
