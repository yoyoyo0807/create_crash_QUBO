import streamlit as st
from utils.data_loader import load_zone_data
from utils.visualizer import plot_heatmap_50, plot_network_graph

st.title("📊 ゾーン相関ネットワーク分析")

df_cases, df_zones = load_zone_data()

st.header("120×120 相関行列（Vgg')")
if st.checkbox("50×50 高リスクゾーンのみで表示", value=True):
    fig = plot_heatmap_50(df_cases, df_zones)
else:
    fig = plot_heatmap_50(df_cases, df_zones, top_n=120)

st.pyplot(fig)

st.header("ネットワークグラフ")
fig2 = plot_network_graph(df_cases, df_zones)
st.pyplot(fig2)
