import pandas as pd

def compute_qubo_vs_rank():
    df = pd.read_csv("data/systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv")
    df["overshoot_diff"] = df["overshoot_qubo"] - df["overshoot_rank"]
    return df

def load_hospital_scores():
    df = pd.read_csv("data/hospital_systemic_indices_SSS_CDS_SE.csv")
    return df
