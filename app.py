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

# Apply custom CSS for Solarpunk visuals
st.markdown(
    """
    <style>
    body {
        background-image: url('https://your-solarpunk-background-image-url.com'); /* Replace with your Solarpunk background image URL */
        background-size: cover;
        color: #2c5f2d;  /* Earthy green font */
    }
    .stButton>button {
        background-color: #2c5f2d;  /* Button background - Deep green */
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #8AB17D;  /* Lighter green for hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title and Introduction
st.title("🌞 Solarpunk World 🌱")
st.subheader("Building a Better, Sustainable Future Through Harmony with Nature and Technology")

# Initialize session state for ecosystem
if 'ecosystem' not in st.session_state:
    st.session_state.ecosystem = {
        'vegetation': 50,
        'water': 50,
        'energy': 50,
        'biodiversity': 50,
        'sustainability': 50
    }
    st.session_state.plot_type = None

# Choose Eco-Community
st.markdown("### Choose your Eco-Community:")
plot_type = st.selectbox("Choose your community type", ["Forest Village", "Solar City", "Urban Eco-Hub"], key='plot_selector')

# User input for latitude and longitude
st.markdown("### Enter your location:")
latitude = st.number_input("Latitude:", format="%.6f", value=19.9312)  # Default to Kochi
longitude = st.number_input("Longitude:", format="%.6f", value=76.2673)  

if st.button("Start Game"):
    st.session_state.ecosystem = initialize_ecosystem(plot_type)
    st.session_state.plot_type = plot_type
    st.success(f"You have selected **{plot_type}**! ")
    st.rerun()

# Proceed only if the game has started
if st.session_state.plot_type:
    # Fetch real-time GLOBE data using user-entered location
    globe_data = fetch_globe_data(lat=latitude, lon=longitude, start_date="2024-10-01", end_date="2024-10-05")
    
    if globe_data:
        st.write("🌍 Real-time Environmental Data (via GLOBE):", globe_data)
        # Simulate ecosystem changes based on GLOBE data
        st.session_state.ecosystem = simulate_solarpunk_ecosystem(st.session_state.ecosystem, globe_data)
    else:
        st.write("⚠️ Unable to fetch real-time environmental data.")
    
    # Visualize the Solarpunk-themed ecosystem
    plot_solarpunk_ecosystem(st.session_state.ecosystem['vegetation'],
                             st.session_state.ecosystem['water'],
                             st.session_state.ecosystem['energy'])
    
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
