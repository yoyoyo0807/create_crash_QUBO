import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap_50(df_cases, df_zones, top_n=50):
    # 実際のロジックは後で挿入
    fig, ax = plt.subplots(figsize=(8,8))
    mat = np.random.rand(top_n, top_n)
    ax.imshow(mat, cmap="Reds")
    ax.set_title(f"{top_n}x{top_n} Zone Correlation")
    return fig

def plot_network_graph(df_cases, df_zones):
    fig, ax = plt.subplots()
    ax.text(0.1,0.5,"Network Graph Placeholder")
    return fig

def plot_systemic_map(df_sys):
    import plotly.express as px
    fig = px.scatter_mapbox(
        df_sys,
        lat="lat",
        lon="lon",
        color="SSS_scaled",
        size="overshoot_qubo",
        mapbox_style="carto-positron",
        zoom=11
    )
    return fig
