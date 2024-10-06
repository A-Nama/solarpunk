import matplotlib.pyplot as plt
import streamlit as st

def plot_solarpunk_ecosystem(vegetation, water, weather):
    labels = ['vegetation', 'Water', 'weather']
    values = [vegetation, water, weather]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['green', 'blue', 'yellow'])
    
    ax.set_ylim(0, 100)
    ax.set_ylabel('Levels (%)')
    ax.set_title('Solarpunk Ecosystem Health')
    
    st.pyplot(fig)
