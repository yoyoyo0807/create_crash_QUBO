import streamlit as st
from utils.scenario_engine import run_scenario

st.title("🧪 シナリオ・シミュレーション")

scenario = st.selectbox("シナリオ選択", [
    "沿岸部3倍",
    "高齢化 +20%（全域）",
    "徳洲会 + 東北医科 複合停止",
    "ユーザー定義シナリオ"
])

if scenario == "ユーザー定義シナリオ":
    multiplier = st.slider("発生倍増率", 0.0, 5.0, 1.0)
else:
    multiplier = None

if st.button("シミュレーション実行"):
    df_out = run_scenario(scenario, multiplier)
    st.success("完了！")
    st.dataframe(df_out)
