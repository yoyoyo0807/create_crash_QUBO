# pages/5_🏥_Hospital_Risk_Score.py
import streamlit as st
from utils.data_loader import load_hospital_scores

st.title("🏥 病院別 Systemic リスクスコア")

df_scores = load_hospital_scores()

st.write("hospital_systemic_indices_SSS_CDS_SE.csv から読み込み")
st.dataframe(
    df_scores.sort_values("SSS", ascending=False),
    use_container_width=True
)

st.header("Systemic Stress Score")
st.bar_chart(df_scores.set_index("hospital_name")["SSS_scaled"])
