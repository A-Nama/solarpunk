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

# CSS for page style and logo positioning
st.markdown(""" 
    <style>
    .logo {
        position: absolute;
        top: 10px;
        right: 10px;
        width: 100px;
    }
    .outlined-text {
        color: white;
        text-shadow: 1px 1px 0px black, 1px -1px 0px black, -1px 1px 0px black, -1px -1px 0px black;
    }
    </style>
""", unsafe_allow_html=True)

# Add logo to page
st.markdown(
    """
    <div class="logo">
        <img src="https://i.imgur.com/Odnb5GX.png" alt="Solarpunk_Logo">
    </div>
    """,
    unsafe_allow_html=True
)

# Function to set background based on community selection
def set_background(plot_type):
    backgrounds = {
        "Forest Village": "https://i.imgur.com/BG8t66L.jpeg", 
        "Solar City": "https://i.imgur.com/WpPHn5Y.jpeg",
        "Urban Eco-Hub": "https://i.imgur.com/mkKx43m.jpeg"
    }
    background_image = backgrounds.get(plot_type, "https://i.imgur.com/dAw9501")
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

# Initial states for game stages and data management
if 'stage' not in st.session_state:
    st.session_state.stage = "pre-intro"

if 'ecosystem' not in st.session_state:
    st.session_state.ecosystem = None

if 'game_started' not in st.session_state:
    st.session_state.game_started = False

if 'selected_plot_type' not in st.session_state:
    st.session_state.selected_plot_type = "Default Community"

if 'plot_type' not in st.session_state:
    st.session_state.plot_type = "Default Community"

if 'score' not in st.session_state:
    st.session_state.score = 0

# Pre-intro stage: The "Start Simulation" button before playing the video
if st.session_state.stage == "pre-intro":
    st.markdown("<h3 class='outlined-text'>Ready to begin the Solarpunk journey?</h3>", unsafe_allow_html=True)
    
    if st.button("Start Simulation"):
        st.session_state.stage = "intro"
        st.rerun()

# Intro video stage: Play intro video and show another "Start" button
elif st.session_state.stage == "intro":
    st.video("https://youtu.be/GJN1Sa_peX0")
    
    if st.button("Start"):
        st.session_state.stage = "simulation"
        st.rerun()

# Simulation stage: Community selection and game start
elif st.session_state.stage == "simulation":
    st.markdown("<h3 class='outlined-text'>Choose your Eco-Community:</h3>", unsafe_allow_html=True)
    plot_type = st.selectbox("Choose your community type", ["Forest Village", "Solar City", "Urban Eco-Hub"], key='plot_selector')

    st.markdown("<h3 class='outlined-text'>Enter your country code:</h3>", unsafe_allow_html=True)
    country_code = st.text_input("Enter Country Code", value="USA")

    start_date = st.date_input("Start Date").strftime("%Y-%m-%d")
    end_date = st.date_input("End Date").strftime("%Y-%m-%d")

    if st.button("Start Game"):
        st.session_state.ecosystem = initialize_ecosystem(plot_type)
        st.session_state.plot_type = plot_type
        st.session_state.start_date = start_date
        st.session_state.end_date = end_date
        st.session_state.country_code = country_code
        st.session_state.selected_plot_type = plot_type
        st.session_state.game_started = True
        st.rerun()

# Actual game stage
if st.session_state.game_started:
    set_background(st.session_state.selected_plot_type)

    start_date = st.session_state.start_date
    end_date = st.session_state.end_date
    country_code = st.session_state.country_code

    # Fetch GLOBE data
    air_temp_data = fetch_globe_data(protocol="air_temps", country_code=country_code, start_date=start_date, end_date=end_date)
    precipitation_data = fetch_globe_data(protocol="precipitation_monthlies", country_code=country_code, start_date=start_date, end_date=end_date)
    soil_ph_data = fetch_globe_data(protocol="soil_phs", country_code=country_code, start_date=start_date, end_date=end_date)

    globe_data = {**air_temp_data, **precipitation_data, **soil_ph_data}

    if globe_data:
        st.write("<h3 class='outlined-text'>🌍 Real-time Environmental Data (via GLOBE):</h3>", unsafe_allow_html=True)
        st.write(globe_data)

        st.session_state.ecosystem = simulate_solarpunk_ecosystem(st.session_state.ecosystem, globe_data)
    else:
        st.write("<h3 class='outlined-text'>⚠️ Unable to fetch real-time environmental data.</h3>", unsafe_allow_html=True)

    plot_solarpunk_ecosystem(
        st.session_state.ecosystem['vegetation'],
        st.session_state.ecosystem['water'],
        st.session_state.ecosystem['weather']
    )

    status = get_ecosystem_status(st.session_state.ecosystem)
    st.markdown(f"<h3 class='outlined-text'>Ecosystem Status: {status}</h3>", unsafe_allow_html=True)

    # Display score
    st.markdown(f"<h3 class='outlined-text'>Current Score: {st.session_state.score}</h3>", unsafe_allow_html=True)

    # Player Interaction Section
    st.markdown("<h3 class='outlined-text'>Actions to improve your ecosystem:</h3>", unsafe_allow_html=True)

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
        for i in range(3):  # For the first three actions
            with [col1, col2, col3][i]:
                if st.button(selected_actions[i]):
                    st.session_state.ecosystem = perform_action(st.session_state.ecosystem, selected_actions[i], st.session_state.plot_type)
                    st.session_state.score += calculate_score(st.session_state.ecosystem)  # Update score based on ecosystem
                    st.success(f"{selected_actions[i]} performed!")

        # Next set of actions
        col4, col5, col6 = st.columns(3)

        for i in range(3, 6):  # For the next three actions
            with [col4, col5, col6][i - 3]:
                if st.button(selected_actions[i]):
                    st.session_state.ecosystem = perform_action(st.session_state.ecosystem, selected_actions[i], st.session_state.plot_type)
                    st.session_state.score += calculate_score(st.session_state.ecosystem)  # Update score based on ecosystem
                    st.success(f"{selected_actions[i]} performed!")


        if st.button("End Simulation"):
            st.session_state.stage = "outro"
            st.rerun()

# Outro stage: Play outro video
if st.session_state.stage == "outro":
    st.video("https://www.youtube.com/watch?v=q7beMTMQogw")  # Outro video link
