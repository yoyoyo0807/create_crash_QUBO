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
    どちらにも無ければ Streamlit の画面に分かりやすいエラーを出して止める。
    """
    candidates = [DATA_DIR / name, BASE_DIR / name]

    for p in candidates:
        if p.exists():
            return pd.read_csv(p)

    st.error(
        f"❌ データファイルが見つかりませんでした: `{name}`\n\n"
        f"試したパス:\n"
        + "\n".join(f"- {p}" for p in candidates)
        + "\n\n"
        "GitHub リポジトリにファイルがコミットされているか、"
        "ファイル名（全角半角・拡張子含む）が一致しているかを確認してください。"
    )
    st.stop()


# ==== アプリ全体で使うローダー ==== #

@st.cache_data
def load_all_data():
    """
    トップページ(app.py)用：
    ケース・ゾーン・システミック・コミュニティの全部入り。
    """
    df_cases = _read_csv_smart("emergency_with_metrics_and_mesh.csv")
    df_zones = _read_csv_smart("zone_qubo_candidate_space.csv")
    df_systemic = _read_csv_smart(
        "systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv"
    )
    df_comm = _read_csv_smart("community_summary_systemic.csv")
    df_comm_mix = _read_csv_smart("community_hospital_mix_long.csv")
    return df_cases, df_zones, df_systemic, df_comm, df_comm_mix


# ==== 各ページから個別に呼びたい場合用 ==== #

@st.cache_data
def load_cases_and_zones():
    df_cases = _read_csv_smart("emergency_with_metrics_and_mesh.csv")
    df_zones = _read_csv_smart("zone_qubo_candidate_space.csv")
    return df_cases, df_zones


@st.cache_data
def load_systemic_data():
    """
    pages/3_🌐_Systemic_Risk_Map.py から import されているやつ。
    """
    df_systemic = _read_csv_smart(
        "systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv"
    )
    df_comm = _read_csv_smart("community_summary_systemic.csv")
    df_comm_mix = _read_csv_smart("community_hospital_mix_long.csv")
    return df_systemic, df_comm, df_comm_mix


@st.cache_data
def load_hospital_scores():
    """
    病院別 Systemic リスクスコアの CSV。
    （まだ CSV をコミットしてなければ、後で追加）
    """
    df = _read_csv_smart("hospital_systemic_indices_SSS_CDS_SE.csv")
    return df
