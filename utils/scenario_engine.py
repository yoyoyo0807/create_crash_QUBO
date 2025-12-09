import pandas as pd

def run_scenario(scenario_name, multiplier=None):
    # 実際の QUBOパイプラインを後で挿入
    df = pd.read_csv("data/systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv")
    df["overshoot_scenario"] = df["overshoot_qubo"]  # placeholder
    return df
