import streamlit as st
from utils.qubo_analysis import compute_qubo_vs_rank

st.title("🔥 QUBO vs Rank — 病院負荷比較")

df_result = compute_qubo_vs_rank()

st.dataframe(df_result)

st.header("Overshoot 差分（QUBO − Rank）上位病院")
st.bar_chart(df_result.set_index("hospital_name")["overshoot_diff"])
