import streamlit as st
from utils.visualizer import plot_systemic_map
from utils.data_loader import load_systemic_data

st.title("🌐 システミックリスク地図")

df_sys = load_systemic_data()
fig = plot_systemic_map(df_sys)

st.plotly_chart(fig, use_container_width=True)
