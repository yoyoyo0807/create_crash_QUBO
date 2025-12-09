# utils/data_loader.py
import streamlit as st
import pandas as pd
from pathlib import Path

# ベースディレクトリ（create_crash_qubo/）を推定
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _read_csv(filename: str, **kwargs) -> pd.DataFrame:
    """
    data/配下 or カレント直下から CSV を探して読むユーティリティ。
    Streamlit Cloud でパスずれしにくくするためのラッパー。
    """
    candidates = [
        DATA_DIR / filename,   # /repo_root/data/filename
        BASE_DIR / filename,   # /repo_root/filename
        Path(filename),        # 呼び出し元の相対パス
    ]
    last_err = None
    for p in candidates:
        try:
            return pd.read_csv(p, **kwargs)
        except FileNotFoundError as e:
            last_err = e
            continue

    # どこにもなかったらわかりやすいエラーを投げる
    tried = "\n".join(str(c) for c in candidates)
    raise FileNotFoundError(
        f"CSV が見つかりませんでした: {filename}\n試したパス:\n{tried}"
    ) from last_err


# --------------------------------------------------------------------
# ① アプリ全体でまとめて使うロード関数
# --------------------------------------------------------------------
@st.cache_data
def load_all_data():
    """
    アプリ全体で使う軽量データ一式をまとめて読み込む。
    ※巨大な emergency_with_metrics_and_mesh.csv は使わない。
    戻り値:
        df_mesh, df_zones, df_systemic, df_comm, df_comm_mix
    """
    df_mesh     = _read_csv("mesh_location.csv")
    df_zones    = _read_csv("zone_qubo_candidate_space.csv")
    df_systemic = _read_csv("systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv")
    df_comm     = _read_csv("community_summary_systemic.csv")
    df_comm_mix = _read_csv("community_hospital_mix_long.csv")
    return df_mesh, df_zones, df_systemic, df_comm, df_comm_mix


# --------------------------------------------------------------------
# ② ページごとの個別ローダ（必要に応じて使えるようにしておく）
# --------------------------------------------------------------------
@st.cache_data
def load_mesh_location():
    """メッシュ代表点＋リスク（地図・ネットワーク用）"""
    return _read_csv("mesh_location.csv")


@st.cache_data
def load_zones():
    """QUBO候補ゾーン情報"""
    return _read_csv("zone_qubo_candidate_space.csv")


@st.cache_data
def load_systemic_data():
    """
    病院ごとの overshoot 比較（QUBO vs Rank）
    Systemic Risk Map や QUBO vs Rank ページで利用
    """
    return _read_csv("systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv")


@st.cache_data
def load_community_summary():
    """ゾーンクラスタ summary"""
    return _read_csv("community_summary_systemic.csv")


@st.cache_data
def load_community_hospital_mix():
    """クラスタ × 病院のミックス"""
    return _read_csv("community_hospital_mix_long.csv")


@st.cache_data
def load_hospital_scores():
    """
    病院別 Systemic 指標（SSS / CDS / SE）
    Hospital Risk Score ページで利用
    """
    return _read_csv("hospital_systemic_indices_SSS_CDS_SE.csv")
