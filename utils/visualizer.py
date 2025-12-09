# utils/visualizer.py
import plotly.express as px
import pandas as pd


def plot_systemic_map(df: pd.DataFrame):
    """
    Systemic Risk Map 用の図を作成する。

    想定 df:
        mesh_location.csv
        columns: ['mesh_id', 'lon', 'lat', 'n_cases', 'risk_score', ...]
    """
    # 必須カラムがなければ、普通の散布図にフォールバック
    required = {"lon", "lat"}
    if not required.issubset(df.columns):
        # フォールバック: risk_score vs n_cases の散布図
        x_col = "n_cases" if "n_cases" in df.columns else df.columns[0]
        y_col = "risk_score" if "risk_score" in df.columns else df.columns[1]

        fig = px.scatter(
            df,
            x=x_col,
            y=y_col,
            hover_name="mesh_id" if "mesh_id" in df.columns else None,
            title="Systemic Risk (fallback: scatter)",
        )
        return fig

    # lat, lon が数値じゃない場合に備えて型変換
    df = df.copy()
    df["lon"] = pd.to_numeric(df["lon"], errors="coerce")
    df["lat"] = pd.to_numeric(df["lat"], errors="coerce")
    df = df.dropna(subset=["lon", "lat"])

    fig = px.scatter_mapbox(
        df,
        lat="lat",
        lon="lon",
        color="risk_score" if "risk_score" in df.columns else None,
        size="n_cases" if "n_cases" in df.columns else None,
        hover_name="mesh_id" if "mesh_id" in df.columns else None,
        color_continuous_scale="RdYlGn_r",
        zoom=11,
        height=600,
    )
    fig.update_layout(
        mapbox_style="open-street-map",
        margin=dict(l=0, r=0, t=30, b=0),
        title="Systemic Risk Map (mesh level)",
    )
    return fig
