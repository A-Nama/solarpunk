import streamlit as st
import numpy as np
import requests
import matplotlib.pyplot as plt

# Placeholder Gemini API call function for scenario and choices
def fetch_scenario(role, community):
    api_url = "https://gemini.api/your_endpoint"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    payload = {
        "role": role,
        "community": community,
        "request_type": "scenario_and_choices"
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        scenario = data['scenario']
        choices = data['choices']
        return scenario, choices
    else:
        st.error("Error fetching data from Gemini API")
        return None, None

# Fetch AI-generated fact based on user choice
def fetch_fact(choice_type):
    api_url = "https://gemini.api/your_endpoint"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    payload = {
        "choice_type": choice_type,
        "request_type": "fact"
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data['fact']
    else:
        st.error("Error fetching fact from Gemini API")
        return "Couldn't fetch a fact at this time."

# Fetch current global warming data from GLOBE API (placeholder)
def fetch_global_warming_data():
    api_url = "https://www.spaceappschallenge.org/nasa-space-apps-2024/global-offers/"
    response = requests.get(api_url)

    if response.status_code == 200:
        return response.json()  # Replace with actual data structure
    else:
        st.error("Error fetching data from GLOBE API")
        return None

# Fetch AI-generated real-life tasks from Gemini API
def fetch_real_life_tasks():
    api_url = "https://gemini.api/your_endpoint"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}
    payload = {
        "request_type": "real_life_tasks"
    }

    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        return data['tasks']  # AI-generated tasks
    else:
        st.error("Error fetching tasks from Gemini API")
        return ["Couldn't fetch tasks at this time."]

# Function to visualize global warming data
def visualize_global_warming(data):
    years = [entry['year'] for entry in data]
    levels = [entry['level'] for entry in data]

    plt.figure(figsize=(10, 6))
    plt.plot(years, levels, marker='o', linestyle='-', color='blue', label='Global Warming Levels')
    
    # Calculate and plot a line of best fit
    z = np.polyfit(years, levels, 1)  # Linear regression
    p = np.poly1d(z)
    plt.plot(years, p(years), linestyle='--', color='orange', label='Trend Line')

    plt.title('Global Warming Levels Over the Years', fontsize=16)
    plt.xlabel('Year', fontsize=14)
    plt.ylabel('Global Warming Level', fontsize=14)
    plt.xticks(years, rotation=45)  # Rotate year labels for better visibility
    plt.yticks(fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    
    # Show the plot in Streamlit
    st.pyplot(plt)
    plt.clf()  # Clear the plot for future visualizations


# Initialize game state
if 'points' not in st.session_state:
    st.session_state.points = 0
if 'round' not in st.session_state:
    st.session_state.round = 1
if 'choices_made' not in st.session_state:
    st.session_state.choices_made = 0
if 'time_of_day' not in st.session_state:
    st.session_state.time_of_day = "Morning"
if 'game_over' not in st.session_state:
    st.session_state.game_over = False

# Define the time progression order
time_order = ["Morning", "Afternoon", "Evening", "Night"]

# Function to update the time of day
def update_time_of_day():
    if st.session_state.choices_made >= 2:
        st.session_state.choices_made = 0
        current_time_index = time_order.index(st.session_state.time_of_day)
        if current_time_index < len(time_order) - 1:
            st.session_state.time_of_day = time_order[current_time_index + 1]
        else:
            st.session_state.game_over = True  # End game after Night

# Title of the game
st.title("SolarPunk Simulation with AI")

# User selects community and role
community = st.selectbox("Choose your community:", ["Cottage Core", "City Core"])
role = st.selectbox("Are you a student or an adult?", ["Student", "Adult"])

# If the game is still ongoing
if not st.session_state.game_over:
    # Display current time of day
    st.write(f"Time of Day: {st.session_state.time_of_day}")

    # Fetch AI-generated scenario and choices
    scenario, choices = fetch_scenario(role.lower(), community)

    # Display scenario and choices
    if scenario:
        st.header(f"Round {st.session_state.round}: {scenario}")
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
                st.session_state.choices_made += 1
                update_time_of_day()
                st.experimental_rerun()

    # Show points
    st.write(f"Current Points: {st.session_state.points}")

# When the game is over
else:
    st.success("That's a day in your solarpunk life!2")

    # Fetch and display global warming data from GLOBE API
    st.write("Here's a look at the current levels of global warming:")
    global_warming_data = fetch_global_warming_data()

    if global_warming_data:
        visualize_global_warming(global_warming_data)

    st.write("This is how far we are from reaching Solarpunk. To get there faster, do a real-life task today!")

    # Fetch and display AI-generated real-life tasks
    real_life_tasks = fetch_real_life_tasks()
    st.write("Here are some tasks you can do today:")
    for task in real_life_tasks:
        st.write(f"- {task}")

    # Final message
    st.write("Thank you for playing! Remember, your actions matter.")

