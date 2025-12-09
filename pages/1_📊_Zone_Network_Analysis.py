# pages/1_📊_Zone_Network_Analysis.py
from utils.data_loader import load_matrix_data, get_matrix_pivot
import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

st.title("📊 Zone Network Analysis")

# 情報表示用（任意）
df_mat, df_zones = load_matrix_data()
st.caption(f"メッシュ × 病院 行列: {df_mat.shape[0]} 行, メッシュ数: {df_mat['mesh_id'].nunique()}, 病院数: {df_mat['hospital_name'].nunique()}")

# ヒートマップに出すメッシュ数
top_n = st.slider("ヒートマップに表示するメッシュ数 (risk_score 上位)", 10, 120, 50, 5)

# 類似度行列を作成
mat, df_sel = get_matrix_pivot(top_n=top_n)

st.write("選択されたメッシュ（上位 risk_score）:")
st.dataframe(df_sel, width="stretch")

# Cosine 類似度
sim = cosine_similarity(mat.values)
sim_df = pd.DataFrame(sim, index=mat.index, columns=mat.index)

st.subheader("ゾーン間類似度ヒートマップ（0=白, 1=赤）")

fig, ax = plt.subplots(figsize=(6, 6))
sns.heatmap(
    sim_df,
    cmap="Reds",
    vmin=0,
    vmax=1,
    cbar=True,
    ax=ax,
)
ax.set_xlabel("mesh_id")
ax.set_ylabel("mesh_id")
plt.tight_layout()
st.pyplot(fig)
