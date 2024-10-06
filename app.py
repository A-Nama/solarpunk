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

# CSS to style the page and position the logo
st.markdown(""" 
    <style>
    .logo {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 100px; /* Adjust size if needed */
    }
    </style>
""", unsafe_allow_html=True)

# Add the logo from an external hosted link 
st.markdown(
    f"""
    <div class="logo">
        <img src="https://i.imgur.com/Odnb5GX.png" alt="Solarpunk_Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# Initialize session state for ecosystem and game
if 'ecosystem' not in st.session_state:
    st.session_state.ecosystem = None
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
if 'selected_plot_type' not in st.session_state:
    st.session_state.selected_plot_type = "Default Community" 
if 'plot_type' not in st.session_state:
    st.session_state.plot_type = "Default Community"


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

    # User input for country code
    st.markdown("### Enter your country code:")
    country_code = st.text_input("Enter Country Code (e.g., IND)", value="USA")  # Default set as USA

    # User input for date
    start_date = st.date_input("Start Date").strftime("%Y-%m-%d")
    end_date = st.date_input("End Date").strftime("%Y-%m-%d")

    if st.button("Start Game"):
        # Initialize the ecosystem and start the game
        st.session_state.ecosystem = initialize_ecosystem(plot_type)
        st.session_state.plot_type = plot_type
        st.session_state.start_date = start_date  # Save start date
        st.session_state.end_date = end_date #Save end date
        st.session_state.country_code = country_code  # Save country code
        st.session_state.selected_plot_type = plot_type  # Save selected plot type
        st.session_state.game_started = True
        st.rerun()  # Clear page and simulate "new page"
else:
    # Proceed with the game and display the data visualization
    set_background(st.session_state.selected_plot_type)

    # Retrieve the saved start date and country code
    start_date = st.session_state.start_date
    end_date = st.session_state.end_date
    country_code = st.session_state.country_code

    # Fetch real-time GLOBE data using user-entered country code for air temperature, precipitation, and vegetation
    air_temp_data = fetch_globe_data(
        protocol="air_temp_dailies",
        country_code=country_code,
        start_date=start_date,  # Use user-provided start date
        end_date=end_date
    )
    
    precipitation_data = fetch_globe_data(
        protocol="precipitations",
        country_code=country_code,
        start_date=start_date,  # Use user-provided start date
        end_date=end_date
    )

    vegetation_data = fetch_globe_data(
        protocol="vegatation_covers",
        country_code=country_code,
        start_date=start_date,  # Use user-provided start date
        end_date=end_date
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

# Get the selected plot type from session state
plot_type = st.session_state.plot_type

# Define the community actions for Forest Village, Solar City, and Urban Eco-Hub
community_actions = {
    "Forest Village": ["🌱 Organic farming", "🍃 Create Biogas from Compost", "💧 Build Rainwater Harvesting System", "🚰 Reuse grey water", "♻️ Use renewable energy", "🚲 Walk or Cycle as much as possible"],
    "Solar City": ["⚡ Install Solar Panels", "🔋 Use Hydrogen as fuel", "🌳 Plant trees on sidewalk", "🚗 Promote Electric Vehicles", "🌆 Build indoor gardens", "💡 Proper waste management"],
    "Urban Eco-Hub": ["🏙️ Install Vertical Gardens", "🚰 Waste water management", "♻️ Implement Zero-waste Policy", "🔋 Use biogas", "🏡 Install green roof", "🌱 Community gardening"],
}

# Display community-specific actions for the user
selected_actions = community_actions.get(st.session_state.plot_type)  

# Dynamically create buttons for the selected actions
col1, col2, col3 = st.columns(3)

if selected_actions:
    with col1:
        if st.button(selected_actions[0]):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, selected_actions[0], plot_type)
            st.success(f"{selected_actions[0]} performed!")

    with col2:
        if st.button(selected_actions[1]):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, selected_actions[1], plot_type)
            st.success(f"{selected_actions[1]} performed!")

    with col3:
        if st.button(selected_actions[2]):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, selected_actions[2], plot_type)
            st.success(f"{selected_actions[2]} performed!")

    # Repeat the same for more actions 
    col4, col5, col6 = st.columns(3)

    with col4:
        if st.button(selected_actions[3]):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, selected_actions[3], plot_type)
            st.success(f"{selected_actions[3]} performed!")

    with col5:
        if st.button(selected_actions[4]):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, selected_actions[4], plot_type)
            st.success(f"{selected_actions[4]} performed!")

    with col6:
        if st.button(selected_actions[5]):
            st.session_state.ecosystem = perform_action(st.session_state.ecosystem, selected_actions[5], plot_type)
            st.success(f"{selected_actions[5]} performed!")


    # Calculate and display score
    score = calculate_score(st.session_state.ecosystem)
    st.markdown(f"**Your Current Score:** {score}")

    # Display overall status
    st.markdown(f"**Ecosystem Status:** {status}")
