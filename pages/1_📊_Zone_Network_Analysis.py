# pages/1_📊_Zone_Network_Analysis.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.data_loader import load_all_data  # 既存の loader を利用

st.set_page_config(page_title="Zone Network / Similarity", layout="wide")

st.title("📊 Zone Network Analysis")
st.markdown(
    """
QUBO が内部で使っている **病院依存ベクトルの類似度 $V(g,g')$** を  
Top-N ゾーンに絞ってヒートマップで可視化します。

- 0（白） → ほとんど同じ病院を共有していない  
- 1（赤） → ほぼ同じ病院群に依存している  
"""
)

# ------------------------------------------------------------------------------
# 1) データ読み込み（キャッシュ）
# ------------------------------------------------------------------------------
@st.cache_data
def load_cases_zones():
    df_cases, df_zones, df_systemic, df_comm, df_comm_mix = load_all_data()
    return df_cases, df_zones

df_cases, df_zones = load_cases_zones()

need_case_cols = ["case_id", "hospital_name", "mesh_id"]
need_zone_cols = ["mesh_id", "risk_score", "n_cases"]

missing_cases = [c for c in need_case_cols if c not in df_cases.columns]
missing_zones = [c for c in need_zone_cols if c not in df_zones.columns]

if missing_cases or missing_zones:
    st.error(
        f"必要な列が足りません。\n"
        f"cases: {missing_cases}\n"
        f"zones: {missing_zones}"
    )
    st.stop()

# ------------------------------------------------------------------------------
# 2) サイドバー：パラメータ
# ------------------------------------------------------------------------------
st.sidebar.header("表示設定")

# ゾーン数の上限を 50 に
N_max = min(50, len(df_zones))
N_min = 10 if len(df_zones) >= 10 else len(df_zones)

N = st.sidebar.slider(
    "対象ゾーン数（Top-N by risk_score）",
    min_value=N_min,
    max_value=N_max,
    value=N_max,
    step=5,
)

use_qubo_priority = st.sidebar.checkbox(
    "QUBO選択ゾーンを優先的に含める", value=True
)

sim_threshold = st.sidebar.slider(
    "可視化しやすくするための下限（しきい値）",
    min_value=0.0,
    max_value=1.0,
    value=0.2,
    step=0.05,
    help="ここより小さい類似度は色を薄くして、クラスタだけ見えやすくします。",
)

st.sidebar.markdown("---")
st.sidebar.caption("※ 類似度は『病院シェアベクトルの内積』に相当")

# ------------------------------------------------------------------------------
# 3) ゾーン候補の準備
# ------------------------------------------------------------------------------
df_z = df_zones.copy().reset_index(drop=True)
df_z = df_z.sort_values("risk_score", ascending=False).reset_index(drop=True)

# QUBOフラグ列を探す
qubo_col = None
for c in ["selected_qubo", "x_qubo", "x_selected", "x_step2"]:
    if c in df_z.columns:
        qubo_col = c
        break

if qubo_col is None:
    df_z["selected_qubo_flag"] = False
    qubo_col = "selected_qubo_flag"

df_z[qubo_col] = df_z[qubo_col].astype(bool)

def select_zones_for_heatmap(df_z, N, qubo_col, use_qubo_priority=True):
    """Top-N を選ぶときに QUBO ゾーンをできるだけ含める"""
    df_sorted = df_z.sort_values("risk_score", ascending=False).copy()

    if not use_qubo_priority:
        return df_sorted.iloc[:N].copy()

    df_qubo = df_sorted[df_sorted[qubo_col] == True]
    df_non = df_sorted[df_sorted[qubo_col] == False]

    n_qubo = min(len(df_qubo), N)
    df_sel = pd.concat(
        [df_qubo.iloc[:n_qubo], df_non.iloc[: N - n_qubo]],
        axis=0,
    )

    df_sel = df_sel.sort_values("risk_score", ascending=False).reset_index(drop=True)
    return df_sel

df_sel = select_zones_for_heatmap(df_z, N, qubo_col, use_qubo_priority)

st.write(f"**対象ゾーン数: {len(df_sel)} / {len(df_z)}**")
st.dataframe(
    df_sel[["mesh_id", "risk_score", "n_cases", qubo_col]]
    .rename(columns={qubo_col: "selected_by_QUBO"})
    .head(10)
)

# ------------------------------------------------------------------------------
# 4) W_share（mesh × hospital）の計算
# ------------------------------------------------------------------------------
@st.cache_data
def compute_W_share(df_cases: pd.DataFrame, df_zones_subset: pd.DataFrame):
    cand_meshes = set(df_zones_subset["mesh_id"].unique())
    df_sub = df_cases[df_cases["mesh_id"].isin(cand_meshes)].copy()
    df_sub = df_sub.dropna(subset=["mesh_id", "hospital_name", "case_id"])

    mesh_hosp_counts = (
        df_sub.groupby(["mesh_id", "hospital_name"])["case_id"]
        .nunique()
        .reset_index(name="cnt")
    )

    W = mesh_hosp_counts.pivot_table(
        index="mesh_id",
        columns="hospital_name",
        values="cnt",
        fill_value=0,
    )

    # 候補 mesh の順番に並べ替え
    W = W.reindex(df_zones_subset["mesh_id"]).fillna(0)

    row_sum = W.sum(axis=1).replace(0, 1)
    W_share = W.div(row_sum, axis=0)

    return W_share

with st.spinner("病院依存ベクトル（W_share）を計算中..."):
    W_share = compute_W_share(df_cases, df_sel)

# ------------------------------------------------------------------------------
# 5) 類似度行列 V(g,g') の計算
# ------------------------------------------------------------------------------
W_mat = W_share.to_numpy(dtype=float)
V = W_mat @ W_mat.T
np.fill_diagonal(V, 1.0)

V_plot = V.copy()
V_plot[V_plot < sim_threshold] = sim_threshold  # 見やすさ用

# ------------------------------------------------------------------------------
# 6) ヒートマップ表示
# ------------------------------------------------------------------------------
st.subheader("🧩 Zone Similarity Matrix（Top-N）")

fig, ax = plt.subplots(figsize=(6, 6))

im = ax.imshow(
    V_plot,
    origin="lower",
    cmap="Reds",  # 0=白, 1=赤
    vmin=0.0,
    vmax=1.0,
)

ax.set_xticks([])
ax.set_yticks([])
ax.set_xlabel("Zone index (Top-N by risk)")
ax.set_ylabel("Zone index (Top-N by risk)")

cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
cbar.set_label("Similarity V(g, g')")

st.pyplot(fig)

# ------------------------------------------------------------------------------
# 7) ゾーン一覧テーブル
# ------------------------------------------------------------------------------
st.markdown("---")
st.markdown("### 対象ゾーン一覧（Top-N）")

st.dataframe(
    df_sel[["mesh_id", "risk_score", "n_cases", qubo_col]]
    .rename(columns={qubo_col: "selected_by_QUBO"})
)
