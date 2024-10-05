import streamlit as st
import matplotlib.pyplot as plt

def plot_solarpunk_ecosystem(veg, water, energy):
    st.write("Ecosystem Overview:")
    data = {"Vegetation": veg, "Water Resources": water, "Renewable Energy": energy}
    
    st.bar_chart(data)
