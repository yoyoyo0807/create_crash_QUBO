# utils/data_loader.py
import streamlit as st
import pandas as pd

@st.cache_data
def load_all_data():
    """
    Streamlit 用の軽量データローダ
    - mesh_location.csv : メッシュの代表座標＋件数＋リスク
    - zone_qubo_candidate_space.csv : ゾーン候補＆QUBO結果
    - systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv : 病院の overshoot 比較
    - community_summary_systemic.csv : ゾーンクラスタ summary
    - community_hospital_mix_long.csv : クラスタ×病院の mix
    """
    df_mesh     = pd.read_csv("data/mesh_location.csv")
    df_zones    = pd.read_csv("data/zone_qubo_candidate_space.csv")
    df_systemic = pd.read_csv("data/systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv")
    df_comm     = pd.read_csv("data/community_summary_systemic.csv")
    df_comm_mix = pd.read_csv("data/community_hospital_mix_long.csv")
    return df_mesh, df_zones, df_systemic, df_comm, df_comm_mix


@st.cache_data
def load_hospital_scores():
    """
    病院別 Systemic 指標（SSS / CDS / SE）を読み込む
    """
    df = pd.read_csv("data/hospital_systemic_indices_SSS_CDS_SE.csv")
    return df
