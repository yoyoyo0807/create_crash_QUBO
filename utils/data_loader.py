# utils/data_loader.py
import pandas as pd
import streamlit as st

@st.cache_data
def load_matrix_data():
    df = pd.read_csv("data/mesh_hospital_case_matrix.csv")
    return df

@st.cache_data
def get_matrix_pivot(df):
    # ピボット → mesh × hospital の share 行列
    mat = df.pivot_table(
        index="mesh_id",
        columns="hospital_name",
        values="share",
        fill_value=0
    )
    return mat
