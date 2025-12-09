import pandas as pd
import streamlit as st

@st.cache_data
def load_all_data():
    df_cases  = pd.read_csv("data/emergency_with_metrics_and_mesh.csv")
    df_zones  = pd.read_csv("data/zone_qubo_candidate_space.csv")
    df_system = pd.read_csv("data/systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv")
    df_comm   = pd.read_csv("data/community_summary_systemic.csv")
    df_mix    = pd.read_csv("data/community_hospital_mix_long.csv")
    return df_cases, df_zones, df_system, df_comm, df_mix

def load_zone_data():
    df_cases  = pd.read_csv("data/emergency_with_metrics_and_mesh.csv")
    df_zones  = pd.read_csv("data/zone_qubo_candidate_space.csv")
    return df_cases, df_zones

def load_systemic_data():
    return pd.read_csv("data/systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv")
