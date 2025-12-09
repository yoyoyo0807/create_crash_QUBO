import streamlit as st
from utils.qubo_analysis import load_hospital_scores

st.title("🏥 病院別 Systemic リスクスコア")

df_scores = load_hospital_scores()

st.dataframe(df_scores)

st.header("Systemic Stress Score")
st.bar_chart(df_scores.set_index("hospital_name")["SSS_scaled"])
