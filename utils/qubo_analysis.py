# utils/qubo_analysis.py
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _read_csv(filename: str, **kwargs) -> pd.DataFrame:
    candidates = [
        DATA_DIR / filename,
        BASE_DIR / filename,
        Path(filename),
    ]
    last_err = None
    for p in candidates:
        try:
            return pd.read_csv(p, **kwargs)
        except FileNotFoundError as e:
            last_err = e
            continue

    tried = "\n".join(str(c) for c in candidates)
    raise FileNotFoundError(
        f"CSV が見つかりませんでした: {filename}\n試したパス:\n{tried}"
    ) from last_err


def load_hospital_scores():
    """
    病院別 Systemic 指標（SSS / CDS / SE）
    Hospital Risk Score ページで利用
    """
    return _read_csv("hospital_systemic_indices_SSS_CDS_SE.csv")


def compute_qubo_vs_rank():
    """
    QUBO vs Rank 比較ページ用の簡易ラッパー。
    いまは csv をそのまま返すだけ（後でロジックを厚くしてもOK）。
    """
    df = _read_csv("systemic_hospital_nodes_compare_qubo_vs_rank_1h_sync.csv")

    # 安全のため、あれば overshoot 差分も計算して付ける
    if {"overshoot_qubo", "overshoot_rank"}.issubset(df.columns):
        df["overshoot_diff_qubo_minus_rank"] = (
            df["overshoot_qubo"] - df["overshoot_rank"]
        )

    return df
