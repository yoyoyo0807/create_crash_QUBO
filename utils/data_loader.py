# utils/data_loader.py
import pandas as pd
import streamlit as st
from pathlib import Path

# リポジトリのルートと data ディレクトリを推定
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _read_csv_smart(name: str) -> pd.DataFrame:
    """
    1. data/ 配下:   data/name
    2. ルート直下:   name
    の順に探して読み込む。
    どちらにも無ければ Streamlit 側にわかりやすくエラーを出して止める。
    """
    candidates = [DATA_DIR / name, BASE_DIR / name]

    for p in candidates:
        if p.exists():
            return pd.read_csv(p)

    # ここまで来たら本当にファイルが無い
    st.error(
        f"❌ データファイルが見つかりませんでした: `{name}`\n\n"
        f"試したパス:\n"
        + "\n".join([f"- {p}" for p in candidates])
        + "\n\n"
        "GitHub 上でファイルが存在するか、パス/ファイル名が一致しているか確認してください。"
    )
    st.stop()


@st.cache_data
def load_all_data():
    """
    アプリ全体で共通して使うメインデータを読み込む。
    （パスは data/ とルート直下の両方に対応）
    """
    df_cases = _read_csv_smart("emergency_with_metrics_and_mesh.csv")
    df_zones = _read_csv_smart("zone_qubo_candidate_space.csv")
    df_systemic = _read_csv_smart(
        "systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv"
    )
    df_comm = _read_csv_smart("community_summary_systemic.csv")
    df_comm_mix = _read_csv_smart("community_hospital_mix_long.csv")

    return df_cases, df_zones, df_systemic, df_comm, df_comm_mix
