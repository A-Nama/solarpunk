import matplotlib.pyplot as plt
import streamlit as st

def plot_solarpunk_ecosystem(vegetation, water, weather):
    labels = ['Vegetation', 'Water', 'Weather']
    values = [vegetation, water, weather]

    fig, ax = plt.subplots()

    # Set the color of the bars to pastel blue
    ax.bar(labels, values, color=['#B3CDE0', '#A4D0E1', '#BFD3C1'])  # Use pastel blue shades
    
    ax.set_ylim(0, 100)
    ax.set_ylabel('Levels (%)')
    ax.set_title('Solarpunk Ecosystem Health')

    # Make the background of the figure transparent
    fig.patch.set_alpha(0)  # Make figure background transparent
    ax.set_facecolor((1, 1, 1, 0))  # Set axes background transparent

    st.pyplot(fig, transparent=True)  # Set transparent=True to make the figure background transparent
