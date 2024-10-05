import streamlit as st
import random

# Helper functions for sustainable and non-sustainable tasks
def get_sustainable_fact():
    return random.choice([
        "Using a reusable bottle can save 150 single-use bottles annually.",
        "Reducing food waste can reduce 8% of global emissions.",
        "Solar panels reduce 1 ton of CO2 for every megawatt hour generated."
    ])

def get_unsustainable_fact():
    return random.choice([
        "Plastic pollution accounts for 8 million tons of waste entering oceans annually.",
        "Food waste is one of the largest contributors to methane emissions.",
        "Fossil fuel electricity generation emits 2.2 billion tons of CO2 each year."
    ])

# Display the welcome message
st.title("Sustainability Simulation")
st.subheader("Choose your path and make sustainable choices!")

# Step 1: Choosing between Cottagecore or Citycore community
community = st.selectbox("Choose your community", ("Cottagecore", "Citycore"))

# Step 2: Choosing life phase
life_phase = st.selectbox("Are you a student or an adult?", ("Student", "Adult"))

# Step 3: Generating a task with sustainable and non-sustainable options
if st.button("Start your task"):
    task_type = random.choice(["Energy", "Food", "Waste", "Water"])

    # Display the task to the user
    st.write(f"Your task is related to: {task_type}")

    if task_type == "Energy":
        st.write("Do you choose to install solar panels on your home or use fossil fuel energy?")
    elif task_type == "Food":
        st.write("Do you choose to eat locally sourced vegetables or imported meat products?")
    elif task_type == "Waste":
        st.write("Do you choose to compost your food waste or throw it into the general waste bin?")
    elif task_type == "Water":
        st.write("Do you choose to install a rainwater harvesting system or use tap water for everything?")

    # Step 4: Sustainable and non-sustainable options
    choice = st.radio("Make your choice:", ("Sustainable", "Non-sustainable"))

    # Step 5: Providing feedback based on the choice
    if choice == "Sustainable":
        st.success("Great choice! You're contributing to reducing climate change.")
        st.write(get_sustainable_fact())
    else:
        st.warning("This option contributes to climate change.")
        st.write(get_unsustainable_fact())

# Step 6: Displaying a summary and map from GLOBE API
if st.button("End Simulation and Show Map"):
    st.write("Simulation completed! Here's a map showing the current climate change status.")
    st.write("You can take on missions based on this data to help combat climate change!")
    
    # Placeholder for GLOBE API map (You will need to integrate the API here)
    st.image("https://globe.gov/GLOBE/images/hero-globe.png", caption="Climate Change Map (GLOBE API)")

    # Example missions
    st.write("Mission 1: Reduce carbon emissions by 10% in your community.")
    st.write("Mission 2: Improve waste management practices.")
    st.write("Mission 3: Switch to renewable energy sources.")
