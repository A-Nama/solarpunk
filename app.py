import streamlit as st
import requests
import random

# Placeholder Gemini API call function
def fetch_scenario(role, community):
    # Replace with actual Gemini API URL and request
    api_url = "https://gemini.api/your_endpoint"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}

    # The data payload might include user role, community, etc.
    payload = {
        "role": role,
        "community": community,
        "request_type": "scenario_and_choices"
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        scenario = data['scenario']
        choices = data['choices']  # This would return 3 choices
        return scenario, choices
    else:
        st.error("Error fetching data from Gemini API")
        return None, None

# Fetch AI-generated fact based on user choice
def fetch_fact(choice_type):
    # Replace with actual Gemini API URL and request
    api_url = "https://gemini.api/your_endpoint"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}

    # The payload will include what type of choice was made
    payload = {
        "choice_type": choice_type,
        "request_type": "fact"
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data['fact']  # AI-generated fact
    else:
        st.error("Error fetching fact from Gemini API")
        return "Couldn't fetch a fact at this time."

# Initialize game state
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'round' not in st.session_state:
    st.session_state.round = 1

# Title of the game
st.title("SolarPunk Simulation with AI")

# User chooses community and role
community = st.selectbox("Choose your community:", ["Cottage Core", "City Core"])
role = st.selectbox("Are you a student or an adult?", ["Student", "Adult"])

# Set up background based on time of day
time_of_day = st.selectbox("Choose time of day:", ["Morning", "Afternoon", "Evening", "Night"])
st.write(f"Background: {time_of_day} mode")

# Fetch AI-generated scenario and choices from Gemini API
scenario, choices = fetch_scenario(role.lower(), community)

# Display the scenario
if scenario:
    st.header(f"Round {st.session_state.round}: {scenario}")
    
    # Display the AI-generated choices
    for i, choice in enumerate(choices):
        if st.button(choice['text']):
            if choice['type'] == 'sustainable':
                st.session_state.points += 10
                fact = fetch_fact("sustainable")
                st.success(f"Good choice! {fact}")
            else:
                st.session_state.points -= 5
                fact = fetch_fact("unsustainable")
                st.error(f"Uh-oh! {fact}")
                
            st.session_state.round += 1
            st.experimental_rerun()  # Rerun the app for the next round

# Show points
st.write(f"Current Points: {st.session_state.points}")
