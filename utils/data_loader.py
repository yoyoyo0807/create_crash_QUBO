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
    軽量データ一式をまとめて読み込む。
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
# ② ページごとの個別ローダ
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


# --------------------------------------------------------------------
# ③ Zone Network Analysis 用（120×H の行列 → 50×H など）
# --------------------------------------------------------------------
@st.cache_data
def load_matrix_data():
    """
    ゾーン×病院シェア行列とゾーン情報を読み込む。

    戻り値:
        df_mat  : mesh_hospital_case_matrix.csv
                  ['mesh_id', 'hospital_name', 'n_cases', 'share', 'risk_score']
        df_zones: zone_qubo_candidate_space.csv
    """
    df_mat = _read_csv("mesh_hospital_case_matrix.csv")
    df_zones = load_zones()
    return df_mat, df_zones


@st.cache_data
def get_matrix_pivot(top_n: int = 50, mode: str = "qubo"):
    """
    Zone Network Analysis ページ向け:
    - 上位メッシュを選び
    - メッシュ×病院の share 行列（ピボット）を返す

    引数:
        top_n : 使いたいメッシュ数（例: 50）
        mode  : "qubo" → QUBO選択ゾーン優先,
                "risk" → risk_score の高い順

    戻り値:
        W      : (N_mesh × N_hospital) の行列（DataFrame）
        sel_df : 選択されたメッシュのメタデータ（mesh_id, risk_score など）
    """
    df_mat, df_zones = load_matrix_data()

    # まず候補ゾーンだけに絞る（zone ファイルに出てくる mesh_id）
    candidate_ids = df_zones["mesh_id"].unique()
    df_mat_cand = df_mat[df_mat["mesh_id"].isin(candidate_ids)].copy()

    # 選択ロジック
    df_sel = df_zones.copy()
    if mode == "qubo" and "selected_qubo" in df_sel.columns:
        # QUBOで選ばれたゾーンを優先しつつ、足りない分は risk_score 上位
        df_sel = df_sel.sort_values(
            ["selected_qubo", "risk_score"],
            ascending=[False, False]
        )
    else:
        # risk_score の高い順
        df_sel = df_sel.sort_values("risk_score", ascending=False)

    df_sel = df_sel.head(top_n)
    sel_ids = df_sel["mesh_id"].unique()

    df_mat_sel = df_mat_cand[df_mat_cand["mesh_id"].isin(sel_ids)].copy()

    # ピボット（行=mesh_id, 列=hospital_name, 値=share）
    W = df_mat_sel.pivot_table(
        index="mesh_id",
        columns="hospital_name",
        values="share",
        aggfunc="sum",
        fill_value=0.0,
    )

    # 行順を df_sel に合わせる
    W = W.reindex(df_sel["mesh_id"].values)

    return W, df_sel
