# utils/qubo_analysis.py
import pandas as pd
from utils.data_loader import load_hospital_scores


def get_hospital_scores():
    """
    Streamlit ページ用のラッパー関数。
    そのまま load_hospital_scores() を返すだけ。
    """
    return load_hospital_scores()
