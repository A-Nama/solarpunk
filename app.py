import streamlit as st
from globe_data import fetch_globe_data
from game_logic import (
    initialize_ecosystem,
    simulate_solarpunk_ecosystem,
    perform_action,
    calculate_score,
    get_ecosystem_status
)
from visualization import plot_solarpunk_ecosystem

# Initialize session state for ecosystem and game
if 'ecosystem' not in st.session_state:
    st.session_state.ecosystem = None
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'selected_plot_type' not in st.session_state:
    st.session_state.selected_plot_type = "Default Community" 

# Function to set background based on selected community type
def set_background(plot_type):
    backgrounds = {
        "Forest Village": "https://i.imgur.com/WpPHn5Y.jpeg",
        "Solar City": "https://i.imgur.com/BG8t66L.jpeg",
        "Urban Eco-Hub": "https://i.imgur.com/mkKx43m.jpeg",
        "Default Community": "https://imgur.com/dAw9501"
    }
    background_image = backgrounds.get(plot_type, backgrounds["Default Community"])
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{background_image}');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            color: white;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Title and Introduction
st.title("🌞 Solarpunk World 🌱")
st.subheader("Building a Better, Sustainable Future Through Harmony with Nature and Technology")

# Display the location input form if the game has not started
if not st.session_state.game_started:
    # Choose Eco-Community
    st.markdown("### Choose your Eco-Community:")
    plot_type = st.selectbox("Choose your community type", ["Forest Village", "Solar City", "Urban Eco-Hub"], key='plot_selector')

    # User input for latitude and longitude
    st.markdown("### Enter your location:")
    latitude = st.number_input("Latitude:", format="%.6f", value=19.9312)  # Default to Kochi
    longitude = st.number_input("Longitude:", format="%.6f", value=76.2673)

    if st.button("Start Game"):
        # Initialize the ecosystem and start the game
        st.session_state.ecosystem = initialize_ecosystem(plot_type)
        st.session_state.plot_type = plot_type
        st.session_state.latitude = latitude
        st.session_state.longitude = longitude
        st.session_state.selected_plot_type = plot_type  # Save selected plot type
        st.session_state.game_started = True
        st.rerun()  # Clear page and simulate "new page"
else:
    # Proceed with the game and display the data visualization
    set_background(st.session_state.selected_plot_type)

    # Fetch real-time GLOBE data using user-entered location for air temperature, precipitation, and vegetation
    air_temp_data = fetch_globe_data(
        lat=st.session_state.latitude,
        lon=st.session_state.longitude,
        start_date="2024-10-01", 
        end_date="2024-10-05",
        protocol="air_temp_dailies"
    )
    
    precipitation_data = fetch_globe_data(
        lat=st.session_state.latitude,
        lon=st.session_state.longitude,
        start_date="2024-10-01", 
        end_date="2024-10-05",
        protocol="precipitations"
    )

    vegetation_data = fetch_globe_data(
        lat=st.session_state.latitude,
        lon=st.session_state.longitude,
        start_date="2024-10-01", 
        end_date="2024-10-05",
        protocol="vegetation_covers"
    )

    # Combine fetched data into one dictionary
    globe_data = {
        **air_temp_data,
        **precipitation_data,
        **vegetation_data
    }

    if globe_data:
        st.write("🌍 Real-time Environmental Data (via GLOBE):", globe_data)
        # Simulate ecosystem changes based on GLOBE data
        st.session_state.ecosystem = simulate_solarpunk_ecosystem(st.session_state.ecosystem, globe_data)
    else:
        st.write("⚠️ Unable to fetch real-time environmental data.")

    # Visualize the Solarpunk-themed ecosystem
    plot_solarpunk_ecosystem(
        st.session_state.ecosystem['vegetation'],
        st.session_state.ecosystem['water'],
        st.session_state.ecosystem['energy']
    )

    # Display ecosystem status
    status = get_ecosystem_status(st.session_state.ecosystem)
    st.markdown(f"**Ecosystem Status:** {status}")

    # Player Interaction Section
    st.markdown("#### Actions to improve your ecosystem:")
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🌱 Plant Trees"):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, "Plant Trees")
            st.success("🌳 You've planted new trees to increase vegetation!")

    with col2:
        if st.button("⚡ Install Solar Panels"):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, "Install Solar Panels")
            st.success("🔋 Solar energy production has increased!")

    with col3:
        if st.button("💧 Build Rainwater Harvesting System"):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, "Build Rainwater Harvesting System")
            st.success("🌧️ You've improved water management!")

    # Optional: Additional Actions
    st.markdown("#### Additional Actions:")
    col4, col5 = st.columns(2)

    with col4:
        if st.button("🌿 Upgrade to Vertical Gardens"):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, "Upgrade to Vertical Gardens")
            st.success("🌾 Vertical gardens have been established!")

    with col5:
        if st.button("💨 Implement Wind Turbines"):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, "Implement Wind Turbines")
            st.success("🌬️ Wind energy production has increased!")

    # Calculate and display score
    score = calculate_score(st.session_state.ecosystem)
    st.markdown(f"**Your Current Score:** {score}")

    # Display overall status
    st.markdown(f"**Ecosystem Status:** {status}")
