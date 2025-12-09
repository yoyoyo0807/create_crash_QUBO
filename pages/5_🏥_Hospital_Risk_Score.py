import streamlit as st
from utils.data_loader import load_hospital_scores

st.title("🏥 病院別 Systemic リスクスコア")

df_scores = load_hospital_scores()

st.dataframe(
    df_scores.sort_values("SSS", ascending=False),
    use_container_width=True
)
