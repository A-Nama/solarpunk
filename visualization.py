import matplotlib.pyplot as plt
import streamlit as st

def plot_solarpunk_ecosystem(vegetation, water, energy):
    labels = ['Vegetation', 'Water', 'Energy']
    values = [vegetation, water, energy]

    fig, ax = plt.subplots()
    ax.bar(labels, values, color=['blue', 'blue', 'blue'])
    
    ax.set_ylim(0, 100)
    ax.set_ylabel('Levels (%)')
    ax.set_title('Solarpunk Ecosystem Health')
    
    st.pyplot(fig)