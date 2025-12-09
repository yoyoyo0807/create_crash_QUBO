# utils/data_loader.py
import pandas as pd
import streamlit as st

MATRIX_FILE = "data/mesh_hospital_case_matrix.csv"
ZONE_FILE   = "data/zone_qubo_candidate_space.csv"

@st.cache_data
def load_matrix_data():
    """軽量行列とゾーン情報を読み込む（ページから使いたいとき用）"""
    df_mat   = pd.read_csv(MATRIX_FILE)
    df_zones = pd.read_csv(ZONE_FILE)
    return df_mat, df_zones


@st.cache_data
def get_matrix_pivot(top_n: int = 50):
    """
    mesh_hospital_case_matrix.csv と zone_qubo_candidate_space.csv から

    - risk_score 上位 top_n メッシュを選び
    - メッシュ × 病院 の share 行列（ピボット）を返す

    戻り値:
        mat    : rows = mesh_id, cols = hospital_name, values = share
        df_sel : 選ばれたメッシュの情報（mesh_id, risk_score, n_cases など）
    """
    # 1. 読み込み
    df_mat, df_zones = load_matrix_data()

    # 2. zone 側から必要な列だけ
    cols_zone = ["mesh_id", "risk_score", "n_cases"]
    cols_zone = [c for c in cols_zone if c in df_zones.columns]
    df_z = df_zones[cols_zone].copy()

    # 3. 行列に risk_score をマージ
    df_all = df_mat.merge(df_z, on="mesh_id", how="left")

    # 4. メッシュごとの代表 risk_score（最大）と件数
    df_zone_risk = (
        df_all.groupby("mesh_id")
        .agg(
            risk_score=("risk_score", "max"),
            n_cases=("n_cases", "sum"),
        )
        .reset_index()
        .sort_values("risk_score", ascending=False)
    )

    # 5. 上位 top_n メッシュを選択
    if isinstance(top_n, int):
        df_sel = df_zone_risk.head(top_n).copy()
    else:
        # 万一おかしな値が来たときの保険
        df_sel = df_zone_risk.head(50).copy()

    sel_ids = df_sel["mesh_id"].tolist()

    # 6. 選ばれたメッシュだけに絞る
    df_mat_sel = df_all[df_all["mesh_id"].isin(sel_ids)].copy()

    # 7. ピボット（メッシュ × 病院）
    mat = df_mat_sel.pivot_table(
        index="mesh_id",
        columns="hospital_name",
        values="share",       # mesh_hospital_case_matrix.csv の列名
        fill_value=0.0,
    )

    # 行順を risk_score の降順に揃える
    mat = mat.loc[sel_ids]

    return mat, df_sel
