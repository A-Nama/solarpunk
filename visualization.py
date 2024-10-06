import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.patheffects as path_effects

def plot_solarpunk_ecosystem(vegetation, water, weather):
    labels = ['Vegetation', 'Water', 'Weather']
    values = [vegetation, water, weather]

    fig, ax = plt.subplots()

    # Set the color of the bars to pastel yellow
    ax.bar(labels, values, color='#FDFD96')  # Use pastel yellow for all bars

    ax.set_ylim(0, 100)
    ax.set_ylabel('Levels (%)')
    ax.set_title('Solarpunk Ecosystem Health')

    # Add white outline to the title and axis labels
    title = ax.title
    title.set_path_effects([path_effects.withStroke(linewidth=2, foreground="white")])

    ylabel = ax.yaxis.label
    ylabel.set_path_effects([path_effects.withStroke(linewidth=2, foreground="white")])

    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_path_effects([path_effects.withStroke(linewidth=2, foreground="white")])

    # Make the background of the figure transparent
    fig.patch.set_alpha(0)  # Make figure background transparent
    ax.set_facecolor((1, 1, 1, 0))  # Set axes background transparent

    st.pyplot(fig, transparent=True)  # Set transparent=True to make the figure background transparent
